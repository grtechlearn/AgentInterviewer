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
pip install -r requirements.txt  # Installs AgentX from GitHub + aiohttp
python app.py                    # Starts on :8081 (mock mode, no API key needed)
```

To enable real LLM responses:
```bash
export ANTHROPIC_API_KEY=your-key-here
python app.py
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

## Agents (16)

| # | Agent | Purpose |
|---|-------|---------|
| 1 | InterviewerAgent | Mock interviews with adaptive difficulty |
| 2 | EvaluatorAgent | Answer scoring (0-100) with feedback |
| 3 | CoachAgent | Learning tips and motivation |
| 4 | ReportAgent | Session reports and study plans |
| 5 | GoalTrackerAgent | Goals, streaks, daily check-ins |
| 6 | MotivatorAgent | Daily motivation, topic of the day |
| 7 | SkillMonitorAgent | Skill levels per domain |
| 8 | QuizMasterAgent | Quick MCQ quizzes |
| 9 | ChatBotAgent | Free-form AI chat |
| 10 | SalaryCoachAgent | Salary negotiation practice |
| 11 | ResumeAnalyzerAgent | Resume parsing, tailored questions |
| 12 | ForumPostingAgent | Auto-generate forum content |
| 13 | GroupManagerAgent | Study group management |
| 14 | AdminAnalyticsAgent | System analytics and reports |
| 15 | PanelInterviewerAgent | Multi-persona panel interviews |
| 16 | MultiRoundAgent | 5-round interview pipeline |

## Tech Stack

- **Backend:** Python 3.11+ / AgentX Framework
- **Frontend:** Next.js 14 / React 18 / Tailwind CSS / Recharts
- **Database:** SQLite (dev) / PostgreSQL (prod)

## License

MIT
