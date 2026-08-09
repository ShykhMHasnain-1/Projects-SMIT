"""
DatabaseManager — Parameterized SQLite Data Access Layer for AI Smart Civic Services.
Handles schema initialization, CRUD operations, transactions, and initial seed data.
"""
import os
import sqlite3
from typing import List, Dict, Any, Optional
from werkzeug.security import generate_password_hash
from .models import User, Citizen, Admin, Complaint, Notification


class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        db_dir = os.path.dirname(os.path.abspath(db_path))
        os.makedirs(db_dir, exist_ok=True)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Create tables if they do not exist and seed initial demo data."""
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'citizen',
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    citizen_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    location TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    image_path TEXT,
                    contact_phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sla_hours INTEGER DEFAULT 48,
                    assigned_dept TEXT DEFAULT 'General Municipal Admin',
                    ai_confidence REAL DEFAULT 0.85,
                    ai_summary TEXT,
                    FOREIGN KEY (citizen_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS complaint_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    complaint_id INTEGER NOT NULL,
                    status_from TEXT,
                    status_to TEXT NOT NULL,
                    comment TEXT,
                    updated_by_id INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
                    FOREIGN KEY (updated_by_id) REFERENCES users(id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    complaint_id INTEGER,
                    is_read BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
                );
            """)

            # Seed default admin user
            admin_row = conn.execute("SELECT id FROM users WHERE role = 'admin'").fetchone()
            if not admin_row:
                conn.execute("""
                    INSERT INTO users (name, email, password_hash, role, phone)
                    VALUES (?, ?, ?, 'admin', ?)
                """, (
                    "Municipal Admin",
                    "admin@civic.gov",
                    generate_password_hash("Admin@123"),
                    "+1-800-CIVIC-01"
                ))

            # Seed default demo citizen user
            citizen_row = conn.execute("SELECT id FROM users WHERE email = 'citizen@civic.gov'").fetchone()
            if not citizen_row:
                cursor = conn.execute("""
                    INSERT INTO users (name, email, password_hash, role, phone)
                    VALUES (?, ?, ?, 'citizen', ?)
                """, (
                    "Jane Doe",
                    "citizen@civic.gov",
                    generate_password_hash("Citizen@123"),
                    "+1-555-019-2831"
                ))
                citizen_id = cursor.lastrowid
            else:
                citizen_id = citizen_row["id"]

            # Seed initial sample complaints if empty
            c_count = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
            if c_count == 0 and citizen_id:
                sample_tickets = [
                    (
                        citizen_id,
                        "Dangerous Pothole on 5th Avenue & Main",
                        "Deep pothole causing traffic slowdown and potential wheel damage near central station.",
                        "Roads & Infrastructure",
                        "High",
                        "In Progress",
                        "5th Ave & Main St, Downtown",
                        37.7749, -122.4194,
                        "Public Works Department",
                        24,
                        0.92,
                        "High priority road repair required on primary thoroughfare."
                    ),
                    (
                        citizen_id,
                        "Broken Water Pipeline Leaking Fresh Water",
                        "Major underground pipe leakage spraying water onto sidewalk and weakening road foundation.",
                        "Water Supply",
                        "Critical",
                        "Pending",
                        "124 Elm Street, North Ward",
                        37.7833, -122.4167,
                        "Water & Sewage Board",
                        4,
                        0.98,
                        "CRITICAL: Immediate water supply valve isolation needed."
                    ),
                    (
                        citizen_id,
                        "Uncollected Garbage Piles near Public Market",
                        "Overflowing waste containers causing foul odor and hygienic hazard near fresh market area.",
                        "Sanitation",
                        "Medium",
                        "Resolved",
                        "Market Square Plaza",
                        37.7690, -122.4480,
                        "Waste Management & Hygiene",
                        48,
                        0.88,
                        "Sanitation crew dispatched; area cleared and disinfected."
                    ),
                    (
                        citizen_id,
                        "Flickering Street Lamp & Exposed Wiring",
                        "Street light on 9th street pole is out and base box panel cover is missing.",
                        "Street Lighting",
                        "Medium",
                        "In Progress",
                        "9th Street & Oak Ave",
                        37.7550, -122.4200,
                        "Electrical & Energy Board",
                        48,
                        0.91,
                        "Electrical inspection scheduled."
                    ),
                ]
                for ticket in sample_tickets:
                    cursor = conn.execute("""
                        INSERT INTO complaints (
                            citizen_id, title, description, category, priority, status,
                            location, latitude, longitude, assigned_dept, sla_hours,
                            ai_confidence, ai_summary
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, ticket)
                    cid = cursor.lastrowid
                    conn.execute("""
                        INSERT INTO notifications (user_id, message, complaint_id)
                        VALUES (?, ?, ?)
                    """, (
                        citizen_id,
                        f"Ticket #{cid} '{ticket[1]}' registered and routed to {ticket[9]}.",
                        cid
                    ))

    # --- User Management ---
    def create_user(self, user: User) -> int:
        try:
            with self._connect() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (name, email, password_hash, role, phone)
                    VALUES (?, ?, ?, ?, ?)
                """, (user.name, user.email, user.password_hash, user.role, user.phone))
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise DatabaseError("An account with this email address already exists.")
        except sqlite3.Error as e:
            raise DatabaseError(f"Database error while creating user: {e}")

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
            if not row:
                return None
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                role=row["role"],
                phone=row["phone"],
                created_at=row["created_at"]
            )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                return None
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                role=row["role"],
                phone=row["phone"],
                created_at=row["created_at"]
            )

    # --- Complaint Management ---
    def create_complaint(self, complaint: Complaint) -> int:
        try:
            with self._connect() as conn:
                cursor = conn.execute("""
                    INSERT INTO complaints (
                        citizen_id, title, description, category, priority, status,
                        location, latitude, longitude, image_path, contact_phone,
                        sla_hours, assigned_dept, ai_confidence, ai_summary
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    complaint.citizen_id, complaint.title, complaint.description,
                    complaint.category, complaint.priority, complaint.status,
                    complaint.location, complaint.latitude, complaint.longitude,
                    complaint.image_path, complaint.contact_phone, complaint.sla_hours,
                    complaint.assigned_dept, complaint.ai_confidence, complaint.ai_summary
                ))
                cid = cursor.lastrowid
                
                # Add initial audit track log
                conn.execute("""
                    INSERT INTO complaint_updates (complaint_id, status_from, status_to, comment, updated_by_id)
                    VALUES (?, 'Submitted', 'Pending', 'Issue ticket submitted by citizen & classified by AI Engine.', ?)
                """, (cid, complaint.citizen_id))
                return cid
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to create complaint record: {e}")

    def get_complaint(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("""
                SELECT c.*, u.name as citizen_name, u.email as citizen_email
                FROM complaints c
                LEFT JOIN users u ON c.citizen_id = u.id
                WHERE c.id = ?
            """, (complaint_id,)).fetchone()
            if not row:
                return None
            d = dict(row)
            
            # Fetch status updates timeline
            updates = conn.execute("""
                SELECT cu.*, u.name as updated_by_name
                FROM complaint_updates cu
                LEFT JOIN users u ON cu.updated_by_id = u.id
                WHERE cu.complaint_id = ?
                ORDER BY cu.created_at ASC
            """, (complaint_id,)).fetchall()
            d["timeline"] = [dict(u) for u in updates]
            return d

    def get_all_complaints(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT c.*, u.name as citizen_name, u.email as citizen_email
                FROM complaints c
                LEFT JOIN users u ON c.citizen_id = u.id
                ORDER BY c.created_at DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]

    def get_citizen_complaints(self, citizen_id: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT * FROM complaints
                WHERE citizen_id = ?
                ORDER BY created_at DESC
            """, (citizen_id,)).fetchall()
            return [dict(r) for r in rows]

    def update_complaint_status(self, complaint_id: int, new_status: str, comment: str, admin_id: int) -> bool:
        with self._connect() as conn:
            row = conn.execute("SELECT status FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
            if not row:
                return False
            old_status = row["status"]
            
            conn.execute("""
                UPDATE complaints
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_status, complaint_id))
            
            conn.execute("""
                INSERT INTO complaint_updates (complaint_id, status_from, status_to, comment, updated_by_id)
                VALUES (?, ?, ?, ?, ?)
            """, (complaint_id, old_status, new_status, comment, admin_id))
            return True

    # --- Notifications ---
    def create_notification(self, user_id: int, message: str, complaint_id: Optional[int] = None) -> int:
        with self._connect() as conn:
            cursor = conn.execute("""
                INSERT INTO notifications (user_id, message, complaint_id)
                VALUES (?, ?, ?)
            """, (user_id, message, complaint_id))
            return cursor.lastrowid

    def get_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            query = "SELECT * FROM notifications WHERE user_id = ?"
            params = [user_id]
            if unread_only:
                query += " AND is_read = 0"
            query += " ORDER BY created_at DESC LIMIT 50"
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def mark_notifications_read(self, user_id: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
