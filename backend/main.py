import os
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from prompt import SYSTEM_PROMPT

app = FastAPI()

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


class AskRequest(BaseModel):
    message: str


# 🌐 ANA SAYFA (HTML)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ❤️ HEALTH CHECK (artık /health)
@app.get("/health")
def health():
    return {"status": "ok"}


# 🤖 AI ENDPOINT
@app.post("/ask")
def ask_ai(data: AskRequest):
    if not GROQ_API_KEY:
        return {"answer": "Sunucu yapılandırma hatası: API key yok."}

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.message}
        ],
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        result = res.json()
        return {"answer": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"answer": f"Hata oluştu: {str(e)}"}
