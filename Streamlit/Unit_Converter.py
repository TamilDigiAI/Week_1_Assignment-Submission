import streamlit as st
import requests
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="🔄 Day5 Task Universal Unit Converter",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .converter-tabs {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .converter-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 2rem;
    }
    
    .result-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .tab-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔄 Day5 Task Universal Unit Converter</h1>', unsafe_allow_html=True)

# Tab selection buttons
st.markdown("### 🎯 Choose Your Converter:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    currency_btn = st.button("💰 Currency", use_container_width=True)
with col2:
    temp_btn = st.button("🌡️ Temperature", use_container_width=True)
with col3:
    length_btn = st.button("📏 Length", use_container_width=True)
with col4:
    weight_btn = st.button("⚖️ Weight", use_container_width=True)

# Initialize session state
if 'converter_type' not in st.session_state:
    st.session_state.converter_type = "💰 Currency"

# Update converter type based on button clicks
if currency_btn:
    st.session_state.converter_type = "💰 Currency"
elif temp_btn:
    st.session_state.converter_type = "🌡️ Temperature"
elif length_btn:
    st.session_state.converter_type = "📏 Length"
elif weight_btn:
    st.session_state.converter_type = "⚖️ Weight"

st.markdown("---")

# Currency Converter
if st.session_state.converter_type == "💰 Currency":
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Currency Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        amount = st.number_input("💵 Amount:", min_value=0.01, value=1.0, step=0.01, key="curr_amount")
        from_currency = st.selectbox("From Currency:", [
            "USD 🇺🇸", "EUR 🇪🇺", "GBP 🇬🇧", "JPY 🇯🇵", "CAD 🇨🇦", 
            "AUD 🇦🇺", "CHF 🇨🇭", "CNY 🇨🇳", "INR 🇮🇳", "KRW 🇰🇷"
        ], key="from_curr")
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("### ➡️")
    
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        to_currency = st.selectbox("To Currency:", [
            "EUR 🇪🇺", "USD 🇺🇸", "GBP 🇬🇧", "JPY 🇯🇵", "CAD 🇨🇦",
            "AUD 🇦🇺", "CHF 🇨🇭", "CNY 🇨🇳", "INR 🇮🇳", "KRW 🇰🇷"
        ], key="to_curr")
    
    # Mock exchange rates
    exchange_rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "CAD": 1.25, "AUD": 1.35, 
                "CHF": 0.92, "CNY": 6.45, "INR": 74.5, "KRW": 1180.0},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.5, "CAD": 1.47, "AUD": 1.59,
                "CHF": 1.08, "CNY": 7.6, "INR": 87.8, "KRW": 1390.0},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.5, "CAD": 1.71, "AUD": 1.85,
                "CHF": 1.26, "CNY": 8.84, "INR": 102.0, "KRW": 1617.0},
        "JPY": {"USD": 0.0091, "EUR": 0.0077, "GBP": 0.0066, "CAD": 0.011, "AUD": 0.012,
                "CHF": 0.0084, "CNY": 0.059, "INR": 0.68, "KRW": 10.7},
        "INR": {"USD": 0.013, "EUR": 0.011, "GBP": 0.0098, "JPY": 1.47, "CAD": 0.017,
                "AUD": 0.018, "CHF": 0.012, "CNY": 0.087, "KRW": 15.8}
    }
    
    from_curr = from_currency.split()[0]
    to_curr = to_currency.split()[0]
    
    if from_curr != to_curr:
        if from_curr in exchange_rates and to_curr in exchange_rates[from_curr]:
            rate = exchange_rates[from_curr][to_curr]
            result = amount * rate
            
            st.markdown(f"""
            <div class="result-box">
                💰 {amount:,.2f} {from_curr} = {result:,.2f} {to_curr}
                <br><small>💱 Exchange Rate: 1 {from_curr} = {rate} {to_curr}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📊 Exchange rate not available for this pair. In production, use a live API!")
    else:
        st.markdown(f"""
        <div class="result-box">
            💰 {amount:,.2f} {from_curr} = {amount:,.2f} {to_curr}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Temperature Converter
elif st.session_state.converter_type == "🌡️ Temperature":
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.markdown("### 🌡️ Temperature Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        temp_value = st.number_input("🌡️ Temperature:", value=0.0, step=0.1, key="temp_val")
        from_temp = st.selectbox("From Unit:", ["°C Celsius", "°F Fahrenheit", "K Kelvin"], key="from_temp")
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("### 🔄")
    
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        to_temp = st.selectbox("To Unit:", ["°F Fahrenheit", "°C Celsius", "K Kelvin"], key="to_temp")
    
    # Temperature conversion functions
    def celsius_to_fahrenheit(c):
        return (c * 9/5) + 32
    
    def celsius_to_kelvin(c):
        return c + 273.15
    
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5/9
    
    def fahrenheit_to_kelvin(f):
        return celsius_to_kelvin(fahrenheit_to_celsius(f))
    
    def kelvin_to_celsius(k):
        return k - 273.15
    
    def kelvin_to_fahrenheit(k):
        return celsius_to_fahrenheit(kelvin_to_celsius(k))
    
    from_unit = from_temp.split()[0]
    to_unit = to_temp.split()[0]
    
    if from_unit == to_unit:
        result = temp_value
    elif from_unit == "°C":
        if to_unit == "°F":
            result = celsius_to_fahrenheit(temp_value)
        else:  # K
            result = celsius_to_kelvin(temp_value)
    elif from_unit == "°F":
        if to_unit == "°C":
            result = fahrenheit_to_celsius(temp_value)
        else:  # K
            result = fahrenheit_to_kelvin(temp_value)
    else:  # K
        if to_unit == "°C":
            result = kelvin_to_celsius(temp_value)
        else:  # °F
            result = kelvin_to_fahrenheit(temp_value)
    
    # Temperature status emoji
    celsius_temp = result if to_unit == "°C" else (fahrenheit_to_celsius(result) if to_unit == "°F" else kelvin_to_celsius(result))
    
    if celsius_temp < 0:
        status = "🧊 Freezing Cold"
    elif celsius_temp < 10:
        status = "❄️ Cold"
    elif celsius_temp < 25:
        status = "😊 Pleasant"
    elif celsius_temp < 35:
        status = "☀️ Warm"
    else:
        status = "🔥 Hot"
    
    st.markdown(f"""
    <div class="result-box">
        🌡️ {temp_value} {from_unit} = {result:.2f} {to_unit}
        <br><small>{status}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Length Converter
elif st.session_state.converter_type == "📏 Length":
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.markdown("### 📏 Length Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        length_value = st.number_input("📐 Length:", min_value=0.0, value=1.0, step=0.001, key="len_val")
        from_length = st.selectbox("From Unit:", [
            "mm Millimeter", "cm Centimeter", "m Meter", "km Kilometer",
            "in Inch", "ft Feet", "yd Yard", "mi Mile"
        ], key="from_len")
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("### ↔️")
    
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        to_length = st.selectbox("To Unit:", [
            "m Meter", "cm Centimeter", "mm Millimeter", "km Kilometer",
            "ft Feet", "in Inch", "yd Yard", "mi Mile"
        ], key="to_len")
    
    # Length conversion to meters
    to_meters = {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.34
    }
    
    from_unit = from_length.split()[0]
    to_unit = to_length.split()[0]
    
    # Convert to meters first, then to target unit
    meters = length_value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    
    # Add some context for large/small values
    if result > 1000000:
        context = "🚀 That's astronomical!"
    elif result > 1000:
        context = "🏢 That's quite long!"
    elif result < 0.001:
        context = "🔬 That's microscopic!"
    else:
        context = "✨ Perfect size!"
    
    st.markdown(f"""
    <div class="result-box">
        📏 {length_value:,.3f} {from_unit} = {result:,.6f} {to_unit}
        <br><small>{context}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Weight Converter
elif st.session_state.converter_type == "⚖️ Weight":
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.markdown("### ⚖️ Weight Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        weight_value = st.number_input("⚖️ Weight:", min_value=0.0, value=1.0, step=0.001, key="weight_val")
        from_weight = st.selectbox("From Unit:", [
            "mg Milligram", "g Gram", "kg Kilogram", "t Tonne",
            "oz Ounce", "lb Pound", "st Stone"
        ], key="from_weight")
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("### ⚡")
    
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        to_weight = st.selectbox("To Unit:", [
            "kg Kilogram", "g Gram", "mg Milligram", "t Tonne",
            "lb Pound", "oz Ounce", "st Stone"
        ], key="to_weight")
    
    # Weight conversion to grams
    to_grams = {
        "mg": 0.001, "g": 1, "kg": 1000, "t": 1000000,
        "oz": 28.3495, "lb": 453.592, "st": 6350.29
    }
    
    from_unit = from_weight.split()[0]
    to_unit = to_weight.split()[0]
    
    # Convert to grams first, then to target unit
    grams = weight_value * to_grams[from_unit]
    result = grams / to_grams[to_unit]
    
    # Add some fun comparisons
    kg_weight = grams / 1000
    if kg_weight > 100:
        comparison = "🐘 That's heavy as an elephant!"
    elif kg_weight > 10:
        comparison = "🐕 Like a medium dog!"
    elif kg_weight > 1:
        comparison = "📱 Like a smartphone!"
    elif kg_weight > 0.1:
        comparison = "🍎 Like an apple!"
    else:
        comparison = "🪶 Light as a feather!"
    
    st.markdown(f"""
    <div class="result-box">
        ⚖️ {weight_value:,.3f} {from_unit} = {result:,.6f} {to_unit}
        <br><small>{comparison}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features showcase
st.markdown("---")
st.markdown("## 🎯 Why Choose This Converter?")

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>🔄</h3>
        <h4>Instant Results</h4>
        <p>Real-time conversion with every input change</p>
    </div>
    <div class="feature-card">
        <h3>🎨</h3>
        <h4>Beautiful UI</h4>
        <p>Modern gradients and smooth animations</p>
    </div>
    <div class="feature-card">
        <h3>📊</h3>
        <h4>High Precision</h4>
        <p>Accurate calculations up to 6 decimal places</p>
    </div>
    <div class="feature-card">
        <h3>🌟</h3>
        <h4>Smart Context</h4>
        <p>Fun comparisons and helpful indicators</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h3>🚀 All-in-One Converter</h3>
    <p>✨ Currency | 🌡️ Temperature | 📏 Length | ⚖️ Weight</p>
    <p>Made with ❤️ using Streamlit - No sidebars, just pure conversion magic!</p>
</div>
""", unsafe_allow_html=True)