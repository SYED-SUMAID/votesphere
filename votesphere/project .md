# VoteSphere

A simple voting application built with FastAPI, SQLite, and JavaScript.

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend API |
| SQLite | Database |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation |
| Jinja2 | HTML templates |
| HTML, CSS, JavaScript | Frontend |
| Uvicorn | Development server |

## Project Structure

    votesphere/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── templates/
    │   │   └── index.html
    │   └── static/
    │       ├── style.css
    │       └── app.js
    ├── requirements.txt
    └── voting.db

## Setup

Create and activate a virtual environment.

    python3 -m venv venv
    source venv/bin/activate

Install dependencies.

    pip install -r requirements.txt

Start the application.

    uvicorn app.main:app --reload

Open the application at `http://127.0.0.1:8000`.

![alt text](<Screenshot From 2026-10-14 18-56-55.png>)

API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Display the voting page |
| GET | `/api/polls` | Retrieve polls |
| POST | `/api/polls/{poll_id}/vote/{option_id}` | Submit a vote |
| GET | `/api/polls/{poll_id}/results` | Retrieve results |

## How It Works

1. FastAPI handles incoming requests.
2. SQLAlchemy interacts with the SQLite database.
3. Jinja2 renders the HTML template.
4. JavaScript fetches poll data and submits votes.
5. The API returns responses and voting results.

## Key Concepts

- REST API development
- HTTP methods and status codes
- Database models and relationships
- Request validation with Pydantic
- HTML templates and static files
- Frontend and backend communication
