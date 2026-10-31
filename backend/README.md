# DecorAI v3 Backend

FastAPI + SQLAlchemy backend for the complete DecorAI application.

## Core features
- JWT authentication
- Email verification code
- Resend verification
- Forgot password + reset code
- Persistent users/designs/wishlist/cart/orders
- AI Design Studio provider adapters
- Explore detail endpoints
- Local worker profiles + worker applications
- Razorpay order creation + signature verification
- Notifications
- SQLite for local development; use PostgreSQL for production

## Setup on Windows
Use Python 3.11 for the easiest installation path.

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Email
For Gmail, create an App Password and place it in `SMTP_PASSWORD`. Never commit `.env`.

If SMTP is empty in development, verification/reset codes are printed to the backend terminal. This is intentionally a development fallback, not a production email system.

## AI
Set:
- `AI_PROVIDER=gemini` and `AI_API_KEY=...`, or
- `AI_PROVIDER=xai` / `grok` and the corresponding key/model.

The API key stays server-side. React never receives it.

## Payments
Set Razorpay credentials only in the backend `.env`. The frontend calls `/api/orders/checkout`; the backend creates the Razorpay order and `/api/orders/verify` verifies the signature.

For production add webhooks, idempotency, PostgreSQL migrations, object storage, rate limiting and background jobs.


## AI Design Studio

The free Studio uses Gemini for **image understanding + written interior recommendations**. It does not call an image-generation provider. Configure:

```env
AI_API_KEY=your_gemini_api_key
AI_TEXT_PROVIDER=gemini
AI_TEXT_MODEL=gemini-3.8-flash
AI_TEXT_FALLBACK_MODELS=gemini-3.1-flash-lite
```

The backend retries temporary 429/5xx responses and then tries the configured fallback model. The UI keeps photorealistic image generation locked.
