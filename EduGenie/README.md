# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS learning assistant based on the supplied project document. It supports:
- Q&A (`POST /qa`)
- Concept explanation (`POST /explain`)
- Three-question MCQ quiz (`POST /quiz`)
- Summarization (`POST /summarize`)
- Beginner-to-advanced learning paths (`POST /learn/recommendations`)

The document names Gemini 1.5 Pro. Since model availability changes, this implementation uses the configurable `GEMINI_MODEL` setting and defaults to `gemini-2.5-flash`. Set another model available to your Google AI Studio key if needed. Gemini API access is required for the cloud tasks. The optional local LaMini explainer is disabled by default because it downloads model weights and requires additional packages.

## Requirements
- Python 3.10+
- Google AI Studio Gemini API key
- VS Code (recommended)

## Setup in VS Code (Windows PowerShell)
1. Extract the project ZIP and open the `EduGenie` folder in VS Code.
2. Open Terminal → New Terminal.
3. Create and activate a virtual environment:
   ```powershell
   py -3.10 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If `py` is unavailable, use `python -m venv .venv`.
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env`, then replace `your_api_key_here` with your Gemini API key.
6. Start the server:
   ```powershell
   uvicorn main:app --reload
   ```
7. Open http://127.0.0.1:8000 in your browser.

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Gemini API key
uvicorn main:app --reload
```

## Test
- Open the UI and try each task.
- API health: `GET http://127.0.0.1:8000/health`
- Interactive API docs: http://127.0.0.1:8000/docs
- Example Q&A:
  ```bash
  curl -X POST http://127.0.0.1:8000/qa \
    -H "Content-Type: application/json" \
    -d '{"text":"Which is the largest ocean?","level":"Beginner"}'
  ```
- Example quiz:
  ```bash
  curl -X POST http://127.0.0.1:8000/quiz \
    -H "Content-Type: application/json" \
    -d '{"text":"The Pythagorean theorem relates the sides of a right triangle.","level":"Beginner"}'
  ```

## Optional local LaMini explanation
Install optional packages:
```bash
pip install transformers torch sentencepiece
```
Set `USE_LOCAL_EXPLAINER=true` in `.env`. First run downloads the model weights; CPU inference can be slow and needs disk space. Other features continue using Gemini.

## Project layout
```text
EduGenie/
├── main.py
├── ai_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Notes
- Never commit `.env` or expose your API key in frontend code.
- AI outputs can be inaccurate; verify important educational information.
- API endpoints return JSON: `{"result": ...}`. Quiz results contain three objects with `question`, `options`, `answer`, and `explanation`.
