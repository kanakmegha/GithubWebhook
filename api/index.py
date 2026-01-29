import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

# Vercel-specific pathing: Look for 'templates' in the root folder
# (One level up from this 'api' folder)
app = Flask(__name__, template_folder='../templates')

# Initialize MongoDB safely
def get_db_collection():
    # Vercel automatically provides this from your Project Settings
    uri = os.environ.get("MONGO_URI") 
    if not uri:
        print("CRITICAL: MONGO_URI not found in Environment Variables")
        return None
    try:
        # We use a 5-second timeout so the app doesn't hang forever if DB is down
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return client['github_events']['actions']
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/test')
def test():
    return "App is alive!", 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    collection = get_db_collection()
    if collection is None:
        return jsonify([{"author": "System", "action": "ERROR", "timestamp": "Check MONGO_URI in Vercel settings"}])
    
    try:
        docs = list(collection.find().sort("_id", -1).limit(10))
        for doc in docs:
            doc['_id'] = str(doc['_id'])
        return jsonify(docs)
    except Exception as e:
        return jsonify([{"author": "System", "action": "DB_ERROR", "timestamp": str(e)}])

@app.route('/webhook', methods=['POST'])
def webhook():
    # Your webhook logic here...
    return "OK", 200