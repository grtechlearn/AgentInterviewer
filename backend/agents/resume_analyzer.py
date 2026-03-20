"""
ResumeAnalyzerAgent - Parse resume text and generate tailored interview questions.
"""

from __future__ import annotations

import json
import re
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

SKILL_KEYWORDS: dict[str, list[str]] = {
    "Python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
    "JavaScript": ["javascript", "typescript", "node", "express", "vue"],
    "React": ["react", "redux", "next.js", "nextjs", "jsx"],
    "iOS": ["swift", "swiftui", "uikit", "xcode", "cocoapods"],
    "Android": ["android", "kotlin", "jetpack", "gradle"],
    "Java": ["java", "spring", "hibernate", "maven", "junit"],
    "DevOps": ["docker", "kubernetes", "k8s", "ci/cd", "terraform", "aws", "azure", "gcp"],
    "SystemDesign": ["microservices", "distributed", "scalability", "load balancing", "caching"],
    "ReactNative": ["react native", "expo", "react-native"],
}

EXPERIENCE_KEYWORDS: dict[str, list[str]] = {
    "junior": ["intern", "fresher", "entry level", "graduate", "0-1 year", "0-2 year"],
    "mid": ["2-4 year", "3-5 year", "associate", "mid-level", "mid level"],
    "senior": ["senior", "lead", "principal", "architect", "5+ year", "7+ year", "10+ year", "manager", "staff"],
}

TAILORED_QUESTIONS: dict[str, list[str]] = {
    "Python": [
        "I see you have Python experience. How do you handle memory optimization in large-scale Python apps?",
        "Can you walk me through a complex Python project you built?",
        "How do you approach testing in Python codebases?",
    ],
    "React": [
        "You have listed React. Explain how you would optimize a React app with slow renders.",
        "Describe a challenging state management problem you solved in React.",
        "How do you handle error boundaries in production React apps?",
    ],
    "DevOps": [
        "Your resume mentions DevOps. Walk me through your CI/CD pipeline setup.",
        "How do you handle zero-downtime deployments?",
        "Describe a production incident you resolved and what you learned.",
    ],
    "default": [
        "Tell me about your most impactful project.",
        "How do you stay current with technology trends?",
        "Describe a technical challenge and how you overcame it.",
    ],
}


class ResumeAnalyzerAgent(BaseAgent):
    """Parse resume text and generate tailored interview questions."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="resume_analyzer",
            role="Resume Analyzer",
            system_prompt=(
                "You analyze resumes to extract skills and experience, "
                "then generate tailored interview questions."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "analyze_resume")

        if action == "analyze_resume":
            return self._analyze(message, context)
        if action == "get_tailored_questions":
            return self._get_questions(message, context)

        return message.error(f"Unknown action: {action}")

    def _analyze(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        resume_text = message.data.get("resume_text", "").lower()

        # Extract skills
        extracted: list[str] = []
        domains: list[str] = []
        for domain, keywords in SKILL_KEYWORDS.items():
            for kw in keywords:
                if kw in resume_text and domain not in domains:
                    domains.append(domain)
                    extracted.append(kw)

        # Determine experience level
        experience_level = "mid"
        for level, keywords in EXPERIENCE_KEYWORDS.items():
            if any(kw in resume_text for kw in keywords):
                experience_level = level
                break

        # Extract years if mentioned
        years_match = re.search(r"(\d+)\+?\s*years?", resume_text)
        years = int(years_match.group(1)) if years_match else 0
        if years >= 5:
            experience_level = "senior"
        elif years <= 1:
            experience_level = "junior"

        context.set("extracted_skills", extracted)
        context.set("suggested_domains", domains)
        context.set("experience_level", experience_level)

        result = {
            "extracted_skills": extracted,
            "suggested_domains": domains or ["Python"],
            "experience_level": experience_level,
            "years_detected": years,
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _get_questions(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        domains = context.get("suggested_domains", message.data.get("domains", []))
        questions: list[str] = []
        for domain in domains:
            questions.extend(TAILORED_QUESTIONS.get(domain, []))
        if not questions:
            questions = TAILORED_QUESTIONS["default"]

        result = {
            "tailored_questions": questions,
            "based_on_domains": domains,
            "experience_level": context.get("experience_level", "mid"),
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)
