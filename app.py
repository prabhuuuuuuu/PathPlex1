from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS
from datetime import datetime

app = Flask(_name_)
CORS(app)

# ✅ Load ML Model
try:
    model = joblib.load(r"C:\\Users\\Shourya\\Downloads\\xgb_pipeline_compressed.joblib")  # Adjust path if needed
    print("✅ Model loaded successfully!")
except Exception as e:
    model = None
    print(f"⚠ Error loading model: {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "🚀 PathPlex API is Live!",
        "api_version": "1.0.0",
        "backend": "Flask",
        "ml_model": "Loaded ✅" if model else "Not Loaded ❌",
        "available_endpoints": {
            "GET /": "API Home",
            "GET /questions": "Fetch quiz questions",
            "POST /predict": "Submit quiz responses for prediction",
            "POST /results": "Submit quiz scores an
