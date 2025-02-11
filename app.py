from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS
from datetime import datetime
import xgbmodel from "../assets/icons/xgb_pipeline_compressed.joblib"

app = Flask(__name__)
CORS(app)

# ✅ Load ML Model
try:
    model = joblib.load(xgbmodel)  # Adjust path if needed
    print("✅ Model loaded successfully!")
except Exception as e:
    model = None
    print(f"⚠️ Error loading model: {e}")

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
            "POST /results": "Submit quiz scores and get results"
        }
    })

@app.route("/questions", methods=["GET"])
def get_questions():
    questions = [
    # Personality Traits Questions
    # 1. Openness to Experience
    {
        "id": "O1",
        "category": "Openness",
        "question": "I enjoy trying out new and unfamiliar activities.",
        "options": [
            {"text": "Strongly Agree", "value": 5},
            {"text": "Agree", "value": 3.75},
            {"text": "Neutral", "value": 2.5},
            {"text": "Disagree", "value": 1.25},
        ],
    },
    {
        "id": "O2",
        "category": "Openness",
        "question": "How often do you engage in creative activities like painting, writing, or music?",
        "options": [
            {"text": "Very Often", "value": 5},
            {"text": "Sometimes", "value": 3.75},
            {"text": "Rarely", "value": 2.5},
            {"text": "Never", "value": 1.25},
        ],
    },
    # 2. Conscientiousness
    {
        "id": "C1",
        "category": "Conscientiousness",
        "question": "How do you handle tasks and responsibilities?",
        "options": [
            {"text": "Plan everything in advance and stay organized", "value": 5},
            {"text": "Try to plan but sometimes procrastinate", "value": 3.75},
            {"text": "Often leave things for the last moment", "value": 2.5},
            {"text": "Handle things spontaneously without planning", "value": 1.25},
        ],
    },
    {
        "id": "C2",
        "category": "Conscientiousness",
        "question": "How well do you follow schedules and deadlines?",
        "options": [
            {"text": "Always meet deadlines and stay on track", "value": 5},
            {"text": "Mostly follow deadlines with few delays", "value": 3.75},
            {"text": "Often struggle with deadlines", "value": 2.5},
            {"text": "Rarely follow a fixed schedule", "value": 1.25},
        ],
    },
    # 3. Extraversion
    {
        "id": "E1",
        "category": "Extraversion",
        "question": "How do you feel about social gatherings?",
        "options": [
            {"text": "I love them and enjoy meeting new people", "value": 5},
            {"text": "I like them but prefer familiar groups", "value": 3.75},
            {"text": "I don't mind them but don't actively seek them out", "value": 2.5},
            {"text": "I avoid them whenever possible", "value": 1.25},
        ],
    },
    {
        "id": "E2",
        "category": "Extraversion",
        "question": "How often do you initiate conversations in a social setting?",
        "options": [
            {"text": "Almost always", "value": 5},
            {"text": "Sometimes, depending on the situation", "value": 3.75},
            {"text": "Rarely, I wait for others to start", "value": 2.5},
            {"text": "Never, I prefer to stay quiet", "value": 1.25},
        ],
    },
    # 4. Agreeableness
    {
        "id": "A1",
        "category": "Agreeableness",
        "question": "How do you usually respond to conflicts with others?",
        "options": [
            {"text": "Try to find a fair solution for everyone", "value": 5},
            {"text": "Compromise if necessary but stand my ground", "value": 3.75},
            {"text": "Defend my viewpoint strongly", "value": 2.5},
            {"text": "Avoid the issue and let things escalate", "value": 1.25},
        ],
    },
    {
        "id": "A2",
        "category": "Agreeableness",
        "question": "How do you react if a friend needs help with a difficult task?",
        "options": [
            {"text": "Help immediately without hesitation", "value": 5},
            {"text": "Help if it's convenient for me", "value": 3.75},
            {"text": "Consider but usually decline", "value": 2.5},
            {"text": "Avoid helping altogether", "value": 1.25},
        ],
    },
    # 5. Neuroticism
    {
        "id": "N1",
        "category": "Neuroticism",
        "question": "How often do you feel anxious or stressed?",
        "options": [
            {"text": "Almost all the time", "value": 5},
            {"text": "Frequently but I manage it", "value": 3.75},
            {"text": "Occasionally, but not a big issue", "value": 2.5},
            {"text": "Rarely or never", "value": 1.25},
        ],
    },
    {
        "id": "N2",
        "category": "Neuroticism",
        "question": "When faced with a failure, how do you respond?",
        "options": [
            {"text": "Feel overwhelmed and struggle to move on", "value": 5},
            {"text": "Get upset but try to learn from it", "value": 3.75},
            {"text": "Acknowledge it but move on quickly", "value": 2.5},
            {"text": "Accept it easily and stay unaffected", "value": 1.25},
        ],
    },
    # Cognitive Aptitude Questions
    {
        "id": "NA1",
        "category": "Numerical Aptitude",
        "question": "If the price of an item increases by 20% and then decreases by 20%, what is the final percentage change?",
        "options": [
            {"text": "0%", "value": 1.25},
            {"text": "-4%", "value": 5},
            {"text": "+4%", "value": 2.5},
            {"text": "-2%", "value": 3.75},
        ],
    },
    {
        "id": "NA2",
        "category": "Numerical Aptitude",
        "question": "A train moves at a speed of 60 km/h. How much time will it take to cover 300 km?",
        "options": [
            {"text": "3 hours", "value": 2.5},
            {"text": "5 hours", "value": 5},
            {"text": "6 hours", "value": 1.25},
            {"text": "4 hours", "value": 3.75},
        ],
    },
    {
        "id": "SA1",
        "category": "Spatial Aptitude",
        "question": "Which shape will be formed when a cube is unfolded?",
        "options": [
            {"text": "A rectangle", "value": 1.25},
            {"text": "A cross-shaped net", "value": 5},
            {"text": "A triangle", "value": 2.5},
            {"text": "A pentagon", "value": 3.75},
        ],
    },
    {
        "id": "SA2",
        "category": "Spatial Aptitude",
        "question": "How will the reflection appear if a mirror is placed on the right side of an object?",
        "options": [
            {"text": "Left and right are reversed", "value": 5},
            {"text": "Upside-down", "value": 2.5},
            {"text": "No change in orientation", "value": 1.25},
            {"text": "Only the top and bottom are reversed", "value": 3.75},
        ],
    },
    {
        "id": "PA1",
        "category": "Perceptual Aptitude",
        "question": "Find the odd one out: Circle, Triangle, Sphere, Square.",
        "options": [
            {"text": "Circle", "value": 1.25},
            {"text": "Sphere", "value": 5},
            {"text": "Triangle", "value": 2.5},
            {"text": "Square", "value": 3.75},
        ],
    },
    {
        "id": "PA2",
        "category": "Perceptual Aptitude",
        "question": "Which number is missing in the series? 2, 6, 12, 20, __, 42",
        "options": [
            {"text": "28", "value": 3.75},
            {"text": "30", "value": 1.25},
            {"text": "32", "value": 2.5},
            {"text": "36", "value": 5},
        ],
    },
    {
        "id": "AR1",
        "category": "Abstract Reasoning",
        "question": "If CIRCLE is coded as RICELC, how would SQUARE be coded?",
        "options": [
            {"text": "QSUERA", "value": 5},
            {"text": "UQSAER", "value": 1.25},
            {"text": "ERSQUA", "value": 2.5},
            {"text": "SUQARE", "value": 3.75},
        ],
    },
    {
        "id": "AR2",
        "category": "Abstract Reasoning",
        "question": "If A = 1, B = 2, and C = 3... then what is the sum of the letters in the word \"DOG\"?",
        "options": [
            {"text": "26", "value": 2.5},
            {"text": "24", "value": 5},
            {"text": "20", "value": 1.25},
            {"text": "22", "value": 3.75},
        ],
    },
    {
        "id": "VR1",
        "category": "Verbal Reasoning",
        "question": "Which word best completes the sentence? \"The scientist conducted an ___ experiment to test the hypothesis.\"",
        "options": [
            {"text": "Amazing", "value": 1.25},
            {"text": "Controlled", "value": 5},
            {"text": "Random", "value": 2.5},
            {"text": "Impossible", "value": 3.75},
        ],
    },
    {
        "id": "VR2",
        "category": "Verbal Reasoning",
        "question": "Choose the correct synonym for \"Innovative.\"",
        "options": [
            {"text": "Traditional", "value": 1.25},
            {"text": "Creative", "value": 5},
            {"text": "Boring", "value": 2.5},
            {"text": "Risky", "value": 3.75},
        ],
    },
]
    return jsonify({
        "status": "success",
        "count": len(questions),
        "categories": [
            "Medical & Healthcare", "Engineering & Technology", "Science & Research",
            "Finance & Business", "Creative & Design", "Education & Training",
            "Law & Government", "Administration & HR", "Social & Public Services",
            "Miscellaneous & Specialized Roles"
        ],
        "questions": questions
    })

@app.route("/results", methods=["POST"])
def store_results():
    try:
        data = request.json
        if not data or 'scores' not in data:
            return jsonify({"error": "⚠️ Invalid data format, 'scores' field is required!"}), 400
        
        # Get the original scores array from the request.
        scores = data['scores']
        
        # Transform the scores: group every 2 responses (question 1 & 2, 3 & 4, etc.)
        transformed_scores = []
        for i in range(0, len(scores), 2):
            avg = float((scores[i] + scores[i + 1]))   # Average the two scores
            transformed_scores.append(avg)
        
        # Log the transformed array in the console
        print("Transformed Scores:", transformed_scores)
        
        timestamp = datetime.now().isoformat()
        
        # Get the prediction without converting to int (since our model returns a string)
        prediction_value = model.predict([transformed_scores])[0] if model else None
        
        # Map the prediction string to a career using string keys
        career_map = {
            "Medical & Healthcare": {"career": "Medical & Healthcare", "description": "Best suited for medical sciences."},
            "Engineering & Technology": {"career": "Engineering & Technology", "description": "Perfect for logical thinkers."},
            "Science & Research": {"career": "Science & Research", "description": "Ideal for analytical minds."},
            "Finance & Business": {"career": "Finance & Business", "description": "For problem-solvers in finance."},
            "Creative & Design": {"career": "Creative & Design", "description": "Great for artists and creators."},
            "Education & Training": {"career": "Education & Training", "description": "For those who love teaching."},
            "Law & Government": {"career": "Law & Government", "description": "Ideal for leaders and policy-makers."},
            "Administration & HR": {"career": "Administration & HR", "description": "Best fit for organization management."},
            "Social & Public Services": {"career": "Social & Public Services", "description": "For those passionate about impact."},
            "Miscellaneous & Specialized Roles": {"career": "Miscellaneous & Specialized Roles", "description": "For unique and hybrid careers."}
        }
        
        mapped_prediction = career_map.get(prediction_value, {"career": "Unknown", "description": "No mapping found."})
        
        result = {
            "original_scores": scores,
            "transformed_scores": transformed_scores,
            "timestamp": timestamp,
            "prediction": mapped_prediction
        }

        return jsonify({
            "status": "success",
            "message": "Results computed successfully",
            "result": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
