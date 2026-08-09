"""
Domain Models for AI Smart Civic Services.
Includes Citizen, Admin, User, Complaint, and Notification data structures.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        email: str = "",
        password: str = "",
        password_hash: str = "",
        role: str = "citizen",
        phone: str = "",
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.name = name.strip()
        self.email = email.strip().lower()
        self.role = role
        self.phone = phone.strip()
        self.created_at = created_at or datetime.now().isoformat()
        
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = password_hash

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def validate(self) -> List[str]:
        errors = []
        if not self.name or len(self.name) < 2:
            errors.append("Full name must be at least 2 characters.")
        if not self.email or "@" not in self.email or "." not in self.email:
            errors.append("Valid email address is required.")
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "created_at": self.created_at,
        }


class Citizen(User):
    def __init__(self, **kwargs):
        kwargs["role"] = "citizen"
        super().__init__(**kwargs)


class Admin(User):
    def __init__(self, **kwargs):
        kwargs["role"] = "admin"
        super().__init__(**kwargs)


class Complaint:
    VALID_CATEGORIES = [
        "Roads & Infrastructure",
        "Water Supply",
        "Sanitation",
        "Public Safety",
        "Street Lighting",
        "Parks & Environment",
        "General Civic Issue",
    ]

    VALID_PRIORITIES = ["Critical", "High", "Medium", "Low"]

    VALID_STATUSES = ["Pending", "In Progress", "Resolved", "Rejected"]

    DEFAULT_SLA_HOURS = {
        "Critical": 4,
        "High": 24,
        "Medium": 48,
        "Low": 72,
    }

    CATEGORY_DEPARTMENTS = {
        "Roads & Infrastructure": "Public Works Department",
        "Water Supply": "Water & Sewage Board",
        "Sanitation": "Waste Management & Hygiene",
        "Public Safety": "Civic Protection & Safety Team",
        "Street Lighting": "Electrical & Energy Board",
        "Parks & Environment": "Horticulture & Parks Dept",
        "General Civic Issue": "General Municipal Admin",
    }

    def __init__(
        self,
        id: Optional[int] = None,
        citizen_id: int = 0,
        title: str = "",
        description: str = "",
        category: str = "General Civic Issue",
        priority: str = "Medium",
        status: str = "Pending",
        location: str = "",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        image_path: Optional[str] = None,
        contact_phone: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        sla_hours: int = 48,
        assigned_dept: str = "General Municipal Admin",
        ai_confidence: float = 0.85,
        ai_summary: str = "",
    ):
        self.id = id
        self.citizen_id = citizen_id
        self.title = title.strip() or (description[:40] + "..." if len(description) > 40 else description)
        self.description = description.strip()
        self.category = category if category in self.VALID_CATEGORIES else "General Civic Issue"
        self.priority = priority if priority in self.VALID_PRIORITIES else "Medium"
        self.status = status if status in self.VALID_STATUSES else "Pending"
        self.location = location.strip()
        self.latitude = latitude
        self.longitude = longitude
        self.image_path = image_path
        self.contact_phone = contact_phone.strip()
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.sla_hours = sla_hours or self.DEFAULT_SLA_HOURS.get(self.priority, 48)
        self.assigned_dept = assigned_dept or self.CATEGORY_DEPARTMENTS.get(self.category, "General Municipal Admin")
        self.ai_confidence = ai_confidence
        self.ai_summary = ai_summary

    def validate(self) -> List[str]:
        errors = []
        if not self.description or len(self.description) < 10:
            errors.append("Please provide a detailed issue description (at least 10 characters).")
        if not self.location or len(self.location) < 3:
            errors.append("Please specify a location or landmark (at least 3 characters).")
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "citizen_id": self.citizen_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "image_path": self.image_path,
            "contact_phone": self.contact_phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "sla_hours": self.sla_hours,
            "assigned_dept": self.assigned_dept,
            "ai_confidence": round(self.ai_confidence, 2),
            "ai_summary": self.ai_summary,
        }


class Notification:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        message: str = "",
        complaint_id: Optional[int] = None,
        is_read: bool = False,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.complaint_id = complaint_id
        self.is_read = is_read
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "complaint_id": self.complaint_id,
            "is_read": self.is_read,
            "created_at": self.created_at,
        }
