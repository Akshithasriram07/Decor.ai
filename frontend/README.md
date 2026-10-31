# DecorAI v2 — Premium React Frontend

A complete Vite + React frontend for the DecorAI AI interior design product.

## Run locally

```bash
npm install
npm run dev
```

Open the local URL shown by Vite, normally:

`http://localhost:5173`

## Pages

- `/` — cinematic door-opening intro
- `/welcome` — premium marketing landing page
- `/signin` — sign in
- `/signup` — account creation
- `/app` — personal dashboard
- `/studio` — AI Design Studio
- `/explore` — searchable inspiration gallery
- `/shopping` — searchable products + wishlist
- `/workers` — searchable local professionals
- `/account` — dynamic profile, saved designs and wishlist

## Architecture

src/
- components/ — reusable UI
- context/ — authentication and design state
- data/ — prototype data sources
- pages/ — route-level pages
- styles/ — global design system

## Current data behavior

This is a fully working frontend prototype:
- authentication state is stored in localStorage
- user profile is dynamic
- saved designs persist in localStorage
- product wishlist persists in localStorage
- search/filter interactions work
- image upload preview works
- AI generation currently simulates the generation pipeline

## Production integration points

The frontend is deliberately structured so the mock behavior can be replaced by a real backend without rebuilding the UI.

Recommended production architecture:

React/Vite
→ FastAPI
→ PostgreSQL
→ Object storage
→ AI image generation service
→ Product/service APIs

Replace:
- AuthContext signIn/signUp with real auth API
- DesignContext persistence with backend endpoints
- Studio generate() with the FastAPI image-generation endpoint
- products/workers data files with API calls
- localStorage with server-side user/session state

## Design direction

The visual system uses warm ivory, deep forest green, muted gold, editorial serif typography, large interior photography, subtle shadows, restrained motion and generous whitespace.

No decorative emoji UI is used.
