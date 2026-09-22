-- ============================================================================
-- AutomateX (Akhil Pandey) - Supabase Cloud Database Schema & Initial Seed
-- Execute this script in: Supabase Dashboard -> SQL Editor -> New Query -> Run
-- ============================================================================

-- 1. Table: Profile & Global Settings
CREATE TABLE IF NOT EXISTS public.profile (
    id TEXT PRIMARY KEY DEFAULT 'main',
    name TEXT NOT NULL DEFAULT 'Akhil Pandey',
    brand TEXT NOT NULL DEFAULT 'AutomateX',
    role_title TEXT NOT NULL DEFAULT 'Software Developer & Automation Specialist',
    tagline TEXT NOT NULL DEFAULT 'Software Developer | Python & FastAPI | Workflow Automation',
    short_bio TEXT DEFAULT 'MCA graduate from Nirma University with 2+ years of professional IT experience building scalable backend APIs, custom CRM systems, and automated business workflows.',
    about TEXT DEFAULT 'I am a backend-focused Software Developer with hands-on expertise in Python, FastAPI, Django, and automated workflow pipelines (n8n, Zapier, Make.com). I help businesses and clients streamline operations, eliminate repetitive manual data entry, and deploy robust, live applications on Render and Cloud platforms.',
    email TEXT NOT NULL DEFAULT 'akhil.pandeyy1@gmail.com',
    phone TEXT NOT NULL DEFAULT '+91 76003 47544',
    location TEXT NOT NULL DEFAULT 'Navsari, Gujarat, India - 396445',
    github TEXT NOT NULL DEFAULT 'https://github.com/akhiil1',
    linkedin TEXT NOT NULL DEFAULT 'https://linkedin.com/in/akhiil1',
    admin_pin TEXT NOT NULL DEFAULT 'akhil123',
    status_badge TEXT NOT NULL DEFAULT 'Available for Full-Time & Freelance Projects',
    resume_url TEXT NOT NULL DEFAULT '/resume',
    stats JSONB DEFAULT '[
        {"label": "Years Experience", "value": "2+"},
        {"label": "Manual Effort Cut", "value": "75%"},
        {"label": "APIs & Workflows Built", "value": "30+"},
        {"label": "State Merit Rank", "value": "65th"}
    ]'::jsonb,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Table: Projects (Render Live & GitHub Showcase)
CREATE TABLE IF NOT EXISTS public.projects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'backend',
    category_label TEXT DEFAULT 'Backend & APIs',
    description TEXT NOT NULL,
    tech_stack JSONB DEFAULT '[]'::jsonb,
    github_url TEXT DEFAULT '',
    render_url TEXT DEFAULT '',
    has_render BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'GitHub Repo',
    date TEXT DEFAULT '2025',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Table: Work Experience
CREATE TABLE IF NOT EXISTS public.experience (
    id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT NOT NULL,
    period TEXT NOT NULL,
    badge TEXT DEFAULT 'Full-Time',
    points JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Table: Education & Qualifications
CREATE TABLE IF NOT EXISTS public.education (
    id TEXT PRIMARY KEY,
    degree TEXT NOT NULL,
    institution TEXT NOT NULL,
    location TEXT NOT NULL,
    period TEXT NOT NULL,
    grade TEXT NOT NULL,
    highlights TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Table: Technical Skills
CREATE TABLE IF NOT EXISTS public.skills (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Table: Client Inquiries & Messages
CREATE TABLE IF NOT EXISTS public.messages (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT DEFAULT 'General Inquiry',
    message TEXT NOT NULL,
    date TEXT DEFAULT '',
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- Enable Row Level Security (RLS) & Grant Access
-- ============================================================================
ALTER TABLE public.profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.education ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Allow anonymous / service role read & write (protected via backend Admin PIN)
CREATE POLICY "Allow All on profile" ON public.profile FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow All on projects" ON public.projects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow All on experience" ON public.experience FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow All on education" ON public.education FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow All on skills" ON public.skills FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow All on messages" ON public.messages FOR ALL USING (true) WITH CHECK (true);

-- ============================================================================
-- Initial Seed Data (Pre-Populated for Akhil Pandey)
-- ============================================================================

-- Profile
INSERT INTO public.profile (id, name, brand, role_title, tagline, about, email, phone, location, github, linkedin, admin_pin, status_badge)
VALUES (
    'main',
    'Akhil Pandey',
    'AutomateX',
    'Software Developer & Automation Specialist',
    'Software Developer | Python & FastAPI | Workflow Automation',
    'I am a backend-focused Software Developer with hands-on expertise in Python, FastAPI, Django, and automated workflow pipelines (n8n, Zapier, Make.com). I help businesses and clients streamline operations, eliminate repetitive manual data entry, and deploy robust, live applications on Render and Cloud platforms.',
    'akhil.pandeyy1@gmail.com',
    '+91 76003 47544',
    'Navsari, Gujarat, India - 396445',
    'https://github.com/akhiil1',
    'https://linkedin.com/in/akhiil1',
    'akhil123',
    'Available for Opportunities'
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    brand = EXCLUDED.brand,
    role_title = EXCLUDED.role_title;

-- Projects
INSERT INTO public.projects (id, title, category, category_label, description, tech_stack, github_url, render_url, has_render, status, date)
VALUES
(
    'proj-1',
    'AutomateX API Gateway & Workflow Orchestrator',
    'backend',
    'Backend & APIs',
    'High-throughput asynchronous REST API built with FastAPI, PostgreSQL, and Redis. Features automated webhook ingestion, retry mechanisms, and rate-limited endpoints. Deployed live on Render.',
    '["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "Render"]'::jsonb,
    'https://github.com/akhiil1/automatex-api-gateway',
    'https://automatex-api-gateway.onrender.com',
    TRUE,
    'Live on Render',
    '2025'
),
(
    'proj-2',
    'AI-Powered Customer CRM & Automated Leads Engine',
    'automation',
    'Workflow Automation',
    'Custom CRM engine engineered for rapid client query intake, automated email alerts, and multi-step webhook sync between forms, database, and notification channels. Hosted live on Render.',
    '["Python", "Django", "N8N", "Zapier", "REST APIs", "Render"]'::jsonb,
    'https://github.com/akhiil1/ai-leads-crm-automation',
    'https://leads-crm-engine.onrender.com',
    TRUE,
    'Live on Render',
    '2025'
),
(
    'proj-3',
    'Smart Document Data Extraction & OCR Pipeline',
    'automation',
    'Automation & AI',
    'Automated OCR extraction pipeline that reads invoices and vouchers, executes strict mathematical validation rules, and saves structured records into databases.',
    '["Python", "OpenCV", "FastAPI", "Make.com", "SQL"]'::jsonb,
    'https://github.com/akhiil1/doc-extractor-pipeline',
    '',
    FALSE,
    'GitHub Repo',
    '2024'
),
(
    'proj-4',
    'Scalable Authentication & Microservices Boilerplate',
    'backend',
    'Microservices',
    'Production-ready template for microservices architecture featuring JWT authentication, role-based access control (RBAC), rate-limiting middleware, and health-check monitoring.',
    '["Python", "FastAPI", "JWT", "Docker", "PostgreSQL", "Render"]'::jsonb,
    'https://github.com/akhiil1/fastapi-auth-microservices',
    'https://fastapi-microservices-demo.onrender.com',
    TRUE,
    'Live on Render',
    '2024'
),
(
    'proj-5',
    'RPA Financial Reconciliation & Reporting Bot',
    'automation',
    'RPA Automation',
    'Automated desktop & web scraping bot to match bank receipts with internal ledger records, generating audit-ready Excel reports and notifying stakeholders on Slack/Email.',
    '["Python", "Pandas", "Zapier", "Office 365"]'::jsonb,
    'https://github.com/akhiil1/rpa-finance-reconciler',
    '',
    FALSE,
    'GitHub Repo',
    '2024'
)
ON CONFLICT (id) DO NOTHING;

-- Experience
INSERT INTO public.experience (id, company, role, location, period, badge, points)
VALUES
(
    'exp-1',
    'Digipie Technologies',
    'Python Developer',
    'Surat, Gujarat',
    'Jul 2025 – Present',
    'Current Role',
    '[
        "Architecting robust backend APIs using Python (FastAPI & Django); coordinating closely with cross-functional teams and clients to resolve queries and deliver milestones on time.",
        "Automating routine office workflows using Make.com, Zapier, and N8N, slashing manual operational effort and error rates.",
        "Performing strict data validation and consistency checks; identifying root causes of data issues and maintaining audit-ready records and reports."
    ]'::jsonb
),
(
    'exp-2',
    'Biztechnosys Infotech Pvt Ltd',
    'Software Developer',
    'Bangalore, Karnataka',
    'Jul 2024 – Jun 2025',
    'Full-Time',
    '[
        "Interacted directly with enterprise clients to map business workflows and customized CRM software matching exact day-to-day operational requirements.",
        "Maintained structured schemas, rigorous validation rules, and automated reporting formats to keep enterprise records clean and audit-ready.",
        "Significantly improved turnaround time of backend data processes through proactive coordination, query optimization, and follow-ups."
    ]'::jsonb
),
(
    'exp-3',
    '1Rivet India LLP',
    'RPA Developer (Internship)',
    'Valsad, Gujarat',
    'Feb 2024 – Jun 2024',
    'Internship',
    '[
        "Identified repetitive manual tasks in office workflows and engineered automated RPA bots, vastly enhancing operational throughput.",
        "Collaborated with senior engineers to track, benchmark, and report runtime performance gains of automated processes."
    ]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

-- Education
INSERT INTO public.education (id, degree, institution, location, period, grade, highlights)
VALUES
(
    'edu-1',
    'Master of Computer Application (MCA)',
    'Institute of Technology, Nirma University',
    'Ahmedabad, Gujarat',
    '2022 – 2024',
    '78.60%',
    'Served as Vice President of Association of MCA Students (AMS); Secured 65th Rank in national-level ACPC-CMAT entrance exam.'
),
(
    'edu-2',
    'Bachelor of Computer Application (BCA)',
    'Naran Lala College of Professional & Applied Sciences',
    'Navsari, Gujarat',
    '2019 – 2022',
    '80.40%',
    'Core specialization in Algorithms, Database Systems, Object-Oriented Software Design, and Web Applications.'
),
(
    'edu-3',
    'Higher Secondary (HSC) & Secondary (SSC)',
    'Navchetan High School',
    'Navsari, Gujarat',
    '2017 – 2019',
    'HSC: 70.26% | SSC: 66.00%',
    'Science and Computer foundation with distinction in practical coursework.'
)
ON CONFLICT (id) DO NOTHING;

-- Skills
INSERT INTO public.skills (name) VALUES
('Python'),
('FastAPI'),
('Django'),
('RESTful APIs & Microservices'),
('PostgreSQL'),
('MySQL'),
('SQLite'),
('Redis Caching'),
('n8n Workflow Automation'),
('Zapier'),
('Make.com'),
('RPA Automation'),
('Docker & Containers'),
('Render Cloud Deployment'),
('Git & GitHub'),
('Postman API Testing'),
('AI & LLM Integrations'),
('JavaScript & HTML/CSS')
ON CONFLICT (name) DO NOTHING;
