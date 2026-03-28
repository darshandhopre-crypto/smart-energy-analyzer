import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Smart Energy Analyzer ⚡", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0a1f12;}
    h1 {color: #4ade80 !important; text-align: center;}
    .suggestion {background-color: #1a2f22; padding: 15px; border-radius: 10px; margin: 12px 0;}
    .reward {background-color: #2a3f2a; padding: 15px; border-radius: 10px; margin: 12px 0; border: 2px solid #4ade80;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 Smart Energy Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### Presented by **Code Encoders**")
st.caption("AI Energy Coach with Alexa Voice Integration | SDG 7 • 12 • 13")

# City Data
city_data = {
    "Delhi": {"co2": 0.73, "note": "Subsidy up to 200 units"},
    "Mumbai": {"co2": 0.75, "note": "High urban demand"},
    "Bangalore": {"co2": 0.72, "note": "Good solar incentives"}
}

selected_city = st.selectbox("🌆 Select Your City", list(city_data.keys()), index=0)
CO2_FACTOR = city_data[selected_city]["co2"]

# Appliances
appliances = {
    "AC 1 Ton (5-star)": 800, "AC 1.5 Ton (5-star)": 1200, "AC 2 Ton (5-star)": 1600,
    "Washing Machine 7kg": 450, "Refrigerator 250L (5-star)": 150,
    "Ceiling Fan (60W)": 60, "LED Bulb (9W)": 9, "TV (LED 55\")": 100,
    "Geyser 15L Instant": 2500
}

# Sidebar
st.sidebar.header("Your Home Details")
num_people = st.sidebar.number_input("Number of people in house", value=4)

selected_appliances = st.sidebar.multiselect("Select Your Appliances", 
    list(appliances.keys()),
    default=["Ceiling Fan (60W)", "Refrigerator 250L (5-star)", "AC 1.5 Ton (5-star)"])

# Base Calculation
base_breakdown = {}
total_monthly = 0.0
base_usage = {}

for app in selected_appliances:
    hours = st.sidebar.slider(f"Hours/day - {app}", 0.0, 24.0, 8.0 if "AC" in app else 4.0, 0.5)
    base_usage[app] = hours
    kwh = round((appliances[app] * hours * 30) / 1000, 1)
    base_breakdown[app] = kwh
    total_monthly += kwh

estimated_bill = int(total_monthly * 6.5)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ Energy & Cost", 
    "🔄 What-If Simulator", 
    "🏆 Rewards & Coupons", 
    "🌟 Smart Suggestions", 
    "🎤 Alexa Voice Assistant"
])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Monthly Consumption", f"{total_monthly:.1f} kWh")
    with col2: st.metric("Estimated Bill", f"₹{estimated_bill}")
    with col3: st.metric("People", f"{num_people}")

with tab2:
    st.subheader("🔄 What-If Simulator")
    sim_apps = st.multiselect("Select appliances to simulate", selected_appliances, default=selected_appliances)
    simulated_total = 0.0
    for app in sim_apps:
        current_hours = base_usage.get(app, 6.0)
        new_hours = st.slider(f"New hours/day for {app}", 0.0, 24.0, current_hours, 0.5, key=f"sim_{app}")
        simulated_total += (appliances[app] * new_hours * 30) / 1000
    new_monthly = round(simulated_total, 1)
    savings_kwh = max(0, total_monthly - new_monthly)
    savings_rs = int(savings_kwh * 6.5)
    col1, col2 = st.columns(2)
    with col1: st.metric("Original Usage", f"{total_monthly:.1f} kWh")
    with col2: st.metric("New Usage", f"{new_monthly} kWh", delta=f"-{savings_kwh:.1f} kWh")
    st.success(f"**Potential Monthly Savings: ₹{savings_rs}** 💰")

# ================== NEW REWARDS & COUPONS TAB ==================
with tab3:
    st.subheader("🏆 Rewards & Coupons")
    st.write("Earn rewards by saving energy!")

    # Calculate reward points (simple logic)
    total_saving_potential = int(total_monthly * 0.25 * 6.5)  # assume 25% saving potential
    points = int((5000 - total_monthly) / 10) if total_monthly < 5000 else 50
    points = max(50, min(500, points))

    st.metric("Your Current Energy Points", f"{points} ⭐")

    st.write("**Available Rewards**")
    col1, col2 = st.columns(2)
    with col1:
        if points >= 150:
            st.success("🎟️ **₹200 Amazon Coupon** (150 points)")
        else:
            st.warning("🔒 150 points needed for ₹200 Amazon Coupon")
    with col2:
        if points >= 300:
            st.success("☀️ **Solar Panel Discount Voucher** (300 points)")
        else:
            st.warning("🔒 300 points needed for Solar Discount")

    st.info("**How to earn more points?** Follow the Smart Suggestions below!")

# ================== IMPROVED SMART SUGGESTIONS ==================
with tab4:
    st.subheader("🌟 Smart Suggestions Engine")
    st.write("**AI-powered personalized recommendations**")

    if base_breakdown:
        top_app = max(base_breakdown, key=base_breakdown.get)
        top_kwh = base_breakdown[top_app]
        percent = round(top_kwh / total_monthly * 100)

        st.markdown(f"""
        <div class="suggestion">
            <h4>🔥 {top_app} is your highest consumer ({percent}%)</h4>
            <p><strong>Action:</strong> Service regularly + use timer/smart plug</p>
            <p><strong>Potential Saving:</strong> ₹{int(top_kwh * 0.4 * 6.5)}/month</p>
        </div>
        """, unsafe_allow_html=True)

    if any("AC" in app for app in selected_appliances):
        st.markdown(f"""
        <div class="suggestion">
            <h4>❄️ Optimize your Air Conditioner</h4>
            <p><strong>Action:</strong> Set temperature to 24-26°C and use with fan</p>
            <p><strong>Potential Saving:</strong> ₹800 - 1500/month</p>
        </div>
        """, unsafe_allow_html=True)

    if total_monthly > 350:
        st.markdown(f"""
        <div class="suggestion">
            <h4>☀️ Go Solar in {selected_city}</h4>
            <p><strong>Action:</strong> Install 2-3 kW rooftop solar system</p>
            <p><strong>Potential Saving:</strong> ₹{int(total_monthly * 0.6 * 6.5)}/month (50-70% bill reduction)</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="suggestion">
        <h4>🔌 Kill Standby Power</h4>
        <p><strong>Action:</strong> Unplug chargers, TV, router when not in use</p>
        <p><strong>Potential Saving:</strong> ₹200 - 400/month</p>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.subheader("🎤 Alexa Voice Assistant")
    st.write("**Smart voice commands for your home**")
    if st.button("🔗 Connect to Alexa", type="primary"):
        st.success("✅ Connected to Alexa!")
        st.balloons()

    st.write("### Recommended Alexa Commands")
    for app in selected_appliances:
        if "AC" in app:
            st.markdown(f"<div class='alexa-box'>🎙️ Alexa, set the {app} to 25 degrees</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='alexa-box'>🎙️ Alexa, turn off the {app} when no one is in the room</div>", unsafe_allow_html=True)

    st.caption("In future, these commands can be sent directly to Alexa devices.")

st.caption("Built by **Code Encoders** • Smart Energy Analyzer with Rewards System")