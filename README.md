# 🏸 Court Booker PWA
Badminton booking dashboard for the Rugby group — Queen's Diamond Jubilee Centre.

## Files
- `app.py` — Flask server + booking data API
- `requirements.txt` — Python dependencies
- `render.yaml` — Render deployment config
- `public/index.html` — The full PWA app
- `public/manifest.json` — PWA manifest (makes it installable)
- `public/sw.js` — Service worker (offline support)
- `public/icon-192.svg` — App icon

## Deploy Steps

### 1. GitHub
1. github.com → Sign up / log in
2. New repository → name: `badminton-booker` → Public → Create
3. Add file → Upload files → upload ALL files (keeping the `public/` folder structure)
4. Commit changes

### 2. Render
1. render.com → Sign up free
2. New → Web Service → Connect GitHub → select `badminton-booker`
3. Render reads `render.yaml` automatically → Deploy
4. Wait ~3 mins → get your live URL

### 3. Install on phone

**Android (Chrome):**
Open URL → 3-dot menu → Add to Home Screen → Install

**iPhone (Safari):**
Open URL → Share button → Add to Home Screen → Add

Days: Monday, Wednesday, Thursday
