# Team Task Manager

A full-stack task management web application where admins can create projects, assign tasks, and track team progress with role-based authentication.

A beginner-friendly full-stack web application for managing team projects and tasks with role-based access control.

---

## Live Demo

Frontend:
https://team-task-270056.netlify.app

Backend API Docs:
https://team-task-manager-production-0245.up.railway.app/docs

---

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | FastAPI, SQLAlchemy, MySQL, JWT, bcrypt |
| Frontend | HTML, CSS, Vanilla JavaScript, Bootstrap 5 |

---

## Features

- Authentication — Signup, login, JWT tokens, bcrypt password hashing
- Roles — Admin (manage projects/tasks) and Member (view assigned tasks, update status)
- Projects — Create and list projects
- Tasks — CRUD operations, assign users, update status (Pending / In Progress / Completed)
- Dashboard — Total, completed, pending, and overdue task counts
- Responsive UI — Beginner-friendly interface using Bootstrap 5

---

## Project Structure

```bash
team-task-manager/
├── backend/          # FastAPI backend API
├── frontend/         # Static HTML/CSS/JS frontend
└── README.md
Prerequisites
Python 3.10+
MySQL 8+
VS Code Live Server or any static file server

## 1. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE taskmanager;
```

## 2. Backend Setup

```bash
cd team-task-manager/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials and SECRET_KEY
```

Example `.env`:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskmanager
```

**Password special characters:** If your MySQL password contains `@`, `#`, `:`, or `/`, you must [URL-encode](https://en.wikipedia.org/wiki/Percent-encoding) them in `DATABASE_URL`. For example, password `Anviam@123` becomes:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskmanager
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Tables are created automatically on first run (`Base.metadata.create_all`).

## 3. Frontend Setup

1. Open `frontend/app.js` and set `API_BASE_URL` to your backend URL.
2. Serve the `frontend/` folder with any static server.

**VS Code Live Server** (port 5500 is included in default CORS):

```bash
cd team-task-manager/frontend
python3 -m http.server 5500
```

3. Open [http://127.0.0.1:5500](http://127.0.0.1:5500) (or your server URL).

### First-time usage

First-Time Usage
Sign up as Admin or Member
Admin can:
Create projects
Create tasks
Assign tasks to members
Members can:
View assigned tasks
Update task status
## API Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/signup` | Public | Register user |
| POST | `/login` | Public | Login, get JWT |
| GET | `/users` | Admin | List users (for assignment) |
| GET | `/projects` | Auth | List projects |
| POST | `/projects` | Admin | Create project |
| GET | `/tasks` | Auth | List tasks |
| POST | `/tasks` | Admin | Create task |
| PUT | `/tasks/{id}` | Auth | Update task (member: status only) |
| DELETE | `/tasks/{id}` | Admin | Delete task |
| GET | `/dashboard` | Auth | Dashboard stats |

Send JWT in header: `Authorization: Bearer <token>`

## Deployment

### Backend (Railway)

1. Push `backend/` to GitHub.
2. Create a Railway project and add **MySQL** plugin.
3. Set environment variables from `.env.example` (use Railway MySQL URL).
4. Railway uses the `Procfile` automatically:

   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

5. Set root directory to `backend` if deploying from monorepo.

### Frontend (Netlify / Vercel)

1. Deploy the `frontend/` folder as a static site.
2. Update `API_BASE_URL` in `app.js` to your Railway API URL.
3. Add your frontend URL to backend `CORS_ORIGINS` on Railway.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | `mysql+pymysql://user:pass@host:3306/dbname` |
| `SECRET_KEY` | JWT signing secret |
| `ALGORITHM` | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins |

## License

MIT — free for learning and portfolio use.