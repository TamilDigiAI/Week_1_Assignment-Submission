import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import numpy as np

# Page config
st.set_page_config(
    page_title="🏋️ Gym Workout Logger",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for creative UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background: linear-gradient(90deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%); }
        50% { background: linear-gradient(90deg, #48dbfb 0%, #ff6b6b 50%, #feca57 100%); }
        100% { background: linear-gradient(90deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%); }
    }
    
    .workout-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .workout-card:hover {
        transform: translateY(-5px);
    }
    
    .exercise-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 0.8rem 0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .exercise-button {
        background: linear-gradient(45deg, #ff9a56, #feca57);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .exercise-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workout_history' not in st.session_state:
    st.session_state.workout_history = pd.DataFrame(columns=[
        'Date', 'Exercise', 'Sets', 'Reps', 'Weight', 'Volume', 'Category'
    ])

if 'current_workout' not in st.session_state:
    st.session_state.current_workout = []

# Exercise database
EXERCISES = {
    'Chest': ['Bench Press', 'Incline Press', 'Dumbbell Fly', 'Push-ups', 'Dips', 'Chest Press'],
    'Back': ['Pull-ups', 'Lat Pulldown', 'Barbell Row', 'Deadlift', 'T-Bar Row', 'Cable Row'],
    'Shoulders': ['Shoulder Press', 'Lateral Raise', 'Front Raise', 'Rear Delt Fly', 'Upright Row', 'Arnold Press'],
    'Arms': ['Bicep Curl', 'Tricep Pushdown', 'Hammer Curl', 'Overhead Extension', 'Preacher Curl', 'Dips'],
    'Legs': ['Squat', 'Leg Press', 'Lunges', 'Leg Curl', 'Leg Extension', 'Calf Raise'],
    'Core': ['Plank', 'Crunches', 'Russian Twist', 'Leg Raise', 'Mountain Climbers', 'Dead Bug']
}

# Header
st.markdown("""
<div class="main-header">
    <h1>🏋️ GYM BEAST LOGGER</h1>
    <p>Track your workouts, crush your goals, become unstoppable! 💪</p>
</div>
""", unsafe_allow_html=True)

# Workout Logger Section
st.header("🔥 Log Your Workout")

# Exercise selection
col1, col2 = st.columns([1, 1])

with col1:
    selected_category = st.selectbox(
        "💪 Select Muscle Group",
        list(EXERCISES.keys()),
        help="Choose the muscle group you're training"
    )

with col2:
    selected_exercise = st.selectbox(
        "🏋️ Select Exercise",
        EXERCISES[selected_category],
        help="Pick your exercise"
    )

# Exercise input form
st.subheader("📝 Exercise Details")

input_col1, input_col2, input_col3, input_col4 = st.columns(4)

with input_col1:
    sets = st.number_input("Sets", min_value=1, max_value=20, value=3)

with input_col2:
    reps = st.number_input("Reps", min_value=1, max_value=100, value=10)

with input_col3:
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=20.0, step=2.5)

with input_col4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add Exercise", type="primary"):
        volume = sets * reps * weight
        exercise_data = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Exercise': selected_exercise,
            'Sets': sets,
            'Reps': reps,
            'Weight': weight,
            'Volume': volume,
            'Category': selected_category
        }
        
        # Add to current workout
        st.session_state.current_workout.append(exercise_data)
        st.success(f"Added {selected_exercise}: {sets} sets × {reps} reps @ {weight}kg! 🎯")

# Current workout display
if st.session_state.current_workout:
    st.subheader("🔥 Current Workout Session")
    
    current_df = pd.DataFrame(st.session_state.current_workout)
    
    # Display current workout in a nice format
    for i, exercise in enumerate(st.session_state.current_workout):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="exercise-card">
                    <h4>💪 {exercise['Exercise']} ({exercise['Category']})</h4>
                    <p><strong>{exercise['Sets']} sets × {exercise['Reps']} reps @ {exercise['Weight']}kg</strong></p>
                    <p>Volume: {exercise['Volume']:.1f}kg</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    st.info("Edit functionality - Select exercise above and modify values")
            
            with col3:
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.current_workout.pop(i)
                    st.rerun()
    
    # Workout summary
    total_volume = sum(ex['Volume'] for ex in st.session_state.current_workout)
    total_exercises = len(st.session_state.current_workout)
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Total Exercises", total_exercises)
    
    with summary_col2:
        st.metric("Total Volume", f"{total_volume:.1f} kg")
    
    with summary_col3:
        st.metric("Muscle Groups", len(set(ex['Category'] for ex in st.session_state.current_workout)))
    
    # Save workout button
    if st.button("💾 Save Workout", type="primary"):
        new_data = pd.DataFrame(st.session_state.current_workout)
        st.session_state.workout_history = pd.concat([st.session_state.workout_history, new_data], ignore_index=True)
        st.session_state.current_workout = []
        st.balloons()
        st.success("🎉 Workout saved! Great job crushing those goals!")
        st.rerun()

# Workout History Section
st.header("📊 Workout History & Analytics")

if not st.session_state.workout_history.empty:
    # Filter options
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        date_filter = st.date_input(
            "Filter from date",
            value=date.today() - timedelta(days=30),
            max_value=date.today()
        )
    
    with filter_col2:
        category_filter = st.multiselect(
            "Filter by muscle group",
            options=list(EXERCISES.keys()),
            default=list(EXERCISES.keys())
        )
    
    with filter_col3:
        exercise_filter = st.multiselect(
            "Filter by exercise",
            options=st.session_state.workout_history['Exercise'].unique(),
            default=st.session_state.workout_history['Exercise'].unique()
        )
    
    # Apply filters
    filtered_history = st.session_state.workout_history.copy()
    filtered_history['Date'] = pd.to_datetime(filtered_history['Date'])
    
    filtered_history = filtered_history[
        (filtered_history['Date'] >= pd.to_datetime(date_filter)) &
        (filtered_history['Category'].isin(category_filter)) &
        (filtered_history['Exercise'].isin(exercise_filter))
    ]
    
    if not filtered_history.empty:
        # Statistics
        st.subheader("📈 Your Stats")
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            total_workouts = len(filtered_history['Date'].unique())
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_workouts}</h3>
                <p>Workout Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            total_volume = filtered_history['Volume'].sum()
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_volume:.0f}kg</h3>
                <p>Total Volume</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col3:
            avg_volume = filtered_history.groupby('Date')['Volume'].sum().mean()
            st.markdown(f"""
            <div class="stats-card">
                <h3>{avg_volume:.0f}kg</h3>
                <p>Avg Daily Volume</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col4:
            favorite_exercise = filtered_history['Exercise'].mode().iloc[0] if not filtered_history.empty else "None"
            st.markdown(f"""
            <div class="stats-card">
                <h3>{favorite_exercise}</h3>
                <p>Favorite Exercise</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Weekly Progress Graph
        st.subheader("📊 Weekly Progress")
        
        # Prepare data for weekly chart
        filtered_history['Week'] = filtered_history['Date'].dt.isocalendar().week
        filtered_history['Year'] = filtered_history['Date'].dt.year
        filtered_history['Week_Year'] = filtered_history['Year'].astype(str) + '-W' + filtered_history['Week'].astype(str).str.zfill(2)
        
        weekly_volume = filtered_history.groupby('Week_Year')['Volume'].sum().reset_index()
        weekly_workouts = filtered_history.groupby('Week_Year')['Date'].nunique().reset_index()
        weekly_workouts.columns = ['Week_Year', 'Workout_Days']
        
        weekly_data = pd.merge(weekly_volume, weekly_workouts, on='Week_Year')
        
        # Create subplot with secondary y-axis
        fig = go.Figure()
        
        # Add volume bars
        fig.add_trace(go.Bar(
            x=weekly_data['Week_Year'],
            y=weekly_data['Volume'],
            name='Weekly Volume (kg)',
            marker_color='#ff6b6b',
            yaxis='y',
            opacity=0.8
        ))
        
        # Add workout frequency line
        fig.add_trace(go.Scatter(
            x=weekly_data['Week_Year'],
            y=weekly_data['Workout_Days'],
            mode='lines+markers',
            name='Workout Days',
            line=dict(color='#4ecdc4', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Weekly Volume & Workout Frequency",
            xaxis_title="Week",
            yaxis=dict(title="Volume (kg)", side="left"),
            yaxis2=dict(title="Workout Days", side="right", overlaying="y"),
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Exercise Progress Chart
        st.subheader("💪 Exercise Progress")
        
        # Select exercise for progress tracking
        progress_exercise = st.selectbox(
            "Select exercise to track progress",
            filtered_history['Exercise'].unique()
        )
        
        exercise_progress = filtered_history[filtered_history['Exercise'] == progress_exercise].copy()
        exercise_progress = exercise_progress.sort_values('Date')
        
        if not exercise_progress.empty:
            fig_progress = go.Figure()
            
            # Add max weight line
            fig_progress.add_trace(go.Scatter(
                x=exercise_progress['Date'],
                y=exercise_progress['Weight'],
                mode='lines+markers',
                name='Weight (kg)',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=8)
            ))
            
            # Add volume line
            fig_progress.add_trace(go.Scatter(
                x=exercise_progress['Date'],
                y=exercise_progress['Volume'],
                mode='lines+markers',
                name='Volume (kg)',
                line=dict(color='#4ecdc4', width=3),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            fig_progress.update_layout(
                title=f"{progress_exercise} - Progress Over Time",
                xaxis_title="Date",
                yaxis=dict(title="Weight (kg)", side="left"),
                yaxis2=dict(title="Volume (kg)", side="right", overlaying="y"),
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_progress, use_container_width=True)
        
        # Workout History Table
        st.subheader("📋 Detailed History")
        
        # Display table with formatting
        display_history = filtered_history.copy()
        display_history['Date'] = display_history['Date'].dt.strftime('%Y-%m-%d')
        display_history = display_history.sort_values('Date', ascending=False)
        
        st.dataframe(
            display_history,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Volume": st.column_config.NumberColumn(
                    "Volume (kg)",
                    format="%.1f kg"
                ),
                "Weight": st.column_config.NumberColumn(
                    "Weight (kg)",
                    format="%.1f kg"
                )
            }
        )
        
        # Export functionality
        if st.button("📥 Export Workout Data"):
            csv = display_history.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name=f"workout_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No workouts found for the selected filters. Adjust your filters or add some workouts!")

else:
    st.info("🎯 No workout history yet. Start logging your exercises above to see your progress!")

# Data Management
st.header("🗂️ Data Management")

manage_col1, manage_col2, manage_col3 = st.columns(3)

with manage_col1:
    if st.button("🗑️ Clear Current Workout"):
        st.session_state.current_workout = []
        st.success("Current workout cleared!")

with manage_col2:
    if st.button("⚠️ Reset All History", type="secondary"):
        if st.checkbox("I confirm I want to delete all workout history"):
            st.session_state.workout_history = pd.DataFrame(columns=[
                'Date', 'Exercise', 'Sets', 'Reps', 'Weight', 'Volume', 'Category'
            ])
            st.session_state.current_workout = []
            st.success("All workout history has been reset!")

with manage_col3:
    # Quick stats
    if not st.session_state.workout_history.empty:
        total_days = len(st.session_state.workout_history['Date'].unique())
        st.metric("Total Workout Days", total_days)

# Motivational footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h3>💪 "The only bad workout is the one that didn't happen!"</h3>
    <p>Keep pushing your limits and tracking your progress. You've got this! 🔥</p>
    <p><small>Remember: Progressive overload is key. Gradually increase weight, reps, or sets over time.</small></p>
</div>
""", unsafe_allow_html=True)