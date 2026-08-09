"""
NotificationManager — handles in-app notifications for citizens and admins.
Kept as its own class so a real channel (email/SMS push) can be added later
without touching ComplaintManager.
"""
from __future__ import annotations
from .database import DatabaseManager


class NotificationManager:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def notify(self, user_id: int, message: str, complaint_id: int | None = None) -> None:
        try:
            self.db.create_notification(user_id, message, complaint_id)
        except Exception:
            # Notification failures must never break the core complaint workflow.
            pass

    def notify_admins_of_critical(self, complaint) -> None:
        """Automatic escalation: alert every admin account when a Critical
        complaint is created."""
        with self.db._connect() as conn:  # internal read, acceptable within backend layer
            admins = conn.execute("SELECT id FROM users WHERE role = 'admin'").fetchall()
        for row in admins:
            self.notify(
                row["id"],
                f"CRITICAL complaint #{complaint.id} reported in {complaint.location} "
                f"({complaint.category}). Immediate review recommended.",
                complaint.id,
            )

    def get_notifications(self, user_id: int, unread_only: bool = False) -> list[dict]:
        return self.db.get_notifications(user_id, unread_only)

    def mark_read(self, user_id: int) -> None:
        self.db.mark_notifications_read(user_id)