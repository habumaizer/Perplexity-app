from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests
import pymongo
from pymongo import MongoClient
from transformers import pipeline
from better_profanity import profanity
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.chat_db
threads_collection = db.threads

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

summarizer = pipeline("summarization")

templates = Jinja2Templates(directory="templates")

router = APIRouter()

def check_politeness(query: str) -> bool:
    return not profanity.contains_profanity(query)

def generate_follow_up_recommendations(response: str):
    summary = summarizer(response, max_length=60, min_length=20, do_sample=False)[0]['summary_text']

    sentences = summary.split('. ')
    questions = [f"Can you explain more about '{sentence.strip()}?'" for sentence in sentences if sentence]

    return questions[:4]

def process_query(query: str, user_id: str):
    if not check_politeness(query):
        return "Your query contains inappropriate content. Please rephrase your query.", []

    thread = threads_collection.find_one({"user_id": user_id})
    if not thread:
        thread = {"user_id": user_id, "conversation": []}
        threads_collection.insert_one(thread)
    
    messages = [{"role": "system", "content": "Be precise and concise."}]
    for q, r in thread["conversation"]:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": r})
    messages.append({"role": "user", "content": query})

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": messages
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {PERPLEXITY_API_KEY}"
    }

    response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
    data = response.json()

    ai_response = data.get("choices", [{}])[0].get("message", {}).get("content", "I'm not sure about that. Can you provide more details?")

    thread["conversation"].append((query, ai_response))
    threads_collection.update_one({"user_id": user_id}, {"$set": {"conversation": thread["conversation"]}})

    recommendations = generate_follow_up_recommendations(ai_response)

    return ai_response, recommendations

@router.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, user_query: str = Form(...)):
    user_id = request.client.host
    response, recommendations = process_query(user_query, user_id)
    return templates.TemplateResponse("index.html", {"request": request, "response": response, "recommendations": recommendations})
