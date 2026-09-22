# ⚡ AutomateX - Python & FastAPI Portfolio with Full Admin CMS & Supabase

> **Production-Grade FastAPI Web Application, Supabase Cloud Database & Developer CMS**  
> Engineered by **Akhil Pandey** with **FastAPI**, **Supabase Cloud (PostgreSQL)**, **Pydantic**, **Jinja2 Templates**, **Uvicorn**, and **Vanilla CSS** with seamless Render Cloud deployment.

---

## 🌟 Key Features

1. **Supabase Cloud Database + Resilient JSON Fallback**:
   - Connected directly to Supabase cloud PostgreSQL with real-time CRUD.
   - Dual-mode architecture: seamlessly reads/writes to Supabase, with automatic zero-downtime fallback to local storage if offline or tables are pending.
   - Includes complete `supabase_schema.sql` DDL script pre-seeded with all portfolio records and Row Level Security (RLS) policies.

2. **Complete Admin CMS Control (`/admin`)**:
   - **PIN-Protected Authentication**: Default PIN is **`akhil123`** (can be updated anytime from the Profile tab).
   - **Everything is Editable**: Modify company names, roles, employment dates, responsibilities, degree titles, universities, percentages/grades, honors, skills, projects, and personal bio.
   - **Dedicated Multi-Page Architecture**: Home (`/`), Work Experience (`/experience`), and Academic Background (`/education`) have dedicated, high-performance pages.

3. **Compact Single-Box Skillset**:
   - Clean, unified skillset view—no unnecessary progress bars.
   - Skills can be edited in one textarea as comma-separated or newline values, rendering as stylish glowing chips.

4. **PDF Resume Viewer & Uploader**:
   - **Browser PDF Viewer**: Accessible publicly at **`/resume`** (e.g., `http://localhost:8000/resume`).
   - **Backend Upload**: Admin can upload any updated `.pdf` resume directly from the Admin CMS (`📄 Resume PDF` tab) with instant server-side replacement.

5. **Projects Showcase (Render Live & GitHub Repos)**:
   - Supports both **Live on Render** demo URLs (with a pulsing 🚀 "Live Demo" badge) and open-source **GitHub Repo** links.
   - If a project doesn't have a Render URL, it cleanly falls back to "📦 GitHub Only".

6. **Client Inquiries & Live Ping**:
   - Working contact form sending inquiries directly to the backend database.
   - Interactive live API latency ping button demonstrating FastAPI's speed (10–20ms response time).

---

## 🗄️ Supabase Cloud Database Setup (1-Click)

To connect your Supabase project:
1. Open your [Supabase Dashboard](https://supabase.com/dashboard).
2. Go to **SQL Editor** -> **New Query**.
3. Copy and paste the entire contents of **`supabase_schema.sql`**.
4. Click **Run**.
   - This creates all tables (`profile`, `projects`, `experience`, `education`, `skills`, `messages`), enables RLS policies, and pre-seeds all data.
5. In `.env` (or Render Environment Variables), set:
   ```env
   SUPABASE_URL=https://<your-project-ref>.supabase.co
   SUPABASE_KEY=<your-secret-or-publishable-key>
   ```

---

## 🚀 How to Run Locally

### 1-Click Launcher (Windows)
Double-click:
👉 **`start.bat`**

This will automatically launch Uvicorn with hot-reload and open your browser:
- **Live Portfolio**: `http://localhost:8000`
- **Work Experience**: `http://localhost:8000/experience`
- **Academic Background**: `http://localhost:8000/education`
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
   git add .
   git commit -m "Deploy FastAPI Portfolio with Supabase & Admin CMS"
   git push origin main
   ```
2. In your Render Dashboard, add the environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
3. Click **Deploy Web Service**!

---

## 📁 Clean File Structure

```
d:\akhil-portfolio\
├── main.py                    # FastAPI Application & Uvicorn runner
├── models.py                  # Pydantic Schemas (Experience, Education, Skills, Profile, Projects)
├── database.py                # Dual-mode Supabase Cloud + Local JSON Database Manager
├── supabase_schema.sql        # Supabase DDL schema, RLS policies & seed dataset
├── start.bat                  # 1-Click Windows Launcher (uvicorn main:app --reload)
├── requirements.txt           # Dependencies (fastapi, uvicorn, supabase, python-dotenv, jinja2, pydantic)
├── Procfile                   # Process declaration for Render
├── render.yaml                # Render deployment blueprint
├── README.md                  # Documentation
├── data/
│   └── portfolio.json         # Master Local JSON Database Backup
├── templates/
│   ├── index.html             # Client-facing Portfolio Template
│   ├── experience.html        # Dedicated Work Experience Template
│   ├── education.html         # Dedicated Academic Background Template
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
