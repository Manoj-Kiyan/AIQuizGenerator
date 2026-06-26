🧠 AI Quiz Generator

An AI-powered quiz application built with FastAPI, SQLite, and Vanilla JavaScript. Generate quizzes on different topics, submit answers, track scores, and view quiz history. If an Anthropic Claude API key is not provided, the application automatically uses built-in mock questions.

---

🚀 Tech Stack

- Backend: Python + FastAPI
- Database: SQLite (SQLAlchemy)
- Frontend: HTML5 + Vanilla JavaScript
- AI: Anthropic Claude API (Optional)

---

📂 Project Structure

quiz-app/
├── backend/
│   └── main.py
├── frontend/
│   └── index.html
├── requirements.txt
└── README.md

---

⚙️ Installation

1. Install dependencies

pip install -r requirements.txt

2. (Optional) Configure Claude API

export ANTHROPIC_API_KEY=your_api_key

«If no API key is provided, the application automatically uses mock quiz data.»

3. Start the server

cd backend
python main.py

4. Open in your browser

http://localhost:8000

---

✨ Features

- 🤖 AI-generated quizzes using Claude API
- 📦 Built-in mock quizzes (No API key required)
- 💾 SQLite database for storing quiz sessions and scores
- 📊 Instant results with score, percentage, and grade
- 📜 Quiz history (Last 10 attempts)
- 🎯 Multiple built-in quiz topics

---

📚 Available Topics

- Python
- JavaScript
- HTML
- SQL
- Machine Learning

---

🔌 API Endpoints

Method| Endpoint| Description
GET| "/api/topics"| Get available quiz topics
POST| "/api/generate"| Generate a new quiz
POST| "/api/submit"| Submit quiz answers
GET| "/api/history"| View recent quiz history

---

📝 Example Request

Generate a quiz:

POST /api/generate

{
  "topic": "python",
  "count": 5
}

Submit answers:

POST /api/submit

{
  "session_id": 1,
  "answers": [0, 2, 1, 3, 0]
}

---

📌 Notes

- No API key is required to run the project.
- Mock quiz data is used automatically when the Claude API is unavailable.
- Quiz sessions and scores are stored locally using SQLite.

---

📄 License

This project is open-source and intended for learning and educational purposes.