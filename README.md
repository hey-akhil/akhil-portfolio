# ⚡ Akhil Pandey - Python & FastAPI Portfolio with Full Admin CMS

> **Production-Grade FastAPI Web Application & Developer CMS**  
> Engineered with **FastAPI**, **Pydantic**, **Jinja2 Templates**, **Uvicorn**, and **Vanilla CSS** with seamless Render Cloud deployment.

---

## 🌟 Key Features

1. **Complete Admin CMS Control (`/admin`)**:
   - **PIN-Protected Authentication**: Default PIN is **`akhil123`** (can be updated anytime from the Profile tab).
   - **Everything is Editable**: Modify company names, roles, employment dates, responsibilities, degree titles, universities, percentages/grades, honors, skills, projects, and personal bio.
   - **Separate Sections**: Work Experience and Education are completely separated in the database, API, Admin dashboard, and frontend display.

2. **Compact Single-Box Skillset**:
   - Clean, unified skillset view—no excessive progress bars.
   - Skills can be edited in one textarea as comma-separated or newline values, rendering as stylish glowing chips.

3. **PDF Resume Viewer & Uploader**:
   - **Browser PDF Viewer**: Accessible publicly at **`/resume`** (e.g., `http://localhost:8000/resume`).
   - **Backend Upload**: Admin can upload any updated `.pdf` resume directly from the Admin CMS (`📄 Resume PDF` tab) with instant server-side replacement.

4. **Projects Showcase (Render Live & GitHub Repos)**:
   - Supports both **Live on Render** demo URLs (with a pulsing 🚀 "Live Demo" badge) and open-source **GitHub Repo** links.
   - If a project doesn't have a Render URL, it cleanly falls back to "📦 GitHub Only".

5. **Client Inquiries & Live Ping**:
   - Working contact form sending inquiries directly to the backend database.
   - Interactive live API latency ping button demonstrating FastAPI's speed (10–20ms response time).

---

## 🚀 How to Run Locally

### 1-Click Launcher (Windows)
Double-click:
👉 **`start.bat`**

This will automatically launch Uvicorn with hot-reload and open your browser:
- **Live Portfolio**: `http://localhost:8000`
- **PDF Resume Viewer**: `http://localhost:8000/resume`
- **Admin CMS Dashboard**: `http://localhost:8000/admin` *(Default PIN: `akhil123`)*
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

### Manual Terminal Command
```bash
python -m uvicorn main:app --reload --port 8000
```

---

## ☁️ Deploying on Render Cloud

1. Push this directory to your GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Deploy FastAPI Portfolio with Full Admin CMS"
   git branch -M main
   git remote add origin https://github.com/akhiil1/akhil-portfolio.git
   git push -u origin main
   ```
2. Log into [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **Web Service**.
3. Select your repository `akhil-portfolio`.
4. Render will automatically detect `render.yaml` or use:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy Web Service**!

---

## 📁 Clean File Structure

```
d:\akhil-portfolio\
├── main.py                    # FastAPI Application & Uvicorn runner
├── models.py                  # Pydantic Schemas (Experience, Education, Skills, Profile, Projects)
├── database.py                # Persistent JSON Database Manager & CRUD
├── start.bat                  # 1-Click Windows Launcher (uvicorn main:app --reload)
├── requirements.txt           # Dependencies (fastapi, uvicorn, jinja2, pydantic, python-multipart)
├── Procfile                   # Process declaration for Render
├── render.yaml                # Render deployment blueprint
├── README.md                  # Documentation
├── data/
│   └── portfolio.json         # Master JSON Database
├── templates/
│   ├── index.html             # Client-facing Portfolio Template
│   └── admin.html             # Full Admin CMS Dashboard Template
└── static/
    ├── css/
    │   ├── style.css          # Modern dark zinc/emerald design system
    │   └── admin.css          # Admin CMS layout & modal styling
    ├── js/
    │   ├── main.js            # Frontend filters, search, ping, contact form
    │   └── admin.js           # Admin CMS CRUD controllers & PDF upload
    └── uploads/
        └── resume.pdf         # Uploaded PDF Resume served at /resume
```
