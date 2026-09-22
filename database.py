"""
JSON File Database Manager for Akhil Pandey's FastAPI Portfolio
Supports full CRUD for Projects, Experience, Education, Skills, Profile, and Messages.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "portfolio.json")

DEFAULT_DATA: Dict[str, Any] = {
    "profile": {
        "name": "Akhil Pandey",
        "brand": "AutomateX",
        "role_title": "Software Developer & Automation Specialist",
        "tagline": "Software Developer | Python & FastAPI | Workflow Automation",
        "short_bio": "MCA graduate from Nirma University with 2+ years of professional IT experience building scalable backend APIs, custom CRM systems, and automated business workflows.",
        "about": "I am a backend-focused Software Developer with hands-on expertise in Python, FastAPI, Django, and automated workflow pipelines (n8n, Zapier, Make.com). I help businesses and clients streamline operations, eliminate repetitive manual data entry, and deploy robust, live applications on Render and Cloud platforms.",
        "email": "akhil.pandeyy1@gmail.com",
        "phone": "+91 76003 47544",
        "location": "Navsari, Gujarat, India - 396445",
        "github": "https://github.com/akhiil1",
        "linkedin": "https://linkedin.com/in/akhiil1",
        "admin_pin": "akhil123",
        "status_badge": "Available for Full-Time & Freelance Projects",
        "resume_url": "/resume",
        "stats": [
            {"label": "Years Experience", "value": "2+"},
            {"label": "Manual Effort Cut", "value": "75%"},
            {"label": "APIs & Workflows Built", "value": "30+"},
            {"label": "State Merit Rank", "value": "65th"}
        ]
    },
    "skills": [
        "Python",
        "FastAPI",
        "Django",
        "RESTful APIs & Microservices",
        "PostgreSQL",
        "MySQL",
        "SQLite",
        "Redis Caching",
        "n8n Workflow Automation",
        "Zapier",
        "Make.com",
        "RPA Automation",
        "Docker & Containers",
        "Render Cloud Deployment",
        "Git & GitHub",
        "Postman API Testing",
        "AI & LLM Integrations",
        "JavaScript & HTML/CSS"
    ],
    "services": [
        {
            "id": "srv-1",
            "icon": "🔄",
            "color": "green",
            "title": "Workflow & Process Automation",
            "desc": "Stop wasting hours on manual spreadsheet entry. I connect your tools (Make.com, Zapier, n8n) so your business operations run smoothly on autopilot.",
            "deliverables": [
                "Automated multi-app data synchronization",
                "Instant customer & team notification alerts",
                "Elimination of manual office mistakes"
            ]
        },
        {
            "id": "srv-2",
            "icon": "⚡",
            "color": "purple",
            "title": "Backend APIs & Microservices",
            "desc": "Fast, rock-solid server backends built with Python, FastAPI, and Django. Designed for speed, high concurrency, and zero downtime.",
            "deliverables": [
                "RESTful API design & interactive Swagger docs",
                "Asynchronous background task queues (Celery/Redis)",
                "Secure token authentication & data validation"
            ]
        },
        {
            "id": "srv-3",
            "icon": "💼",
            "color": "cyan",
            "title": "CRM Software & Business Systems",
            "desc": "Customized CRM software and internal dashboards tailored to your exact daily operational and client tracking requirements.",
            "deliverables": [
                "Custom business logic & lead pipelines",
                "Structured database validation & audit readiness",
                "Faster turnaround on client inquiries"
            ]
        },
        {
            "id": "srv-4",
            "icon": "🤖",
            "color": "amber",
            "title": "AI & Document Data Extraction",
            "desc": "Automated document processing pipelines that extract invoices, receipts, and client inquiries directly into structured database records.",
            "deliverables": [
                "Intelligent OCR data extraction",
                "Automated mathematical & consistency checks",
                "LLM & OpenAI API integrations"
            ]
        }
    ],
    "projects": [
        {
            "id": "proj-1",
            "title": "AutomateX API Gateway & Workflow Orchestrator",
            "category": "backend",
            "category_label": "Backend & APIs",
            "description": "High-throughput asynchronous REST API built with FastAPI, PostgreSQL, and Redis. Features automated webhook ingestion, retry mechanisms, and rate-limited endpoints. Deployed live on Render.",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "Render"],
            "github_url": "https://github.com/akhiil1/automatex-api-gateway",
            "render_url": "https://automatex-api-gateway.onrender.com",
            "has_render": True,
            "status": "Live on Render",
            "date": "2025"
        },
        {
            "id": "proj-2",
            "title": "AI-Powered Customer CRM & Automated Leads Engine",
            "category": "automation",
            "category_label": "Workflow Automation",
            "description": "Custom CRM engine engineered for rapid client query intake, automated email alerts, and multi-step webhook sync between forms, database, and notification channels. Hosted live on Render.",
            "tech_stack": ["Python", "Django", "N8N", "Zapier", "REST APIs", "Render"],
            "github_url": "https://github.com/akhiil1/ai-leads-crm-automation",
            "render_url": "https://leads-crm-engine.onrender.com",
            "has_render": True,
            "status": "Live on Render",
            "date": "2025"
        },
        {
            "id": "proj-3",
            "title": "Smart Document Data Extraction & OCR Pipeline",
            "category": "automation",
            "category_label": "Automation & AI",
            "description": "Automated OCR extraction pipeline that reads invoices and vouchers, executes strict mathematical validation rules, and saves structured records into databases.",
            "tech_stack": ["Python", "OpenCV", "FastAPI", "Make.com", "SQL"],
            "github_url": "https://github.com/akhiil1/doc-extractor-pipeline",
            "render_url": "",
            "has_render": False,
            "status": "GitHub Repo",
            "date": "2024"
        },
        {
            "id": "proj-4",
            "title": "Scalable Authentication & Microservices Boilerplate",
            "category": "backend",
            "category_label": "Microservices",
            "description": "Production-ready template for microservices architecture featuring JWT authentication, role-based access control (RBAC), rate-limiting middleware, and health-check monitoring.",
            "tech_stack": ["Python", "FastAPI", "JWT", "Docker", "PostgreSQL", "Render"],
            "github_url": "https://github.com/akhiil1/fastapi-auth-microservices",
            "render_url": "https://fastapi-microservices-demo.onrender.com",
            "has_render": True,
            "status": "Live on Render",
            "date": "2024"
        },
        {
            "id": "proj-5",
            "title": "RPA Financial Reconciliation & Reporting Bot",
            "category": "automation",
            "category_label": "RPA Automation",
            "description": "Automated desktop & web scraping bot to match bank receipts with internal ledger records, generating audit-ready Excel reports and notifying stakeholders on Slack/Email.",
            "tech_stack": ["Python", "Pandas", "Zapier", "Office 365"],
            "github_url": "https://github.com/akhiil1/rpa-finance-reconciler",
            "render_url": "",
            "has_render": False,
            "status": "GitHub Repo",
            "date": "2024"
        }
    ],
    "experience": [
        {
            "id": "exp-1",
            "role": "Python Developer",
            "company": "Digipie Technologies",
            "location": "Surat, Gujarat",
            "period": "Jul 2025 – Present",
            "badge": "Current Role",
            "points": [
                "Architecting robust backend APIs using Python (FastAPI & Django); coordinating with team members and clients to resolve queries and deliver work on time.",
                "Automating routine office workflows using Make.com, Zapier, and N8N, reducing manual operational effort by 75% and minimizing errors.",
                "Performing data validation and consistency checks; identifying root causes of data issues and maintaining audit-ready records."
            ]
        },
        {
            "id": "exp-2",
            "role": "Software Developer",
            "company": "Biztechnosys Infotech Pvt Ltd",
            "location": "Bangalore, Karnataka",
            "period": "Jul 2024 – Jun 2025",
            "badge": "Full-Time",
            "points": [
                "Interacted with clients to understand their working process and customized CRM software as per their day-to-day requirements.",
                "Maintained structured data, validation rules, and reporting formats to keep enterprise records clean and audit-ready.",
                "Improved turnaround time of backend processes through better coordination, query tuning, and proactive follow-ups."
            ]
        },
        {
            "id": "exp-3",
            "role": "RPA Developer (Internship)",
            "company": "1Rivet India LLP",
            "location": "Valsad, Gujarat",
            "period": "Feb 2024 – Jun 2024",
            "badge": "Internship",
            "points": [
                "Identified repetitive manual tasks in office processes and helped automate them, significantly improving overall efficiency.",
                "Collaborated with senior engineers to track, benchmark, and report runtime improvements of automated processes."
            ]
        }
    ],
    "education": [
        {
            "id": "edu-1",
            "degree": "Master of Computer Application (MCA)",
            "institution": "Institute of Technology, Nirma University",
            "location": "Ahmedabad, Gujarat",
            "period": "2022 – 2024",
            "grade": "78.60%",
            "highlights": "Served as Vice President of Association of MCA Students (AMS); Secured 65th State Rank in national-level ACPC-CMAT entrance exam."
        },
        {
            "id": "edu-2",
            "degree": "Bachelor of Computer Application (BCA)",
            "institution": "Naran Lala College of Professional & Applied Sciences",
            "location": "Navsari, Gujarat",
            "period": "2019 – 2022",
            "grade": "80.40%",
            "highlights": "Specialized in Computer Programming, Database Management Systems, and Software Engineering."
        },
        {
            "id": "edu-3",
            "degree": "Higher Secondary (HSC) & Secondary (SSC)",
            "institution": "Navchetan High School",
            "location": "Navsari, Gujarat",
            "period": "2017 – 2019",
            "grade": "HSC: 70.26% | SSC: 66.00%",
            "highlights": "Strong foundation in Science and Computer Operations."
        }
    ],
    "messages": []
}

def load_data() -> Dict[str, Any]:
    """Loads portfolio database from JSON or initializes with defaults."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure resume_url and skills array exist
                if "profile" in data and "resume_url" not in data["profile"]:
                    data["profile"]["resume_url"] = "/resume"
                if "skills" not in data or isinstance(data.get("skills"), dict):
                    data["skills"] = DEFAULT_DATA["skills"]
                return data
        except Exception as e:
            print(f"[!] Warning reading {DATA_FILE}: {e}. Using defaults.")
    
    save_data(DEFAULT_DATA)
    return DEFAULT_DATA

def save_data(data: Dict[str, Any]) -> bool:
    """Saves portfolio database to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[!] Error saving to {DATA_FILE}: {e}")
        return False

# ============================================================================
# Projects CRUD
# ============================================================================

def get_projects() -> List[Dict[str, Any]]:
    return load_data().get("projects", [])

def get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    for p in get_projects():
        if p.get("id") == project_id:
            return p
    return None

def add_project(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    db = load_data()
    tech_stack = data_dict.get("tech_stack", [])
    if isinstance(tech_stack, str):
        tech_stack = [t.strip() for t in tech_stack.split(",") if t.strip()]

    render_url = data_dict.get("render_url", "").strip()
    has_render = bool(render_url) and bool(data_dict.get("has_render", True))

    category = data_dict.get("category", "backend")
    category_label = data_dict.get("category_label")
    if not category_label:
        cat_map = {
            "backend": "Backend & APIs",
            "automation": "Workflow Automation & AI",
            "microservices": "Microservices",
            "fullstack": "Full-Stack Application"
        }
        category_label = cat_map.get(category, "Software Project")

    new_project = {
        "id": f"proj-{int(datetime.now().timestamp() * 1000)}",
        "title": data_dict.get("title", "").strip(),
        "category": category,
        "category_label": category_label,
        "description": data_dict.get("description", "").strip(),
        "tech_stack": tech_stack,
        "github_url": data_dict.get("github_url", "").strip(),
        "render_url": render_url,
        "has_render": has_render,
        "status": "Live on Render" if has_render else "GitHub Repo",
        "date": str(datetime.now().year)
    }

    db.setdefault("projects", []).insert(0, new_project)
    save_data(db)
    return new_project

def update_project(project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = load_data()
    projects = db.get("projects", [])
    for i, p in enumerate(projects):
        if p.get("id") == project_id:
            if "title" in updates and updates["title"] is not None:
                p["title"] = updates["title"].strip()
            if "category" in updates and updates["category"] is not None:
                p["category"] = updates["category"]
            if "category_label" in updates and updates["category_label"] is not None:
                p["category_label"] = updates["category_label"]
            if "description" in updates and updates["description"] is not None:
                p["description"] = updates["description"].strip()
            if "tech_stack" in updates and updates["tech_stack"] is not None:
                ts = updates["tech_stack"]
                p["tech_stack"] = [t.strip() for t in ts.split(",") if t.strip()] if isinstance(ts, str) else ts
            if "github_url" in updates and updates["github_url"] is not None:
                p["github_url"] = updates["github_url"].strip()
            if "render_url" in updates and updates["render_url"] is not None:
                p["render_url"] = updates["render_url"].strip()
            
            has_render = bool(p.get("render_url")) and bool(updates.get("has_render", True))
            p["has_render"] = has_render
            p["status"] = "Live on Render" if has_render else "GitHub Repo"

            projects[i] = p
            db["projects"] = projects
            save_data(db)
            return p
    return None

def delete_project(project_id: str) -> bool:
    db = load_data()
    projects = db.get("projects", [])
    filtered = [p for p in projects if p.get("id") != project_id]
    if len(filtered) != len(projects):
        db["projects"] = filtered
        save_data(db)
        return True
    return False

# ============================================================================
# Experience CRUD (Company, Role, Dates, Details)
# ============================================================================

def get_experience() -> List[Dict[str, Any]]:
    return load_data().get("experience", [])

def get_experience_by_id(exp_id: str) -> Optional[Dict[str, Any]]:
    for e in get_experience():
        if e.get("id") == exp_id:
            return e
    return None

def add_experience(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    db = load_data()
    points = data_dict.get("points", [])
    if isinstance(points, str):
        # Support split by newline or bullet or comma
        points = [p.strip().lstrip("•-▹* ") for p in points.replace("\r", "").split("\n") if p.strip()]

    new_exp = {
        "id": f"exp-{int(datetime.now().timestamp() * 1000)}",
        "company": data_dict.get("company", "").strip(),
        "role": data_dict.get("role", "").strip(),
        "location": data_dict.get("location", "").strip(),
        "period": data_dict.get("period", "").strip(),
        "badge": data_dict.get("badge", "Full-Time").strip(),
        "points": points
    }
    db.setdefault("experience", []).insert(0, new_exp)
    save_data(db)
    return new_exp

def update_experience(exp_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = load_data()
    experiences = db.get("experience", [])
    for i, e in enumerate(experiences):
        if e.get("id") == exp_id:
            if "company" in updates and updates["company"] is not None:
                e["company"] = updates["company"].strip()
            if "role" in updates and updates["role"] is not None:
                e["role"] = updates["role"].strip()
            if "location" in updates and updates["location"] is not None:
                e["location"] = updates["location"].strip()
            if "period" in updates and updates["period"] is not None:
                e["period"] = updates["period"].strip()
            if "badge" in updates and updates["badge"] is not None:
                e["badge"] = updates["badge"].strip()
            if "points" in updates and updates["points"] is not None:
                pts = updates["points"]
                if isinstance(pts, str):
                    e["points"] = [p.strip().lstrip("•-▹* ") for p in pts.replace("\r", "").split("\n") if p.strip()]
                else:
                    e["points"] = pts

            experiences[i] = e
            db["experience"] = experiences
            save_data(db)
            return e
    return None

def delete_experience(exp_id: str) -> bool:
    db = load_data()
    experiences = db.get("experience", [])
    filtered = [e for e in experiences if e.get("id") != exp_id]
    if len(filtered) != len(experiences):
        db["experience"] = filtered
        save_data(db)
        return True
    return False

# ============================================================================
# Education CRUD (Degree, Institution, Dates, Grade, Highlights)
# ============================================================================

def get_education() -> List[Dict[str, Any]]:
    return load_data().get("education", [])

def get_education_by_id(edu_id: str) -> Optional[Dict[str, Any]]:
    for ed in get_education():
        if ed.get("id") == edu_id:
            return ed
    return None

def add_education(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    db = load_data()
    new_edu = {
        "id": f"edu-{int(datetime.now().timestamp() * 1000)}",
        "degree": data_dict.get("degree", "").strip(),
        "institution": data_dict.get("institution", "").strip(),
        "location": data_dict.get("location", "").strip(),
        "period": data_dict.get("period", "").strip(),
        "grade": data_dict.get("grade", "").strip(),
        "highlights": data_dict.get("highlights", "").strip()
    }
    db.setdefault("education", []).insert(0, new_edu)
    save_data(db)
    return new_edu

def update_education(edu_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = load_data()
    educations = db.get("education", [])
    for i, ed in enumerate(educations):
        if ed.get("id") == edu_id:
            if "degree" in updates and updates["degree"] is not None:
                ed["degree"] = updates["degree"].strip()
            if "institution" in updates and updates["institution"] is not None:
                ed["institution"] = updates["institution"].strip()
            if "location" in updates and updates["location"] is not None:
                ed["location"] = updates["location"].strip()
            if "period" in updates and updates["period"] is not None:
                ed["period"] = updates["period"].strip()
            if "grade" in updates and updates["grade"] is not None:
                ed["grade"] = updates["grade"].strip()
            if "highlights" in updates and updates["highlights"] is not None:
                ed["highlights"] = updates["highlights"].strip()

            educations[i] = ed
            db["education"] = educations
            save_data(db)
            return ed
    return None

def delete_education(edu_id: str) -> bool:
    db = load_data()
    educations = db.get("education", [])
    filtered = [ed for ed in educations if ed.get("id") != edu_id]
    if len(filtered) != len(educations):
        db["education"] = filtered
        save_data(db)
        return True
    return False

# ============================================================================
# Skills Management (Compact, Single-Box List)
# ============================================================================

def get_skills() -> List[str]:
    raw_skills = load_data().get("skills", [])
    if isinstance(raw_skills, list):
        return raw_skills
    if isinstance(raw_skills, dict):
        # Flatten if old format was dict
        flat = []
        for cat, items in raw_skills.items():
            for it in items:
                flat.append(it.get("name") if isinstance(it, dict) else str(it))
        return flat
    return DEFAULT_DATA["skills"]

def update_skills(skills_list: List[str]) -> List[str]:
    db = load_data()
    clean_skills = [s.strip() for s in skills_list if s.strip()]
    db["skills"] = clean_skills
    save_data(db)
    return clean_skills

# ============================================================================
# Profile CRUD
# ============================================================================

def get_profile() -> Dict[str, Any]:
    return load_data().get("profile", {})

def update_profile(updates: Dict[str, Any]) -> Dict[str, Any]:
    db = load_data()
    profile = db.get("profile", {})
    profile.update(updates)
    db["profile"] = profile
    save_data(db)
    return profile

# ============================================================================
# Messages CRUD
# ============================================================================

def add_message(name: str, email: str, subject: str, message: str) -> Dict[str, Any]:
    db = load_data()
    new_msg = {
        "id": f"msg-{int(datetime.now().timestamp() * 1000)}",
        "name": name.strip(),
        "email": email.strip(),
        "subject": subject.strip() if subject else "General Inquiry",
        "message": message.strip(),
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "read": False
    }
    db.setdefault("messages", []).insert(0, new_msg)
    save_data(db)
    return new_msg

def get_messages() -> List[Dict[str, Any]]:
    return load_data().get("messages", [])

def toggle_message_read(msg_id: str) -> bool:
    db = load_data()
    for m in db.get("messages", []):
        if m.get("id") == msg_id:
            m["read"] = not m.get("read", False)
            save_data(db)
            return True
    return False

def delete_message(msg_id: str) -> bool:
    db = load_data()
    msgs = db.get("messages", [])
    filtered = [m for m in msgs if m.get("id") != msg_id]
    if len(filtered) != len(msgs):
        db["messages"] = filtered
        save_data(db)
        return True
    return False
