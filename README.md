# AI Performance Hub: Requirements Specification & Initial Design

This document outlines the requirements and initial design for the AI Performance Hub, a web application focused on team performance tracking, goal management (OKRs), feedback logging, and AI-assisted insights.

> **Note:** This version specifies SQLite for the initial alpha development phase and Nuxt.js + PrimeVue for the frontend.

---

## Table of Contents
1. [Detailed Requirements Specification](#detailed-requirements-specification)
    - [Goals & Objectives](#goals--objectives)
    - [Functional Requirements](#functional-requirements)
    - [Non-Functional Requirements](#non-functional-requirements)
2. [Initial Design](#initial-design)
    - [Architecture](#architecture)
    - [Data Models (High-Level Schema for SQLite)](#data-models-high-level-schema-for-sqlite)
    - [API Endpoints (FastAPI Routers)](#api-endpoints-fastapi-routers)
    - [Frontend Structure (Nuxt.js 3)](#frontend-structure-nuxtjs-3)
    - [Key Technology Considerations](#key-technology-considerations)
3. [Implementation Guide](#implementation-guide)
    - [Backend Setup (FastAPI with SQLite)](#backend-setup-fastapi-with-sqlite)
    - [Frontend Setup (Nuxt.js 3 + PrimeVue)](#frontend-setup-nuxtjs-3--primevue)
    - [Development Environment Setup (Backend)](#development-environment-setup-backend)
4. [Next Steps & Considerations](#next-steps--considerations)

---

## 1. Detailed Requirements Specification

### 1.1. Goals & Objectives

- **Primary Goal:** Provide managers with a centralized, efficient platform (AI Performance Hub) to track team member performance goals (OKRs), manage ongoing feedback via 1-on-1 notes, link feedback to goals, track action items, and streamline the performance review process.
- **Secondary Goal:** Leverage AI to provide actionable insights, automate summaries (meetings, progress), extract key information (action items), and assist in drafting performance evaluations, saving managers time and improving feedback quality within the AI Performance Hub.
- **Target Audience:** Primarily Managers. Future iterations might include Team Member access (view-only or limited interaction) and System Administrators.

### 1.2. Functional Requirements

#### FR1: User Authentication & Authorization
- **FR1.1:** Secure user login (e.g., email/password).
- **FR1.2:** Role-Based Access Control (RBAC): Define 'Manager' and potentially 'Admin' roles.
- **FR1.3:** Hierarchy Support: Managers can only view/manage data for their direct reports. The system must support reporting structures (linking team members to their superiors).
- **FR1.4:** Secure session management (e.g., JWT).

#### FR2: Team Member Management
- **FR2.1:** Managers can view a list/grid of their direct reports.
- **FR2.2:** Access a detailed profile page for each team member.
- **FR2.3:** Profile Attributes:
    - `first_name` (Text, Required)
    - `last_name` (Text, Required)
    - `position` (Text)
    - `email` (Email, Required, Unique)
    - `start_date` (Date)
    - `is_active` (Boolean, Default: True)
    - `profile_picture_url` (URL, Optional)
    - `superior_id` (Link to another Team Member record, defines manager)
    - `public_notes` (Text Area, potentially visible to member in future)
    - `manager_notes` (Text Area, private to manager hierarchy)
- **FR2.4:** (Admin) Ability to Create, Read, Update, Deactivate Team Member profiles.
- **FR2.5:** (Manager) Ability to Read/Update profiles of direct reports.

#### FR3: Goal Management (OKRs / Performance Goals)
- **FR3.1: Objectives:**
    - **FR3.1.1:** CRUD operations for Objectives linked to a Team Member.
    - **FR3.1.2:** Attributes: `title` (Text, Required), `description` (Text Area), `team_member_id` (Link), `status` (Select: e.g., 'Active', 'Achieved', 'On Hold', 'Archived'), `start_period` (Date/Quarter/Year), `end_period` (Date/Quarter/Year).
- **FR3.2: Key Results (KRs):**
    - **FR3.2.1:** CRUD operations for Key Results linked to a specific Objective.
    - **FR3.2.2:** Attributes: `title` (Text, Required), `description` (Text Area), `objective_id` (Link), `measurement_type` (Select: e.g., 'Percentage', 'Numeric', 'Currency', 'Boolean', 'Completion'), `target_value` (Numeric/Text based on type), `current_value` (Numeric/Text based on type), `start_date` (Date), `deadline` (Date, Required), `complexity` (Select: e.g., 'Low', 'Medium', 'High'), `status` (Select: e.g., 'Not Started', 'On Track', 'At Risk', 'Achieved', 'Missed'), `result_evaluation` (Text Area for final notes).
- **FR3.3:** Ability to easily update `current_value` and `status` for KRs.
- **FR3.4:** Visual indicators for KR progress (e.g., progress bars based on current/target values for applicable types).

#### FR4: 1-on-1 Meeting Management
- **FR4.1:** Log 1-on-1 meeting notes associated with a specific Team Member.
- **FR4.2:** Attributes: `team_member_id` (Link), `manager_id` (Link, auto-filled), `meeting_date` (DateTime, Required), `notes` (Rich Text/Markdown supporting bullet points, basic formatting).
- **FR4.3:** Ability to flag specific bullet points or sections within notes for follow-up (e.g., a checkbox or visual tag).
- **FR4.4:** View a chronological history of meeting logs for a team member, filterable by date range.

#### FR5: Action Item Tracking
- **FR5.1:** CRUD operations for Action Items.
- **FR5.2:** Ability to link an Action Item to a specific Meeting Log (optional, can also be standalone).
- **FR5.3:** Attributes: `description` (Text, Required), `assigned_to_member_id` (Link), `assigned_by_manager_id` (Link), `meeting_log_id` (Optional Link), `due_date` (Date), `status` (Select: e.g., 'To Do', 'In Progress', 'Done', 'Blocked'), `priority` (Select: e.g., 'Low', 'Medium', 'High').

#### FR6: Manager Dashboard
- **FR6.1:** Central overview page upon login.
- **FR6.2:** Display list/cards of direct reports with quick links to profiles.
- **FR6.3:** Highlight key information: upcoming KR deadlines, overdue Action Items, meeting notes flagged for follow-up.
- **FR6.4:** Quick access/navigation to primary sections (Team, Goals, Meetings).
- **FR6.5:** (Optional) High-level visualization of team goal progress.

#### FR7: AI Integration Features
- **FR7.1:** Meeting Note Summarization: Button/action on a Meeting Log view to generate a concise summary of the notes field. Display summary clearly marked as AI-generated, potentially editable/savable.
- **FR7.2:** Action Item Extraction: Button/action on a Meeting Log view to analyze notes and suggest potential Action Items (pre-filling description, maybe assignee/due date if mentioned). Manager reviews, edits, confirms, or discards suggestions before creation.
- **FR7.3:** Goal Progress Analysis: Button/action on an Objective view. AI analyzes linked KR statuses/updates and potentially relevant snippets from meeting notes (within a timeframe) to provide a textual summary of progress, achievements, or recurring blockers. Mark as AI-generated.
- **FR7.4:** Performance Summary Draft: Dedicated feature (e.g., "Start Review Draft"). Manager selects Team Member and review period. AI uses selected Objectives, KR statuses/evaluations, meeting note highlights (e.g., flagged items, positive mentions), and completed Action Items within the period to generate draft text for review sections (e.g., Key Achievements, Areas for Development). Manager must review, heavily edit, and finalize.
- **FR7.5:** (Optional) Sentiment Analysis: If implemented: Analyze manager's notes (meeting logs, manager notes) over time for a team member. Provide high-level trend indicators (e.g., predominantly positive/negative/neutral language trend) – NOT definitive sentiment scores. Must be presented cautiously, marked experimental, require opt-in, and emphasize it reflects the manager's logged language, not necessarily the employee's actual sentiment. Strong ethical considerations required.

### 1.3. Non-Functional Requirements
- **NFR1: Security:** Secure authentication (JWT), HTTPS, encryption at rest for sensitive fields (e.g., manager_notes), input validation (prevent XSS, SQLi), API rate limiting, dependency vulnerability scanning. Nuxt security features (e.g., security headers module).
- **NFR2: Performance:** API response times < 500ms (typical), efficient database queries (indexing supported by SQLite), fast frontend load times (Nuxt optimizations like code splitting, SSR/SSG), asynchronous handling of AI tasks (FastAPI BackgroundTasks or Celery/RQ) with UI feedback (spinners/loaders). Note: Performance under high concurrency will be limited with SQLite compared to PostgreSQL.
- **NFR3: Usability:** Intuitive UI (PrimeVue components with Material Design theme), responsive design (desktop, tablet), consistent navigation (Nuxt routing), clear user feedback (toasts/dialogs).
- **NFR4: Scalability:** Stateless API design. Nuxt's SSR/SSG capabilities can improve perceived performance and handle higher loads than pure CSR SPAs. Note: SQLite limits vertical scalability (single file) and makes horizontal scaling difficult. Plan migration to PostgreSQL or similar for production/growth.
- **NFR5: Maintainability:** Modular code (FastAPI routers/services, Nuxt structure: pages, components, composables, stores), code comments/docstrings, linters/formatters (Black, Ruff, ESLint, Prettier), unit/integration tests (Pytest, Vitest).
- **NFR6: Data Privacy:** Compliance with relevant regulations (e.g., GDPR), clear data visibility rules, careful handling of personal data, especially AI outputs derived from it. Audit trails for sensitive actions.

---

## 2. Initial Design

### 2.1. Architecture

- **Frontend:** Nuxt 3 framework (built on Vue 3). Leverages features like file-based routing, auto-imports, server-side rendering (SSR) or static site generation (SSG) capabilities. PrimeVue for the UI component library, themed for Material Design. Pinia for state management (integrated with Nuxt).
- **Backend:** FastAPI (Python 3.9+) RESTful API using async/await. Pydantic for data validation/serialization.
- **Database:** SQLite for the initial alpha development phase (simple, file-based, located in backend/data/). SQLAlchemy (async version with aiosqlite) with Alembic for ORM and migrations. Note: Plan to migrate to PostgreSQL for later stages.
- **AI Integration:** Dedicated ai_service module in FastAPI. Uses httpx for async calls to external AI APIs (e.g., OpenAI, Google Gemini). Long-running tasks use FastAPI BackgroundTasks or a dedicated task queue (Celery/RQ with Redis/RabbitMQ broker).
- **Deployment:** Containerize frontend (Node.js server for Nuxt SSR or Nginx for static) and backend (Uvicorn/Gunicorn) with Docker/Docker Compose. Note: SQLite database file needs careful handling in containerized/deployed environments (volume mounting, permissions).

### 2.2. Data Models (High-Level Schema for SQLite)

Note: The following SQL uses standard syntax compatible with SQLite. Some advanced features or data types available in PostgreSQL (like native JSONB operations or specific index types) are not used here. Foreign key constraints are supported but might need explicit enabling (PRAGMA foreign_keys = ON;). Timestamps default to CURRENT_TIMESTAMP.

```sql
-- Users & Roles
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'manager', -- 'manager', 'admin'
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Team Members
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE SET NULL, -- Link if member can log in
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT,
    email TEXT UNIQUE NOT NULL, -- Work email
    start_date DATE,
    profile_picture_url TEXT,
    public_notes TEXT,
    manager_notes TEXT, -- Consider encryption or strict access control
    superior_id INTEGER REFERENCES team_members(id) ON DELETE SET NULL, -- Manager link
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_team_members_superior_id ON team_members(superior_id);
CREATE INDEX idx_team_members_email ON team_members(email); -- Added index

-- Objectives
CREATE TABLE objectives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_member_id INTEGER NOT NULL REFERENCES team_members(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'Active',
    start_period TEXT, -- e.g., '2025-Q1', '2025-01-01'
    end_period TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_objectives_team_member_id ON objectives(team_member_id);

-- Key Results
CREATE TABLE key_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    objective_id INTEGER NOT NULL REFERENCES objectives(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    measurement_type TEXT NOT NULL,
    target_value TEXT, -- Use TEXT to accommodate different types, validate in app
    current_value TEXT,
    start_date DATE,
    deadline DATE NOT NULL,
    complexity TEXT,
    status TEXT DEFAULT 'Not Started',
    result_evaluation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_key_results_objective_id ON key_results(objective_id);
CREATE INDEX idx_key_results_deadline ON key_results(deadline);

-- Meeting Logs
CREATE TABLE meeting_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_member_id INTEGER NOT NULL REFERENCES team_members(id) ON DELETE CASCADE,
    manager_id INTEGER NOT NULL REFERENCES team_members(id), -- Could reference users table if managers always log in
    meeting_date TIMESTAMP NOT NULL,
    notes TEXT, -- Store Markdown or HTML from rich text editor
    notes_structured TEXT, -- Optional: Store JSON as TEXT for flags {'follow_up_indices': [1, 5]}
    ai_summary TEXT, -- Store generated summary
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_meeting_logs_team_member_id ON meeting_logs(team_member_id);
CREATE INDEX idx_meeting_logs_meeting_date ON meeting_logs(meeting_date);

-- Action Items
CREATE TABLE action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    assigned_to_member_id INTEGER REFERENCES team_members(id) ON DELETE SET NULL,
    assigned_by_manager_id INTEGER REFERENCES team_members(id), -- Or users table
    meeting_log_id INTEGER REFERENCES meeting_logs(id) ON DELETE SET NULL,
    due_date DATE,
    status TEXT DEFAULT 'To Do',
    priority TEXT DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_action_items_assigned_to ON action_items(assigned_to_member_id);
CREATE INDEX idx_action_items_due_date ON action_items(due_date);
CREATE INDEX idx_action_items_status ON action_items(status);

-- Trigger for updated_at timestamp (Requires manual creation in SQLite if needed via application logic or specific triggers)
-- Example (Conceptual - implementation depends on how/where you manage updates):
-- CREATE TRIGGER update_users_updated_at AFTER UPDATE ON users
-- BEGIN
--     UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
-- END;
-- (Repeat for other tables)
```

### 2.3. API Endpoints (FastAPI Routers)

Organize endpoints into logical routers:
- `/auth (auth.py)`: `POST /token`, `GET /me`
- `/users (users.py)`: (Admin) CRUD for users.
- `/team-members (team_members.py)`: `GET /` (list reports), `POST /` (Admin), `GET /{id}`, `PUT /{id}`, `GET /{id}/objectives`, `GET /{id}/meeting-logs`, `GET /{id}/action-items`
- `/objectives (objectives.py)`: `POST /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`, `GET /{id}/key-results`
- `/key-results (key_results.py)`: `POST /`, `GET /{id}`, `PUT /{id}` (update value/status), `DELETE /{id}`
- `/meeting-logs (meeting_logs.py)`: `POST /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`, `POST /{id}/summarize` (AI), `POST /{id}/extract-actions` (AI)
- `/action-items (action_items.py)`: `POST /`, `GET /{id}`, `PUT /{id}` (update status), `DELETE /{id}`
- `/ai (ai_service.py - potentially internal calls or specific endpoints)`: `POST /analyze/goal-progress/{objective_id}`, `POST /draft/performance-summary/{member_id}`

### 2.4. Frontend Structure (Nuxt.js 3)

Standard Nuxt 3 Directories:
- `components/`: Reusable Vue components (auto-imported). Use PrimeVue components extensively here (e.g., Card, DataTable, InputText, Button, Dialog).
- `pages/`: Application views and routes (file-based routing). Examples: `pages/index.vue` (Dashboard), `pages/login.vue`, `pages/team/[id].vue`, `pages/team/[id]/goals.vue`.
- `layouts/`: Define common page layouts (e.g., `default.vue` with navigation, `auth.vue` for login page).
- `composables/`: Reusable Composition API functions (auto-imported, e.g., `useApi.js`, `useAuth.js`).
- `stores/`: Pinia stores for state management (auto-imported if using the Nuxt Pinia module).
- `server/`: API routes or server middleware (if needed within Nuxt itself, though most API calls go to the FastAPI backend).
- `plugins/`: For integrating Vue plugins (e.g., custom setup for Axios if needed beyond basic composable usage). PrimeVue setup might be handled via its module.
- `assets/`: Uncompiled assets like CSS, fonts, images.
- `public/`: Static assets directly served (e.g., `favicon.ico`).

Configuration:
- `nuxt.config.ts`: Main Nuxt configuration file (modules, plugins, runtime config, CSS, PrimeVue options).
- `app.vue`: Root Vue component, typically contains `<NuxtLayout>` and `<NuxtPage>`.
- `.env`: Environment variables (accessible via runtimeConfig in `nuxt.config.ts`).

### 2.5. Key Technology Considerations

- **FastAPI:** Use `Depends` for dependency injection (DB sessions, current user). Use Pydantic models extensively for request/response validation and auto-generated OpenAPI docs. Leverage `BackgroundTasks` for non-blocking AI calls.
- **Nuxt.js/PrimeVue:** Leverage Nuxt's features (SSR/SSG, file-based routing, auto-imports, modules). Use the official `primevue-nuxt-module` for easy integration. Configure PrimeVue themes (Material Design) in `nuxt.config.ts`. Use Pinia for state management. Consider Nuxt's built-in data fetching composables (`useFetch`, `useAsyncData`).
- **AI:** Choose an AI provider API. Store API keys securely (env vars, potentially exposed to backend via Nuxt runtime config if needed, but prefer keeping them backend-only). Design prompts carefully for each feature. Handle potential errors from the AI API gracefully. Clearly indicate AI-generated content in the UI.
- **Database:** Use async SQLAlchemy with aiosqlite for the alpha phase. Use Alembic for managing schema migrations (works with SQLite). Define clear relationships and use appropriate indexing. Be mindful of SQLite limitations (e.g., write concurrency, lack of certain advanced features) and plan for future migration.
- **Error Handling:** Implement consistent error handling on both backend (FastAPI exception handlers) and frontend (Nuxt error page, component-level error handling, user-friendly messages).

---

## 3. Implementation Guide

This section provides basic steps to set up the initial project skeletons for both the backend and frontend, using SQLite for the backend database located in a data subdirectory and Nuxt.js + PrimeVue for the frontend.

### 3.1. Backend Setup (FastAPI with SQLite)

**Prerequisites:** Python 3.9+.

**Create Project Directory and Data Subdirectory:**
```sh
mkdir backend
cd backend
mkdir data # Create data subdirectory
```

**Set up Virtual Environment:**
```sh
python -m venv venv
source venv/bin/activate
```

**Install Dependencies:**
```sh
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite alembic pydantic python-dotenv passlib[bcrypt] python-jose[cryptography] httpx flake8 black
```

- `fastapi`: The core framework.
- `uvicorn[standard]`: ASGI server to run FastAPI.
- `sqlalchemy[asyncio]`: ORM for database interaction (async version).
- `aiosqlite`: Async driver for SQLite.
- `alembic`: Database migration tool.
- `pydantic`: Data validation (used by FastAPI).
- `python-dotenv`: For loading environment variables (e.g., secrets).
- `passlib[bcrypt]`: For hashing passwords.
- `python-jose[cryptography]`: For JWT handling.
- `httpx`: For making async HTTP requests (to AI APIs).
- `flake8`: Linter for Python code style and errors.
- `black`: Code formatter for Python.

**Initialize Alembic (for migrations):**
```sh
alembic init alembic
```

Configure `alembic.ini` with your SQLite database URL. The URL format is `sqlite+aiosqlite:///./data/aiphb.db` (pointing to the file inside the data directory).
Edit `alembic/env.py` to import your SQLAlchemy models and configure it for async and SQLite.

**Create Initial Project Structure:**
```sh
backend/
├── alembic/
├── data/                 # Directory for database file
│   └── aiphb.db          # The SQLite database file (will be created here)
├── venv/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app instance, middleware
│   ├── database.py     # SQLAlchemy setup (using aiosqlite), session management
│   ├── models.py       # SQLAlchemy ORM models (mirroring DB tables)
│   ├── schemas.py      # Pydantic models for request/response validation
│   ├── crud.py         # Database interaction functions
│   ├── dependencies.py # Reusable dependencies (e.g., get_db, get_current_user)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py   # Settings management (from .env)
│   │   └── security.py # Password hashing, JWT creation/verification
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── team_members.py
│   │   └── ... (other routers)
│   └── services/
│       ├── __init__.py
│       └── ai_service.py # Logic for interacting with AI APIs
├── alembic.ini
├── requirements.txt    # Freeze dependencies: pip freeze > requirements.txt
├── .env                # Store environment variables (SECRET_KEY, AI_API_KEY, etc.) - DO NOT COMMIT
└── .flake8             # Flake8 configuration file
```

**Create Basic `app/main.py`:** (Example - ensure database setup uses aiosqlite and correct path)
```python
# app/main.py
from fastapi import FastAPI
# Ensure database.py initializes engine with 'sqlite+aiosqlite:///./data/aiphb.db'
# from app import models # Import models if needed for Alembic or initial setup
# from app.database import engine
from app.routers import auth, team_members # Import your routers
from app.core.config import settings
import os # Import os module

# Ensure data directory exists
if not os.path.exists('./data'):
    os.makedirs('./data')

# Optional: Create tables if not using Alembic initially
# models.Base.metadata.create_all(bind=engine) # Note: Use Alembic for production

# Use the application name from settings if defined, otherwise default
app_title = getattr(settings, 'PROJECT_NAME', "AI Performance Hub")
app = FastAPI(title=app_title)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(team_members.router, prefix="/team-members", tags=["team-members"])
# ... include other routers

@app.get("/")
async def root():
    return {"message": f"{app_title} API (SQLite Alpha)"}

# Add CORS middleware if frontend is on a different origin
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(...)
```

**Run Development Server:**
```sh
uvicorn app.main:app --reload
```

### 3.2. Frontend Setup (Nuxt.js 3 + PrimeVue)

**Prerequisites:** Node.js (LTS version recommended) and npm/pnpm/yarn.

**Create Project Directory (outside the backend directory):**
```sh
cd .. # Go up from backend
mkdir frontend
cd frontend
```

**Initialize Nuxt Project:**
```sh
npx nuxi init . # Initialize Nuxt in the current directory
```

Follow prompts if any. This creates the basic Nuxt 3 structure.

**Install Dependencies:**
```sh
npm install # Or pnpm install / yarn install
```

**Add PrimeVue and Nuxt Module:**
```sh
npm install primevue primeicons primevue-nuxt-module --save-dev
```

- `primevue`: The core component library.
- `primeicons`: Icon library for PrimeVue.
- `primevue-nuxt-module`: Official Nuxt module for integration.

**Configure Nuxt (`nuxt.config.ts`):**
Edit `nuxt.config.ts` to include the PrimeVue module and configure it. Choose a Material Design theme.
```typescript
// frontend/nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true }, // Enable Nuxt DevTools

  modules: [
      'primevue-nuxt-module', // Add the PrimeVue module
      '@pinia/nuxt', // Add Pinia module if needed for state management
  ],

  primevue: {
      usePrimeVue: true,
      options: {
          ripple: true, // Optional: Enable ripple effect
          // unstyled: true // Set to true if using Tailwind pass-through (advanced)
      },
      components: {
          // Optionally register components globally, or import them where needed
          // prefix: 'Prime', // Optional prefix
          // include: ['Button', 'Card', 'DataTable'] // Example: include specific components
      },
      // Import chosen theme and icons CSS
      cssLayerOrder: 'tailwind-base, primevue, tailwind-utilities' // Adjust if using Tailwind
  },

  css: [
      'primevue/resources/themes/mdc-light-indigo/theme.css', // Choose your Material theme (light)
      // or 'primevue/resources/themes/mdc-dark-indigo/theme.css' // (dark)
      'primevue/resources/primevue.min.css', // Core CSS
      'primeicons/primeicons.css' // Icons
      // Add global CSS files here if needed: '~/assets/css/main.css'
  ],

  runtimeConfig: {
      // Variables available only on the server-side
      // Example: apiSecret: process.env.API_SECRET,
      public: {
          // Variables exposed to the frontend
          // Example: API base URL for client-side calls
          apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
      }
  },

  // Add Pinia configuration if using it
  // pinia: {
  //   autoImports: [
  //     // automatically import `defineStore`
  //     'defineStore', // import { defineStore } from 'pinia'
  //     ['defineStore', 'definePiniaStore'], // import { defineStore as definePiniaStore } from 'pinia'
  //   ],
  // },
})
```

**Create `.env` for Frontend:**
Create a `.env` file in the frontend directory for environment variables used by Nuxt (like the API base URL).
```sh
# frontend/.env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1 # Example: Adjust port/path if needed
```

**Basic App Structure (`app.vue`):**
Ensure `frontend/app.vue` includes `<NuxtLayout>` and `<NuxtPage>`:
```vue
<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
```

**Create Layouts and Pages:**
Create files like `layouts/default.vue` and `pages/index.vue`.
Start using PrimeVue components within your pages and components.

**Run Development Server:**
```sh
npm run dev -- -o # Or pnpm dev / yarn dev
```

### 3.3. Development Environment Setup (Backend)

This section covers setting up linters and formatters for the backend Python code to ensure consistency and quality.

**Activate Virtual Environment:**
Make sure your backend virtual environment is activated:
```sh
cd backend
source venv/bin/activate
```

**Install Linters/Formatters:**
We installed `flake8` (linter) and `black` (formatter) in step 3.1.4. If you missed them, install now:
```sh
pip install flake8 black
```

**Configure Flake8:**
Flake8 checks for PEP 8 style guide violations, programming errors, and code complexity. You can configure it via a file in the project root (backend/). Common options are `.flake8` or `setup.cfg`.
Create a file named `.flake8` in the backend directory.
Add the following configuration to adjust the maximum line length (default is 79) and potentially ignore certain rules or exclude directories:
```ini
# backend/.flake8
[flake8]
# Set the maximum line length (e.g., 88 to match Black, or 120)
max-line-length = 88
# You can ignore specific error codes if needed:
# ignore = E203, E501, W503
# Exclude directories like the virtual environment or migrations
exclude =
    .git,
    __pycache__,
    venv,
    alembic/versions/
```

**Configure Black:**
Black is an opinionated code formatter that automatically reformats your code to its style. It often works well with Flake8's default line length or a slightly longer one (like 88). Black can be configured in `pyproject.toml`.
Create or edit the `pyproject.toml` file in the backend directory.
Add a `[tool.black]` section:
```toml
# backend/pyproject.toml
[tool.black]
line-length = 88
# You can specify files/directories to include or exclude if needed
# include = '\.pyi?$'
# exclude = '''
# /(
#     \.git
#   | \.hg
#   | \.mypy_cache
#   | \.tox
#   | \.venv
#   | _build
#   | buck-out
#   | build
#   | dist
#   | venv
#   | alembic/versions
# )/
# '''
```

**Running Linters/Formatters:**
- **Run Black:** To format your code automatically:
```sh
black .
```
(The `.` refers to the current directory).
- **Run Flake8:** To check for style issues and errors after formatting:
```sh
flake8 .
```

**IDE Integration (Recommended):**
Configure your IDE (like VS Code, PyCharm) to automatically run Black on save and show Flake8 warnings directly in the editor. This provides immediate feedback during development. Check your IDE's documentation for instructions on setting up Python linters and formatters.

---

## 4. Next Steps & Considerations

- **MVP Definition:** Prioritize core features (Team CRUD, Objective/KR CRUD, Meeting Log CRUD) for the Minimum Viable Product. Add AI features incrementally.
- **UI/UX Mockups:** Create basic wireframes or mockups to visualize the user flow and layout before deep diving into PrimeVue component implementation.
- **AI Prompt Engineering:** This will be iterative. Start with simple prompts and refine based on the quality of AI output.
- **Testing Strategy:** Plan for unit tests (Pytest, Vitest), integration tests (testing API endpoints), and potentially E2E tests (Cypress/Playwright). Note: Testing with SQLite might differ slightly from PostgreSQL, especially regarding concurrency.
- **Security Review:** Regularly review security aspects, especially around authentication, authorization, and data storage.
- **Ethical AI:** Continuously revisit the ethical implications, provide user controls where appropriate, and ensure transparency.
- **Database Migration Plan:** Keep in mind the need to migrate from SQLite to a more robust database like PostgreSQL before scaling or moving to production. Design your SQLAlchemy models and Alembic migrations to facilitate this transition.

This detailed plan should give you a strong starting point for developing the AI Performance Hub.
