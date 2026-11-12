"""Маленький сервис-заглушка «агента» для учебного CI/CD.

/health — проверка живости (её будет дёргать smoke-тест после деплоя).
/ask    — имитация ответа агента: пока просто эхо, без модели.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="demo-agent", version="0.1.0")


class Question(BaseModel):
    text: str


class Answer(BaseModel):
    answer: str
    length: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(question: Question) -> Answer:
    text = question.text.strip()
    return Answer(answer=f"Вы спросили: {text}", length=len(text))
