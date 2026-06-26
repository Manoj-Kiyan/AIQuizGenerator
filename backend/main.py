from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json, random, os, httpx

# ─── DB Setup ───────────────────────────────────────────────
DATABASE_URL = "sqlite:///./quiz.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id         = Column(Integer, primary_key=True, index=True)
    topic      = Column(String(200))
    questions  = Column(Text)   # JSON string
    score      = Column(Integer, default=0)
    total      = Column(Integer, default=0)
    completed  = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ─── Mock Quiz Data (fallback when no API key) ───────────────
MOCK_QUIZZES = {
    "python": [
        {"question": "How do you write a list comprehension in Python?", "options": ["[x for x in range(10)]", "{x for x in range(10)}", "(x for x in range(10))", "x for x in range(10)"], "answer": 0, "explanation": "Square brackets are used to write list comprehensions in Python."},
        {"question": "Which symbol is used to create a dictionary in Python?", "options": ["[]", "()", "{}", "<>"], "answer": 2, "explanation": "Curly braces {} are used to create dictionaries."},
        {"question": "Which keyword is used to define a function in Python?", "options": ["func", "def", "function", "fn"], "answer": 1, "explanation": "The 'def' keyword is used to define functions in Python."},
        {"question": "What does 'None' represent in Python?", "options": ["0", "Empty string", "Null/absence of value", "False"], "answer": 2, "explanation": "'None' represents the absence of a value or a null value."},
        {"question": "What is the purpose of the __init__ method?", "options": ["To delete a class", "To initialize an object", "To import a module", "To open a file"], "answer": 1, "explanation": "__init__ is a constructor method that is automatically called when an object is created."},
    ],
    "javascript": [
        {"question": "What is the modern way to declare a variable in JavaScript?", "options": ["var x = 5", "let x = 5", "int x = 5", "dim x = 5"], "answer": 1, "explanation": "'let' and 'const' are the preferred ways to declare variables in modern JavaScript."},
        {"question": "What is the correct syntax for an arrow function?", "options": ["function => {}", "() => {}", "=> () {}", "fn() {}"], "answer": 1, "explanation": "The syntax for an arrow function is () => {}."},
        {"question": "How do you find the length of an array in JavaScript?", "options": ["array.size()", "array.length", "array.count()", "len(array)"], "answer": 1, "explanation": "Use the .length property to find the size of an array."},
        {"question": "What is a Promise in JavaScript?", "options": ["Synchronous operation", "Asynchronous operation result", "Error handler", "Variable type"], "answer": 1, "explanation": "A Promise represents the eventual result of an asynchronous operation."},
        {"question": "What does the typeof operator return?", "options": ["Value", "Variable name", "Data type as a string", "Memory address"], "answer": 2, "explanation": "The typeof operator returns the data type of its operand in the form of a string."},
    ],
    "html": [
        {"question": "How many levels of heading tags are there in HTML?", "options": ["4", "5", "6", "7"], "answer": 2, "explanation": "There are 6 levels of heading tags, from h1 to h6."},
        {"question": "Which attribute is mandatory in an image tag?", "options": ["class", "id", "alt", "style"], "answer": 2, "explanation": "The 'alt' attribute is mandatory for accessibility and SEO."},
        {"question": "Which input type is used to submit an HTML form?", "options": ["text", "button", "submit", "reset"], "answer": 2, "explanation": "type='submit' is used to submit forms."},
        {"question": "Which of the following is a semantic HTML element?", "options": ["<div>", "<span>", "<article>", "<b>"], "answer": 2, "explanation": "<article> is a semantic element that describes the meaning of its content."},
        {"question": "Which of the following is a new input type in HTML5?", "options": ["text", "password", "email", "submit"], "answer": 2, "explanation": "email, date, range, and color are among the new input types introduced in HTML5."},
    ],
    "sql": [
        {"question": "Which command is used to retrieve data in SQL?", "options": ["GET", "FETCH", "SELECT", "RETRIEVE"], "answer": 2, "explanation": "The SELECT command is used to retrieve data from a database."},
        {"question": "Which clause is used to combine rows from two or more tables?", "options": ["CONNECT", "JOIN", "MERGE", "LINK"], "answer": 1, "explanation": "The JOIN clause is used to combine multiple tables based on a related column."},
        {"question": "How do you remove duplicate rows from the result set?", "options": ["UNIQUE", "DISTINCT", "DIFFERENT", "SINGLE"], "answer": 1, "explanation": "SELECT DISTINCT is used to eliminate duplicate rows."},
        {"question": "What is the difference between WHERE and HAVING?", "options": ["They are the same thing", "WHERE filters rows, HAVING filters groups", "HAVING filters rows, WHERE filters groups", "No difference"], "answer": 1, "explanation": "WHERE is for row-level filtering, while HAVING is used for group filtering after a GROUP BY."},
        {"question": "What is a Primary key?", "options": ["The first column of a table", "A unique identifier for each row", "A foreign key reference", "An auto-incrementing number only"], "answer": 1, "explanation": "A primary key is a unique identifier for each row in a table and cannot contain NULL values."},
    ],
    "machine learning": [
        {"question": "What is required for Supervised learning?", "options": ["Only data", "Labeled training data", "Unlabeled data", "No data"], "answer": 1, "explanation": "Supervised learning requires labeled data consisting of inputs and expected outputs."},
        {"question": "What is Overfitting?", "options": ["The model is too simple", "The model memorizes training data but fails on new data", "Having too much training data", "Training happens too fast"], "answer": 1, "explanation": "Overfitting happens when a model memorizes the training data and performs poorly on unseen data."},
        {"question": "What is a CNN primarily used for?", "options": ["Text processing", "Image processing", "Audio processing", "Video only"], "answer": 1, "explanation": "Convolutional Neural Networks (CNN) are specialized for processing image and visual data."},
        {"question": "Why do we perform a Train/Test split?", "options": ["To save memory", "To evaluate the model on unseen data", "For faster training", "To completely remove overfitting"], "answer": 1, "explanation": "The test set is used to evaluate how well the model performs on data it has not seen before."},
        {"question": "What is Gradient descent?", "options": ["A data preprocessing step", "An optimization algorithm to minimize loss", "A feature selection method", "A model evaluation metric"], "answer": 1, "explanation": "Gradient descent is an optimization algorithm used to update weights by minimizing the loss function."},
    ],
}

def get_mock_quiz(topic: str, count: int = 5):
    topic_lower = topic.lower()
    for key in MOCK_QUIZZES:
        if key in topic_lower or topic_lower in key:
            return MOCK_QUIZZES[key][:count]
            
    all_q = []
    for q_list in MOCK_QUIZZES.values():
        all_q.extend(q_list)
    return random.sample(all_q, min(count, len(all_q)))

def extract_json_from_text(text: str):
    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("Could not find JSON array in the response")
    return json.loads(text[start:end])

# ─── AI Quiz Generation ────────────────────
async def generate_ai_quiz(topic: str, count: int, difficulty: str, provider: str, api_key: str):
    if not api_key or not provider:
        return get_mock_quiz(topic, count)

    prompt = f"""Generate {count} multiple choice quiz questions about "{topic}".
The difficulty level of the questions should be: {difficulty}.

Return ONLY a JSON array, no markdown formatting around it, no explanations before or after. The response must be perfectly valid JSON.
[
  {{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0,
    "explanation": "Brief explanation why this is correct"
  }}
]

Rules:
- 'answer' must be the integer index (0-3) of the correct option in the options array.
- Mix easy, medium, and hard questions.
- Make questions practical, clear, and educational.
- Provide the response purely in English."""

    headers = {}
    payload = {}
    url = ""
    
    provider = provider.lower()
    
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            if provider == "openai":
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                text = resp.json()["choices"][0]["message"]["content"]
                
            elif provider == "groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                text = resp.json()["choices"][0]["message"]["content"]
                
            elif provider == "gemini":
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                
            elif provider == "cohere":
                url = "https://api.cohere.com/v1/chat"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {"model": "command", "message": prompt}
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                text = resp.json()["text"]
                
            else:
                return get_mock_quiz(topic, count)
                
            return extract_json_from_text(text)
            
    except Exception as e:
        print(f"AI API error with {provider}: {e}")
        return get_mock_quiz(topic, count)

# ─── FastAPI App ──────────────────────────────────────────────
app = FastAPI(title="AI Quiz Generator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ─── API Routes ───────────────────────────────────────────────
class GenerateRequest(BaseModel):
    topic: str
    count: int = 5
    difficulty: str = "Medium"
    provider: str = ""
    api_key: str = ""

class SubmitRequest(BaseModel):
    session_id: int
    answers: list[int]

@app.get("/api/topics")
def get_topics():
    return {
        "featured": list(MOCK_QUIZZES.keys()),
        "suggestions": ["React", "CSS", "FastAPI", "Docker", "Git", "TypeScript", "MongoDB", "AWS"]
    }

@app.post("/api/generate")
async def generate_quiz(req: GenerateRequest):
    if not req.topic.strip():
        raise HTTPException(400, "Topic cannot be empty")
    
    questions = await generate_ai_quiz(req.topic.strip(), min(req.count, 10), req.difficulty, req.provider, req.api_key)
    
    db = SessionLocal()
    try:
        session = QuizSession(
            topic=f"{req.topic} ({req.difficulty})",
            questions=json.dumps(questions),
            total=len(questions)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        safe_questions = [{"question": q["question"], "options": q["options"]} for q in questions]
        return {"session_id": session.id, "topic": req.topic, "questions": safe_questions, "total": len(questions)}
    finally:
        db.close()

@app.post("/api/submit")
def submit_quiz(req: SubmitRequest):
    db = SessionLocal()
    try:
        session = db.query(QuizSession).filter(QuizSession.id == req.session_id).first()
        if not session:
            raise HTTPException(404, "Session not found")
        
        questions = json.loads(session.questions)
        score = 0
        results = []
        for i, q in enumerate(questions):
            user_ans = req.answers[i] if i < len(req.answers) else -1
            correct = q["answer"]
            is_correct = user_ans == correct
            if is_correct:
                score += 1
            results.append({
                "question": q["question"],
                "options": q["options"],
                "user_answer": user_ans,
                "correct_answer": correct,
                "is_correct": is_correct,
                "explanation": q.get("explanation", "")
            })
        
        session.score = score
        session.completed = True
        db.commit()
        
        percentage = round((score / len(questions)) * 100) if len(questions) > 0 else 0
        grade = "A+" if percentage >= 90 else "A" if percentage >= 80 else "B" if percentage >= 70 else "C" if percentage >= 60 else "F"
        
        return {"score": score, "total": len(questions), "percentage": percentage, "grade": grade, "results": results}
    finally:
        db.close()

@app.get("/api/history")
def get_history():
    db = SessionLocal()
    try:
        sessions = db.query(QuizSession).filter(QuizSession.completed == True).order_by(QuizSession.created_at.desc()).limit(10).all()
        return [{"id": s.id, "topic": s.topic, "score": s.score, "total": s.total, 
                 "percentage": round((s.score/s.total)*100) if s.total else 0,
                 "date": s.created_at.strftime("%d %b %Y, %I:%M %p")} for s in sessions]
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
