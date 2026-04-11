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

Real-world OpenEnv for training AI agents to triage workplace emails.

## Tasks
| Task | Difficulty | Description |
|------|-----------|-------------|
| task_1_classify | Easy | Classify 6 emails as urgent/normal/spam |
| task_2_extract | Medium | Extract action items from 2 emails |
| task_3_draft | Hard | Draft professional reply to complaints |

## API
- POST /reset - Start episode
- POST /step - Take action
- GET /state - Current state
- GET /tasks - List tasks
- POST /grader - Get score
- GET /baseline - Baseline scores
- GET /health - Health check
