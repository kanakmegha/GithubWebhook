import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

# Vercel-friendly pathing for templates
app = Flask(__name__, template_folder='../templates')

# MongoDB Connection
def get_db():
    uri = os.environ.get("MONGO_URI")
    if not uri:
        return None
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return client['github_events']['actions']
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/latest', methods=['GET'])
def get_latest():
    collection = get_db()
    if collection is None:
        return jsonify([])
    # Get last 10 events
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return jsonify(docs)

@app.route('/webhook', methods=['POST'])
def webhook():
    collection = get_db()
    if collection is None:
        return "DB Connection Failed", 500

    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    # Standard info for all events
    entry = {
        "author": data.get('sender', {}).get('login', 'Unknown'),
        "timestamp": datetime.now().strftime('%d %B %Y - %I:%M %p')
    }

    # Custom logic based on the event type
    if event_type == "push":
        entry["action"] = "PUSH"
        entry["to_branch"] = data.get('ref', '').split('/')[-1]
    
    elif event_type == "pull_request":
        action = data.get('action') # 'opened', 'closed', etc.
        pr = data.get('pull_request', {})
        
        if action == "closed" and pr.get('merged') == True:
            entry["action"] = "MERGE"
        else:
            entry["action"] = "PULL_REQUEST"
            
        entry["from_branch"] = pr.get('head', {}).get('ref')
        entry["to_branch"] = pr.get('base', {}).get('ref')

    # Save to MongoDB if it's an event we care about
    if "action" in entry:
        collection.insert_one(entry)
        return "Event Stored", 200
    
    return "Event ignored", 200