from fastapi import FastAPI
from session_manager import session_manager
from pydantic import BaseModel

app = FastAPI()

class AskRequest(BaseModel):
    user_id: str
    question: str


@app.post("/ask")
def ask(req: AskRequest):

    session, context = session_manager.route_session(
        req.user_id,
        req.question
    )

    answer = session.ask(req.question)

    return {
        "context": context,
        "answer": answer
    }
