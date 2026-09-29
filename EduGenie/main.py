import os
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class TaskRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    level: str = Field(default="Beginner", max_length=40)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))}

@app.post("/qa")
async def qa(payload: TaskRequest):
    return {"result": await run_task(answer_question, payload)}

@app.post("/explain")
async def explain(payload: TaskRequest):
    return {"result": await run_task(explain_concept, payload)}

@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return {"result": await run_task(generate_quiz, payload)}

@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return {"result": await run_task(summarize_text, payload)}

@app.post("/learn/recommendations")
async def recommendations(payload: TaskRequest):
    return {"result": await run_task(get_learning_recommendations, payload)}

async def run_task(func, payload):
    try:
        return await func(payload.text, payload.level)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}")
