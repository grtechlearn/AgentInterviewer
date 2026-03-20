# Contributing to AgentInterviewer

Thanks for your interest in contributing! This document covers setup, testing, and the PR process.

## Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- [AgentX](https://github.com/grtechlearn/agentx) cloned alongside this repo (or installed via pip)

## Setup

### Clone the Repository

```bash
git clone https://github.com/AntisGravity/AgentInterviewer.git
cd AgentInterviewer
```

### Backend

```bash
cd backend
pip install -e ../../agentx        # Install AgentX from local clone
pip install pytest pytest-asyncio   # Test dependencies
python app.py                       # Starts on :8081 (mock mode)
```

### Frontend

```bash
cd frontend
npm install
npm run dev    # Starts on :3000
```

### Docker

```bash
docker compose up -d
# Frontend: http://localhost:3001
# Backend:  http://localhost:8081/api/v1/health
```

## Running Tests

### Backend Tests

```bash
cd backend
PYTHONPATH=. pytest tests/ -v
```

Or from the project root with AgentX in the path:

```bash
PYTHONPATH=../../agentx pytest backend/tests/ -v
```

### Frontend Build Check

```bash
cd frontend
npm run build
```

## Code Style

- **Python:** Follow PEP 8. Use type hints on all function signatures. Use `from __future__ import annotations` in every module.
- **TypeScript/React:** Follow the existing patterns. Use functional components with hooks.
- **Formatting:** Keep lines under 100 characters where practical.
- **Naming:** Agents use `PascalCaseAgent` class names and `snake_case` registration names.

## Adding a New Agent

1. Create `backend/agents/your_agent.py` extending `BaseAgent`
2. Implement `async process(message, context)` with mock mode support
3. Add import and registration in `backend/agents/__init__.py`
4. Add routing function and registration in `backend/app.py`
5. Write tests in `backend/tests/test_your_agent.py`
6. Update `docs/TECHNICAL_SPECIFICATION.md`

## Pull Request Process

1. Fork the repository and create a feature branch from `main`
2. Make your changes with tests
3. Ensure all tests pass: `PYTHONPATH=. pytest tests/ -v`
4. Ensure frontend builds: `cd frontend && npm run build`
5. Write a clear PR description explaining what and why
6. Request review

## Reporting Issues

Open an issue on GitHub with:
- Steps to reproduce
- Expected vs actual behavior
- Python/Node version
- Whether you are running in mock mode or with an API key

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
