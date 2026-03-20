# Changelog

All notable changes to AgentInterviewer are documented in this file.

## [1.2.0] - 2025-03-19

### Added
- Dark mode support across all frontend pages
- Anti-cheating measures in EvaluatorAgent (short answer penalty, keyword validation)
- PanelInterviewerAgent with 3 rotating personas (Technical Lead, System Architect, HR Manager)
- MultiRoundAgent with 5-round interview pipeline (Phone Screen, Technical, System Design, Behavioral, Offer)
- Technical specification document (`docs/TECHNICAL_SPECIFICATION.md`)
- CI/CD workflows for GitHub Actions
- GitHub Pages landing page
- CONTRIBUTING guide
- This changelog

### Improved
- Evaluator scoring with difficulty adjustment recommendations
- Coach agent with expanded domain-specific tips and resources

### Tests
- 254 tests passing

---

## [1.1.0] - 2025-02-15

### Added
- SalaryCoachAgent for salary negotiation practice with INR offers
- ResumeAnalyzerAgent for resume parsing and tailored question generation
- ForumPostingAgent for community content (daily challenges, discussions, social posts)
- GroupManagerAgent for study group CRUD and leaderboards
- AdminAnalyticsAgent for admin dashboard reports (system overview, user report, agent performance, cost report)
- Pricing page (`/pricing`)
- Forums page (`/forums`)
- Groups page (`/groups`)
- Login page (`/login`)
- Profile page (`/profile`)
- Onboarding page (`/onboarding`)
- Admin page (`/admin`)
- Leaderboard page (`/leaderboard`)
- Interview page (`/interview`)
- PWA manifest for installable web app

### Tests
- 229 tests passing

---

## [1.0.0] - 2025-01-10

### Added
- Initial release of AgentInterviewer
- 9 core agents: InterviewerAgent, EvaluatorAgent, CoachAgent, ReportAgent, GoalTrackerAgent, MotivatorAgent, SkillMonitorAgent, QuizMasterAgent, ChatBotAgent
- 10 tech domains: Python, JavaScript, React, iOS, Android, ReactNative, Java, DevOps, SystemDesign, HR
- Gamification engine with XP system (10 actions), 30 levels (6 tiers), 30 achievements, streak tracking with grace period
- Real-time WebSocket streaming
- Voice input support
- Quick quiz mode with MCQ questions
- Dashboard with skill radar charts (Recharts)
- Pipelines: full_evaluation (interviewer -> evaluator -> coach), session_report
- Scheduled jobs: daily motivation (24h), health summary (1h)
- Custom gamification API endpoint (`/api/v1/gamification`)
- Docker Compose deployment (frontend :3001, backend :8081)
- Full mock mode (works without API key)
- 7 frontend pages: Home, Dashboard, Quiz, Chat, Results, Goals, Leaderboard

### Tech Stack
- Backend: Python 3.11+ / AgentX Framework
- Frontend: Next.js 14 / React 18 / Tailwind CSS / Recharts
- Database: SQLite (dev) / PostgreSQL (prod)
