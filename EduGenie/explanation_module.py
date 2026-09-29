import os
from ai_client import generate

async def explain_concept(text: str, level: str = "Beginner") -> str:
    # Gemini is the reliable default. Optional local model can be enabled explicitly.
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true":
        try:
            from transformers import pipeline
            model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
            generator = _local_pipeline(model_name)
            output = generator(f"Explain simply for a {level} learner: {text}", max_new_tokens=220, do_sample=False)
            return output[0]["generated_text"].strip()
        except Exception as exc:
            raise RuntimeError(f"Local explanation model could not load: {exc}") from exc
    return await generate(f"""Explain this concept to a {level} learner.
Start with a plain-language definition, then use a small example and finish with one key takeaway.
Concept: {text}""")

_local_cache = {}
def _local_pipeline(model_name):
    if model_name not in _local_cache:
        from transformers import pipeline
        _local_cache[model_name] = pipeline("text2text-generation", model=model_name, device=-1)
    return _local_cache[model_name]
