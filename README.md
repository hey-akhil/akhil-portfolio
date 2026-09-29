# ⚡ AutomateX — Full-Stack Python & FastAPI Portfolio CMS

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon_Serverless-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![Render](https://img.shields.io/badge/Render-Cloud_Deploy-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com)
[![Uvicorn](https://img.shields.io/badge/ASGI-Uvicorn-2C3E50?style=for-the-badge&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)

**A high-performance, asynchronous developer portfolio & full Admin CMS powered by FastAPI, Neon Serverless PostgreSQL, and Jinja2.**

[Live Demo](https://akhil-portfolio.onrender.com) • [API Documentation](https://akhil-portfolio.onrender.com/docs) • [Resume Viewer](https://akhil-portfolio.onrender.com/resume)

</div>

---

## 📌 Executive Overview

**AutomateX** is an enterprise-grade personal portfolio and content management system engineered for backend software engineers and automation specialists. It combines asynchronous Python API architecture with a serverless PostgreSQL database to deliver sub-millisecond page delivery, zero maintenance overhead, and real-time administrative controls.

---

## 🌟 Key Architecture & Capabilities

### 1. 🐘 Neon Serverless PostgreSQL Backend
- **Zero 7-Day Inactivity Shutdown**: Built on Neon's autoscaling serverless PostgreSQL architecture. Automatically scales to zero when idle and auto-wakes instantly (<1s) upon visitor requests.
- **Single-Pipeline Multi-Query Loader**: Fetches profile, skills, projects, work experience, education, and client inquiries within a single database round-trip for optimal performance.
- **Resilient Dual-Sync Storage**: Writes asynchronously to Neon Cloud PostgreSQL while maintaining an automatic local JSON snapshot (`data/portfolio.json`) for seamless zero-downtime offline fallback.

### 2. 🛡️ Secure Admin CMS Dashboard (`/admin`)
- **PIN-Protected Session Authentication**: Secure access token validation with cookie-based session persistence (Default PIN: `akhil123`, customizable via Profile settings).
- **Full In-Place CRUD**: Real-time management of Projects, Work Experience, Academic Background, Glowing Skillset Chips, and Bio/Contact details.
- **Client Inquiry Inbox**: Contact form submissions are recorded in PostgreSQL with mark-as-read and delete capabilities.

### 3. 📄 Integrated PDF Resume Engine (`/resume`)
- **Direct Browser Viewer**: Embedded, high-fidelity PDF viewer served at `/resume`.
- **Admin File Uploader**: Instant server-side resume PDF replacement directly through the Admin CMS interface with validation.

### 4. 🚀 Projects Showcase & Micro-Interactions
- Direct support for **Render Cloud Live Demos** (pulsing badge) and open-source **GitHub Repositories**.
- Dynamic category filters: *Backend & APIs*, *Workflow Automation*, *Microservices*, and *AI Document Extraction*.
- Interactive API latency benchmark button demonstrating live round-trip backend speeds (10–25ms).

### 5. 🩺 Real-Time System Healthcheck (`/api/health`)
- Live health monitoring endpoint reporting database connectivity, engine type (`Neon Serverless PostgreSQL`), and exact query round-trip latency in milliseconds.

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Asynchronous routing, OpenAPI / Swagger generation |
| **Runtime & Server** | [Python 3.11+](https://www.python.org/) & [Uvicorn](https://www.uvicorn.org/) | High-concurrency ASGI production server |
| **Database** | [Neon Serverless Postgres](https://neon.tech/) | Native PostgreSQL with connection pooling & auto-wake |
| **DB Driver** | [psycopg2-binary](https://www.psycopg.org/) | High-performance PostgreSQL client with JSONB support |
| **Templating** | [Jinja2](https://palletsprojects.com/p/jinja/) | Server-Side Rendered (SSR) components & clean HTML5 |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict request payload validation and serialization |
| **Deployment** | [Render Cloud](https://render.com/) | Continuous Deployment directly connected to GitHub |

---

## ⚡ Quick Start & Local Execution

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/hey-akhil/akhil-portfolio.git
cd akhil-portfolio
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Neon Serverless PostgreSQL Connection String
DATABASE_URL=postgresql://<username>:<password>@<neon-host>/<database>?sslmode=require&channel_binding=require
```
*(If no `DATABASE_URL` is supplied, the application automatically falls back to `data/portfolio.json` for offline development).*

### 4. Launch Application

**Windows (1-Click Launcher):**
Double-click `start.bat`

**Terminal Command:**
```bash
python -m uvicorn main:app --reload --port 8000
```

Access the local services:
- **Portfolio Interface**: [http://localhost:8000](http://localhost:8000)
- **Work Experience**: [http://localhost:8000/experience](http://localhost:8000/experience)
- **Academic Background**: [http://localhost:8000/education](http://localhost:8000/education)
- **PDF Resume Viewer**: [http://localhost:8000/resume](http://localhost:8000/resume)
- **Admin CMS Dashboard**: [http://localhost:8000/admin](http://localhost:8000/admin) *(PIN: `akhil123`)*
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Healthcheck Endpoint**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 🌐 Cloud Deployment (Render)

This repository includes continuous deployment configurations ready for **Render**:

1. Create a **New Web Service** connected to your GitHub repository.
2. Configure settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. In **Environment Variables**, set:
   ```
   DATABASE_URL = <your-neon-postgres-connection-string>
   PYTHON_VERSION = 3.11.0
   ```
4. Click **Deploy Web Service**.

---

## 📂 Project Structure

```
akhil-portfolio/
├── main.py                    # Application entrypoint & ASGI router
├── models.py                  # Pydantic schemas for data validation
├── database.py                # Neon Serverless PostgreSQL manager & local JSON fallback
├── supabase_schema.sql        # Standard PostgreSQL DDL schema & seed records
├── requirements.txt           # Production dependencies
├── render.yaml                # Render Cloud blueprint
├── Procfile                   # Process declarations
├── start.bat                  # Local 1-click Windows development script
├── README.md                  # Comprehensive project documentation
├── data/
│   └── portfolio.json         # Offline JSON dual-sync storage & backup
├── templates/
│   ├── index.html             # Main executive landing page
│   ├── experience.html        # Professional work experience template
│   ├── education.html         # Academic qualifications template
│   └── admin.html             # Full Administrative CMS interface
└── static/
    ├── css/
    │   ├── style.css          # Executive zinc & emerald design system
    │   └── admin.css          # Admin CMS management styles
    ├── js/
    │   ├── main.js            # Client-side reactivity, search & ping
    │   └── admin.js           # Admin CMS CRUD API handlers
    └── uploads/
        └── resume.pdf         # Dynamic PDF resume storage
```

---

## 📡 RESTful API Overview

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/health` | Service health & PostgreSQL response latency | No |
| `GET` | `/api/projects` | List all portfolio projects | No |
| `POST` | `/api/projects` | Create a new project | Admin PIN |
| `PUT` | `/api/projects/{id}` | Update existing project details | Admin PIN |
| `DELETE` | `/api/projects/{id}` | Delete a project | Admin PIN |
| `GET` | `/api/experience` | Fetch work experience timeline | No |
| `POST` | `/api/experience` | Add new work experience entry | Admin PIN |
| `GET` | `/api/education` | Fetch academic credentials | No |
| `POST` | `/api/education` | Add new education record | Admin PIN |
| `GET` | `/api/skills` | Retrieve technical skillset chips | No |
| `POST` | `/api/skills` | Batch update skillset items | Admin PIN |
| `POST` | `/api/contact` | Submit client inquiry message | No |
| `GET` | `/api/messages` | View all client inquiries | Admin PIN |
| `POST` | `/api/resume/upload` | Upload & replace PDF resume | Admin PIN |

Interactive visual API documentation is accessible at [`/docs`](http://localhost:8000/docs).

---

## 👨‍💻 Developer & Maintainer

**Akhil Pandey**  
*Software Developer & Workflow Automation Specialist*  
- **Email:** [akhil.pandeyy1@gmail.com](mailto:akhil.pandeyy1@gmail.com)  
- **LinkedIn:** [linkedin.com/in/akhiil1](https://linkedin.com/in/akhiil1)  
- **GitHub:** [github.com/akhiil1](https://github.com/akhiil1)  
- **Location:** Navsari, Gujarat, India
