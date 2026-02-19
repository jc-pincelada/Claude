# Delivery Agent

An AI-powered conversational agent specialized in:

- **Software Delivery Life Cycle (SDLC)** — Agile, Scrum, Kanban, SAFe, DevOps, CI/CD, release management
- **Service Delivery** — ITIL v4, SLA/SLO management, continual improvement
- **Management Frameworks** — PMP, PRINCE2, risk management, stakeholder communication
- **Customer Service** — expectation management, escalation handling, account management
- **Conflict Resolution** — de-escalation, negotiation, mediation
- **Outcome-Oriented Delivery** — OKRs, KPIs, value stream optimization

Powered by Claude (Anthropic).

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install -e .
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Run the agent

```bash
# If installed as a package:
delivery-agent

# Or run directly:
python -m delivery_agent.cli
```

## Usage

```
You: We're struggling with long release cycles. Our team does 2-week sprints
     but deployments happen only once a quarter. How can we improve?

Agent: [Provides actionable guidance on CI/CD, release trains, deployment
       frequency improvement, etc.]
```

### Commands

| Command  | Description                |
|----------|----------------------------|
| `/reset` | Clear conversation history |
| `/quit`  | Exit the agent             |

## Project Structure

```
src/delivery_agent/
├── __init__.py
├── agent.py      # Core agent with Claude API integration
├── cli.py        # Terminal chat interface
└── prompts.py    # System prompt with domain expertise
```

## Configuration

By default the agent uses `claude-sonnet-4-5-20250929`. To use a different model:

```python
from delivery_agent.agent import DeliveryAgent

agent = DeliveryAgent(model="claude-opus-4-6")
response = agent.chat("How should we structure our SLAs?")
```
