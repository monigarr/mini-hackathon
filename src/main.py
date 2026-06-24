# ============================================================================
# Module: main.py
# Purpose: FastAPI entry point for the Agentic Tax-Filing Assistant
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.conversation.engine import ConversationEngine
from src.models.session import SessionManager
from src.tools.logger import get_observations

APP_VERSION = "1.0.0"

app = FastAPI(
    title="Agentic Tax-Filing Assistant",
    version=APP_VERSION,
    description="Hackathon prototype for simple W-2 Form 1040 generation.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "ui" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

sessions = SessionManager()
engine = ConversationEngine()


class SessionResponse(BaseModel):
    """API response for a newly created session."""

    session_id: str
    message: str
    question_count: int
    state: str


class ChatRequest(BaseModel):
    """Chat request body."""

    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """Chat response body."""

    session_id: str
    message: str
    question_count: int
    state: str
    download_url: str | None = None


@app.get("/")
async def index() -> FileResponse:
    """Serve the browser chat UI."""
    return FileResponse(static_dir / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    """Return application health for local and Render smoke tests."""
    return {"status": "healthy", "version": APP_VERSION}


@app.post("/api/sessions", response_model=SessionResponse)
async def create_session() -> SessionResponse:
    """Create a conversation session and return the first agent question."""
    session = sessions.create_session()
    message = engine.start_session(session)
    return SessionResponse(
        session_id=session.session_id,
        message=message,
        question_count=session.question_count,
        state=session.state.value,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process one chat message."""
    try:
        session = sessions.require_session(request.session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown session_id") from exc

    message = engine.process_message(session, request.message)
    download_url = (
        f"/api/download/{session.session_id}" if session.download_ready else None
    )
    return ChatResponse(
        session_id=session.session_id,
        message=message,
        question_count=session.question_count,
        state=session.state.value,
        download_url=download_url,
    )


@app.get("/api/download/{session_id}")
async def download(session_id: str) -> Response:
    """Download the generated Form 1040 PDF for a completed session."""
    try:
        session = sessions.require_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown session_id") from exc
    if not session.pdf_bytes:
        raise HTTPException(status_code=404, detail="No generated PDF for this session")
    headers = {
        "Content-Disposition": f'attachment; filename="Form_1040_{session_id}.pdf"'
    }
    return Response(
        content=session.pdf_bytes,
        media_type="application/pdf",
        headers=headers,
    )


@app.get("/api/observations/{session_id}")
async def observations(session_id: str) -> dict[str, object]:
    """Return judge-visible structured observations for a session."""
    if sessions.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Unknown session_id")
    return {"session_id": session_id, "observations": get_observations(session_id)}

