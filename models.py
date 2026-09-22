"""
Pydantic Data Models for Akhil Pandey's FastAPI Portfolio & Full Admin CMS
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class StatItem(BaseModel):
    label: str
    value: str

class Profile(BaseModel):
    name: str = "Akhil Pandey"
    brand: str = "AutomateX"
    role_title: str = "Software Developer & Automation Specialist"
    tagline: str = "Software Developer | Python & FastAPI | Workflow Automation"
    short_bio: str = "MCA graduate from Nirma University with 2+ years of professional IT experience building scalable backend APIs, custom CRM systems, and automated business workflows."
    about: str = "I am a backend-focused Software Developer with hands-on expertise in Python, FastAPI, Django, and automated workflow pipelines (n8n, Zapier, Make.com). I help businesses and clients streamline operations, eliminate repetitive manual data entry, and deploy robust, live applications on Render and Cloud platforms."
    email: str = "akhil.pandeyy1@gmail.com"
    phone: str = "+91 76003 47544"
    location: str = "Navsari, Gujarat, India - 396445"
    github: str = "https://github.com/akhiil1"
    linkedin: str = "https://linkedin.com/in/akhiil1"
    admin_pin: str = "akhil123"
    status_badge: str = "Available for Full-Time & Freelance Projects"
    resume_url: str = "/resume"

class ProfileUpdate(BaseModel):
    name: str
    brand: Optional[str] = "AutomateX"
    role_title: str
    tagline: str
    about: str
    email: str
    phone: str
    location: str
    github: str
    linkedin: str
    status_badge: str
    admin_pin: str

# --- Projects ---
class Project(BaseModel):
    id: str
    title: str
    category: str = "backend"
    category_label: str = "Backend & APIs"
    description: str
    tech_stack: List[str] = []
    github_url: Optional[str] = ""
    render_url: Optional[str] = ""
    has_render: bool = False
    status: str = "GitHub Repo"
    date: str = "2025"

class ProjectCreate(BaseModel):
    title: str
    category: str = "backend"
    category_label: Optional[str] = "Backend & APIs"
    description: str
    tech_stack: str = ""
    github_url: Optional[str] = ""
    render_url: Optional[str] = ""
    has_render: Optional[bool] = False

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    category_label: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_url: Optional[str] = None
    render_url: Optional[str] = None
    has_render: Optional[bool] = None

# --- Experience ---
class ExperienceCreate(BaseModel):
    company: str
    role: str
    location: str
    period: str
    badge: Optional[str] = "Full-Time"
    points: str = ""  # Multi-line or comma-separated bullet points

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    period: Optional[str] = None
    badge: Optional[str] = None
    points: Optional[str] = None

# --- Education ---
class EducationCreate(BaseModel):
    degree: str
    institution: str
    location: str
    period: str
    grade: str
    highlights: Optional[str] = ""

class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    period: Optional[str] = None
    grade: Optional[str] = None
    highlights: Optional[str] = None

# --- Skills ---
class SkillsUpdate(BaseModel):
    skills_text: str  # Comma-separated or line-separated list of skills

# --- Messages & Auth ---
class ContactCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = "General Inquiry"
    message: str

class AdminLogin(BaseModel):
    pin: str
