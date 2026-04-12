---
title: Email Triage OpenEnv
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
tags:
  - openenv
---

# Email Triage Environment

Production-grade OpenEnv for training AI agents on real workplace email management.

## Why Email Triage?
Professionals spend 2.6 hours daily on email. This environment trains agents to prioritize urgent vs routine vs spam, extract actionable tasks, and draft professional responses. Immediate enterprise value - not a toy or game.

## Tasks
| Task | Difficulty | Description |
|------|-----------|-------------|
| task_1_classify | Easy | Classify 6 emails as urgent/normal/spam |
| task_2_extract | Medium | Extract action items from 2 emails |
| task_3_draft | Hard | Draft professional complaint replies |

## Reward Design
All scores strictly in (0.01, 0.99):
- task_1_classify: 0.95 correct, 0.35 close, 0.05 wrong
- task_2_extract: Proportional across 7 expected action groups
- task_3_draft: Multi-factor: apology + acknowledge + resolve + compensate + contact + timeline

## API
- POST /reset - Start episode
- POST /step - Take action
- GET /state - Current state
- GET /tasks - List tasks
- POST /grader - Get score
- GET /baseline - Baseline scores
- GET /health - Health check

## Baseline Scores
| Task | Score |
|------|-------|
| task_1_classify | 0.77 |
| task_2_extract | 0.95 |
| task_3_draft | 0.93 |
| Average | 0.88 |

## Setup
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
