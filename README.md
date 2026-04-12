# Compass

**Your AI, guided by the Voices who know you.**

Compass is a guidance network platform where trusted people -- doctors, caregivers, coaches, family -- control how AI interacts with you. The AI channels human wisdom, not its own opinions.

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Demo Personas

- **Margaret** (74, independent elder): Voices from Dr. Patel (doctor), Lisa (caregiver), Jake & Emma (grandchildren)
- **David** (35, fitness enthusiast): Voices from Coach Mike (coach), Sarah (partner)

## Demo Script

1. Open **Voices** tab -- browse each Voice's guidance
2. Open **My Compass** tab -- see all guidance in one transparent view
3. Open **Chat** tab -- ask Margaret: "I have a headache, can I take ibuprofen?"
4. Watch the AI respond guided by Dr. Patel's safety rules
5. Ask: "What's a nice thing I could do today?" -- see grandkids' guidance shine
6. Switch to David, log a workout, ask "How was my day?"
7. Try: "I'll skip legs tomorrow" -- Coach Mike pushes back
8. Go to Voices, add a new guideline live, then ask a related question -- see it reflected immediately
# Compass
