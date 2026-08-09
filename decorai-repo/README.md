# DecorAI — Frontend Prototype

A static, front-end-only clone of the DecorAI interior design app UI. Built with plain **HTML, CSS, and JavaScript** — no frameworks, no build step. Open it and it just runs.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| AI Design Studio | `ai-design-studio.html` |
| Explore | `explore.html` |
| Shopping | `shopping.html` |
| Local Workers | `local-workers.html` |
| Account | `account.html` |

## Project structure

```
decorai/
├── index.html
├── ai-design-studio.html
├── explore.html
├── shopping.html
├── local-workers.html
├── account.html
├── assets/
│   ├── css/
│   │   └── style.css      # shared design system (colors, layout, components)
│   └── js/
│       └── app.js         # shared interactions (favorites, chips, style picker, AI-generate simulation)
└── README.md
```

## Running it

No install, no server required.

**Option A — just open it**
Double-click `index.html` (or any page) and it opens in your browser. All pages link to each other with relative paths, so navigation works fully offline.

**Option B — local server (recommended for consistent behavior across browsers)**
```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```
Then visit `http://localhost:8080`.

## What's implemented

- Full 6-screen layout matching the design reference (sidebar nav, headers, cards, grids)
- Shared design tokens in `style.css` (`:root` CSS variables) for color, radius, and shadow — change once, updates everywhere
- Interactive bits in `app.js`:
  - Favorite/heart toggle on design & product cards
  - Chip/tab filter selection (Explore, Shopping, Local Workers categories)
  - Style & room-type picker in AI Design Studio
  - Budget slider synced to a Low/Medium/High label
  - "Generate Designs" button simulates an AI generation delay before revealing results
- Fully responsive down to tablet width (sidebar collapses on narrow screens)
- All room/product imagery is represented with CSS gradient placeholders (`.p1`–`.p8` classes in `style.css`) — swap these `<div class="art pX">` blocks for real `<img>` tags once you have photography or generated assets.

## What's NOT implemented (front-end only)

This is a UI prototype — there's no backend yet. Not wired up:
- Real authentication / user accounts
- Actual AI image generation (the "Generate Designs" flow is a simulated delay, not a real model call)
- Persisting saved designs, cart, wishlist, or worker bookings
- Real product/worker data (everything is static placeholder content)
- Payments

## Suggested next steps

1. **Backend & data**: stand up an API (Node/Express, Django, etc.) for users, saved designs, products, and worker profiles.
2. **AI generation**: connect the "Generate Designs" flow to an actual image-generation model/service.
3. **Real imagery**: replace the `.art pX` placeholder divs with real photos or generated renders.
4. **State management**: if this grows past static pages, consider moving to a framework (React/Vue) once there's real dynamic data to manage.
5. **Auth & payments**: wire up account creation/login and a checkout flow for the Shopping page.

## Customizing the look

All colors, spacing, and radii live at the top of `assets/css/style.css` in the `:root` block — edit there to reskin the whole app in one place.
