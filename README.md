# AgentInterviewer

AI-Powered Mock Interview Platform built with [AgentX](https://github.com/grtechlearn/agentx)

## Features

- 10 tech domains (Python, React, iOS, Android, Java, etc.)
- AI-powered question generation and answer evaluation
- Gamification (XP, levels, streaks, achievements)
- Real-time streaming via WebSocket
- Voice input support
- Quick quiz mode
- Dashboard with skill radar charts
- Works in mock mode (no API key needed)

## Architecture

```
Next.js Frontend :3001  <-->  AgentX Backend :8081
```

## Quick Start

### Backend

```bash
cd backend
pip install -e ../../agentx  # Install AgentX framework
python app.py                # Starts on :8081
```

### Frontend

```bash
cd frontend
npm install
npm run dev                  # Starts on :3000
```

### Docker

```bash
docker compose up -d
# Frontend: http://localhost:3001
# Backend API: http://localhost:8081/api/v1/health
```

## API

- `POST /api/v1/chat` — Chat with agents
- `POST /api/v1/dispatch` — Direct agent calls
- `WS /ws` — WebSocket streaming
- `GET /api/v1/health` — Health check

## Agents (9)

1. **InterviewerAgent** — Question generation
2. **EvaluatorAgent** — Answer scoring
3. **CoachAgent** — Learning tips
4. **ReportAgent** — Session reports
5. **GoalTrackerAgent** — Goals & streaks
6. **MotivatorAgent** — Daily motivation
7. **SkillMonitorAgent** — Skill tracking
8. **QuizMasterAgent** — Quick quizzes
9. **ChatBotAgent** — Free-form chat

## Tech Stack

- **Backend:** Python 3.11+ / AgentX Framework
- **Frontend:** Next.js 14 / React 18 / Tailwind CSS / Recharts
- **Database:** SQLite (dev) / PostgreSQL (prod)

## License

MIT
