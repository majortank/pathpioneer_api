from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import random
import sqlite3

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    level: str
    industry: str
    focus_area: str
    topic: str

class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    level: str
    industry: str
    focus_area: str
    topic: str

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect('../pathpioneerapi/questions.db')
    cursor = conn.cursor()
    return conn, cursor

@app.get("/question/{level}")
async def get_question(level: str):
    conn, cursor = get_db()
    cursor.execute('SELECT * FROM questions WHERE level = ?', (level,))
    questions = cursor.fetchall()
    conn.close()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this level")

    random_question = random.choice(questions)
    response = QuestionResponse(question=random_question[1], options=random_question[2].split(","), correct_answer=random_question[3], level=random_question[4], industry=random_question[5], focus_area=random_question[6], topic=random_question[7])
    return response

@app.get("/question/all/{level}")
async def get_all_questions(level: str):
    conn, cursor = get_db()
    cursor.execute('SELECT * FROM questions WHERE level = ?', (level,))
    questions = cursor.fetchall()
    conn.close()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this level")

    response_data = [{"question": question[1], "options": question[2].split(","), "correct_answer": question[3], "level": question[4], "industry": question[5], "focus_area": question[6], "topic": question[7]} for question in questions]
    return response_data

@app.post("/question/create/")
async def create_questions(questions: List[QuestionCreate]):
    conn, cursor = get_db()
    question_ids = []
    for question in questions:
        cursor.execute('''
            INSERT INTO questions (question, options, correct_answer, level, industry, focus_area, topic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (question.question, ",".join(question.options), question.correct_answer, question.level, question.industry, question.focus_area, question.topic))
        conn.commit()
        question_id = cursor.lastrowid
        question_ids.append(question_id)
    conn.close()
    return {"message": "Questions created successfully", "question_ids": question_ids}

@app.put("/question/update/{question_id}")
async def update_question(question_id: int, question: QuestionCreate):
    conn, cursor = get_db()
    cursor.execute('''
        UPDATE questions
        SET question = ?, options = ?, correct_answer = ?, level = ?, industry = ?, focus_area = ?, topic = ?
        WHERE id = ?
    ''', (question.question, ",".join(question.options), question.correct_answer, question.level, question.industry, question.focus_area, question.topic, question_id))
    conn.commit()
    conn.close()
    return {"message": "Question updated successfully"}

@app.delete("/question/delete/{question_id}")
async def delete_question(question_id: int):
    conn, cursor = get_db()
    cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    return {"message": "Question deleted successfully"}
