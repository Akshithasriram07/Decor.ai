<<<< HEAD
# DecorAI — Premium AI Interior Design SaaS

DecorAI is a React + FastAPI interior-design application designed as a realistic end-to-end local development project.

## Included

### Customer experience
- Intro / landing experience
- Sign up, email verification, sign in
- Forgot password + reset code flow
- JWT authentication
- Dashboard with saved design statistics
- AI Design Studio with image upload, room/style selection and provider abstraction
- Explore gallery with public designs and detail views
- Shopping catalog, cart, wishlist and demo checkout
- Orders and order-success flow
- Local worker directory and worker profile/application flow
- Account profile, notifications, designs, wishlist and orders
- Responsive premium ivory / forest / gold visual system

### Administration
- Role-based admin authorization on the backend
- Admin dashboard and operating metrics
- User/member listing
- Design visibility moderation
- Order status management
- Worker availability management
- Worker application review and approval/rejection
- Approved worker applications can become worker listings

## Free development mode

The default configuration is:

```env
AI_PROVIDER=mock
```

This keeps the whole application usable without a paid image API. The mock provider copies the uploaded room image so you can fully test the upload, generation request, database, history and UI flows.

For real AI image generation, use a provider that your account has access to and configure it in `.env`. Image APIs are not assumed to be free.

## Requirements

- Python 3.11 recommended
- Node.js 20+ recommended
- npm

## Backend

```powershell
cd backend
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`
Docs: `http://127.0.0.1:8000/docs`

## Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`

## Admin development account

The seed script creates an admin using:

```env
ADMIN_EMAIL=admin@decorai.local
ADMIN_PASSWORD=ChangeMe123!
```

Change these values in `.env` before using anything outside local development.

Sign in through the normal `/signin` page. An admin user will automatically see **Admin** in the sidebar and can open `/admin`.

## Important production notes

This package is a strong local/full-stack development build, not a claim of production deployment certification. Before production use, replace SQLite with PostgreSQL, rotate secrets, configure real email delivery, configure a real payment provider, add object storage, add migrations (Alembic), rate limiting, audit logs and deployment secrets.
=======
# Decor.ai
>>>>>>> origin/main
