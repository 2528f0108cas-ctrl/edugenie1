from ai_client import generate

async def summarize_text(text: str, level: str = "Beginner") -> str:
    return await generate(f"""Summarize the following educational text for a {level} learner.
Keep the central facts and terminology, remove repetition, and use concise bullets when helpful.
Text: {text}""")
