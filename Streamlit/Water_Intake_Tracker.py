import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import json

# Page config
st.set_page_config(
    page_title="💧 Hydration Station",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for creative UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .water-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .goal-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'water_data' not in st.session_state:
    st.session_state.water_data = {}
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 3000  # Default 3L in ml

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 Hydration Station</h1>
    <p>Stay hydrated, stay healthy! Track your daily water intake and reach your goals.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Daily goal setting
    new_goal = st.number_input(
        "Daily Water Goal (ml)", 
        min_value=500, 
        max_value=5000, 
        value=st.session_state.daily_goal,
        step=100,
        help="Recommended: 2500-3500ml per day"
    )
    st.session_state.daily_goal = new_goal
    
    st.markdown("---")
    st.markdown("### 💡 Hydration Tips")
    tips = [
        "🌅 Start your day with a glass of water",
        "🍎 Eat water-rich fruits and vegetables",
        "⏰ Set regular hydration reminders",
        "🏃‍♀️ Drink extra water when exercising",
        "🌡️ Increase intake on hot days"
    ]
    for tip in tips:
        st.markdown(f"- {tip}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Today's Progress")
    
    # Date selector
    selected_date = st.date_input(
        "Select Date",
        value=date.today(),
        max_value=date.today()
    )
    
    date_str = selected_date.strftime("%Y-%m-%d")
    
    # Water intake input
    st.subheader("💧 Add Water Intake")
    
    input_col1, input_col2, input_col3 = st.columns([2, 1, 1])
    
    with input_col1:
        water_amount = st.number_input(
            "Amount (ml)", 
            min_value=0, 
            max_value=2000, 
            value=250,
            step=50
        )
    
    with input_col2:
        if st.button("💧 Add Water", type="primary"):
            if date_str not in st.session_state.water_data:
                st.session_state.water_data[date_str] = 0
            st.session_state.water_data[date_str] += water_amount
            st.success(f"Added {water_amount}ml! 🎉")
    
    with input_col3:
        # Quick add buttons
        st.markdown("**Quick Add:**")
        quick_amounts = [250, 500, 750]
        for amount in quick_amounts:
            if st.button(f"{amount}ml", key=f"quick_{amount}"):
                if date_str not in st.session_state.water_data:
                    st.session_state.water_data[date_str] = 0
                st.session_state.water_data[date_str] += amount
                st.success(f"Added {amount}ml! 💦")

    # Current day's intake
    today_intake = st.session_state.water_data.get(date_str, 0)
    progress_percentage = min(today_intake / st.session_state.daily_goal * 100, 100)
    
    # Progress visualization
    st.subheader("🎯 Daily Progress")
    
    # Create a beautiful progress chart
    fig_progress = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = today_intake,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Water Intake (ml)"},
        delta = {'reference': st.session_state.daily_goal},
        gauge = {
            'axis': {'range': [None, st.session_state.daily_goal * 1.2]},
            'bar': {'color': "#4facfe"},
            'steps': [
                {'range': [0, st.session_state.daily_goal * 0.5], 'color': "#ffebee"},
                {'range': [st.session_state.daily_goal * 0.5, st.session_state.daily_goal], 'color': "#e3f2fd"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.daily_goal
            }
        }
    ))
    
    fig_progress.update_layout(height=400)
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Progress bar
    st.progress(progress_percentage / 100)
    
    if progress_percentage >= 100:
        st.balloons()
        st.success("🎉 Congratulations! You've reached your daily goal!")
    elif progress_percentage >= 75:
        st.info("💪 Almost there! Keep it up!")
    elif progress_percentage >= 50:
        st.warning("📈 Good progress! Don't forget to keep hydrating!")

with col2:
    st.header("📈 Stats")
    
    # Daily stats
    remaining = max(st.session_state.daily_goal - today_intake, 0)
    glasses_equivalent = today_intake / 250  # Assuming 250ml per glass
    
    st.metric("Today's Intake", f"{today_intake:,} ml", f"{today_intake - st.session_state.water_data.get((date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), 0):+,} ml")
    st.metric("Remaining", f"{remaining:,} ml")
    st.metric("Glasses", f"{glasses_equivalent:.1f}", "🥤")
    st.metric("Progress", f"{progress_percentage:.1f}%")
    
    # Hydration level indicator
    if progress_percentage >= 100:
        hydration_status = "🌟 Excellently Hydrated"
        status_color = "#4caf50"
    elif progress_percentage >= 75:
        hydration_status = "💧 Well Hydrated"
        status_color = "#2196f3"
    elif progress_percentage >= 50:
        hydration_status = "⚡ Moderately Hydrated"
        status_color = "#ff9800"
    elif progress_percentage >= 25:
        hydration_status = "⚠️ Low Hydration"
        status_color = "#ff5722"
    else:
        hydration_status = "🚨 Dehydrated"
        status_color = "#f44336"
    
    st.markdown(f"""
    <div style="background-color: {status_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
        <h3>{hydration_status}</h3>
    </div>
    """, unsafe_allow_html=True)

# Weekly chart
st.header("📊 Weekly Hydration Chart")

# Generate data for the last 7 days
end_date = selected_date
start_date = end_date - timedelta(days=6)
date_range = [start_date + timedelta(days=i) for i in range(7)]

weekly_data = []
for d in date_range:
    date_str = d.strftime("%Y-%m-%d")
    intake = st.session_state.water_data.get(date_str, 0)
    weekly_data.append({
        'Date': d.strftime("%m/%d"),
        'Day': d.strftime("%a"),
        'Intake': intake,
        'Goal': st.session_state.daily_goal,
        'Full_Date': d
    })

df_weekly = pd.DataFrame(weekly_data)

# Create weekly chart
fig_weekly = go.Figure()

# Add intake bars
fig_weekly.add_trace(go.Bar(
    x=df_weekly['Day'],
    y=df_weekly['Intake'],
    name='Daily Intake',
    marker_color='#4facfe',
    text=df_weekly['Intake'].apply(lambda x: f"{x:,}ml"),
    textposition='auto'
))

# Add goal line
fig_weekly.add_trace(go.Scatter(
    x=df_weekly['Day'],
    y=df_weekly['Goal'],
    mode='lines+markers',
    name='Daily Goal',
    line=dict(color='red', width=3, dash='dash'),
    marker=dict(size=8)
))

fig_weekly.update_layout(
    title="Weekly Water Intake vs Goal",
    xaxis_title="Day",
    yaxis_title="Water Intake (ml)",
    height=400,
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_weekly, use_container_width=True)

# Weekly summary stats
col1, col2, col3, col4 = st.columns(4)

weekly_total = df_weekly['Intake'].sum()
weekly_average = df_weekly['Intake'].mean()
days_goal_met = len(df_weekly[df_weekly['Intake'] >= st.session_state.daily_goal])
weekly_goal = st.session_state.daily_goal * 7

with col1:
    st.metric("Weekly Total", f"{weekly_total:,} ml")

with col2:
    st.metric("Daily Average", f"{weekly_average:.0f} ml")

with col3:
    st.metric("Goals Met", f"{days_goal_met}/7 days")

with col4:
    weekly_progress = min(weekly_total / weekly_goal * 100, 100)
    st.metric("Weekly Progress", f"{weekly_progress:.1f}%")

# Data management
st.header("🗂️ Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗑️ Clear Today's Data"):
        if date_str in st.session_state.water_data:
            del st.session_state.water_data[date_str]
            st.success("Today's data cleared!")
        else:
            st.info("No data to clear for today.")

with col2:
    if st.button("📊 Export Data"):
        if st.session_state.water_data:
            export_data = pd.DataFrame([
                {'Date': date, 'Intake_ml': intake} 
                for date, intake in st.session_state.water_data.items()
            ])
            csv = export_data.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name=f"water_intake_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data to export yet.")

with col3:
    if st.button("🔄 Reset All Data"):
        st.session_state.water_data = {}
        st.success("All data has been reset!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💧 Stay hydrated, stay healthy! Remember to drink water regularly throughout the day.</p>
    <p><small>Recommended daily water intake varies by individual. Consult with healthcare professionals for personalized advice.</small></p>
</div>
""", unsafe_allow_html=True)