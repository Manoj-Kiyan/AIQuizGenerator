# 🧠 AI Quiz Generator — Full Stack App

## Tech Stack
- **Backend**: Python + FastAPI
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML5 + Vanilla JS
- **AI**: Anthropic Claude API (optional — mock data works without it!)

---

## Setup & Run (5 Steps!)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) AI enable பண்ண — API key add பண்ணு
```bash
export ANTHROPIC_API_KEY=your_key_here
```
> API key இல்லாம் run பண்ணினாலும் **Mock data** automatically use ஆகும்! ✅

### 3. Start the server
```bash
cd backend
python main.py
```

### 4. Browser-ல் open பண்ணு
```
http://localhost:8000
```

---

## Features

| Feature | Details |
|---------|---------|
| 🤖 AI Quiz | Claude API → auto generate questions |
| 📦 Mock Data | API key இல்லாம் 5 built-in topics |
| 💾 SQLite DB | Sessions + scores save ஆகும் |
| 📊 Results | Grade, score %, detailed review |
| 📜 History | Last 10 quiz sessions |
| 🔥 Topics | Python, JS, HTML, SQL, ML built-in |

## Mock Topics (No API key needed!)
- `python`
- `javascript`
- `html`
- `sql`
- `machine learning`

---

## API Endpoints

```
GET  /api/topics    → Available topics list
POST /api/generate  → Generate quiz {topic, count}
POST /api/submit    → Submit answers {session_id, answers}
GET  /api/history   → Recent quiz history
```

## Project Structure
```
quiz-app/
├── backend/
│   └── main.py       # FastAPI app + SQLite models
├── frontend/
│   └── index.html    # Single-page HTML5 app
├── requirements.txt
└── README.md
```
