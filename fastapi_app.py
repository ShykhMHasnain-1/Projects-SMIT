"""
FastAPI Microservice for AI Smart Civic Services.
Provides async RESTful API endpoints for AI prediction, complaint management, & analytics.

Run with Uvicorn:
    uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
"""
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import Config
from backend.database import DatabaseManager
from backend.ai_analyser import AIAnalyzer
from backend.notifications import NotificationManager
from backend.complaint_manager import ComplaintManager, ComplaintValidationError
from backend.analytics import AnalyticsManager

# Initialize FastAPI App
app = FastAPI(
    title="AI Smart Civic Services API",
    description="High-performance async REST API powered by FastAPI, Scikit-learn AI NLP Engine, and SQLite.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for web/mobile frontend consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service singletons
db_path = Config.DATABASE_PATH
model_dir = Config.AI_MODEL_DIR

db = DatabaseManager(db_path)
ai = AIAnalyzer(model_dir)
notifier = NotificationManager(db)
complaint_mgr = ComplaintManager(db, ai, notifier)
analytics_mgr = AnalyticsManager(db)


# --- Pydantic Schemas ---
class AIAnalyzeRequest(BaseModel):
    title: Optional[str] = Field(default="", example="Deep Pothole on Main St")
    description: str = Field(..., example="Deep dangerous pothole on the main road causing car wheel damage.")


class AIAnalyzeResponse(BaseModel):
    category: str
    priority: str
    confidence: float
    reasoning: str
    sla_hours: int
    assigned_dept: str
    ai_summary: str
    keywords_detected: List[str]


class ChatbotRequest(BaseModel):
    message: str = Field(..., example="How do I report a broken streetlight?")


class ChatbotResponse(BaseModel):
    reply: str
    action: str
    timestamp: str


class ComplaintCreateRequest(BaseModel):
    citizen_id: int = Field(..., example=2)
    title: Optional[str] = Field(default="")
    description: str = Field(..., example="Water pipeline leak spraying onto street.")
    category: Optional[str] = Field(default="Auto-Detect")
    location: str = Field(..., example="124 Elm Street")
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    contact_phone: Optional[str] = Field(default="")


class StatusUpdateRequest(BaseModel):
    status: str = Field(..., example="In Progress")
    comment: Optional[str] = Field(default="Crew dispatched to site.")
    admin_id: int = Field(..., example=1)


# --- API Routes ---
@app.get("/", tags=["Health"])
def root():
    return {
        "service": "AI Smart Civic Services Microservice",
        "status": "online",
        "framework": "FastAPI",
        "docs": "/docs",
    }


@app.post("/api/v1/ai/analyze", response_model=AIAnalyzeResponse, tags=["AI Engine"])
def analyze_complaint_endpoint(payload: AIAnalyzeRequest):
    """Analyze issue text using scikit-learn model + hazard trigger rules."""
    result = ai.analyze_complaint(payload.description, payload.title or "")
    return result


@app.post("/api/v1/chatbot", response_model=ChatbotResponse, tags=["AI Engine"])
def chatbot_endpoint(payload: ChatbotRequest):
    """Get CivicBot AI responses."""
    result = ai.generate_chatbot_reply(payload.message)
    return result


@app.get("/api/v1/complaints", tags=["Complaints"])
def list_complaints(
    limit: int = Query(default=50, ge=1, le=200),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    category_filter: Optional[str] = Query(default=None, alias="category"),
):
    """List complaints with optional filters."""
    items = complaint_mgr.get_all_complaints(limit=limit)
    if status_filter:
        items = [c for c in items if c["status"] == status_filter]
    if category_filter:
        items = [c for c in items if c["category"] == category_filter]
    return {"count": len(items), "items": items}


@app.get("/api/v1/complaints/{complaint_id}", tags=["Complaints"])
def get_complaint_detail(complaint_id: int):
    """Get detailed complaint timeline and info."""
    c = complaint_mgr.get_complaint(complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint ticket not found")
    return c


@app.post("/api/v1/complaints", status_code=status.HTTP_201_CREATED, tags=["Complaints"])
def create_complaint_endpoint(payload: ComplaintCreateRequest):
    """Submit a new civic complaint via REST API."""
    try:
        res = complaint_mgr.submit_complaint(
            citizen_id=payload.citizen_id,
            title=payload.title or "",
            description=payload.description,
            category=payload.category or "Auto-Detect",
            location=payload.location,
            latitude=payload.latitude,
            longitude=payload.longitude,
            contact_phone=payload.contact_phone or "",
        )
        return res
    except ComplaintValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/v1/complaints/{complaint_id}/status", tags=["Complaints"])
def update_status_endpoint(complaint_id: int, payload: StatusUpdateRequest):
    """Update ticket status and log comment."""
    try:
        success = complaint_mgr.update_status(
            complaint_id=complaint_id,
            new_status=payload.status,
            comment=payload.comment or f"Status updated to {payload.status}",
            admin_id=payload.admin_id,
        )
        if not success:
            raise HTTPException(status_code=404, detail="Complaint ticket not found")
        return {"message": "Status updated successfully", "complaint_id": complaint_id, "new_status": payload.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/analytics", tags=["Analytics"])
def get_analytics():
    """Retrieve municipal analytics metrics & geo points."""
    return analytics_mgr.get_overview_stats()
