"""Daydream marketing site backend.

Serves the static site under /site and handles the contact form at
POST /api/contact. Validation, honeypot, simple in-memory rate limit,
email delivery via Resend.
"""

from __future__ import annotations

import logging
import os
import re
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field, field_validator

log = logging.getLogger("daydream")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SITE_DIR = Path(__file__).resolve().parent.parent.parent / "site"

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
CONTACT_TO = os.environ.get("CONTACT_TO", "hola@letsdaydream.ai")
# Resend requires the From address to be on a verified domain.
# Default uses Resend's onboarding sender so the app works out of the box;
# replace with hola@letsdaydream.ai once SPF/DKIM/DMARC are set up.
CONTACT_FROM = os.environ.get("CONTACT_FROM", "Daydream <onboarding@resend.dev>")

ALLOWED_NEEDS = {"Brand", "Identity", "Website", "Product", "Engineering", "All of it"}

MTY_TZ = ZoneInfo("America/Monterrey")

# Per-IP rate limit windows: (max submissions, window seconds).
RATE_LIMITS = ((1, 30), (5, 3600))

# ---------------------------------------------------------------------------
# Rate limiter (in-memory; fine for a single-instance deploy)
# ---------------------------------------------------------------------------

_submissions: dict[str, deque[float]] = {}


def _check_rate_limit(ip: str) -> Optional[str]:
    now = time.time()
    queue = _submissions.setdefault(ip, deque())
    # drop anything older than the longest window
    cutoff = now - max(window for _, window in RATE_LIMITS)
    while queue and queue[0] < cutoff:
        queue.popleft()

    for limit, window in RATE_LIMITS:
        recent = sum(1 for t in queue if t >= now - window)
        if recent >= limit:
            return f"Too many submissions. Try again later."

    queue.append(now)
    return None


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class ContactPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: str = Field("", max_length=200)
    message: str = Field("", max_length=5000)
    needs: list[str] = Field(default_factory=list)
    # Honeypot: must be empty for real submissions.
    website: str = ""

    @field_validator("needs")
    @classmethod
    def _validate_needs(cls, v: list[str]) -> list[str]:
        # silently drop anything not in the allowed set; don't reject the whole submission
        return [n for n in v if n in ALLOWED_NEEDS][:6]


# ---------------------------------------------------------------------------
# Email delivery
# ---------------------------------------------------------------------------


def _format_email(payload: ContactPayload, ip: str, ua: str) -> tuple[str, str, str]:
    """Return (subject, text_body, html_body)."""
    ts = datetime.now(MTY_TZ).strftime("%Y-%m-%d %H:%M %Z")
    needs = ", ".join(payload.needs) if payload.needs else "—"
    subject = f"New inquiry · {payload.name}" + (f" · {payload.company}" if payload.company else "")

    text = (
        f"New contact form submission\n"
        f"---------------------------\n"
        f"Name:    {payload.name}\n"
        f"Email:   {payload.email}\n"
        f"Company: {payload.company or '—'}\n"
        f"Needs:   {needs}\n\n"
        f"Message:\n{payload.message or '—'}\n\n"
        f"---\n"
        f"Submitted: {ts}\n"
        f"IP:        {ip}\n"
        f"UA:        {ua}\n"
    )

    # Minimal HTML — keep it safe by escaping.
    import html as _html

    def esc(s: str) -> str:
        return _html.escape(s or "—").replace("\n", "<br/>")

    html_body = f"""\
<div style="font-family:ui-sans-serif,system-ui,sans-serif;color:#14142b">
  <h2 style="margin:0 0 12px">New inquiry</h2>
  <table style="border-collapse:collapse">
    <tr><td style="padding:4px 12px 4px 0;color:#8a8aa8">Name</td><td>{esc(payload.name)}</td></tr>
    <tr><td style="padding:4px 12px 4px 0;color:#8a8aa8">Email</td><td><a href="mailto:{esc(payload.email)}">{esc(payload.email)}</a></td></tr>
    <tr><td style="padding:4px 12px 4px 0;color:#8a8aa8">Company</td><td>{esc(payload.company)}</td></tr>
    <tr><td style="padding:4px 12px 4px 0;color:#8a8aa8">Needs</td><td>{esc(needs)}</td></tr>
  </table>
  <h3 style="margin:18px 0 6px">Message</h3>
  <div style="white-space:pre-wrap;line-height:1.5">{esc(payload.message)}</div>
  <hr style="border:none;border-top:1px solid #eee;margin:18px 0"/>
  <p style="color:#8a8aa8;font-size:12px;margin:0">
    Submitted {esc(ts)}<br/>
    IP {esc(ip)}<br/>
    UA {esc(ua)}
  </p>
</div>
"""
    return subject, text, html_body


async def _send_via_resend(subject: str, text: str, html_body: str, reply_to: str) -> None:
    if not RESEND_API_KEY:
        # Dev mode: log and continue so the form path is testable without a key.
        log.warning("RESEND_API_KEY not set — would have sent: %s", subject)
        log.info("Email body:\n%s", text)
        return

    payload = {
        "from": CONTACT_FROM,
        "to": [CONTACT_TO],
        "subject": subject,
        "text": text,
        "html": html_body,
        "reply_to": reply_to,
    }
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post("https://api.resend.com/emails", json=payload, headers=headers)
    if r.status_code >= 300:
        log.error("Resend error %s: %s", r.status_code, r.text)
        raise HTTPException(status_code=502, detail="Email delivery failed. Try again or email hola@letsdaydream.ai.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="Daydream marketing site", docs_url=None, redoc_url=None)


def _client_ip(request: Request) -> str:
    # Render / most PaaS hosts set X-Forwarded-For. Take the first IP.
    fwd = request.headers.get("x-forwarded-for") or request.headers.get("x-real-ip")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/contact")
async def contact(payload: ContactPayload, request: Request) -> JSONResponse:
    ip = _client_ip(request)
    ua = request.headers.get("user-agent", "")[:300]

    # Honeypot: pretend it succeeded so bots don't learn the field is checked.
    if payload.website.strip():
        log.info("Honeypot tripped from %s", ip)
        return JSONResponse({"ok": True})

    err = _check_rate_limit(ip)
    if err:
        raise HTTPException(status_code=429, detail=err)

    subject, text, html_body = _format_email(payload, ip, ua)
    await _send_via_resend(subject, text, html_body, reply_to=payload.email)

    return JSONResponse({"ok": True})


# ---------------------------------------------------------------------------
# Static site
# ---------------------------------------------------------------------------


@app.get("/")
async def home() -> FileResponse:
    return FileResponse(SITE_DIR / "index.html")


@app.get("/work/octus")
async def octus() -> FileResponse:
    return FileResponse(SITE_DIR / "octus.html")


@app.get("/propuesta-risk")
async def propuesta_risk() -> FileResponse:
    return FileResponse(SITE_DIR / "propuesta-risk" / "index.html")


@app.get("/propuesta-risk/print")
async def propuesta_risk_print() -> FileResponse:
    return FileResponse(SITE_DIR / "propuesta-risk" / "print.html")


# Re-validate that the site dir exists before mounting — surfaces a clear
# error if the image is built without the site/ tree.
if not SITE_DIR.is_dir():
    raise RuntimeError(f"site/ directory not found at {SITE_DIR}")

# Serve everything else (styles, JS, /assets/...) from the site dir.
app.mount("/", StaticFiles(directory=str(SITE_DIR), html=False), name="site")
