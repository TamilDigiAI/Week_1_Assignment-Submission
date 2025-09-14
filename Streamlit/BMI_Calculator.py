import streamlit as st
import math
from datetime import datetime
import random
import time

# Page configuration
st.set_page_config(
    page_title="🌟 Day4 Task BMI Calculator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and creative effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
        to { text-shadow: 0 0 30px rgba(255,255,255,0.8), 0 0 40px rgba(255,255,255,0.6); }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    .bmi-result-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 3rem 2rem;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .bmi-result-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg) translate(-50%, -50%); }
        100% { transform: rotate(360deg) translate(-50%, -50%); }
    }
    
    .bmi-value {
        font-size: 5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 3s ease infinite;
        position: relative;
        z-index: 2;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .category-card {
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1rem 0;
        color: white;
        position: relative;
        overflow: hidden;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .underweight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 0 30px rgba(118, 75, 162, 0.5);
    }
    
    .normal {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 0 30px rgba(79, 172, 254, 0.5);
    }
    
    .overweight {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        box-shadow: 0 0 30px rgba(250, 112, 154, 0.5);
    }
    
    .obese {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
    }
    
    .creative-input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    .health-tip-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
        border-left: 4px solid #4ecdc4;
        color: white;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease forwards;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .health-tip-card:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(78, 205, 196, 0.3);
    }
    
    .metric-display {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-display:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.05);
    }
    
    .bmi-gauge {
        width: 100%;
        height: 200px;
        background: linear-gradient(90deg, 
            #667eea 0% 18.5%, 
            #4facfe 18.5% 25%, 
            #fa709a 25% 30%, 
            #ff6b6b 30% 100%);
        border-radius: 100px;
        position: relative;
        margin: 2rem 0;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.3);
    }
    
    .bmi-pointer {
        position: absolute;
        top: -20px;
        width: 6px;
        height: 240px;
        background: white;
        border-radius: 3px;
        box-shadow: 0 0 10px rgba(255,255,255,0.8);
        transition: all 0.5s ease;
        animation: pointerGlow 2s infinite alternate;
    }
    
    @keyframes pointerGlow {
        from { box-shadow: 0 0 10px rgba(255,255,255,0.8); }
        to { box-shadow: 0 0 20px rgba(255,255,255,1); }
    }
    
    .history-item {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4ecdc4;
        color: white;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease forwards;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(5px);
    }
    
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .shape {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .celebration-text {
        font-size: 2rem;
        text-align: center;
        color: white;
        animation: celebrate 1s ease-in-out;
        text-shadow: 0 0 20px rgba(255,255,255,0.8);
    }
    
    @keyframes celebrate {
        0% { transform: scale(0.5) rotate(-180deg); opacity: 0; }
        50% { transform: scale(1.2) rotate(0deg); opacity: 1; }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        background: linear-gradient(45deg, #4ecdc4, #ff6b6b);
    }
    
    .motivational-quote {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        font-style: italic;
        font-size: 1.2rem;
        color: white;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: quoteFade 3s ease-in-out infinite alternate;
    }
    
    @keyframes quoteFade {
        from { opacity: 0.8; }
        to { opacity: 1; }
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#4ecdc4 0deg, transparent 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem auto;
        position: relative;
    }
    
    .progress-ring::before {
        content: '';
        position: absolute;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .custom-metric {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.3), rgba(255, 107, 107, 0.3));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        transition: all 0.3s ease;
    }
    
    .custom-metric:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.4), rgba(255, 107, 107, 0.4));
    }
</style>

<div class="floating-shapes">
    <div class="shape" style="top: 10%; left: 10%; width: 50px; height: 50px; animation-delay: 0s;"></div>
    <div class="shape" style="top: 20%; right: 10%; width: 30px; height: 30px; animation-delay: 1s;"></div>
    <div class="shape" style="bottom: 20%; left: 20%; width: 40px; height: 40px; animation-delay: 2s;"></div>
    <div class="shape" style="bottom: 10%; right: 20%; width: 60px; height: 60px; animation-delay: 3s;"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []
if 'current_quote_index' not in st.session_state:
    st.session_state.current_quote_index = 0
if 'celebration_mode' not in st.session_state:
    st.session_state.celebration_mode = False

# Motivational quotes
motivational_quotes = [
    "💪 Your body can do it. It's your mind you have to convince!",
    "🌟 Health is not about the weight you lose, but about the life you gain!",
    "🎯 Every small step counts towards your health journey!",
    "✨ You are stronger than your excuses!",
    "🌈 Progress, not perfection!",
    "🚀 Your health is an investment, not an expense!",
    "💎 Take care of your body, it's the only place you have to live!",
    "🏆 Champions keep playing until they get it right!",
    "🌸 Health is the greatest wealth!",
    "⭐ Believe in yourself and you will be unstoppable!"
]

# Helper functions
def calculate_bmi(weight, height_cm):
    """Calculate BMI given weight in kg and height in cm"""
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def get_bmi_category_creative(bmi):
    """Get BMI category with creative styling"""
    if bmi < 18.5:
        return "Underweight", "underweight", "🔵", "Time to nourish your body!"
    elif 18.5 <= bmi < 25:
        return "Normal Weight", "normal", "🟢", "Perfect! Keep it up!"
    elif 25 <= bmi < 30:
        return "Overweight", "overweight", "🟡", "Small changes, big results!"
    else:
        return "Obese", "obese", "🔴", "Your health journey starts now!"

def get_creative_health_tips(category):
    """Get creative health tips with emojis"""
    tips = {
        "Underweight": [
            "🍽️ Fuel your body with nutrient-dense powerhouse foods!",
            "🏋️‍♂️ Build your strength with resistance training magic!",
            "🥑 Embrace healthy fats - they're your new best friends!",
            "👨‍⚕️ Partner with professionals for your transformation journey!",
            "🌰 Snack smart with nuts, seeds, and energy-packed treats!",
            "🥤 Power smoothies can be your secret weapon!"
        ],
        "Normal Weight": [
            "🎉 You're crushing it! Keep this amazing momentum going!",
            "🏃‍♀️ Stay active and make movement your daily celebration!",
            "🥗 Continue your love affair with balanced nutrition!",
            "⚖️ Regular check-ins keep you on your winning streak!",
            "💃 Dance, play, move - make fitness fun and joyful!",
            "🧘‍♀️ Mind-body harmony is your secret to sustained success!"
        ],
        "Overweight": [
            "🥗 Transform your plate into a colorful rainbow of health!",
            "🚶‍♂️ Every step is a victory - start your movement revolution!",
            "💧 Hydration is your superpower - drink up for success!",
            "📱 Track your progress and celebrate every small win!",
            "🍎 Make friends with whole foods - they're rooting for you!",
            "😴 Quality sleep is your secret weight management tool!"
        ],
        "Obese": [
            "👨‍⚕️ Build your dream team with healthcare heroes!",
            "📋 Structured plans create extraordinary transformations!",
            "🏊‍♀️ Gentle movements lead to powerful changes!",
            "🎯 Small, achievable goals build unstoppable momentum!",
            "🤝 Find your support squad - you don't journey alone!",
            "💝 Self-compassion is the foundation of lasting change!"
        ]
    }
    return tips.get(category, [])

def calculate_ideal_weight_range(height_cm):
    """Calculate ideal weight range"""
    height_m = height_cm / 100
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return min_weight, max_weight

def create_creative_bmi_gauge(bmi_value):
    """Create an animated BMI gauge"""
    max_bmi = 40
    position_percent = min((bmi_value / max_bmi) * 100, 100)
    
    gauge_html = f"""
    <div class="bmi-gauge">
        <div class="bmi-pointer" style="left: {position_percent}%;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; color: white; font-weight: 600; margin-top: 1rem;">
        <span>🔵 Under</span>
        <span>🟢 Normal</span>
        <span>🟡 Over</span>
        <span>🔴 Obese</span>
    </div>
    """
    return gauge_html

def get_random_quote():
    """Get a random motivational quote"""
    return random.choice(motivational_quotes)

def create_progress_ring(percentage):
    """Create a progress ring visual"""
    return f"""
    <div class="progress-ring" style="background: conic-gradient(#4ecdc4 {percentage * 3.6}deg, transparent 0deg);">
        <div style="color: white; font-weight: 600; z-index: 1;">{int(percentage)}%</div>
    </div>
    """

# Main header with animation
st.markdown('<h1 class="main-header">🌟 Week 2 Day4 Task BMI Calculator</h1>', unsafe_allow_html=True)

# Show motivational quote
current_quote = motivational_quotes[st.session_state.current_quote_index]
st.markdown(f'<div class="motivational-quote">"{current_quote}"</div>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Enter Your Details")
    
    # Unit selection with creative styling
    unit_system = st.radio("🌍 Choose Your Units:", ["🌏 Metric (kg/cm)", "🇺🇸 Imperial (lbs/ft-in)"], horizontal=True)
    
    if unit_system == "🌏 Metric (kg/cm)":
        col_weight, col_height = st.columns(2)
        with col_weight:
            st.markdown("⚖️ **Weight**")
            weight = st.number_input("kg", min_value=1.0, max_value=500.0, value=70.0, step=0.1, key="metric_weight")
        with col_height:
            st.markdown("📏 **Height**")
            height_cm = st.number_input("cm", min_value=50.0, max_value=250.0, value=170.0, step=0.1, key="metric_height")
    else:
        col_weight, col_height = st.columns(2)
        with col_weight:
            st.markdown("⚖️ **Weight**")
            weight_lbs = st.number_input("lbs", min_value=2.0, max_value=1100.0, value=154.0, step=0.1, key="imperial_weight")
            weight = weight_lbs * 0.453592
        with col_height:
            st.markdown("📏 **Height**")
            col_ft, col_in = st.columns(2)
            with col_ft:
                feet = st.number_input("ft", min_value=1, max_value=8, value=5, step=1, key="feet")
            with col_in:
                inches = st.number_input("in", min_value=0, max_value=11, value=7, step=1, key="inches")
            height_cm = (feet * 12 + inches) * 2.54
    
    # Additional info
    col_age, col_gender = st.columns(2)
    with col_age:
        st.markdown("🎂 **Age**")
        age = st.number_input("years", min_value=1, max_value=120, value=30, step=1, key="age")
    with col_gender:
        st.markdown("👤 **Gender**")
        gender = st.selectbox("", ["Male 👨", "Female 👩", "Other 🏳️"], key="gender")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Creative calculate button
    if st.button("🚀 CALCULATE MY BMI!", use_container_width=True, type="primary"):
        st.session_state.celebration_mode = True
        # Cycle through quotes
        st.session_state.current_quote_index = (st.session_state.current_quote_index + 1) % len(motivational_quotes)

with col2:
    if st.session_state.celebration_mode or st.session_state.bmi_history:
        if st.session_state.celebration_mode:
            bmi = calculate_bmi(weight, height_cm)
            category, css_class, emoji, message = get_bmi_category_creative(bmi)
            
            # Store in history
            st.session_state.bmi_history.append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'bmi': round(bmi, 1),
                'weight': round(weight, 1),
                'height': round(height_cm, 1),
                'category': category,
                'age': age,
                'gender': gender.split()[0]
            })
            
            # Keep only last 50 records
            if len(st.session_state.bmi_history) > 50:
                st.session_state.bmi_history = st.session_state.bmi_history[-50:]
            
            st.session_state.celebration_mode = False
        
        if st.session_state.bmi_history:
            latest_record = st.session_state.bmi_history[-1]
            bmi = latest_record['bmi']
            category, css_class, emoji, message = get_bmi_category_creative(bmi)
            
            # BMI Result with celebration
            st.markdown('<div class="bmi-result-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="bmi-value">{bmi}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="celebration-text">Your BMI Score</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Category with creative styling
            st.markdown(f'<div class="category-card {css_class}">{emoji} {category}<br><small>{message}</small></div>', unsafe_allow_html=True)
            
            # Creative BMI Gauge
            st.markdown(create_creative_bmi_gauge(bmi), unsafe_allow_html=True)
            
            # Show celebration effects for healthy BMI
            if 18.5 <= bmi < 25:
                st.balloons()
                time.sleep(0.1)
                st.snow()
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3 style="color: white; margin-bottom: 2rem;">🎭 Ready for Your Health Adventure?</h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem;">
                Enter your details and click the magic button to discover your BMI and unlock personalized health insights!
            </p>
            <div style="font-size: 4rem; margin: 2rem 0;">⭐</div>
        </div>
        """, unsafe_allow_html=True)

# Health Insights Section
if st.session_state.bmi_history:
    latest_record = st.session_state.bmi_history[-1]
    bmi = latest_record['bmi']
    category, _, _, _ = get_bmi_category_creative(bmi)
    
    st.markdown("---")
    
    # Health insights with creative layout
    col_insights, col_metrics = st.columns([1.5, 1])
    
    with col_insights:
        st.markdown("### 🎨 Your Personalized Health Canvas")
        tips = get_creative_health_tips(category)
        
        # Display tips with staggered animation
        for i, tip in enumerate(tips):
            time.sleep(0.05)  # Small delay for effect
            st.markdown(f'<div class="health-tip-card" style="animation-delay: {i*0.1}s;">{tip}</div>', unsafe_allow_html=True)
    
    with col_metrics:
        st.markdown("### 📊 Your Health Dashboard")
        
        # Ideal weight range
        min_weight, max_weight = calculate_ideal_weight_range(height_cm)
        st.markdown(f"""
        <div class="custom-metric">
            <h4>🎯 Ideal Weight Zone</h4>
            <h3>{min_weight:.1f} - {max_weight:.1f} kg</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Health score calculation
        current_weight = latest_record['weight']
        if min_weight <= current_weight <= max_weight:
            health_score = 100
            status_message = "🏆 Perfect Zone!"
            progress_color = "#4ecdc4"
        else:
            diff = min(abs(current_weight - min_weight), abs(current_weight - max_weight))
            health_score = max(0, 100 - (diff * 5))
            status_message = f"🎯 {health_score:.0f}% Healthy"
            progress_color = "#ff6b6b" if health_score < 50 else "#fa709a"
        
        st.markdown(f"""
        <div class="custom-metric">
            <h4>💎 Health Score</h4>
            {create_progress_ring(health_score)}
            <p>{status_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # BMI trend if multiple records
        if len(st.session_state.bmi_history) >= 2:
            current_bmi = st.session_state.bmi_history[-1]['bmi']
            previous_bmi = st.session_state.bmi_history[-2]['bmi']
            trend = current_bmi - previous_bmi
            
            if trend > 0:
                trend_emoji = "📈"
                trend_message = f"Up {abs(trend):.1f}"
                trend_color = "#ff6b6b"
            elif trend < 0:
                trend_emoji = "📉"
                trend_message = f"Down {abs(trend):.1f}"
                trend_color = "#4ecdc4"
            else:
                trend_emoji = "➡️"
                trend_message = "Stable"
                trend_color = "#fa709a"
            
            st.markdown(f"""
            <div class="custom-metric">
                <h4>{trend_emoji} BMI Trend</h4>
                <h3 style="color: {trend_color};">{trend_message}</h3>
            </div>
            """, unsafe_allow_html=True)

# Advanced Analytics Section
if len(st.session_state.bmi_history) > 1:
    st.markdown("---")