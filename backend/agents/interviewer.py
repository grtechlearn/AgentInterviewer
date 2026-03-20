"""
InterviewerAgent - Generates interview questions by domain and difficulty.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

MOCK_QUESTIONS: dict[str, list[dict[str, Any]]] = {
    "Python": [
        {"question": "Explain the difference between a list and a tuple in Python.", "topic": "Data Structures", "hint": "Think about mutability."},
        {"question": "What are Python decorators and how do they work?", "topic": "Functions", "hint": "Functions that wrap other functions."},
        {"question": "Explain the GIL and its impact on multithreading.", "topic": "Concurrency", "hint": "Global Interpreter Lock."},
        {"question": "How does Python memory management work?", "topic": "Memory", "hint": "Reference counting and garbage collection."},
        {"question": "What are generators and when would you use them?", "topic": "Iterators", "hint": "Lazy evaluation with yield."},
        {"question": "Explain metaclasses in Python.", "topic": "OOP", "hint": "Classes that create classes."},
    ],
    "JavaScript": [
        {"question": "Explain the event loop in JavaScript.", "topic": "Async", "hint": "Call stack, task queue, microtask queue."},
        {"question": "What is the difference between var, let, and const?", "topic": "Variables", "hint": "Scoping and hoisting."},
        {"question": "How does prototypal inheritance work?", "topic": "OOP", "hint": "Prototype chain."},
        {"question": "Explain closures with a practical example.", "topic": "Functions", "hint": "Function remembers its lexical scope."},
        {"question": "What are Promises and how do they differ from callbacks?", "topic": "Async", "hint": "Chaining and error handling."},
        {"question": "Explain the difference between == and ===.", "topic": "Types", "hint": "Type coercion."},
    ],
    "React": [
        {"question": "Explain the virtual DOM and reconciliation.", "topic": "Core", "hint": "Diffing algorithm."},
        {"question": "What are React hooks and why were they introduced?", "topic": "Hooks", "hint": "State in functional components."},
        {"question": "How does useEffect cleanup work?", "topic": "Hooks", "hint": "Return function from useEffect."},
        {"question": "Explain React context vs Redux for state management.", "topic": "State", "hint": "Scale and complexity."},
        {"question": "What is React.memo and when should you use it?", "topic": "Performance", "hint": "Preventing unnecessary re-renders."},
        {"question": "Explain server-side rendering in React.", "topic": "SSR", "hint": "Initial HTML from server."},
    ],
    "iOS": [
        {"question": "Explain ARC (Automatic Reference Counting) in Swift.", "topic": "Memory", "hint": "Strong, weak, unowned references."},
        {"question": "What is the difference between structs and classes in Swift?", "topic": "Types", "hint": "Value vs reference types."},
        {"question": "Explain the SwiftUI view lifecycle.", "topic": "SwiftUI", "hint": "Body recomputation."},
        {"question": "How does Grand Central Dispatch work?", "topic": "Concurrency", "hint": "Dispatch queues."},
        {"question": "What are property wrappers in Swift?", "topic": "Swift", "hint": "@State, @Binding, custom wrappers."},
        {"question": "Explain Core Data vs SwiftData.", "topic": "Persistence", "hint": "Object graph management."},
    ],
    "Android": [
        {"question": "Explain the Android Activity lifecycle.", "topic": "Components", "hint": "onCreate through onDestroy."},
        {"question": "What is Jetpack Compose and how does it differ from XML layouts?", "topic": "UI", "hint": "Declarative vs imperative."},
        {"question": "Explain coroutines in Kotlin for Android.", "topic": "Concurrency", "hint": "Structured concurrency."},
        {"question": "How does the Android ViewModel survive configuration changes?", "topic": "Architecture", "hint": "ViewModelStore."},
        {"question": "What is Hilt and how does dependency injection work on Android?", "topic": "DI", "hint": "Annotation-based DI."},
        {"question": "Explain Room database and its components.", "topic": "Persistence", "hint": "DAO, Entity, Database."},
    ],
    "ReactNative": [
        {"question": "How does the React Native bridge work?", "topic": "Architecture", "hint": "JS thread to native thread."},
        {"question": "Explain the new architecture (Fabric and TurboModules).", "topic": "Architecture", "hint": "JSI-based communication."},
        {"question": "How do you optimize FlatList performance?", "topic": "Performance", "hint": "getItemLayout, windowSize."},
        {"question": "What are native modules and when would you create one?", "topic": "Native", "hint": "Platform-specific functionality."},
        {"question": "Explain navigation patterns in React Native.", "topic": "Navigation", "hint": "Stack, tab, drawer navigators."},
        {"question": "How do you handle platform-specific code?", "topic": "Cross-platform", "hint": "Platform.OS and .ios/.android files."},
    ],
    "Java": [
        {"question": "Explain the JVM memory model and garbage collection.", "topic": "JVM", "hint": "Heap, stack, GC algorithms."},
        {"question": "What are the SOLID principles? Give examples.", "topic": "OOP", "hint": "Five design principles."},
        {"question": "Explain the Java Stream API with examples.", "topic": "Streams", "hint": "Functional-style operations."},
        {"question": "How does the Java Concurrency framework work?", "topic": "Concurrency", "hint": "ExecutorService, CompletableFuture."},
        {"question": "What are design patterns you commonly use in Java?", "topic": "Patterns", "hint": "Singleton, Factory, Observer."},
        {"question": "Explain Spring Boot dependency injection.", "topic": "Spring", "hint": "IoC container."},
    ],
    "DevOps": [
        {"question": "Explain the CI/CD pipeline and its stages.", "topic": "CI/CD", "hint": "Build, test, deploy."},
        {"question": "How does Docker containerization work?", "topic": "Containers", "hint": "Images, containers, layers."},
        {"question": "Explain Kubernetes architecture.", "topic": "Orchestration", "hint": "Pods, services, deployments."},
        {"question": "What is Infrastructure as Code? Compare Terraform and Pulumi.", "topic": "IaC", "hint": "Declarative infrastructure."},
        {"question": "How do you implement monitoring and alerting?", "topic": "Monitoring", "hint": "Prometheus, Grafana, PagerDuty."},
        {"question": "Explain blue-green vs canary deployments.", "topic": "Deployment", "hint": "Zero-downtime strategies."},
    ],
    "SystemDesign": [
        {"question": "Design a URL shortener like bit.ly.", "topic": "Design", "hint": "Hashing, redirection, analytics."},
        {"question": "How would you design a chat application like WhatsApp?", "topic": "Design", "hint": "WebSockets, message queues."},
        {"question": "Design a rate limiter for an API.", "topic": "Design", "hint": "Token bucket, sliding window."},
        {"question": "How would you design a notification system?", "topic": "Design", "hint": "Push, pull, fan-out."},
        {"question": "Design a distributed cache system.", "topic": "Design", "hint": "Consistent hashing, eviction."},
        {"question": "How would you scale a database to handle millions of users?", "topic": "Scaling", "hint": "Sharding, replication, read replicas."},
    ],
    "HR": [
        {"question": "Tell me about a time you resolved a conflict in your team.", "topic": "Behavioral", "hint": "Use the STAR method."},
        {"question": "Why are you interested in this role?", "topic": "Motivation", "hint": "Align with company mission."},
        {"question": "Describe a project you are most proud of.", "topic": "Experience", "hint": "Impact and learnings."},
        {"question": "How do you handle tight deadlines and pressure?", "topic": "Behavioral", "hint": "Prioritization strategies."},
        {"question": "Where do you see yourself in 5 years?", "topic": "Growth", "hint": "Career trajectory."},
        {"question": "What is your biggest weakness and how are you improving it?", "topic": "Self-awareness", "hint": "Genuine with improvement plan."},
    ],
}

DIFFICULTY_MAP = {"easy": 0, "medium": 1, "hard": 2}


class InterviewerAgent(BaseAgent):
    """Generates interview questions for various tech domains."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="interviewer",
            role="Interview Question Generator",
            system_prompt=(
                "You are a senior technical interviewer. Generate clear, "
                "challenging interview questions appropriate for the given "
                "domain and difficulty level."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "start_interview")
        domain = message.data.get("domain", "Python")
        difficulty = message.data.get("difficulty", "medium")
        total = message.data.get("total_questions", 5)

        if action == "start_interview":
            context.set("domain", domain)
            context.set("difficulty", difficulty)
            context.set("total_questions", total)
            context.set("current_question", 1)
            context.set("topics_covered", [])
            return self._pick_question(message, context, domain, difficulty, 1, total)

        if action == "next_question":
            qnum = context.get("current_question", 1) + 1
            context.set("current_question", qnum)
            domain = context.get("domain", domain)
            difficulty = context.get("difficulty", difficulty)
            total = context.get("total_questions", total)
            return self._pick_question(message, context, domain, difficulty, qnum, total)

        if action == "follow_up":
            return self._follow_up(message, context)

        return message.error(f"Unknown action: {action}")

    # ------------------------------------------------------------------

    def _pick_question(
        self,
        message: AgentMessage,
        context: AgentContext,
        domain: str,
        difficulty: str,
        qnum: int,
        total: int,
    ) -> AgentMessage:
        questions = MOCK_QUESTIONS.get(domain, MOCK_QUESTIONS["Python"])
        covered = context.get("topics_covered", [])
        remaining = [q for q in questions if q["topic"] not in covered]
        if not remaining:
            remaining = questions
        q = random.choice(remaining)
        covered.append(q["topic"])
        context.set("topics_covered", covered)

        result = {
            "question": q["question"],
            "topic": q["topic"],
            "difficulty": difficulty,
            "question_number": qnum,
            "total_questions": total,
            "hint": q["hint"],
            "domain": domain,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _follow_up(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        domain = context.get("domain", "Python")
        topic = context.get("topics_covered", ["General"])[-1]
        result = {
            "question": f"Can you elaborate more on {topic} in {domain}?",
            "topic": topic,
            "difficulty": context.get("difficulty", "medium"),
            "question_number": context.get("current_question", 1),
            "total_questions": context.get("total_questions", 5),
            "hint": "Go deeper into the concept.",
            "domain": domain,
            "is_follow_up": True,
        }
        return message.reply(content=json.dumps(result), data=result)
