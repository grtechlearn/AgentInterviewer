"""
QuizMasterAgent - Quick quiz mode with MCQ questions.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

QUIZ_BANK: dict[str, list[dict[str, Any]]] = {
    "Python": [
        {"q": "What is the output of `len([1, [2, 3], 4])`?", "options": ["3", "4", "5", "Error"], "answer": "3"},
        {"q": "Which keyword creates a generator?", "options": ["return", "yield", "async", "lambda"], "answer": "yield"},
        {"q": "What does `__init__` do?", "options": ["Destructor", "Constructor", "Iterator", "Decorator"], "answer": "Constructor"},
        {"q": "Which is immutable?", "options": ["list", "dict", "set", "tuple"], "answer": "tuple"},
        {"q": "What does PEP 8 define?", "options": ["Syntax", "Style guide", "Data types", "Imports"], "answer": "Style guide"},
        {"q": "What is `self` in Python?", "options": ["Keyword", "Instance reference", "Global var", "Module"], "answer": "Instance reference"},
        {"q": "How do you copy a list?", "options": ["list.copy()", "list = list", "copy(list)", "All of above"], "answer": "list.copy()"},
        {"q": "What does `*args` do?", "options": ["Keyword args", "Variable positional args", "Unpacking", "Multiplication"], "answer": "Variable positional args"},
        {"q": "Which is NOT a Python data type?", "options": ["int", "float", "char", "str"], "answer": "char"},
        {"q": "What does `pip` stand for?", "options": ["Python Install Packages", "Pip Installs Packages", "Package Installer for Python", "Python Index Package"], "answer": "Pip Installs Packages"},
    ],
    "JavaScript": [
        {"q": "What is `typeof null`?", "options": ["null", "undefined", "object", "boolean"], "answer": "object"},
        {"q": "Which is NOT a JS data type?", "options": ["Symbol", "BigInt", "char", "undefined"], "answer": "char"},
        {"q": "What does `===` check?", "options": ["Value only", "Type only", "Value and type", "Reference"], "answer": "Value and type"},
        {"q": "What is hoisting?", "options": ["Moving declarations up", "Error handling", "Async pattern", "Module loading"], "answer": "Moving declarations up"},
        {"q": "Which creates a Promise?", "options": ["new Promise()", "Promise.make()", "async()", "promise()"], "answer": "new Promise()"},
        {"q": "What is NaN?", "options": ["Not a Null", "Not a Number", "Negative Number", "New Number"], "answer": "Not a Number"},
        {"q": "Which loop guarantees order?", "options": ["for...in", "for...of", "forEach", "while"], "answer": "for...of"},
        {"q": "What does `bind()` do?", "options": ["Copies object", "Sets this", "Creates closure", "Binds event"], "answer": "Sets this"},
        {"q": "Arrow functions have own `this`?", "options": ["Yes", "No", "Sometimes", "Only in strict"], "answer": "No"},
        {"q": "What is the DOM?", "options": ["Data Object Model", "Document Object Model", "Digital Output Mode", "Display Object Map"], "answer": "Document Object Model"},
    ],
}


class QuizMasterAgent(BaseAgent):
    """Runs quick MCQ quiz sessions."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="quiz_master",
            role="Quiz Master",
            system_prompt="You run engaging multiple-choice quizzes for interview prep.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "start_quiz")

        if action == "start_quiz":
            return self._start_quiz(message, context)
        if action == "submit_answer":
            return self._submit_answer(message, context)
        if action == "get_results":
            return self._get_results(message, context)

        return message.error(f"Unknown quiz_master action: {action}")

    def _start_quiz(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        domain = message.data.get("domain", "Python")
        bank = QUIZ_BANK.get(domain, QUIZ_BANK["Python"])
        questions = random.sample(bank, min(10, len(bank)))

        context.set("quiz_questions", questions)
        context.set("quiz_domain", domain)
        context.set("quiz_current", 0)
        context.set("quiz_score", 0)
        context.set("quiz_answers", [])

        q = questions[0]
        result = {
            "question_number": 1,
            "total": len(questions),
            "question": q["q"],
            "options": q["options"],
            "domain": domain,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _submit_answer(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        questions = context.get("quiz_questions", [])
        current = context.get("quiz_current", 0)
        user_answer = message.data.get("answer", "")

        if current >= len(questions):
            return self._get_results(message, context)

        q = questions[current]
        correct = user_answer.strip().lower() == q["answer"].strip().lower()
        score = context.get("quiz_score", 0)
        if correct:
            score += 1
        context.set("quiz_score", score)

        answers = context.get("quiz_answers", [])
        answers.append({"question": q["q"], "user_answer": user_answer, "correct_answer": q["answer"], "is_correct": correct})
        context.set("quiz_answers", answers)

        next_idx = current + 1
        context.set("quiz_current", next_idx)

        result: dict[str, Any] = {
            "is_correct": correct,
            "correct_answer": q["answer"],
            "current_score": score,
        }

        if next_idx < len(questions):
            nq = questions[next_idx]
            result["next_question"] = {
                "question_number": next_idx + 1,
                "total": len(questions),
                "question": nq["q"],
                "options": nq["options"],
            }
        else:
            result["quiz_complete"] = True
            result["final_score"] = score
            result["total"] = len(questions)
            result["percentage"] = round(score / len(questions) * 100)

        return message.reply(content=json.dumps(result), data=result)

    def _get_results(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        score = context.get("quiz_score", 0)
        questions = context.get("quiz_questions", [])
        answers = context.get("quiz_answers", [])
        total = len(questions)

        result = {
            "final_score": score,
            "total": total,
            "percentage": round(score / max(1, total) * 100),
            "answers": answers,
            "domain": context.get("quiz_domain", "Python"),
        }
        return message.reply(content=json.dumps(result), data=result)
