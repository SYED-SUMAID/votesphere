from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Poll, Option


BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    try:
        if db.query(Poll).count() == 0:
            poll = Poll(
                question="Which technology should we learn next?"
            )

            poll.options = [
                Option(text="FastAPI"),
                Option(text="Docker"),
                Option(text="Ansible"),
                Option(text="Jenkins")
            ]

            db.add(poll)
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(
    title="VoteSphere API",
    description="A simple online voting application",
    version="1.0.0",
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/api/polls")
def get_polls(db: Session = Depends(get_db)):
    polls = db.query(Poll).all()

    return [
        {
            "id": poll.id,
            "question": poll.question,
            "options": [
                {
                    "id": option.id,
                    "text": option.text,
                    "votes": option.votes
                }
                for option in poll.options
            ]
        }
        for poll in polls
    ]


@app.post("/api/polls/{poll_id}/vote/{option_id}")
def cast_vote(
    poll_id: int,
    option_id: int,
    db: Session = Depends(get_db)
):
    poll = db.query(Poll).filter(Poll.id == poll_id).first()

    if not poll:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    option = (
        db.query(Option)
        .filter(
            Option.id == option_id,
            Option.poll_id == poll_id
        )
        .first()
    )

    if not option:
        raise HTTPException(
            status_code=404,
            detail="Invalid voting option"
        )

    option.votes += 1
    db.commit()
    db.refresh(option)

    return {
        "message": "Vote submitted successfully",
        "option": option.text,
        "votes": option.votes
    }


@app.get("/api/polls/{poll_id}/results")
def get_results(
    poll_id: int,
    db: Session = Depends(get_db)
):
    poll = db.query(Poll).filter(Poll.id == poll_id).first()

    if not poll:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    total_votes = sum(option.votes for option in poll.options)

    return {
        "poll": poll.question,
        "total_votes": total_votes,
        "results": [
            {
                "option": option.text,
                "votes": option.votes,
                "percentage": round(
                    option.votes / total_votes * 100, 2
                ) if total_votes else 0
            }
            for option in poll.options
        ]
    }