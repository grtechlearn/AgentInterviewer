# AgentInterviewer - Technical Specification

## Overview

AgentInterviewer is an AI-powered mock interview platform built on the [AgentX](https://github.com/grtechlearn/agentx) multi-agent framework. It provides interview practice across 10 tech domains with gamification, real-time streaming, and adaptive difficulty.

---

## Architecture

```
+---------------------------+          +------------------------------+
|   Next.js Frontend :3001  |  <--->   |   AgentX Backend :8081       |
|   React 18 / Tailwind CSS |  HTTP/WS |   Python 3.11+ / 16 Agents  |
+---------------------------+          +------------------------------+
                                                  |
                                       +----------+----------+
                                       | SQLite (dev)        |
                                       | PostgreSQL (prod)   |
                                       +---------------------+
```

- **Frontend:** Next.js 14, React 18, Tailwind CSS, Recharts
- **Backend:** Python 3.11+, AgentX framework (orchestrator, daemon, scheduler)
- **Communication:** REST API (`/api/v1/*`), WebSocket (`/ws`)
- **Database:** AgentX DatabaseConfig (in-memory for dev, SQLite/PostgreSQL for prod)
- **LLM:** Anthropic Claude (claude-sonnet-4-6 default, configurable via `AGENTX_MODEL`)

---

## Agents (16)

All agents extend `agentx.core.agent.BaseAgent` and implement `async process(message, context)`. Every agent works fully in mock mode (no API key required) using built-in mock data.

### 1. InterviewerAgent (`interviewer`)
- **Role:** Interview Question Generator
- **Actions:** `start_interview`, `next_question`, `follow_up`
- **Mock mode:** Selects from a bank of 6 questions per domain (60 total across 10 domains), avoids repeating topics within a session.
- **Routing priority:** 10

### 2. EvaluatorAgent (`evaluator`)
- **Role:** Answer Evaluator
- **Actions:** `evaluate` (also matches messages with both `answer` and `question` fields)
- **Mock mode:** Keyword-matching scoring per domain (10-14 keywords each). Scores based on keyword hits (up to 50 pts) + answer length (up to 30 pts) + base 20 pts. Reports correct points, incorrect points, missing points, and difficulty adjustment recommendation.
- **Routing priority:** 10

### 3. CoachAgent (`coach`)
- **Role:** Interview Coach
- **Actions:** `coach`
- **Mock mode:** Returns domain-specific tips (3 per domain), resource recommendations, motivational message based on score, and next topic suggestion from uncovered topics.
- **Routing priority:** 8

### 4. ReportAgent (`report`)
- **Role:** Session Report Generator
- **Actions:** `report`
- **Mock mode:** Aggregates all evaluations from context, computes overall score, per-question breakdown, strengths/weaknesses, and a domain-specific study plan.
- **Routing priority:** 8

### 5. GoalTrackerAgent (`goal_tracker`)
- **Role:** Goal & Streak Tracker
- **Actions:** `set_goal`, `get_progress`, `update_streak`, `check_daily`
- **Mock mode:** Stores goals and streaks in AgentX context. Tracks daily question targets, weekly targets, and best streak.
- **Routing priority:** 7

### 6. MotivatorAgent (`motivator`)
- **Role:** Motivation Coach
- **Actions:** `daily_message`, `topic_of_day`, `celebrate_milestone`
- **Mock mode:** Rotates through 10 daily messages (indexed by day-of-year), 7 topic-of-day entries, and milestone celebrations at 10/25/50/100 questions and 7/30 day streaks.
- **Routing priority:** 7

### 7. SkillMonitorAgent (`skill_monitor`)
- **Role:** Skill Level Tracker
- **Actions:** `update_skill`, `get_skills`, `get_weak_areas`
- **Mock mode:** Maintains weighted-average scores per domain (60% old + 40% new). Classifies skills as beginner (0-30), intermediate (31-70), or advanced (71-100). Keeps last 20 score entries in history.
- **Routing priority:** 7

### 8. QuizMasterAgent (`quiz_master`)
- **Role:** Quiz Master
- **Actions:** `start_quiz`, `submit_answer`, `get_results`
- **Mock mode:** MCQ quizzes with 10 questions per domain (Python, JavaScript). Tracks score, answers, and calculates percentage.
- **Routing priority:** 9

### 9. ChatBotAgent (`chatbot`)
- **Role:** Tech Chat Assistant (fallback agent)
- **Actions:** Handles any unmatched message
- **Mock mode:** Keyword-matched canned responses for 10 topics (python, javascript, react, interview, system design, data structures, algorithms, career, resume, salary).
- **Routing priority:** Fallback

### 10. SalaryCoachAgent (`salary_coach`)
- **Role:** Salary Negotiation Coach
- **Actions:** `start_negotiation`, `respond`, `get_tips`
- **Mock mode:** Generates mock offers in INR (5 role/company combos). Classifies negotiation strategy (aggressive/confident/passive/reasonable) via keyword detection and rates it. Provides counter-offer suggestions and random tips from a bank of 10.
- **Routing priority:** 7

### 11. ResumeAnalyzerAgent (`resume_analyzer`)
- **Role:** Resume Analyzer
- **Actions:** `analyze_resume`, `get_tailored_questions`
- **Mock mode:** Extracts skills via keyword matching across 9 domain keyword lists. Detects experience level (junior/mid/senior) from keywords and years. Generates tailored interview questions based on detected domains.
- **Routing priority:** 8

### 12. ForumPostingAgent (`forum_posting`)
- **Role:** Community Content Generator
- **Actions:** `daily_challenge`, `topic_discussion`, `weekly_summary`, `social_post`
- **Mock mode:** Returns random daily coding challenges (5 templates), discussion topics (5 templates), weekly stats summaries, and social media posts for Twitter/LinkedIn with template variables.
- **Routing priority:** 6

### 13. GroupManagerAgent (`group_manager`)
- **Role:** Study Group Manager
- **Actions:** `create_group`, `add_member`, `get_group_stats`, `set_group_task`, `get_leaderboard`
- **Mock mode:** Full CRUD for study groups stored in AgentX context. Creates groups with domain, manages members, assigns tasks, and generates mock leaderboards.
- **Routing priority:** 6

### 14. AdminAnalyticsAgent (`admin_analytics`)
- **Role:** Admin Analytics Reporter
- **Actions:** `system_overview`, `user_report`, `agent_performance`, `cost_report`
- **Mock mode:** Returns mock analytics data: 1247 total users, 389 active, per-agent request counts and latencies, cost breakdowns (LLM API, infrastructure, storage, bandwidth), retention rates.
- **Routing priority:** 5

### 15. PanelInterviewerAgent (`panel_interviewer`)
- **Role:** Panel Interview Simulator
- **Actions:** `start_panel`, `panel_question`, `panel_evaluate`
- **Mock mode:** Simulates 3 personas rotating questions: Priya Sharma (Technical Lead, 5 deep-technical questions), Arjun Mehta (System Architect, 5 design questions), Kavitha Rajan (HR Manager, 5 behavioral questions). Scores based on answer length + random factor.
- **Routing priority:** 9

### 16. MultiRoundAgent (`multi_round`)
- **Role:** Multi-Round Interview Pipeline Manager
- **Actions:** `start_pipeline`, `next_round`, `get_pipeline_status`, `pipeline_report`
- **Mock mode:** Manages a 5-round pipeline: Phone Screen (easy, 5 Qs) -> Technical (medium, 8 Qs) -> System Design (hard, 2 Qs) -> Behavioral (medium, 5 Qs) -> Offer (medium, 3 Qs). Tracks scores per round and generates final recommendation.
- **Routing priority:** 9

---

## Pipelines

Defined in the orchestrator:

| Pipeline | Agents |
|---|---|
| `full_evaluation` | interviewer -> evaluator -> coach |
| `session_report` | report |

---

## Gamification Engine

Located in `backend/gamification/`.

### XP System (`xp_engine.py`)

| Action | Base XP |
|---|---|
| `answer_question` | 10 |
| `correct_answer` | 20 |
| `perfect_score` | 50 |
| `complete_session` | 30 |
| `daily_streak` | 15 |
| `weekly_streak` | 50 |
| `first_question` | 25 |
| `quiz_complete` | 20 |
| `quiz_perfect` | 75 |
| `achievement_unlock` | 10 |

- Score-based multiplier: `base * (0.5 + score/100)` for answer actions
- Perfect score bonus: +50 XP when score >= 95

### Level System

30 levels across 6 tiers:

| Tier | Levels | XP Range |
|---|---|---|
| Apprentice | 1-5 | 0 - 700 |
| Developer | 6-10 | 1,000 - 3,200 |
| Senior | 11-15 | 4,000 - 9,200 |
| Expert | 16-20 | 11,000 - 22,000 |
| Master | 21-25 | 26,000 - 52,000 |
| Legend | 26-30 | 62,000 - 125,000 |

### Achievements (`achievements.py`)

30 achievements across 7 categories:

- **Milestone:** First Step, Getting Warmed Up, Half Century, Centurion, Marathoner, Interview Ready, Seasoned
- **Streak:** On Fire (5d), Week Warrior (7d), Fortnight Force (14d), Monthly Master (30d), Two-Month Titan (60d), 100 Days Strong
- **Skill:** Flawless, Solid Performer, Top Performer, Elite, Perfectionist
- **Breadth:** Explorer (2 domains), Versatile (5), Full Stack (10)
- **Quiz:** Quiz Taker, Quiz Enthusiast, Quiz Ace
- **Level:** Rising Star (5), Developer (10), Senior Dev (15), Expert (20), Master (25)
- **Special:** Night Owl

### Streaks (`streaks.py`)

- 1-day grace period before streak breaks
- Streak bonus XP: 3d=10, 7d=20, 14d=30, 30d=50, 60d=75, 100d=100

### Gamification API Endpoint

`POST /api/v1/gamification` with actions:
- `xp` - Calculate XP for an action
- `level` - Get level progress for total XP
- `achievements` - Check newly unlocked achievements
- `all_achievements` - List all achievement definitions
- `streak_message` - Get streak encouragement message

---

## API Endpoints

### Core AgentX Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/chat` | Chat with agents (orchestrator routes by content) |
| `POST` | `/api/v1/dispatch` | Direct agent dispatch with `action` field |
| `WS` | `/ws` | WebSocket streaming for real-time responses |
| `GET` | `/api/v1/health` | Health check |

### Custom Endpoint

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/gamification` | Gamification engine (XP, levels, achievements, streaks) |

### Dispatch Actions Reference

```json
// InterviewerAgent
{"action": "start_interview", "domain": "Python", "difficulty": "medium", "total_questions": 5}
{"action": "next_question"}
{"action": "follow_up"}

// EvaluatorAgent
{"action": "evaluate", "question": "...", "answer": "...", "domain": "Python"}

// CoachAgent
{"action": "coach"}

// ReportAgent
{"action": "report"}

// GoalTrackerAgent
{"action": "set_goal", "domain": "Python", "daily_questions": 5, "weekly_target": 25, "target_score": 70}
{"action": "get_progress"}
{"action": "update_streak"}
{"action": "check_daily"}

// MotivatorAgent
{"action": "daily_message"}
{"action": "topic_of_day"}
{"action": "celebrate_milestone"}

// SkillMonitorAgent
{"action": "update_skill", "domain": "Python", "score": 75}
{"action": "get_skills"}
{"action": "get_weak_areas"}

// QuizMasterAgent
{"action": "start_quiz", "domain": "Python"}
{"action": "submit_answer", "answer": "tuple"}
{"action": "get_results"}

// SalaryCoachAgent
{"action": "start_negotiation"}
{"action": "respond", "response": "I believe the market rate is higher..."}
{"action": "get_tips", "count": 5}

// ResumeAnalyzerAgent
{"action": "analyze_resume", "resume_text": "..."}
{"action": "get_tailored_questions"}

// ForumPostingAgent
{"action": "daily_challenge", "domain": "Python"}
{"action": "topic_discussion"}
{"action": "weekly_summary"}
{"action": "social_post", "platform": "twitter", "domain": "Python"}

// GroupManagerAgent
{"action": "create_group", "group_name": "React Masters", "domain": "React"}
{"action": "add_member", "group_name": "React Masters", "member_name": "Alice"}
{"action": "get_group_stats", "group_name": "React Masters"}
{"action": "set_group_task", "group_name": "React Masters", "task": "Complete 3 mock interviews"}
{"action": "get_leaderboard", "group_name": "React Masters"}

// AdminAnalyticsAgent
{"action": "system_overview"}
{"action": "user_report", "period": "weekly"}
{"action": "agent_performance"}
{"action": "cost_report", "period": "monthly"}

// PanelInterviewerAgent
{"action": "start_panel"}
{"action": "panel_question"}
{"action": "panel_evaluate", "answer": "..."}

// MultiRoundAgent
{"action": "start_pipeline"}
{"action": "next_round", "round_score": 75}
{"action": "get_pipeline_status"}
{"action": "pipeline_report"}
```

---

## Frontend Pages (15)

| Page | Route | Description |
|---|---|---|
| Home | `/` | Landing page with domain selection |
| Interview | `/interview` | Main interview session UI |
| Dashboard | `/dashboard` | Skill radar charts, XP progress, recent activity |
| Quiz | `/quiz` | Quick MCQ quiz mode |
| Chat | `/chat` | Free-form chat with AI |
| Results | `/results/[id]` | Detailed session results |
| Goals | `/goals` | Goal setting and streak tracking |
| Leaderboard | `/leaderboard` | User rankings |
| Admin | `/admin` | Admin analytics dashboard |
| Pricing | `/pricing` | Subscription plans |
| Login | `/login` | Authentication |
| Profile | `/profile` | User profile and settings |
| Forums | `/forums` | Community forums and challenges |
| Groups | `/groups` | Study group management |
| Onboarding | `/onboarding` | New user onboarding flow |

---

## Supported Domains (10)

Python, JavaScript, React, iOS, Android, ReactNative, Java, DevOps, SystemDesign, HR

---

## Database Schema

AgentX manages persistence via `DatabaseConfig`. In development, the app uses `DatabaseConfig.memory()` (in-memory storage). Agent state is stored in `AgentContext` per session.

Key data stored in context:
- `domain`, `difficulty`, `total_questions`, `current_question` - Interview session state
- `topics_covered` - Topics already asked in session
- `evaluations` - List of evaluation results
- `last_evaluation` - Most recent evaluation
- `goals` - User goals
- `streak`, `best_streak` - Streak tracking
- `skills` - Per-domain skill scores and history
- `quiz_questions`, `quiz_score`, `quiz_answers` - Quiz state
- `groups` - Study group data
- `pipeline_round`, `pipeline_scores` - Multi-round pipeline state
- `panel_index`, `panel_scores` - Panel interview state
- `current_offer`, `negotiation_round` - Salary negotiation state
- `extracted_skills`, `suggested_domains`, `experience_level` - Resume analysis

---

## Deployment

### Docker Compose

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8081:8081"
    environment:
      - AGENTX_PORT=8081
      - AGENTX_MODEL=claude-sonnet-4-6
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}

  frontend:
    build: ./frontend
    ports:
      - "3001:3001"
    depends_on:
      - backend
```

### Ports

| Service | Port |
|---|---|
| Backend API | 8081 |
| Frontend | 3001 (production) / 3000 (dev) |

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENTX_PORT` | `8081` | Backend server port |
| `AGENTX_MODEL` | `claude-sonnet-4-6` | LLM model to use |
| `ANTHROPIC_API_KEY` | (empty) | API key; empty = mock mode |
| `AGENTX_LOG_LEVEL` | `INFO` | Logging level |

---

## Security

### Authentication
- JWT-based authentication (via AgentX)
- Login page at `/login`

### Authorization
- RBAC: Admin role for `/admin` analytics dashboard
- Regular users access interview, quiz, chat, and profile features

### Content Moderation
- AgentX `ContentModerationConfig.moderate()` enabled
- Filters inappropriate content in user inputs and AI responses

### Anti-Cheating
- Answer evaluation detects overly short answers (< 20 chars) and penalizes score by -20
- Keyword-based scoring prevents copy-paste of unrelated content
- Difficulty auto-adjusts based on performance (score >= 80 -> harder, score <= 40 -> easier)

### CORS
- Configured with `cors_origins=["*"]` (development)
- Should be restricted in production

---

## Configuration

### Backend (`backend/config.py`)

```python
AgentXConfig(
    env=Environment.DEVELOPMENT,
    app_name="AgentInterviewer",
    version="1.0.0",
    debug=True,
    database=DatabaseConfig.memory(),
    llm=LLMConfig.single(provider="anthropic", model="claude-sonnet-4-6"),
    moderation=ContentModerationConfig.moderate(),
)

DaemonConfig(
    server_enabled=True,
    server_host="0.0.0.0",
    server_port=8081,
    cors_origins=["*"],
    scheduler_enabled=True,
    watcher_enabled=False,
    mq_enabled=False,
    watchdog_enabled=True,
)
```

### Scheduled Jobs

| Job | Interval | Description |
|---|---|---|
| `daily_motivation` | 24 hours | Daily motivation check |
| `health_summary` | 1 hour | System health summary |

---

## Mock Mode

When `ANTHROPIC_API_KEY` is not set, all agents operate in mock mode:

- **InterviewerAgent:** Picks from pre-built question banks (6 per domain, 10 domains)
- **EvaluatorAgent:** Scores via keyword matching + answer length heuristic
- **CoachAgent:** Returns static tips and resources per domain
- **ReportAgent:** Aggregates evaluation data from context
- **GoalTrackerAgent:** Tracks goals and streaks in context
- **MotivatorAgent:** Rotates daily messages by day-of-year index
- **SkillMonitorAgent:** Maintains weighted averages in context
- **QuizMasterAgent:** Runs MCQ quizzes from static question banks
- **ChatBotAgent:** Keyword-matched canned responses for 10 topics
- **SalaryCoachAgent:** Mock INR offers, keyword-based strategy classification
- **ResumeAnalyzerAgent:** Keyword extraction across 9 domain lists
- **ForumPostingAgent:** Random selection from template banks
- **GroupManagerAgent:** Full CRUD in context memory
- **AdminAnalyticsAgent:** Returns hardcoded mock metrics
- **PanelInterviewerAgent:** Rotates 3 personas with 5 questions each
- **MultiRoundAgent:** Manages 5-round pipeline with mock scoring

All features are fully functional in mock mode, making the platform usable without any API key.
