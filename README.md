# Daydream marketing site

The Daydream studio home page (single-page) plus the Octus case-study
subpage, served by a tiny FastAPI backend that handles the contact form.

## Stack

- **Frontend** — static HTML / CSS / vanilla JS from the design handoff
  (`site/`). Dev-only bits removed (image-slot placeholders, tweaks panel,
  edit-mode `postMessage` hooks).
- **Backend** — FastAPI (`src/server/app.py`). Serves the static files and
  exposes `POST /api/contact`: server-side validation, honeypot, per-IP
  rate limit (1 / 30s, 5 / hr), email delivery via Resend.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in RESEND_API_KEY (optional in dev — see below)

PYTHONPATH=src uvicorn server.app:app --reload --port 8000
```

Open http://127.0.0.1:8000.

Without `RESEND_API_KEY` set, the contact endpoint still returns `200` and
logs the would-be email body to stdout — handy for testing the form path
without sending real mail.

## Environment variables

| Var | Required | Default | Notes |
|---|---|---|---|
| `RESEND_API_KEY` | yes (prod) | — | Get one at https://resend.com/api-keys |
| `CONTACT_TO` | no | `hola@letsdaydream.ai` | Inbox that receives leads. |
| `CONTACT_FROM` | no | `Daydream <onboarding@resend.dev>` | Must be a Resend-verified sender. Switch to `Daydream <hola@letsdaydream.ai>` after verifying the domain in Resend. |
| `PORT` | no | `8000` | Set by the host. |
| `LOG_LEVEL` | no | `INFO` | Standard `logging` levels. |

## Deploy to Render

1. Push this repo to GitHub.
2. In Render, **New → Blueprint** and point at the repo. Render reads
   `render.yaml` and creates a Docker web service.
3. In the service's **Environment** tab, set `RESEND_API_KEY` (the YAML
   marks it `sync: false` so it has to be entered manually — never commit
   the key).
4. First deploy auto-builds the `Dockerfile`. Health check is `/healthz`.

## Email deliverability before launch

The default `CONTACT_FROM` uses Resend's onboarding sender so the form
works on day one. Before any traffic, do the proper setup:

1. Add `letsdaydream.ai` as a domain in Resend.
2. Add the SPF, DKIM, and DMARC DNS records Resend provides.
3. Switch `CONTACT_FROM` to `Daydream <hola@letsdaydream.ai>` (env var, no
   code change).
4. Set up forwarding from `hola@letsdaydream.ai` to whoever triages leads.

## Project layout

```
.
├── Dockerfile            # production container
├── render.yaml           # Render blueprint
├── .env.example          # env var template
├── pyproject.toml
├── requirements.txt
├── site/                 # static site (served as-is)
│   ├── index.html        # home page
│   ├── octus.html        # /work/octus
│   ├── styles.css
│   ├── case-study.css
│   ├── site.js           # time / chips / reveal / form submit
│   └── assets/logos/*.png
└── src/
    └── server/
        └── app.py        # FastAPI app: static + /api/contact
```

## What's NOT done (deliberately)

The design handoff sketched out a much larger Next.js + Sanity CMS port.
This codebase ships the site as static HTML with a minimal contact
backend — enough to publish. The handoff items still on the table:

- **Booking-status badge** ("Booking Q3 — 2 spots") — currently
  hard-coded in `site/index.html`. Edit by hand for now.
- **Clients list / case studies** — hard-coded in HTML. Adding a new
  case study means duplicating `site/octus.html` and adding a route to
  `src/server/app.py`.
- **Theme/type variants** (`dusk`, `aurora`, `chroma`, …) — left in
  `styles.css` but unreachable without the tweaks panel. Switch by
  hand-editing the `<html data-theme=…>` attribute if you want.
- **Octus product mocks** — the page uses gradient placeholders where
  real screenshots would go. Drop real images into
  `site/assets/work/octus/` and reference them from `site/octus.html`
  when ready.

When the studio outgrows this, the README in the original design
handoff (`design_handoff_daydream_website/README.md` in the upload zip)
has the full CMS schema to port to.
