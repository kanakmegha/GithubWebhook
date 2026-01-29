import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

# Vercel setup: Look for templates in the root folder
app = Flask(__name__, template_folder='../templates')

# MongoDB helper
def get_db():
    uri = os.environ.get("MONGO_URI")
    if not uri:
        return None
    try:
        # 5-second timeout ensures the app doesn't hang if DB is slow
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return client['github_events']['actions']
    except:
        return None

@app.route('/test')
def test():
    return "App is alive and routes are configured!", 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/latest', methods=['GET'])
def get_latest():
    collection = get_db()
    if collection is None:
        return jsonify([])
    # Fetch last 10 entries
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return jsonify(docs)

@app.route('/webhook', methods=['POST'])
def webhook():
    collection = get_db()
    if collection is None:
        return "Database Connection Failed", 500

    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    entry = {
        "author": data.get('sender', {}).get('login', 'Unknown'),
        "timestamp": datetime.now().strftime('%d %B %Y - %I:%M %p')
    }

    if event_type == "push":
        entry["action"] = "PUSH"
        entry["to_branch"] = data.get('ref', '').split('/')[-1]
    
    elif event_type == "pull_request":
        action = data.get('action')
        pr = data.get('pull_request', {})
        if action == "closed" and pr.get('merged'):
            entry["action"] = "MERGE"
        else:
            entry["action"] = "PULL_REQUEST"
        entry["from_branch"] = pr.get('head', {}).get('ref')
        entry["to_branch"] = pr.get('base', {}).get('ref')

    if "action" in entry:
        collection.insert_one(entry)
        return "Success", 200
    
    return "Event ignored", 200
@app.route('/debugdb')
def debug_db():
    uri = os.environ.get("MONGO_URI")
    if not uri:
        return "Error: MONGO_URI environment variable is missing!", 500
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping') # This tests the actual connection
        return "Success: Connected to MongoDB!", 200
    except Exception as e:
        return f"Connection Failed: {str(e)}", 500