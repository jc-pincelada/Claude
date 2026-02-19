# Viewnear - Client Delivery Plan

> **Status:** Draft
> **Created:** 2026-02-19
> **Owner:** Delivery Agent
> **Review Cadence:** Biweekly

---

## 1. Engagement Overview

| Field               | Value                              |
|---------------------|------------------------------------|
| Client              | Viewnear                           |
| Engagement Type     | New Client Onboarding & Delivery   |
| Start Date          | TBD                                |
| Target Go-Live      | TBD                                |
| Delivery Model      | Agile (Scrum-based)                |
| Methodology         | Iterative, outcome-driven          |

---

## 2. Delivery Structure

### 2.1 Phases

| Phase                | Duration (est.) | Key Outcomes                                      |
|----------------------|-----------------|---------------------------------------------------|
| **Discovery**        | 2 weeks         | Requirements validated, risks identified, backlog seeded |
| **Foundation**       | 2-3 weeks       | Architecture decisions, environments provisioned, CI/CD baseline |
| **Build (Iterative)**| 6-10 sprints    | Working increments delivered per sprint            |
| **Hardening**        | 1-2 sprints     | Performance, security, UAT sign-off                |
| **Go-Live & Transition** | 1 sprint   | Production deployment, runbook handover, hypercare begins |
| **Hypercare**        | 2-4 weeks       | Defect triage, knowledge transfer, SLA stabilization |

### 2.2 Team Structure

| Role                        | Responsibility                                                   |
|-----------------------------|------------------------------------------------------------------|
| **Delivery Lead**           | Overall accountability, client relationship, escalation path     |
| **Product Owner (Client)**  | Backlog prioritization, acceptance criteria, business decisions   |
| **Scrum Master**            | Ceremony facilitation, impediment removal, process health        |
| **Tech Lead**               | Architecture oversight, code quality, technical decisions         |
| **Engineers (3-5)**         | Sprint execution, code review, testing                           |
| **QA Lead**                 | Test strategy, automation, release readiness                     |

### 2.3 RACI Matrix

| Activity                     | Delivery Lead | Product Owner | Tech Lead | Scrum Master |
|------------------------------|:---:|:---:|:---:|:---:|
| Backlog prioritization       | C   | A/R | C   | I   |
| Sprint planning              | I   | A   | R   | R   |
| Architecture decisions       | A   | I   | R   | I   |
| Release approval             | A   | R   | C   | I   |
| Risk & issue management      | A/R | C   | C   | R   |
| Stakeholder communication    | R   | R   | I   | I   |
| Retrospective actions        | C   | I   | C   | A/R |

> **A** = Accountable, **R** = Responsible, **C** = Consulted, **I** = Informed

---

## 3. Governance

### 3.1 Decision Authority

| Decision Type                    | Authority                    | Escalation Path                     |
|----------------------------------|------------------------------|--------------------------------------|
| Day-to-day technical decisions   | Tech Lead                    | Delivery Lead                        |
| Scope changes (< 1 sprint)      | Product Owner + Delivery Lead| Steering Committee                   |
| Scope changes (> 1 sprint)      | Steering Committee           | Executive Sponsor                    |
| Budget reallocation              | Steering Committee           | Executive Sponsor                    |
| Go/No-Go release                 | Delivery Lead + Product Owner| Steering Committee                   |
| Team composition changes         | Delivery Lead                | Steering Committee                   |

### 3.2 Steering Committee

- **Composition:** Executive Sponsor (Viewnear), Delivery Lead, Product Owner, Account Manager
- **Cadence:** Monthly (or ad hoc for critical escalations)
- **Purpose:** Strategic alignment, budget oversight, major risk decisions, scope arbitration

### 3.3 Change Control

1. Change requests logged in backlog with `change-request` label
2. Impact assessed by Tech Lead (effort, risk, dependencies)
3. Prioritized by Product Owner against existing backlog
4. Approved/rejected at next Sprint Planning or Steering Committee (if large)
5. All approved changes tracked with acceptance criteria before entering a sprint

### 3.4 Risk Management

| Risk Category       | Review Frequency | Owner          | Mitigation Approach                  |
|---------------------|------------------|----------------|--------------------------------------|
| Technical           | Weekly           | Tech Lead      | Spikes, POCs, architecture reviews   |
| Schedule            | Per sprint       | Scrum Master   | Velocity tracking, buffer management |
| Scope               | Per sprint       | Product Owner  | MoSCoW prioritization, MVP focus     |
| Resource            | Biweekly         | Delivery Lead  | Cross-training, capacity planning    |
| Dependency/External | Weekly           | Delivery Lead  | Dependency board, early integration  |

---

## 4. Cadence

### 4.1 Sprint Rhythm

| Ceremony              | Frequency         | Duration   | Participants                        |
|-----------------------|-------------------|------------|-------------------------------------|
| Sprint Planning       | Biweekly (Day 1)  | 2 hours    | Full team + Product Owner           |
| Daily Standup         | Daily             | 15 min     | Engineering team + Scrum Master     |
| Backlog Refinement    | Weekly (mid-sprint)| 1 hour    | Product Owner, Tech Lead, Scrum Master |
| Sprint Review / Demo  | Biweekly (last day)| 1 hour    | Full team + client stakeholders     |
| Retrospective         | Biweekly (last day)| 45 min    | Full team (internal)                |

### 4.2 Reporting & Communication

| Artifact / Channel          | Frequency     | Audience                  | Owner          |
|-----------------------------|---------------|---------------------------|----------------|
| Sprint Report               | Biweekly      | Client stakeholders       | Delivery Lead  |
| Burndown / Velocity Charts  | Per sprint    | Team + Product Owner      | Scrum Master   |
| Risk & Issue Register       | Weekly update | Steering Committee        | Delivery Lead  |
| Release Notes               | Per release   | Client stakeholders       | QA Lead        |
| Steering Committee Deck     | Monthly       | Executives                | Delivery Lead  |
| Slack/Teams Channel         | Ongoing       | Day-to-day collaboration  | All            |

### 4.3 Sprint Duration

- **Recommended:** 2-week sprints
- **Rationale:** Balances delivery cadence with enough runway for meaningful increments; aligns well with biweekly client demos and reporting

---

## 5. Quality & Definition of Done

### 5.1 Definition of Done (per Story)

- [ ] Code complete and peer-reviewed
- [ ] Unit tests written and passing (minimum 80% coverage on new code)
- [ ] Integration tests passing
- [ ] Acceptance criteria verified by QA
- [ ] No critical or high-severity defects open
- [ ] Documentation updated (if applicable)
- [ ] Product Owner acceptance

### 5.2 Definition of Done (per Sprint)

- [ ] All committed stories meet story-level DoD
- [ ] Regression suite green
- [ ] Sprint demo completed with client
- [ ] Sprint retrospective held and actions logged
- [ ] Updated release/deployment notes

### 5.3 Definition of Done (per Release)

- [ ] All sprint-level DoD criteria met
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] UAT sign-off obtained from client
- [ ] Runbook and rollback plan documented
- [ ] Go/No-Go decision recorded

---

## 6. Tooling & Environments

| Concern               | Tooling (Recommended)        | Notes                          |
|------------------------|------------------------------|--------------------------------|
| Project tracking       | Jira / Linear                | Backlog, sprints, reporting    |
| Source control         | GitHub / GitLab              | Branch protection, PR reviews  |
| CI/CD                  | GitHub Actions / GitLab CI   | Automated build, test, deploy  |
| Communication          | Slack / Microsoft Teams      | Dedicated client channel       |
| Documentation          | Confluence / Notion          | Decision logs, runbooks        |
| Monitoring (prod)      | Datadog / Grafana            | SLA dashboards, alerting       |

### Environment Strategy

| Environment  | Purpose                   | Refresh Cadence         |
|-------------|---------------------------|-------------------------|
| Dev          | Active development         | Continuous (per commit) |
| Staging      | Integration & QA           | Per sprint / on-demand  |
| UAT          | Client acceptance testing  | Per release candidate   |
| Production   | Live system                | Controlled releases     |

---

## 7. Success Metrics & KPIs

| Metric                        | Target            | Measured By        |
|-------------------------------|-------------------|--------------------|
| Sprint velocity (stabilized)  | Consistent +/- 15%| Scrum Master       |
| Defect escape rate            | < 5% to UAT       | QA Lead            |
| Sprint commitment accuracy    | > 85%             | Scrum Master       |
| Client satisfaction (CSAT)    | >= 4/5            | Delivery Lead      |
| Cycle time (story)            | < 5 business days | Tech Lead          |
| Lead time (idea to production)| Decreasing trend  | Delivery Lead      |
| SLA compliance (hypercare)    | >= 99%            | Delivery Lead      |

---

## 8. Escalation Path

```
Engineer / QA
    --> Scrum Master (process / impediment)
    --> Tech Lead (technical blocker)
        --> Delivery Lead (cross-cutting, client-facing)
            --> Steering Committee (strategic, budget, major scope)
                --> Executive Sponsor (final authority)
```

**Escalation SLAs:**
- Blocker impacting sprint goal: escalate within **4 hours**
- Risk to milestone/release: escalate within **1 business day**
- Budget or contractual issue: escalate within **2 business days**

---

## 9. Onboarding Checklist (New Client Kickoff)

- [ ] Signed SOW / contract in place
- [ ] Kickoff meeting scheduled with key stakeholders
- [ ] Access provisioned (repos, project board, communication channels)
- [ ] Discovery workshops planned
- [ ] Initial backlog seeded from requirements
- [ ] Environments provisioned
- [ ] Team introduced and RACI confirmed
- [ ] Reporting cadence agreed and calendar invites sent
- [ ] Steering Committee schedule established
- [ ] Risk register initialized

---

## 10. Appendix

### A. Glossary

| Term       | Definition                                                        |
|------------|-------------------------------------------------------------------|
| MoSCoW     | Must have, Should have, Could have, Won't have (prioritization)   |
| DoD        | Definition of Done                                                |
| UAT        | User Acceptance Testing                                           |
| Hypercare  | Post-launch intensive support period                              |
| CSAT       | Customer Satisfaction Score                                       |
| SLA        | Service Level Agreement                                           |
| SLO        | Service Level Objective                                           |

### B. Document History

| Date       | Author         | Change Description         |
|------------|----------------|----------------------------|
| 2026-02-19 | Delivery Agent | Initial draft              |

---

*This is a living document. It should be reviewed and updated at each Steering Committee meeting or when significant delivery changes occur.*
