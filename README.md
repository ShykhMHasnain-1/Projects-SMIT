# 🏛️ AI Smart Civic Services Portal

An intelligent, full-stack municipal civic issue management platform powered by **Python (Flask & FastAPI)** on the backend and modern **HTML5, CSS3, JavaScript** on the frontend.

---

## 🌟 Key Features

- **🤖 AI Machine Learning Engine (Scikit-Learn + NLP Rules)**: Auto-categorizes citizen reports into categories (Roads & Infrastructure, Water Supply, Sanitation, Public Safety, Street Lighting, Parks & Environment).
- **⚡ Hazard Risk Detector & Auto-Escalation**: Detects critical emergency keywords (e.g. fire, gas leak, building collapse) and automatically assigns 4-hour SLA with real-time admin escalation notifications.
- **💬 CivicBot AI Assistant**: Interactive 24/7 chatbot embedded in the frontend UI to guide citizens, answer SLA questions, and assist in filing complaints.
- **🎨 Glassmorphism Responsive UI**: Dark/Light mode theme switcher, drag-and-drop evidence image dropzone with live preview, real-time debounced AI text analysis feedback.
- **📊 Municipal Command Center**: Admin dashboard featuring resolution analytics, SLA compliance rate indicators, live filtering queue, and status management.
- **🚀 Dual Python Backend**:
  - **Flask**: SSR Web Application serving templates, session-based auth, and portal routes on port `5000`.
  - **FastAPI**: Asynchronous RESTful API microservice serving high-performance API endpoints on port `8000`.

---

## 📁 Project Architecture

```
d:/ai/
├── app.py                     # Flask Application Entry Point (Port 5000)
├── fastapi_app.py             # FastAPI Microservice Entry Point (Port 8000)
├── config.py                  # Environment Configuration & SLA rules
├── requirements.txt           # Dependency Manifest
├── backend/
│   ├── models.py              # Domain Models (User, Citizen, Admin, Complaint, Notification)
│   ├── database.py            # SQLite DatabaseManager with Parameterized SQL & Seed Data
│   ├── ai_analyser.py         # AI NLP Categorization & Chatbot Engine
│   ├── complaint_manager.py   # Complaint Lifecycle Coordinator & Auto-Escalations
│   ├── analytics.py           # BI Analytics & Geospatial Metric Aggregators
│   ├── notifications.py       # In-App Notification Manager
│   ├── training_data.py       # Labeled Training Dataset for Civic Categories
│   └── train_model.py         # Script to Train Scikit-Learn Model Binaries
├── routes/
│   ├── main_routes.py         # Public Home & Info Routes
│   ├── auth_routes.py         # Registration, Login, Logout Routes
│   ├── citizen_routes.py      # Citizen Dashboard, Submission, Ticket Detail Routes
│   ├── admin_routes.py        # Admin Command Center & Status Update Routes
│   └── api_routes.py          # Flask JSON REST Endpoints
└── frontend/
    ├── base.html              # Core Layout Shell (Header, Navigation, Footer, Chatbot)
    ├── style.css              # Main Styling System
    ├── static/
    │   ├── css/style.css      # CSS Variables & Component Styling
    │   └── js/main.js         # Interactive Theme, Chatbot, Dropzone & Live AI Preview JS
    └── templates/
        ├── index.html         # Hero Landing Page & Platform Overview
        ├── login.html         # User Authentication Login Page
        ├── register.html      # Citizen Account Registration Page
        ├── citizen_dashboard.html # Citizen Personal Portal Dashboard
        ├── submit_complaint.html  # Interactive Issue Reporting Form with AI Live Preview
        ├── complaint_detail.html  # Ticket History & Department Resolution Timeline
        ├── my_complaints.html     # Filterable List of Citizen Issues
        ├── admin_dashboard.html   # Admin Command Center & Dispatch Queue
        ├── admin_complaints.html  # Admin Full Ticket Manager & Status Control
        └── admin_analytics.html   # System-Wide Analytics & Metrics Dashboard
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Scikit-Learn AI Model (One-Time Setup)
```bash
python -m backend.train_model
```

### 3. Run the Flask Web Application (Frontend + SSR)
```bash
python app.py
```
Open **`http://localhost:5000`** in your browser.

### 4. Run the FastAPI Microservice (REST API + Swagger Docs)
In a separate terminal:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```
Open **`http://localhost:8000/docs`** to explore interactive Swagger UI API documentation.

---

## 🔑 Default Credentials

- **Admin Account**: `admin@civic.gov` / `Admin@123`
- **Demo Citizen**: `citizen@civic.gov` / `Citizen@123`
