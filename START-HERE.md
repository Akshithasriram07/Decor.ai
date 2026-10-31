# DecorAI — Start Here

## 1. Backend

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

Open `http://127.0.0.1:8000/health` and expect:

```json
{"status":"ok","service":"decorai-backend"}
```

Then open `http://127.0.0.1:8000/docs`.

## 2. Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## 3. Default free mode

Keep:

```env
AI_PROVIDER=mock
```

This is intentional. It lets you test DecorAI end-to-end without paying for an image-generation API. The provider can later be swapped without changing the Studio UI.

## 4. Admin

After `python seed.py`, local development creates:

- Email: `admin@decorai.local`
- Password: `ChangeMe123!`

Change both in `.env` before real use.

Admin tools include:
- metrics
- users
- design moderation
- order status
- worker availability
- worker application approval/rejection

## 5. First test sequence

1. Open the website.
2. Create a normal user.
3. Verify the account if SMTP is configured; for local development you can configure email first or test the API directly.
4. Sign in.
5. Open Dashboard.
6. Open Studio and upload JPG/PNG/WEBP.
7. Generate in mock mode and confirm a design is saved.
8. Open Explore and inspect public seeded designs.
9. Add a shopping product to cart.
10. Complete demo checkout.
11. Open Workers and submit a worker application.
12. Sign out and sign in as the admin account.
13. Open Admin and review the application/order/design controls.


## Demo account

For local development, the sign-in page includes **Continue with Demo Account**. It uses the development-only `/api/auth/demo-signin` endpoint, so no email verification or SMTP configuration is needed for the demo flow.

Demo user: `demo@decorai.local`

The demo endpoint is disabled automatically when `ENVIRONMENT` is not a development/local/test environment.


## Studio AI configuration

For room analysis, put your Gemini API key in `backend/.env` as `AI_API_KEY`. The recommended configuration is:

```env
AI_TEXT_PROVIDER=gemini
AI_TEXT_MODEL=gemini-3.8-flash
AI_TEXT_FALLBACK_MODELS=gemini-3.1-flash-lite
```

The Studio sends the actual uploaded image to Gemini. The selected room and design style are additional context. Image generation is intentionally locked and is not required for room analysis.
