from ai_client import generate

async def answer_question(text: str, level: str = "Beginner") -> str:
    return await generate(f"""You are EduGenie, a careful educational tutor. Answer the student's question at {level} level.
Use clear language, explain key reasoning, and say when something is uncertain. Keep it concise.
Student question: {text}""")
