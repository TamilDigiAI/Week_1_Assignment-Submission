import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="Day3 Task Calculator ➕➖✖➗",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .calculator-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    
    .result-display {
        background: linear-gradient(45deg, #FFE53B 0%, #FF2525 74%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .operation-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-size: 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .history-item {
        background: #f0f2f6;
        padding: 0.5rem;
        border-radius: 10px;
        margin: 0.25rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []

# Header
st.markdown('<h1 class="main-header">🧮 Day3 Task Calculator</h1>', unsafe_allow_html=True)

# Calculator container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### 🔢 First Number")
        num1 = st.number_input("", key="num1", format="%.6f", help="Enter the first number")
    
    with col2:
        st.markdown("### ⚡ Operation")
        operation = st.selectbox(
            "",
            ["➕ Addition", "➖ Subtraction", "✖ Multiplication", "➗ Division", "🔋 Power", "√ Square Root"],
            key="operation"
        )
    
    with col3:
        st.markdown("### 🔢 Second Number")
        if operation == "√ Square Root":
            st.markdown("Not needed for square root")
            num2 = 0
        else:
            num2 = st.number_input("", key="num2", format="%.6f", help="Enter the second number")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate button
st.markdown("<br>", unsafe_allow_html=True)
col_calc = st.columns([1, 2, 1])
with col_calc[1]:
    calculate_btn = st.button("🚀 Calculate Result", use_container_width=True, type="primary")

# Calculation logic
if calculate_btn:
    try:
        result = None
        operation_symbol = ""
        calculation_str = ""
        
        if operation == "➕ Addition":
            result = num1 + num2
            operation_symbol = "+"
            calculation_str = f"{num1} + {num2} = {result}"
            
        elif operation == "➖ Subtraction":
            result = num1 - num2
            operation_symbol = "-"
            calculation_str = f"{num1} - {num2} = {result}"
            
        elif operation == "✖ Multiplication":
            result = num1 * num2
            operation_symbol = "×"
            calculation_str = f"{num1} × {num2} = {result}"
            
        elif operation == "➗ Division":
            if num2 == 0:
                st.error("❌ Error: Division by zero is not allowed!")
            else:
                result = num1 / num2
                operation_symbol = "÷"
                calculation_str = f"{num1} ÷ {num2} = {result}"
                
        elif operation == "🔋 Power":
            result = num1 ** num2
            operation_symbol = "^"
            calculation_str = f"{num1} ^ {num2} = {result}"
            
        elif operation == "√ Square Root":
            if num1 < 0:
                st.error("❌ Error: Cannot calculate square root of negative number!")
            else:
                result = math.sqrt(num1)
                calculation_str = f"√{num1} = {result}"
        
        # Display result if calculation was successful
        if result is not None:
            # Add some excitement with balloons for big results!
            if abs(result) > 1000:
                st.balloons()
            
            # Display result
            st.markdown(
                f'<div class="result-display">🎯 Result: {result:,.6f}</div>',
                unsafe_allow_html=True
            )
            
            # Add to history
            st.session_state.calculation_history.insert(0, calculation_str)
            
            # Keep only last 10 calculations
            if len(st.session_state.calculation_history) > 10:
                st.session_state.calculation_history = st.session_state.calculation_history[:10]
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# History section
if st.session_state.calculation_history:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 Calculation History", expanded=False):
        for i, calc in enumerate(st.session_state.calculation_history):
            st.markdown(f'<div class="history-item">{i+1}. {calc}</div>', unsafe_allow_html=True)
        
        if st.button("🗑 Clear History"):
            st.session_state.calculation_history = []
            st.rerun()

# Footer with fun facts
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col_footer = st.columns([1, 2, 1])
with col_footer[1]:
    st.markdown("""
    <div style='text-align: center; color: #666; font-style: italic;'>
    💡 Fun Fact: The first electronic calculator was invented in 1967!<br>
    Made with ❤ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# Sidebar with additional features
with st.sidebar:
    st.markdown("## ⚙ Calculator Settings")
    
    # Theme selector
    theme = st.selectbox("🎨 Choose Theme", ["Default", "Dark", "Colorful"])
    
    # Number format
    decimal_places = st.slider("🔢 Decimal Places", 0, 10, 6)
    
    # Quick calculations
    st.markdown("## ⚡ Quick Actions")
    if st.button("🧹 Clear All"):
        st.session_state.calculation_history = []
        st.rerun()
    
    # Calculator info
    st.markdown("## ℹ Features")
    st.markdown("""
    - ➕ Basic arithmetic operations
    - 🔋 Power calculations
    - √ Square root
    - 📊 Calculation history
    - 🎯 Error handling
    - 🎨 Beautiful UI
    """)