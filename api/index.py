import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Vercel path fix: ensures it finds the templates folder correctly
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# Initialize MongoDB safely
def get_db_collection():
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Force a connection check
        client.admin.command('ping') 
        return client['github_events']['actions']
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    collection = get_db_collection()
    if collection is None:
        return jsonify([{"author": "System", "action": "ERROR", "timestamp": "Check MONGO_URI in Vercel settings"}])
    
    docs = list(collection.find().sort("_id", -1).limit(10))
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return jsonify(docs)

@app.route('/webhook', methods=['POST'])
def webhook():
    # ... (Your existing webhook logic here) ...
    return "OK", 200