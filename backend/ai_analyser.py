"""
AIAnalyzer — Hybrid AI NLP Engine for Civic Complaint Categorization & Priority Routing.
Combines Scikit-Learn TF-IDF models with a Rule-Based Expert System for high accuracy & zero-downtime fallback.
"""
import os
import re
import pickle
from typing import Dict, Any, List, Tuple
from .models import Complaint


class AIAnalyzer:
    # Key urgency / hazard trigger phrases
    CRITICAL_TRIGGERS = [
        "fire", "gas leak", "explosion", "live wire", "electrical shock",
        "sewage flood", "structural collapse", "building collapse", "life threatening",
        "burst pipeline", "gushing water", "toxic spill", "chemical leak", "bridge collapse"
    ]

    HIGH_TRIGGERS = [
        "deep pothole", "no water", "water shortage", "overflowing garbage", "blackout",
        "traffic signal broken", "open manhole", "falling tree branch", "street light dark",
        "flooded street", "dead animal", "clogged drain"
    ]

    HAZARD_CATEGORY_OVERRIDE = {
        "fire": "Public Safety",
        "gas leak": "Public Safety",
        "explosion": "Public Safety",
        "live wire": "Street Lighting",
        "electrical shock": "Street Lighting",
        "sewage flood": "Water Supply",
        "burst pipeline": "Water Supply",
        "gushing water": "Water Supply",
        "building collapse": "Public Safety",
        "structural collapse": "Public Safety",
        "chemical leak": "Public Safety",
        "toxic spill": "Public Safety",
    }

    CATEGORY_KEYWORDS = {
        "Roads & Infrastructure": [
            "pothole", "road", "street", "asphalt", "crack", "bridge", "sidewalk",
            "pavement", "construction", "guardrail", "speed bump", "tar"
        ],
        "Water Supply": [
            "water", "leak", "pipe", "pipeline", "drainage", "tap", "sewage",
            "contamination", "gushing", "water pressure", "plumbing", "dirty water", "burst"
        ],
        "Sanitation": [
            "garbage", "trash", "waste", "dumpster", "sanitation", "smell", "odor",
            "litter", "uncollected", "cleanliness", "recycling", "dirty"
        ],
        "Public Safety": [
            "fire", "hazard", "gas leak", "accident", "manhole", "danger", "police",
            "safety", "crime", "emergency", "collapse", "unauthorized", "trespass", "explosion"
        ],
        "Street Lighting": [
            "light", "lamp", "pole", "dark", "electricity", "wire", "blackout",
            "flickering", "lighting", "bulb", "power outage"
        ],
        "Parks & Environment": [
            "park", "tree", "branch", "grass", "playground", "lawn", "garden",
            "weed", "environment", "bench", "fence", "vegetation"
        ]
    }

    def __init__(self, model_dir: str = ""):
        self.model_dir = model_dir
        self.model = None
        self.vectorizer = None
        self._load_model_if_available()

    def _load_model_if_available(self):
        if not self.model_dir or not os.path.exists(self.model_dir):
            return
        model_path = os.path.join(self.model_dir, "civic_model.pkl")
        vec_path = os.path.join(self.model_dir, "vectorizer.pkl")
        if os.path.exists(model_path) and os.path.exists(vec_path):
            try:
                with open(model_path, "rb") as mf, open(vec_path, "rb") as vf:
                    self.model = pickle.load(mf)
                    self.vectorizer = pickle.load(vf)
            except Exception:
                self.model = None
                self.vectorizer = None

    def analyze_complaint(self, description: str, title: str = "") -> Dict[str, Any]:
        """Classify category, determine priority, SLA, and reasoning for a complaint."""
        combined_text = f"{title} {description}".lower().strip()
        if not combined_text:
            return self._default_result()

        # Step 1: Check for Critical & High hazard triggers first (Safety First override)
        detected_critical = [kw for kw in self.CRITICAL_TRIGGERS if kw in combined_text]
        detected_high = [kw for kw in self.HIGH_TRIGGERS if kw in combined_text]

        # Step 2: Determine Category
        category, cat_confidence = self._classify_category(combined_text)

        # Check hazard category override if critical hazard matched
        for trig in detected_critical:
            if trig in self.HAZARD_CATEGORY_OVERRIDE:
                category = self.HAZARD_CATEGORY_OVERRIDE[trig]
                break

        # Step 3: Determine Priority & SLA
        if detected_critical:
            priority = "Critical"
            confidence = 0.98
            reasoning = f"CRITICAL HAZARD DETECTED: Contains risk triggers ({', '.join(detected_critical)}). Expedited 4-hour SLA assigned."
        elif detected_high:
            priority = "High"
            confidence = max(cat_confidence, 0.90)
            reasoning = f"HIGH PRIORITY: Urgency keywords detected ({', '.join(detected_high)}). 24-hour SLA assigned."
        else:
            if category in ["Public Safety", "Water Supply"]:
                priority = "High" if cat_confidence > 0.6 else "Medium"
            elif cat_confidence > 0.7:
                priority = "Medium"
            else:
                priority = "Low"
            confidence = cat_confidence
            reasoning = f"Categorized as '{category}' based on semantic keyword mapping. Standard {Complaint.DEFAULT_SLA_HOURS.get(priority, 48)}-hour SLA."

        sla_hours = Complaint.DEFAULT_SLA_HOURS.get(priority, 48)
        assigned_dept = Complaint.CATEGORY_DEPARTMENTS.get(category, "General Municipal Admin")

        # Short automated summary snippet
        clean_desc = re.sub(r'\s+', ' ', description).strip()
        ai_summary = (clean_desc[:120] + "...") if len(clean_desc) > 120 else clean_desc

        return {
            "category": category,
            "priority": priority,
            "confidence": float(confidence),
            "reasoning": reasoning,
            "sla_hours": sla_hours,
            "assigned_dept": assigned_dept,
            "ai_summary": ai_summary,
            "keywords_detected": detected_critical + detected_high
        }

    def _classify_category(self, text: str) -> Tuple[str, float]:
        # Try scikit-learn model if loaded
        if self.model and self.vectorizer:
            try:
                vec = self.vectorizer.transform([text])
                pred = self.model.predict(vec)[0]
                probs = self.model.predict_proba(vec)[0]
                conf = float(max(probs))
                if pred in Complaint.VALID_CATEGORIES:
                    return pred, conf
            except Exception:
                pass

        # Fallback Rule-Based Keyword Scorer
        scores = {}
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text)
            if matches > 0:
                scores[cat] = matches

        if not scores:
            return "General Civic Issue", 0.70

        best_cat = max(scores, key=scores.get)
        match_count = scores[best_cat]
        confidence = min(0.65 + (match_count * 0.10), 0.95)
        return best_cat, confidence

    def _default_result(self) -> Dict[str, Any]:
        return {
            "category": "General Civic Issue",
            "priority": "Medium",
            "confidence": 0.70,
            "reasoning": "Default classification assigned for general inquiry.",
            "sla_hours": 48,
            "assigned_dept": "General Municipal Admin",
            "ai_summary": "General civic ticket submitted.",
            "keywords_detected": []
        }

    def generate_chatbot_reply(self, user_message: str) -> Dict[str, Any]:
        """Generate conversational AI assistant responses for CivicBot."""
        msg = user_message.lower().strip()

        if any(w in msg for w in ["report", "submit", "file", "create"]):
            reply = "You can report a new civic issue by clicking 'Report Issue' in the top menu or visiting the issue submission page. Our AI will automatically analyze your description, select the category, and dispatch it to the correct department."
            action = "navigate_submit"
        elif any(w in msg for w in ["status", "check", "track", "ticket", "my complaint"]):
            reply = "To view your submitted tickets and their live status, visit the 'My Complaints' section on your dashboard. You'll see real-time updates and response timelines."
            action = "navigate_my_complaints"
        elif any(w in msg for w in ["emergency", "critical", "danger", "fire", "leak", "hazard"]):
            reply = "⚠️ If this is a life-threatening emergency, please dial your local emergency services (911/112/100) immediately. For urgent municipal hazards (like live wires or gas leaks), select 'Public Safety' when reporting so our system assigns an immediate 4-hour SLA."
            action = "emergency_warning"
        elif any(w in msg for w in ["admin", "department", "sla", "priority"]):
            reply = "Municipal departments respond based on ticket priority: Critical issues have a 4-hour SLA, High priority has a 24-hour SLA, Medium priority has 48 hours, and Low priority has 72 hours."
            action = "info_sla"
        else:
            reply = "I'm CivicBot AI! I can help you file civic complaint reports, explain how priority SLAs work, check department routing, or answer municipal services questions. How can I help you?"
            action = "general"

        return {
            "reply": reply,
            "action": action,
            "timestamp": os.environ.get("TIMESTAMP", "")
        }
