# DecorAI — setup and deployment

## What this build contains

- PostgreSQL as the single application database.
- FastAPI + SQLAlchemy backend.
- React + Vite frontend.
- Light/dark theme saved locally.
- Larger, high-contrast typography designed for easier reading.
- Persistent React Router navigation without route-level blink/reload animation.
- Footer across authenticated app pages.
- In-app notifications with unread state.
- Gmail verification and password reset using short six-digit codes.
- Strong password rules: 8+ characters, upper/lowercase, number and special character.
- Free local room-image understanding using BLIP (`Salesforce/blip-image-captioning-base`).
- Photorealistic image generation intentionally locked behind an Upgrade section.
- Docker Compose deployment with PostgreSQL, FastAPI and Nginx.

## Windows local setup

### 1. PostgreSQL

Create a PostgreSQL database named `decorai`.

The connection format is:

`postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/decorai`

If your PostgreSQL password contains `@`, encode it as `%40` in the URL. For example, `My@Pass` becomes `My%40Pass`.

### 2. Backend

```powershell
cd backend
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-ai.txt
copy .env.example .env
```

Edit `.env` and set your real `DATABASE_URL`, `SECRET_KEY`, and Gmail SMTP values.

Generate a secret without sharing it:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Then:

```powershell
python seed.py
python -m uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

### 3. Frontend

Open a second PowerShell window:

```powershell
cd frontend
$env:Path = "C:\Program Files\nodejs;$env:Path"
npm.cmd install
npm.cmd run dev
```

Open the URL shown by Vite.

## Gmail verification

Use a Google App Password, not the normal Gmail password.

Set:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourgmail@gmail.com
SMTP_PASSWORD=your-16-character-app-password
SMTP_FROM_EMAIL=yourgmail@gmail.com
```

Never commit `.env`.

## Docker deployment

From the project root:

```powershell
docker compose up --build
```

Then open:

`http://localhost:8080`

The frontend Nginx server proxies `/api` and `/media` to FastAPI, so the browser uses one origin and avoids the common localhost CORS mismatch.

Before using Docker outside your laptop, replace the demo PostgreSQL password and `SECRET_KEY` in `docker-compose.yml` with real secrets.

## Free AI analysis

The first room-analysis request downloads the BLIP model from Hugging Face into the configured cache. That download is not an API charge. Subsequent analysis reuses the local model.

The current build deliberately does not generate a new room image. The UI presents that capability as an Upgrade feature. This keeps the college-project demo at zero per-image API cost.

## Important production hardening

For a public deployment, add HTTPS, a real secrets manager, database migrations (Alembic), rate limiting, object storage for uploads, image-size/content validation, background jobs for model inference, and backups.
