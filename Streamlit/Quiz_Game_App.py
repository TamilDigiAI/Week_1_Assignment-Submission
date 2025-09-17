import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="🧠 Quiz Master Challenge",
    page_icon="❓",
    layout="wide"
)

# Custom CSS for creative UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .quiz-container {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        margin: 2rem 0;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    .question-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .question-number {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffd700;
        margin-bottom: 1rem;
    }
    
    .question-text {
        font-size: 1.8rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 2rem;
    }
    
    .score-display {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffd93d 50%, #6bcf7f 100%);
        height: 15px;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .final-score {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 50%, #4ecdc4 100%);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        margin: 2rem 0;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    .final-score h1 {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .final-score h2 {
        font-size: 2.5rem;
        color: #fff;
        margin-bottom: 1.5rem;
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        color: #333;
        display: inline-block;
        margin: 1rem;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        border: 2px solid #fff;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .stRadio > div:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
        transition: all 0.3s ease;
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        margin: 2rem 0;
    }
    
    .welcome-card h2 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    .welcome-card p {
        font-size: 1.3rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Quiz Questions Database
QUIZ_QUESTIONS = [
    {
        "question": "🌍 What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "correct": 2,
        "category": "Geography"
    },
    {
        "question": "🔬 What is the chemical symbol for Gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "category": "Science"
    },
    {
        "question": "🎨 Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
        "correct": 1,
        "category": "Art"
    },
    {
        "question": "🏔️ Which is the highest mountain in the world?",
        "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"],
        "correct": 2,
        "category": "Geography"
    },
    {
        "question": "💻 What does 'CPU' stand for?",
        "options": ["Computer Processing Unit", "Central Processing Unit", "Core Processing Unit", "Central Program Unit"],
        "correct": 1,
        "category": "Technology"
    },
    {
        "question": "🌟 Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "correct": 2,
        "category": "Science"
    },
    {
        "question": "📚 Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "correct": 1,
        "category": "Literature"
    },
    {
        "question": "🎵 How many strings does a standard guitar have?",
        "options": ["4", "5", "6", "7"],
        "correct": 2,
        "category": "Music"
    },
    {
        "question": "🌊 Which ocean is the largest?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "correct": 3,
        "category": "Geography"
    },
    {
        "question": "🧮 What is 15% of 200?",
        "options": ["25", "30", "35", "40"],
        "correct": 1,
        "category": "Mathematics"
    }
]

# Initialize session state
def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'questions' not in st.session_state:
        st.session_state.questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))

def reset_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.user_answers = []
    st.session_state.questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))

def get_achievement_badge(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "🏆 PERFECT SCORE!", "#FFD700"
    elif percentage >= 90:
        return "🌟 GENIUS LEVEL!", "#FF6B6B"
    elif percentage >= 80:
        return "🎯 EXCELLENT!", "#4ECDC4"
    elif percentage >= 70:
        return "👍 GOOD JOB!", "#45B7D1"
    elif percentage >= 60:
        return "📚 KEEP LEARNING!", "#96CEB4"
    else:
        return "💪 TRY AGAIN!", "#FFEAA7"

def get_motivational_message(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "Absolutely phenomenal! You're a true Quiz Master! 🎉"
    elif percentage >= 90:
        return "Outstanding performance! You're almost perfect! ⭐"
    elif percentage >= 80:
        return "Great job! You really know your stuff! 🚀"
    elif percentage >= 70:
        return "Nice work! You're doing well! 👏"
    elif percentage >= 60:
        return "Good effort! Keep studying and you'll improve! 📖"
    else:
        return "Don't give up! Every expert was once a beginner! 💪"

# Initialize
initialize_session_state()

# Main title
st.markdown('<h1 class="main-title">🧠 Quiz Master Challenge</h1>', unsafe_allow_html=True)

# Welcome Screen
if not st.session_state.quiz_started:
    st.markdown("""
    <div class="welcome-card">
        <h2>🎯 Welcome to Quiz Master Challenge!</h2>
        <p>🧠 Test your knowledge across multiple categories</p>
        <p>⭐ 10 exciting questions await you</p>
        <p>🏆 Can you achieve the perfect score?</p>
        <p>📊 Track your progress in real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats preview
    st.markdown("### 📈 Quiz Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">10</div>
            <div class="stat-label">Questions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">Options Each</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">Fun Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START QUIZ", use_container_width=True, type="primary"):
            st.session_state.quiz_started = True
            st.rerun()

# Quiz Interface
elif st.session_state.quiz_started and not st.session_state.quiz_completed:
    current_q = st.session_state.current_question
    total_questions = len(st.session_state.questions)
    question_data = st.session_state.questions[current_q]
    
    # Progress bar
    progress = (current_q) / total_questions
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; font-size: 1.2rem;">Progress</span>
            <span style="font-weight: 600; font-size: 1.2rem;">{current_q}/{total_questions}</span>
        </div>
        <div style="background: #e0e0e0; border-radius: 10px; overflow: hidden;">
            <div class="progress-bar" style="width: {progress * 100}%; height: 15px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Current score display
    st.markdown(f"""
    <div class="score-display">
        🎯 Current Score: {st.session_state.score}/{current_q} 
        {f"({(st.session_state.score/current_q*100):.1f}%)" if current_q > 0 else ""}
    </div>
    """, unsafe_allow_html=True)
    
    # Question card
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {current_q + 1} of {total_questions} | Category: {question_data['category']}</div>
        <div class="question-text">{question_data['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    st.markdown("### 🤔 Choose your answer:")
    user_answer = st.radio(
        "Select one option:",
        options=question_data['options'],
        key=f"question_{current_q}",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("✅ SUBMIT ANSWER", use_container_width=True, type="primary"):
            # Check if answer is correct
            selected_index = question_data['options'].index(user_answer)
            is_correct = selected_index == question_data['correct']
            
            if is_correct:
                st.session_state.score += 1
                st.success(f"🎉 Correct! The answer is {question_data['options'][question_data['correct']]}")
            else:
                st.error(f"❌ Incorrect! The correct answer is {question_data['options'][question_data['correct']]}")
            
            st.session_state.user_answers.append({
                'question': question_data['question'],
                'user_answer': user_answer,
                'correct_answer': question_data['options'][question_data['correct']],
                'is_correct': is_correct
            })
            
            time.sleep(1)  # Brief pause for feedback
            
            if current_q + 1 >= total_questions:
                st.session_state.quiz_completed = True
            else:
                st.session_state.current_question += 1
            
            st.rerun()

# Results Screen
elif st.session_state.quiz_completed:
    total_questions = len(st.session_state.questions)
    final_score = st.session_state.score
    percentage = (final_score / total_questions) * 100
    
    # Final score display
    achievement, color = get_achievement_badge(final_score, total_questions)
    message = get_motivational_message(final_score, total_questions)
    
    st.markdown(f"""
    <div class="final-score">
        <h1>🏁 Quiz Complete!</h1>
        <h2>Your Final Score</h2>
        <div style="font-size: 4rem; margin: 1rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            {final_score}/{total_questions}
        </div>
        <div style="font-size: 2rem; margin-bottom: 1.5rem; color: #fff;">
            {percentage:.1f}% Correct
        </div>
        <div class="achievement-badge" style="background: {color};">
            {achievement}
        </div>
        <p style="font-size: 1.3rem; margin-top: 1.5rem; color: #fff;">
            {message}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Results
    st.markdown("### 📊 Detailed Results")
    
    for i, answer_data in enumerate(st.session_state.user_answers):
        status_icon = "✅" if answer_data['is_correct'] else "❌"
        status_color = "#4CAF50" if answer_data['is_correct'] else "#F44336"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {'#E8F5E8' if answer_data['is_correct'] else '#FFE8E8'} 0%, {'#F0F8F0' if answer_data['is_correct'] else '#FFF0F0'} 100%); 
             padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
             border-left: 5px solid {status_color};">
            <h4 style="color: #333; margin-bottom: 1rem;">{status_icon} Question {i+1}</h4>
            <p style="color: #666; margin-bottom: 0.5rem;"><strong>Q:</strong> {answer_data['question']}</p>
            <p style="color: #666; margin-bottom: 0.5rem;"><strong>Your Answer:</strong> {answer_data['user_answer']}</p>
            <p style="color: #666;"><strong>Correct Answer:</strong> {answer_data['correct_answer']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 PLAY AGAIN", use_container_width=True, type="primary"):
            reset_quiz()
            st.rerun()
    
    with col2:
        if st.button("📈 VIEW STATS", use_container_width=True):
            st.balloons()
            st.success("🎉 Great job completing the quiz!")
    
    with col3:
        if st.button("🏠 HOME", use_container_width=True):
            reset_quiz()
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h3>🎯 Quiz Master Challenge</h3>
    <p>✨ Challenge Your Mind | 🏆 Track Progress | 📚 Learn & Grow</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)