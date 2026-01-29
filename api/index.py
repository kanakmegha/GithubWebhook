from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
load_env()

app = Flask(__name__, template_folder='../templates')

# MongoDB Connection
# Replace with your Atlas string or set it in Vercel Environment Variables
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['github_events']
collection = db['actions']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    entry = {
        "author": data.get('sender', {}).get('login'),
        "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
    }

    if event_type == "push":
        entry["action"] = "PUSH"
        entry["to_branch"] = data.get('ref', '').split('/')[-1]
    elif event_type == "pull_request":
        pr = data.get('pull_request', {})
        if data.get('action') == 'closed' and pr.get('merged'):
            entry["action"] = "MERGE"
        else:
            entry["action"] = "PULL_REQUEST"
        entry["from_branch"] = pr.get('head', {}).get('ref')
        entry["to_branch"] = pr.get('base', {}).get('ref')

    if "action" in entry:
        collection.insert_one(entry)
    return "OK", 200

@app.route('/api/latest')
def get_latest():
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return jsonify(docs)