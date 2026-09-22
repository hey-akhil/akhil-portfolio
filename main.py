#!/usr/bin/env python3
"""
AutomateX - Akhil Pandey Portfolio & Full Admin CMS
FastAPI Web Application (Run with: uvicorn main:app --reload --port 8000)
"""

import os
import sys
import time
import shutil
import threading
import webbrowser
from typing import Dict, Any, Optional, List

import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
from models import (
    ProjectCreate, ProjectUpdate, 
    ExperienceCreate, ExperienceUpdate,
    EducationCreate, EducationUpdate,
    SkillsUpdate, ContactCreate, 
    AdminLogin, ProfileUpdate
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
RESUME_PDF_PATH = os.path.join(UPLOADS_DIR, "resume.pdf")
DATA_FILE = os.path.join(BASE_DIR, "data", "portfolio.json")

os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize FastAPI App
app = FastAPI(
    title="AutomateX | Python & FastAPI Engineering by Akhil Pandey",
    description="FastAPI application powering AutomateX developer portfolio, full Admin CMS, and PDF resume viewer.",
    version="3.5.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount Static Files & Templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Auth helper
def is_admin(request: Request) -> bool:
    token = request.cookies.get("admin_session")
    return token == "authenticated_akhil"

# ============================================================================
# Front-end HTML Routes
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Renders the main executive portfolio page."""
    db = database.load_data()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": db.get("profile", {}),
            "services": db.get("services", []),
            "projects": db.get("projects", []),
            "skills": database.get_skills(),
            "active_page": "home"
        }
    )

@app.get("/experience", response_class=HTMLResponse)
async def experience_page(request: Request):
    """Renders the dedicated Work Experience page."""
    db = database.load_data()
    return templates.TemplateResponse(
        request=request,
        name="experience.html",
        context={
            "profile": db.get("profile", {}),
            "experience": db.get("experience", []),
            "skills": database.get_skills(),
            "active_page": "experience"
        }
    )

@app.get("/education", response_class=HTMLResponse)
async def education_page(request: Request):
    """Renders the dedicated Academic Background page."""
    db = database.load_data()
    return templates.TemplateResponse(
        request=request,
        name="education.html",
        context={
            "profile": db.get("profile", {}),
            "education": db.get("education", []),
            "achievements": db.get("achievements", []),
            "skills": database.get_skills(),
            "active_page": "education"
        }
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Renders the Admin CMS dashboard."""
    db = database.load_data()
    authenticated = is_admin(request)
    resume_exists = os.path.exists(RESUME_PDF_PATH)
    resume_size_kb = round(os.path.getsize(RESUME_PDF_PATH) / 1024, 1) if resume_exists else 0

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "profile": db.get("profile", {}),
            "projects": db.get("projects", []),
            "experience": db.get("experience", []),
            "education": db.get("education", []),
            "skills": database.get_skills(),
            "messages": db.get("messages", []),
            "authenticated": authenticated,
            "resume_exists": resume_exists,
            "resume_size_kb": resume_size_kb
        }
    )

# ============================================================================
# PDF Resume Routes (Upload & Public Viewer)
# ============================================================================

@app.get("/resume")
async def view_resume():
    """Serves the PDF resume directly in browser viewer."""
    if os.path.exists(RESUME_PDF_PATH):
        return FileResponse(
            path=RESUME_PDF_PATH,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=Akhil_Pandey_Resume.pdf"}
        )
    raise HTTPException(status_code=404, detail="Resume PDF not found. Please upload from Admin.")

@app.post("/api/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Uploads a PDF resume from Admin panel."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        with open(RESUME_PDF_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ensure resume_url in profile points to /resume
        database.update_profile({"resume_url": "/resume"})

        return {
            "success": True,
            "message": "Resume PDF uploaded successfully!",
            "url": "/resume",
            "size_kb": round(os.path.getsize(RESUME_PDF_PATH) / 1024, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {str(e)}")

# ============================================================================
# Authentication API
# ============================================================================

@app.post("/api/admin/login")
async def admin_login(body: AdminLogin, response: Response):
    """Verifies Admin PIN and issues session cookie."""
    profile = database.get_profile()
    correct_pin = profile.get("admin_pin", "akhil123")

    if body.pin == correct_pin:
        response.set_cookie(
            key="admin_session",
            value="authenticated_akhil",
            httponly=True,
            samesite="lax",
            max_age=3600 * 24 * 7
        )
        return {"success": True, "message": "Admin session authenticated."}
    
    raise HTTPException(status_code=401, detail="Incorrect PIN! Default is akhil123")

@app.post("/api/admin/logout")
async def admin_logout(response: Response):
    """Clears Admin session cookie."""
    response.delete_cookie("admin_session")
    return {"success": True, "message": "Logged out successfully."}

# ============================================================================
# Projects CRUD
# ============================================================================

@app.get("/api/projects")
async def list_projects():
    return database.get_projects()

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    p = database.get_project_by_id(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@app.post("/api/projects", status_code=status.HTTP_201_CREATED)
async def create_project(body: ProjectCreate):
    created = database.add_project(body.model_dump())
    return {"success": True, "project": created}

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, body: ProjectUpdate):
    updated = database.update_project(project_id, body.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "project": updated}

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    deleted = database.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "message": "Project deleted."}

# ============================================================================
# Experience CRUD (Company, Role, Dates, Details)
# ============================================================================

@app.get("/api/experience")
async def list_experience():
    return database.get_experience()

@app.get("/api/experience/{exp_id}")
async def get_single_experience(exp_id: str):
    exp = database.get_experience_by_id(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience record not found")
    return exp

@app.post("/api/experience", status_code=status.HTTP_201_CREATED)
async def create_experience(body: ExperienceCreate):
    created = database.add_experience(body.model_dump())
    return {"success": True, "experience": created}

@app.put("/api/experience/{exp_id}")
async def update_experience_item(exp_id: str, body: ExperienceUpdate):
    updated = database.update_experience(exp_id, body.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Experience record not found")
    return {"success": True, "experience": updated}

@app.delete("/api/experience/{exp_id}")
async def delete_experience_item(exp_id: str):
    deleted = database.delete_experience(exp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experience record not found")
    return {"success": True, "message": "Experience record deleted."}

# ============================================================================
# Education CRUD (Degree, Institution, Dates, Grade, Highlights)
# ============================================================================

@app.get("/api/education")
async def list_education():
    return database.get_education()

@app.get("/api/education/{edu_id}")
async def get_single_education(edu_id: str):
    edu = database.get_education_by_id(edu_id)
    if not edu:
        raise HTTPException(status_code=404, detail="Education record not found")
    return edu

@app.post("/api/education", status_code=status.HTTP_201_CREATED)
async def create_education(body: EducationCreate):
    created = database.add_education(body.model_dump())
    return {"success": True, "education": created}

@app.put("/api/education/{edu_id}")
async def update_education_item(edu_id: str, body: EducationUpdate):
    updated = database.update_education(edu_id, body.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Education record not found")
    return {"success": True, "education": updated}

@app.delete("/api/education/{edu_id}")
async def delete_education_item(edu_id: str):
    deleted = database.delete_education(edu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Education record not found")
    return {"success": True, "message": "Education record deleted."}

# ============================================================================
# Skills Management (Compact Single Box)
# ============================================================================

@app.get("/api/skills")
async def list_skills():
    return database.get_skills()

@app.post("/api/skills")
async def save_skills(body: SkillsUpdate):
    # Split by comma or newline
    skills_raw = body.skills_text.replace("\r", "").replace("\n", ",")
    skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
    updated = database.update_skills(skills_list)
    return {"success": True, "skills": updated}

# ============================================================================
# Profile & Backup APIs
# ============================================================================

@app.post("/api/profile")
async def update_profile(body: ProfileUpdate):
    updated = database.update_profile(body.model_dump())
    return {"success": True, "profile": updated}

@app.get("/api/export")
async def export_database():
    if os.path.exists(DATA_FILE):
        return FileResponse(
            path=DATA_FILE,
            filename="portfolio.json",
            media_type="application/json"
        )
    return database.load_data()

# ============================================================================
# Contact Messages & Inquiries APIs
# ============================================================================

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
async def submit_contact(body: ContactCreate):
    saved_msg = database.add_message(
        name=body.name,
        email=body.email,
        subject=body.subject or "General Inquiry",
        message=body.message
    )
    return {"success": True, "message_id": saved_msg["id"]}

@app.get("/api/messages")
async def list_messages():
    return database.get_messages()

@app.put("/api/messages/{message_id}/read")
async def toggle_read(message_id: str):
    success = database.toggle_message_read(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"success": True}

@app.delete("/api/messages/{message_id}")
async def delete_message(message_id: str):
    success = database.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"success": True}

# ============================================================================
# Runner
# ============================================================================

if __name__ == "__main__":
    preferred_port = int(os.environ.get("PORT", 8000))
    print("================================================================")
    print(f"  [+] Akhil Pandey Portfolio & Full Admin CMS")
    print(f"  [>] Live Portfolio : http://localhost:{preferred_port}")
    print(f"  [>] Resume Viewer  : http://localhost:{preferred_port}/resume")
    print(f"  [>] Admin CMS      : http://localhost:{preferred_port}/admin")
    print(f"  [>] Swagger Docs   : http://localhost:{preferred_port}/docs")
    print("================================================================")

    def open_browser():
        time.sleep(1.0)
        try:
            webbrowser.open(f"http://localhost:{preferred_port}")
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("main:app", host="0.0.0.0", port=preferred_port, reload=True)
