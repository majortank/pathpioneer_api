from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import random
import firebase_admin
from firebase_admin import credentials, firestore
import markdown
from datetime import datetime



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

class Notification(BaseModel):
    title: str
    content: str
    version: str
    type: str

class NotificationResponse(Notification):
    timestamp: str
    id: str

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ASCII art for a question mark
QUESTION_MARK = r"""
   _
  /?\
  \__/
"""

# Helper function to generate interesting 404 responses
def get_interesting_404_message(level: str):
    if level.lower() == "advanced":
        return f"🚀 Wow, you've reached the advanced level! No questions found here. Keep exploring! {QUESTION_MARK}"
    return f"🤔 No questions found for '{level}' level. Try a different level or create your own questions! {QUESTION_MARK}"

# Endpoints with enhanced responses
@app.get("/question/{level}")
async def get_question(level: str):
    questions_ref = db.collection('questions')
    query = questions_ref.where('level', '==', level).stream()
    questions = [doc.to_dict() for doc in query]

    if not questions:
        raise HTTPException(status_code=404, detail=get_interesting_404_message(level))

    random_question = random.choice(questions)
    response = QuestionResponse(**random_question)
    return response

@app.get("/question/all/{level}")
async def get_all_questions(level: str):
    questions_ref = db.collection('questions')
    query = questions_ref.where('level', '==', level).stream()
    questions = [doc.to_dict() for doc in query]

    if not questions:
        raise HTTPException(status_code=404, detail=get_interesting_404_message(level))

    return questions


def question_exists(question_text):
    # Implement logic to check if a question with the provided text already exists in Firebase
    questions_ref = db.collection('questions')
    query = questions_ref.where('question', '==', question_text).limit(1)

    existing_questions = query.get()

    return len(existing_questions) > 0 if existing_questions else False



@app.post("/question/create")
async def create_question(questions_data: List[QuestionCreate]):
    if not questions_data:
        raise HTTPException(status_code=400, detail="No questions provided")

    batch = db.batch()

    for question_data in questions_data:
        # Check if the question already exists in Firebase
        if question_exists(question_data.question):
            raise HTTPException(status_code=400, detail="Question already exists")

        new_question_ref = db.collection('questions').document()
        batch.set(new_question_ref, question_data.dict())

    batch.commit()

    return {"message": "Questions created successfully"}



@app.put("/question/update/{question_id}")
async def update_question(question_id: str, question: QuestionCreate):
    questions_ref = db.collection('questions')
    questions_ref.document(question_id).set(question.dict(), merge=True)
    return {"message": "Question updated successfully"}

@app.delete("/question/delete/{question_id}")
async def delete_question(question_id: str):
    questions_ref = db.collection('questions')
    questions_ref.document(question_id).delete()
    return {"message": "Question deleted successfully"}

# Endpoints for notifications

# Create a notification
@app.post("/notifications", response_model=NotificationResponse)
async def create_notification(notification: Notification):
    doc_ref = db.collection('notifications').document()
    id = doc_ref.id
    timestamp = datetime.now().isoformat()
    notification_data = notification.dict()
    notification_data.update({"id": id, "timestamp": timestamp})
    doc_ref.set(notification_data)
    return NotificationResponse(**notification_data)

@app.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications():
    docs = db.collection('notifications').stream()
    return [NotificationResponse(**doc.to_dict()) for doc in docs]

@app.put("/notifications/{id}", response_model=NotificationResponse)
async def update_notification(id: str, notification: Notification):
    doc_ref = db.collection('notifications').document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification_data = notification.dict()
    notification_data.update({"id": id, "timestamp": doc.to_dict()["timestamp"]})
    doc_ref.set(notification_data)
    return NotificationResponse(**notification_data)

@app.delete("/notifications/{id}")
async def delete_notification(id: str):
    doc_ref = db.collection('notifications').document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Notification not found")
    doc_ref.delete()
    return {"detail": "Notification deleted"}


# Default endpoint displaying full API documentation
@app.get("/")
async def read_root():
    with open("api_documentation.md", "r") as file:
        documentation_content = file.read()
        # Convert Markdown content to HTML
        html_content = markdown.markdown(documentation_content)
    return HTMLResponse(content=html_content)
