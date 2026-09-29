from ai_client import generate

async def get_learning_recommendations(text: str, level: str = "Beginner") -> str:
    return await generate(f"""Build a practical learning path for: {text}
Learner's current level: {level}.
Organize from foundations to advanced topics. Include milestones, an estimated timeline, practice projects,
and useful resource types (official docs, books, videos). Do not invent specific URLs. Explain prerequisites.""")
