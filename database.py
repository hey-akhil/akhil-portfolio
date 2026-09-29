"""
AutomateX Database Manager (Neon Serverless PostgreSQL + Resilient Local JSON Fallback)
Supports full CRUD for Projects, Experience, Education, Skills, Profile, and Messages.
Zero 7-day inactivity pause: Neon automatically sleeps when idle and auto-wakes on demand.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "portfolio.json")

# PostgreSQL / Neon Database Connection
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, Json
    HAS_PSYCOPG2 = True
    if DATABASE_URL:
        print(f"[+] Neon Serverless PostgreSQL configured via DATABASE_URL")
except ImportError:
    HAS_PSYCOPG2 = False
    print("[!] Warning: psycopg2 not found. Operating on local JSON fallback.")

# In-Memory Cache for fast page response & instant wake-up
_CACHE_DATA: Optional[Dict[str, Any]] = None
_CACHE_TIMESTAMP: float = 0.0
CACHE_TTL: float = 15.0  # 15 seconds TTL

def invalidate_cache():
    """Invalidates the in-memory cache so updates reflect immediately."""
    global _CACHE_DATA, _CACHE_TIMESTAMP
    _CACHE_DATA = None
    _CACHE_TIMESTAMP = 0.0

# ============================================================================
# PostgreSQL Connection Management
# ============================================================================

def get_pg_connection():
    """Establishes a connection to Neon PostgreSQL with connection timeout."""
    if not DATABASE_URL or not HAS_PSYCOPG2:
        return None
    return psycopg2.connect(DATABASE_URL, connect_timeout=10)

@contextmanager
def pg_cursor(commit: bool = False):
    """Context manager yielding a RealDictCursor with auto-commit/rollback."""
    conn = None
    try:
        conn = get_pg_connection()
        if conn is None:
            raise ConnectionError("No DATABASE_URL configured or psycopg2 unavailable")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        yield cur
        if commit:
            conn.commit()
    except Exception as e:
        if conn and commit:
            try:
                conn.rollback()
            except Exception:
                pass
        raise e
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def _serialize_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Converts datetime objects in a database row to ISO strings."""
    if not row:
        return None
    res = dict(row)
    for k, v in res.items():
        if isinstance(v, datetime):
            res[k] = v.isoformat()
    return res

def _serialize_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Converts datetime objects across a list of database rows."""
    return [_serialize_row(r) for r in rows if r is not None]

# ============================================================================
# Default Fallback Dataset
# ============================================================================

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
    "projects": [],
    "experience": [],
    "education": [],
    "messages": []
}

# ============================================================================
# Local JSON File Operations (Resilient Local Dual-Sync & Offline Fallback)
# ============================================================================

def load_local_data() -> Dict[str, Any]:
    """Loads portfolio database from local JSON file with fallback defaults."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "profile" in data and "resume_url" not in data["profile"]:
                    data["profile"]["resume_url"] = "/resume"
                if "skills" not in data or isinstance(data.get("skills"), dict):
                    data["skills"] = DEFAULT_DATA["skills"]
                return data
        except Exception as e:
            print(f"[!] Warning reading local {DATA_FILE}: {e}. Using defaults.")

    save_local_data(DEFAULT_DATA)
    return DEFAULT_DATA

def save_local_data(data: Dict[str, Any]) -> bool:
    """Saves portfolio database to local JSON file for backup resilience."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[!] Error saving to {DATA_FILE}: {e}")
        return False

# ============================================================================
# Unified Portfolio Loader (NeonDB First + Resilient Fallback)
# ============================================================================

def load_data() -> Dict[str, Any]:
    """
    Unified loader for templates and routes.
    Executes a single pipeline query on Neon Serverless PostgreSQL.
    Caches result for 15s to keep navigation instant.
    Falls back gracefully to local JSON if database is cold-starting or offline.
    """
    global _CACHE_DATA, _CACHE_TIMESTAMP
    now = time.time()
    if _CACHE_DATA is not None and (now - _CACHE_TIMESTAMP) < CACHE_TTL:
        return _CACHE_DATA

    local = load_local_data()

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                # 1. Profile
                cur.execute("SELECT * FROM public.profile WHERE id=%s;", ("main",))
                prof_row = cur.fetchone()
                prof = _serialize_row(prof_row) if prof_row else {}

                # 2. Projects
                cur.execute("SELECT * FROM public.projects ORDER BY created_at DESC;")
                projects = _serialize_rows(cur.fetchall())

                # 3. Experience
                cur.execute("SELECT * FROM public.experience ORDER BY created_at DESC;")
                experience = _serialize_rows(cur.fetchall())

                # 4. Education
                cur.execute("SELECT * FROM public.education ORDER BY created_at ASC;")
                education = _serialize_rows(cur.fetchall())

                # 5. Skills
                cur.execute("SELECT name FROM public.skills ORDER BY id ASC;")
                skills = [r["name"] for r in cur.fetchall()]

                # 6. Messages
                cur.execute("SELECT * FROM public.messages ORDER BY created_at DESC;")
                messages = _serialize_rows(cur.fetchall())

                if prof and prof.get("name"):
                    if "resume_url" not in prof or not prof["resume_url"]:
                        prof["resume_url"] = "/resume"

                    data = {
                        "profile": prof,
                        "skills": skills if skills else local.get("skills", DEFAULT_DATA["skills"]),
                        "services": local.get("services", DEFAULT_DATA["services"]),
                        "projects": projects,
                        "experience": experience,
                        "education": education,
                        "messages": messages
                    }
                    _CACHE_DATA = data
                    _CACHE_TIMESTAMP = now
                    return data
        except Exception as e:
            print(f"[!] NeonDB load_data fallback notice: {e}")

    _CACHE_DATA = local
    _CACHE_TIMESTAMP = now
    return local

def save_data(data: Dict[str, Any]) -> bool:
    """Saves data locally."""
    invalidate_cache()
    return save_local_data(data)

# ============================================================================
# Projects CRUD
# ============================================================================

def get_projects() -> List[Dict[str, Any]]:
    """Fetches all projects from NeonDB or local storage."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.projects ORDER BY created_at DESC;")
                return _serialize_rows(cur.fetchall())
        except Exception as e:
            print(f"[!] NeonDB get_projects notice: {e}")
    return load_local_data().get("projects", [])

def get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    """Gets a project by its unique ID."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.projects WHERE id=%s;", (project_id,))
                row = cur.fetchone()
                if row:
                    return _serialize_row(row)
        except Exception as e:
            print(f"[!] NeonDB get_project_by_id notice: {e}")

    for p in load_local_data().get("projects", []):
        if p.get("id") == project_id:
            return p
    return None

def add_project(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Adds a new project to NeonDB and syncs with local storage."""
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

    # NeonDB Cloud write
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO public.projects (id, title, category, category_label, description, tech_stack, github_url, render_url, has_render, status, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    new_project["id"],
                    new_project["title"],
                    new_project["category"],
                    new_project["category_label"],
                    new_project["description"],
                    Json(new_project["tech_stack"]),
                    new_project["github_url"],
                    new_project["render_url"],
                    new_project["has_render"],
                    new_project["status"],
                    new_project["date"]
                ))
        except Exception as e:
            print(f"[!] NeonDB add_project notice: {e}")

    invalidate_cache()
    db = load_local_data()
    db.setdefault("projects", []).insert(0, new_project)
    save_local_data(db)
    return new_project

def update_project(project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Updates a project in NeonDB and local storage."""
    db = load_local_data()
    projects = db.get("projects", [])
    updated_obj = None

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
            save_local_data(db)
            updated_obj = p
            break

    if DATABASE_URL and HAS_PSYCOPG2 and updated_obj:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE public.projects SET
                        title = %s,
                        category = %s,
                        category_label = %s,
                        description = %s,
                        tech_stack = %s,
                        github_url = %s,
                        render_url = %s,
                        has_render = %s,
                        status = %s,
                        date = %s
                    WHERE id = %s;
                """, (
                    updated_obj.get("title"),
                    updated_obj.get("category"),
                    updated_obj.get("category_label"),
                    updated_obj.get("description"),
                    Json(updated_obj.get("tech_stack", [])),
                    updated_obj.get("github_url"),
                    updated_obj.get("render_url"),
                    updated_obj.get("has_render"),
                    updated_obj.get("status"),
                    updated_obj.get("date"),
                    project_id
                ))
        except Exception as e:
            print(f"[!] NeonDB update_project notice: {e}")

    invalidate_cache()
    return updated_obj

def delete_project(project_id: str) -> bool:
    """Deletes a project from NeonDB and local storage."""
    deleted = False

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("DELETE FROM public.projects WHERE id = %s;", (project_id,))
                deleted = True
        except Exception as e:
            print(f"[!] NeonDB delete_project notice: {e}")

    invalidate_cache()
    db = load_local_data()
    projects = db.get("projects", [])
    filtered = [p for p in projects if p.get("id") != project_id]
    if len(filtered) != len(projects):
        db["projects"] = filtered
        save_local_data(db)
        deleted = True

    return deleted

# ============================================================================
# Experience CRUD
# ============================================================================

def get_experience() -> List[Dict[str, Any]]:
    """Fetches work experience records from NeonDB or local storage."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.experience ORDER BY created_at DESC;")
                return _serialize_rows(cur.fetchall())
        except Exception as e:
            print(f"[!] NeonDB get_experience notice: {e}")
    return load_local_data().get("experience", [])

def get_experience_by_id(exp_id: str) -> Optional[Dict[str, Any]]:
    """Gets an experience record by ID."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.experience WHERE id=%s;", (exp_id,))
                row = cur.fetchone()
                if row:
                    return _serialize_row(row)
        except Exception as e:
            print(f"[!] NeonDB get_experience_by_id notice: {e}")

    for e in load_local_data().get("experience", []):
        if e.get("id") == exp_id:
            return e
    return None

def add_experience(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Adds a work experience item to NeonDB and local storage."""
    points = data_dict.get("points", [])
    if isinstance(points, str):
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

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO public.experience (id, company, role, location, period, badge, points)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    new_exp["id"],
                    new_exp["company"],
                    new_exp["role"],
                    new_exp["location"],
                    new_exp["period"],
                    new_exp["badge"],
                    Json(new_exp["points"])
                ))
        except Exception as e:
            print(f"[!] NeonDB add_experience notice: {e}")

    invalidate_cache()
    db = load_local_data()
    db.setdefault("experience", []).insert(0, new_exp)
    save_local_data(db)
    return new_exp

def update_experience(exp_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Updates a work experience item in NeonDB and local storage."""
    db = load_local_data()
    experiences = db.get("experience", [])
    updated_obj = None

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
            save_local_data(db)
            updated_obj = e
            break

    if DATABASE_URL and HAS_PSYCOPG2 and updated_obj:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE public.experience SET
                        company = %s,
                        role = %s,
                        location = %s,
                        period = %s,
                        badge = %s,
                        points = %s
                    WHERE id = %s;
                """, (
                    updated_obj.get("company"),
                    updated_obj.get("role"),
                    updated_obj.get("location"),
                    updated_obj.get("period"),
                    updated_obj.get("badge"),
                    Json(updated_obj.get("points", [])),
                    exp_id
                ))
        except Exception as e:
            print(f"[!] NeonDB update_experience notice: {e}")

    invalidate_cache()
    return updated_obj

def delete_experience(exp_id: str) -> bool:
    """Deletes an experience record from NeonDB and local storage."""
    deleted = False

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("DELETE FROM public.experience WHERE id = %s;", (exp_id,))
                deleted = True
        except Exception as e:
            print(f"[!] NeonDB delete_experience notice: {e}")

    invalidate_cache()
    db = load_local_data()
    experiences = db.get("experience", [])
    filtered = [e for e in experiences if e.get("id") != exp_id]
    if len(filtered) != len(experiences):
        db["experience"] = filtered
        save_local_data(db)
        deleted = True

    return deleted

# ============================================================================
# Education CRUD
# ============================================================================

def get_education() -> List[Dict[str, Any]]:
    """Fetches education items from NeonDB or local storage."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.education ORDER BY created_at ASC;")
                return _serialize_rows(cur.fetchall())
        except Exception as e:
            print(f"[!] NeonDB get_education notice: {e}")
    return load_local_data().get("education", [])

def get_education_by_id(edu_id: str) -> Optional[Dict[str, Any]]:
    """Gets an education record by ID."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.education WHERE id=%s;", (edu_id,))
                row = cur.fetchone()
                if row:
                    return _serialize_row(row)
        except Exception as e:
            print(f"[!] NeonDB get_education_by_id notice: {e}")

    for ed in load_local_data().get("education", []):
        if ed.get("id") == edu_id:
            return ed
    return None

def add_education(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Adds an education record to NeonDB and local storage."""
    new_edu = {
        "id": f"edu-{int(datetime.now().timestamp() * 1000)}",
        "degree": data_dict.get("degree", "").strip(),
        "institution": data_dict.get("institution", "").strip(),
        "location": data_dict.get("location", "").strip(),
        "period": data_dict.get("period", "").strip(),
        "grade": data_dict.get("grade", "").strip(),
        "highlights": data_dict.get("highlights", "").strip()
    }

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO public.education (id, degree, institution, location, period, grade, highlights)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    new_edu["id"],
                    new_edu["degree"],
                    new_edu["institution"],
                    new_edu["location"],
                    new_edu["period"],
                    new_edu["grade"],
                    new_edu["highlights"]
                ))
        except Exception as e:
            print(f"[!] NeonDB add_education notice: {e}")

    invalidate_cache()
    db = load_local_data()
    db.setdefault("education", []).insert(0, new_edu)
    save_local_data(db)
    return new_edu

def update_education(edu_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Updates an education record in NeonDB and local storage."""
    db = load_local_data()
    educations = db.get("education", [])
    updated_obj = None

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
            save_local_data(db)
            updated_obj = ed
            break

    if DATABASE_URL and HAS_PSYCOPG2 and updated_obj:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE public.education SET
                        degree = %s,
                        institution = %s,
                        location = %s,
                        period = %s,
                        grade = %s,
                        highlights = %s
                    WHERE id = %s;
                """, (
                    updated_obj.get("degree"),
                    updated_obj.get("institution"),
                    updated_obj.get("location"),
                    updated_obj.get("period"),
                    updated_obj.get("grade"),
                    updated_obj.get("highlights"),
                    edu_id
                ))
        except Exception as e:
            print(f"[!] NeonDB update_education notice: {e}")

    invalidate_cache()
    return updated_obj

def delete_education(edu_id: str) -> bool:
    """Deletes an education record from NeonDB and local storage."""
    deleted = False

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("DELETE FROM public.education WHERE id = %s;", (edu_id,))
                deleted = True
        except Exception as e:
            print(f"[!] NeonDB delete_education notice: {e}")

    invalidate_cache()
    db = load_local_data()
    educations = db.get("education", [])
    filtered = [ed for ed in educations if ed.get("id") != edu_id]
    if len(filtered) != len(educations):
        db["education"] = filtered
        save_local_data(db)
        deleted = True

    return deleted

# ============================================================================
# Skills Management
# ============================================================================

def get_skills() -> List[str]:
    """Fetches list of skills from NeonDB or local storage."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT name FROM public.skills ORDER BY id ASC;")
                skill_names = [r["name"] for r in cur.fetchall() if r.get("name")]
                if skill_names:
                    return skill_names
        except Exception as e:
            print(f"[!] NeonDB get_skills notice: {e}")

    raw_skills = load_local_data().get("skills", [])
    if isinstance(raw_skills, list):
        return raw_skills
    if isinstance(raw_skills, dict):
        flat = []
        for cat, items in raw_skills.items():
            for it in items:
                flat.append(it.get("name") if isinstance(it, dict) else str(it))
        return flat
    return DEFAULT_DATA["skills"]

def update_skills(skills_list: List[str]) -> List[str]:
    """Updates skills list in NeonDB and local storage."""
    clean_skills = [s.strip() for s in skills_list if s.strip()]

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("DELETE FROM public.skills;")
                if clean_skills:
                    for s in clean_skills:
                        cur.execute("INSERT INTO public.skills (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (s,))
        except Exception as e:
            print(f"[!] NeonDB skills sync notice: {e}")

    invalidate_cache()
    db = load_local_data()
    db["skills"] = clean_skills
    save_local_data(db)
    return clean_skills

# ============================================================================
# Profile CRUD
# ============================================================================

def get_profile() -> Dict[str, Any]:
    """Fetches user profile from NeonDB with fallback to local JSON."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.profile WHERE id=%s;", ("main",))
                row = cur.fetchone()
                if row:
                    prof = _serialize_row(row)
                    if "resume_url" not in prof or not prof["resume_url"]:
                        prof["resume_url"] = "/resume"
                    return prof
        except Exception as e:
            print(f"[!] NeonDB get_profile notice: {e}")

    return load_local_data().get("profile", DEFAULT_DATA["profile"])

def update_profile(updates: Dict[str, Any]) -> Dict[str, Any]:
    """Updates profile in NeonDB and local storage."""
    db = load_local_data()
    profile = db.get("profile", {})
    profile.update(updates)
    db["profile"] = profile
    save_local_data(db)

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            allowed_cols = [
                "name", "brand", "role_title", "tagline", "short_bio", 
                "about", "email", "phone", "location", "github", 
                "linkedin", "admin_pin", "status_badge", "resume_url"
            ]
            set_parts = []
            values = []

            for col in allowed_cols:
                if col in updates and updates[col] is not None:
                    set_parts.append(f"{col} = %s")
                    values.append(updates[col])

            if "stats" in updates and updates["stats"] is not None:
                set_parts.append("stats = %s")
                values.append(Json(updates["stats"]))

            if set_parts:
                with pg_cursor(commit=True) as cur:
                    values.append("main")
                    sql = f"UPDATE public.profile SET {', '.join(set_parts)}, updated_at = NOW() WHERE id = %s;"
                    cur.execute(sql, tuple(values))
        except Exception as e:
            print(f"[!] NeonDB update_profile notice: {e}")

    invalidate_cache()
    return profile

# ============================================================================
# Messages CRUD
# ============================================================================

def add_message(name: str, email: str, subject: str, message: str) -> Dict[str, Any]:
    """Saves a client message to NeonDB and local storage."""
    new_msg = {
        "id": f"msg-{int(datetime.now().timestamp() * 1000)}",
        "name": name.strip(),
        "email": email.strip(),
        "subject": subject.strip() if subject else "General Inquiry",
        "message": message.strip(),
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "read": False
    }

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO public.messages (id, name, email, subject, message, date, read)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    new_msg["id"],
                    new_msg["name"],
                    new_msg["email"],
                    new_msg["subject"],
                    new_msg["message"],
                    new_msg["date"],
                    new_msg["read"]
                ))
        except Exception as e:
            print(f"[!] NeonDB add_message notice: {e}")

    invalidate_cache()
    db = load_local_data()
    db.setdefault("messages", []).insert(0, new_msg)
    save_local_data(db)
    return new_msg

def get_messages() -> List[Dict[str, Any]]:
    """Fetches all client inquiries from NeonDB or local storage."""
    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor() as cur:
                cur.execute("SELECT * FROM public.messages ORDER BY created_at DESC;")
                return _serialize_rows(cur.fetchall())
        except Exception as e:
            print(f"[!] NeonDB get_messages notice: {e}")
    return load_local_data().get("messages", [])

def toggle_message_read(msg_id: str) -> bool:
    """Toggles read state of a message in NeonDB and local storage."""
    db = load_local_data()
    found = False
    new_read_val = False

    for m in db.get("messages", []):
        if m.get("id") == msg_id:
            m["read"] = not m.get("read", False)
            new_read_val = m["read"]
            save_local_data(db)
            found = True
            break

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("UPDATE public.messages SET read = NOT read WHERE id = %s RETURNING read;", (msg_id,))
                row = cur.fetchone()
                if row is not None:
                    found = True
        except Exception as e:
            print(f"[!] NeonDB toggle_message_read notice: {e}")

    invalidate_cache()
    return found

def delete_message(msg_id: str) -> bool:
    """Deletes a message from NeonDB and local storage."""
    deleted = False

    if DATABASE_URL and HAS_PSYCOPG2:
        try:
            with pg_cursor(commit=True) as cur:
                cur.execute("DELETE FROM public.messages WHERE id = %s;", (msg_id,))
                deleted = True
        except Exception as e:
            print(f"[!] NeonDB delete_message notice: {e}")

    invalidate_cache()
    db = load_local_data()
    msgs = db.get("messages", [])
    filtered = [m for m in msgs if m.get("id") != msg_id]
    if len(filtered) != len(msgs):
        db["messages"] = filtered
        save_local_data(db)
        deleted = True

    return deleted

# ============================================================================
# Health Check / Monitoring
# ============================================================================

def check_health() -> Dict[str, Any]:
    """Checks Neon PostgreSQL connectivity and response latency."""
    if not DATABASE_URL or not HAS_PSYCOPG2:
        return {
            "status": "degraded",
            "backend": "local_json",
            "reason": "DATABASE_URL not configured or psycopg2 not installed"
        }
    try:
        t0 = time.time()
        with pg_cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        latency_ms = round((time.time() - t0) * 1000, 1)
        return {
            "status": "healthy",
            "backend": "Neon Serverless PostgreSQL",
            "latency_ms": latency_ms,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "backend": "local_json_fallback",
            "error": str(e)
        }
