"""
ComplaintManager — Business Domain Coordinator for Complaint Lifecycle, AI Auto-Routing, & Escalations.
"""
from typing import Dict, Any, List, Optional
from .database import DatabaseManager, DatabaseError
from .ai_analyser import AIAnalyzer
from .models import Complaint, User


class ComplaintValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


class ComplaintManager:
    def __init__(self, db: DatabaseManager, ai: AIAnalyzer, notifier=None):
        self.db = db
        self.ai = ai
        self.notifier = notifier

    def submit_complaint(
        self,
        citizen_id: int,
        description: str,
        location: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        title: str = "",
        category: str = "Auto-Detect",
        image_path: Optional[str] = None,
        contact_phone: str = "",
    ) -> Dict[str, Any]:
        """Submit a new complaint, analyze with AI, save to DB, and trigger notifications."""
        # Clean inputs
        description = description.strip()
        location = location.strip()
        title = title.strip()

        # Validate core fields
        temp_c = Complaint(
            citizen_id=citizen_id,
            title=title,
            description=description,
            location=location,
        )
        errors = temp_c.validate()
        if errors:
            raise ComplaintValidationError(errors)

        # Run AI Analysis Engine
        ai_res = self.ai.analyze_complaint(description, title)
        
        # If user explicitly chose a valid category (other than Auto-Detect), honor user's choice
        final_category = category if category in Complaint.VALID_CATEGORIES else ai_res["category"]
        final_priority = ai_res["priority"]
        sla_hours = ai_res["sla_hours"]
        assigned_dept = ai_res["assigned_dept"]

        # Create formal Complaint instance
        complaint = Complaint(
            citizen_id=citizen_id,
            title=title or (description[:40] + "..." if len(description) > 40 else description),
            description=description,
            category=final_category,
            priority=final_priority,
            status="Pending",
            location=location,
            latitude=latitude,
            longitude=longitude,
            image_path=image_path,
            contact_phone=contact_phone,
            sla_hours=sla_hours,
            assigned_dept=assigned_dept,
            ai_confidence=ai_res["confidence"],
            ai_summary=ai_res["ai_summary"],
        )

        cid = self.db.create_complaint(complaint)
        complaint.id = cid

        # Send Notifications
        if self.notifier:
            self.notifier.notify(
                user_id=citizen_id,
                message=f"Your complaint #{cid} '{complaint.title}' has been submitted. Category: '{final_category}' ({final_priority} priority, routed to {assigned_dept}).",
                complaint_id=cid,
            )
            if final_priority == "Critical":
                self.notifier.notify_admins_of_critical(complaint)

        return complaint.to_dict()

    def get_complaint(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        return self.db.get_complaint(complaint_id)

    def get_all_complaints(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.db.get_all_complaints(limit)

    def get_citizen_complaints(self, citizen_id: int) -> List[Dict[str, Any]]:
        return self.db.get_citizen_complaints(citizen_id)

    def update_status(self, complaint_id: int, new_status: str, comment: str, admin_id: int) -> bool:
        if new_status not in Complaint.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {Complaint.VALID_STATUSES}")

        complaint = self.db.get_complaint(complaint_id)
        if not complaint:
            return False

        success = self.db.update_complaint_status(complaint_id, new_status, comment, admin_id)
        if success and self.notifier:
            self.notifier.notify(
                user_id=complaint["citizen_id"],
                message=f"Status update for Ticket #{complaint_id}: Changed to '{new_status}'. Comment: {comment}",
                complaint_id=complaint_id,
            )
        return success
