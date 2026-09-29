import json
from ai_client import generate

async def generate_quiz(text: str, level: str = "Beginner") -> list[dict]:
    prompt = f"""Create exactly 3 multiple-choice questions for a {level} learner from the supplied topic or passage.
Return ONLY a JSON array. Each item must have keys: question, options (exactly four strings), answer (one option string), explanation.
Make sure the answer exactly matches one option. Passage/topic: {text}"""
    raw = await generate(prompt, json_mode=True)
    try:
        data = json.loads(raw)
        if not isinstance(data, list) or len(data) != 3:
            raise ValueError("Expected exactly 3 questions")
        for q in data:
            if not isinstance(q.get("options"), list) or len(q["options"]) != 4 or q.get("answer") not in q["options"]:
                raise ValueError("Invalid question structure")
        return data
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise RuntimeError(f"Quiz response was not valid structured data: {exc}") from exc
