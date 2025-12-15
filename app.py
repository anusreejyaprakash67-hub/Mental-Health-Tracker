from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "replace_with_a_secure_random_key"

# --- Questions (21) DASS-21 Scale ---
questions = [
    "I found it hard to wind down.",
    "I was aware of dryness of my mouth.",
    "I couldn't seem to experience any positive feeling at all.",
    "I experienced breathing difficulty.",
    "I found it difficult to work up the initiative to do things.",
    "I tended to over-react to situations.",
    "I experienced trembling.",
    "I felt that I was using a lot of nervous energy.",
    "I was worried about situations in which I might panic.",
    "I felt down-hearted and blue.",
    "I found myself getting agitated.",
    "I found it difficult to relax.",
    "I felt that I was close to panic.",
    "I felt I wasn't worth much as a person.",
    "I felt that I was rather touchy.",
    "I felt scared without any good reason.",
    "I felt that life was meaningless.",
    "I experienced heart palpitations.",
    "I felt that I had nothing to look forward to.",
    "I felt restless and fidgety.",
    "I felt that I was intolerant of anything."
]

# --- Index groups (0-based indices into `questions`) ---
depression_idx = [2, 4, 9, 13, 16, 18]  # 6 items
anxiety_idx = [1, 3, 6, 8, 11, 14, 17]  # 7 items
stress_idx = [0, 5, 7, 10, 12, 15, 19, 20]  # 8 items

# --- Profession options for login ---
PROFESSIONS = [
    "School Student",
    "College Student",
    "IT Professional",
    "Government Job",
    "Education Sector",
    "Executives",
    "Other"
]

# --- Indian States ---
STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# --- Severity classification functions ---
def classify_depression(score):
    # DASS-21 scaled by 2 usual thresholds
    if score <= 9:
        return "Normal"
    if 10 <= score <= 13:
        return "Mild"
    if 14 <= score <= 20:
        return "Moderate"
    if 21 <= score <= 27:
        return "Severe"
    return "Extremely Severe"

def classify_anxiety(score):
    if score <= 7:
        return "Normal"
    if 8 <= score <= 9:
        return "Mild"
    if 10 <= score <= 14:
        return "Moderate"
    if 15 <= score <= 19:
        return "Severe"
    return "Extremely Severe"

def classify_stress(score):
    if score <= 14:
        return "Normal"
    if 15 <= score <= 18:
        return "Mild"
    if 19 <= score <= 25:
        return "Moderate"
    if 26 <= score <= 33:
        return "Severe"
    return "Extremely Severe"

# --- Advice mapping ---
ADVICE = {
    "Depression": {
        "Normal": "No clinical sign of depression. Keep maintaining healthy routines: regular sleep, exercise, and social connection.",
        "Mild": "Mild depressive symptoms—try journaling, light exercise, structured routine, and talking with someone you trust.",
        "Moderate": "Moderate depression—consider starting brief therapy or counseling and using structured behavioral activation techniques.",
        "Severe": "Severe symptoms—please seek professional mental health support (therapist/psychiatrist) soon.",
        "Extremely Severe": "Extremely severe symptoms—contact a mental health professional immediately; if at risk, seek urgent care."
    },
    "Anxiety": {
        "Normal": "No current clinical anxiety. Continue relaxation habits and stress management.",
        "Mild": "Mild anxiety—practice daily breathing exercises, short mindfulness sessions, and reduce stimulants.",
        "Moderate": "Moderate anxiety—try guided CBT techniques, regular exercise, and consider talking to a counselor.",
        "Severe": "Severe anxiety—consult a mental health professional; consider structured therapy and medical advice if needed.",
        "Extremely Severe": "Extremely severe anxiety—seek urgent professional help; if incapacitated, contact emergency services."
    },
    "Stress": {
        "Normal": "Stress levels are within normal limits. Keep balanced work-rest cycles and self-care.",
        "Mild": "Mild stress—use time management, short relaxation breaks, and hobbies to unwind.",
        "Moderate": "Moderate stress—prioritise tasks, set boundaries, and consider short-term counseling if helpful.",
        "Severe": "Severe stress—speak to a professional or counsellor; consider stress-management programs.",
        "Extremely Severe": "Extremely severe stress—seek urgent support from a mental health professional."
    }
}

# --- Helper to compute scores ---
def compute_scores(answers):
    # answers: list of 21 ints (0-3)
    dep = sum(answers[i] for i in depression_idx) * 2
    anx = sum(answers[i] for i in anxiety_idx) * 2
    strt = sum(answers[i] for i in stress_idx) * 2
    return dep, anx, strt

# --- ROUTES ---

@app.route('/')
def index():
    """Landing page - redirects to login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with user demographic information"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        profession = request.form.get('profession', '').strip()
        state = request.form.get('state', '').strip()
        
        # Validate required fields
        if not name or not age or not profession or not state:
            return render_template('login.html', 
                                   professions=PROFESSIONS, 
                                   states=STATES,
                                   error="All fields are required.")
        
        # Validate age
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                raise ValueError("Invalid age")
        except:
            return render_template('login.html', 
                                   professions=PROFESSIONS, 
                                   states=STATES,
                                   error="Please enter a valid age.")
        
        # Store user data and reset answers
        session['user_name'] = name
        session['user_age'] = age_int
        session['user_profession'] = profession
        session['user_state'] = state
        session['answers'] = []
        
        # Redirect to first question
        return redirect(url_for('question', q_no=1))
    
    return render_template('login.html', professions=PROFESSIONS, states=STATES)

@app.route('/question/<int:q_no>', methods=['GET', 'POST'])
def question(q_no):
    """Display questionnaire questions one by one"""
    # Check if user is logged in
    if 'user_name' not in session:
        return redirect(url_for('login'))
    
    if 'answers' not in session:
        session['answers'] = []
    
    answers = session.get('answers', [])
    
    # Handle POST (answer submission)
    if request.method == 'POST':
        try:
            ans = int(request.form.get('answer', 0))
            if 0 <= ans <= 3:
                answers.append(ans)
                session['answers'] = answers
        except:
            pass
        
        # Move to next question
        if q_no >= len(questions):
            return redirect(url_for('result'))
        return redirect(url_for('question', q_no=q_no + 1))
    
    # Guard: boundary checks
    if q_no < 1:
        return redirect(url_for('question', q_no=1))
    if q_no > len(questions):
        return redirect(url_for('result'))
    
    # Display question (1-based)
    current_question = questions[q_no - 1]
    progress = (q_no - 1) / len(questions) * 100
    
    return render_template('demo.html', 
                           question=current_question, 
                           q_no=q_no, 
                           total=len(questions),
                           progress=progress,
                           user_name=session.get('user_name', 'User'))

@app.route('/result')
def result():
    """Display results with pie chart visualization"""
    # Check if user is logged in
    if 'user_name' not in session:
        return redirect(url_for('login'))
    
    answers = session.get('answers', [])
    
    # If incomplete, fill with zeros (best-effort)
    if len(answers) < len(questions):
        answers = answers + [0] * (len(questions) - len(answers))
    
    # Compute scores
    dep_score, anx_score, str_score = compute_scores(answers)
    
    # Classify severity
    dep_sev = classify_depression(dep_score)
    anx_sev = classify_anxiety(anx_score)
    str_sev = classify_stress(str_score)
    
    # Get advice
    dep_advice = ADVICE["Depression"][dep_sev]
    anx_advice = ADVICE["Anxiety"][anx_sev]
    str_advice = ADVICE["Stress"][str_sev]
    
    # Chart data for pie chart visualization
    chart_data = {
        "labels": ["Anxiety", "Depression", "Stress"],
        "values": [anx_score, dep_score, str_score],
        "backgroundColor": ["#CCAA33", "#888888", "#DD0000"],  # Yellow, Grey, Red
        "borderColor": ["#999900", "#555555", "#990000"]
    }
    
    return render_template('result.html',
                           user_name=session.get('user_name', 'User'),
                           user_age=session.get('user_age', ''),
                           user_profession=session.get('user_profession', ''),
                           user_state=session.get('user_state', ''),
                           dep_score=dep_score,
                           anx_score=anx_score,
                           str_score=str_score,
                           dep_sev=dep_sev,
                           anx_sev=anx_sev,
                           str_sev=str_sev,
                           dep_advice=dep_advice,
                           anx_advice=anx_advice,
                           str_advice=str_advice,
                           chart_data=chart_data)

@app.route('/reset')
def reset():
    """Reset session and return to login"""
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    # set debug=False in production
    app.ruapp.run(host='0.0.0.0', port=5000, debug=False)
