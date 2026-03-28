import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Energy Analyzer ⚡", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0a1f12;}
    h1 {color: #4ade80 !important; text-align: center;}
    .suggestion {background-color: #1a2f22; padding: 15px; border-radius: 10px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 Smart Energy Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### Presented by *Code Encoders*")
st.caption("Your Personal AI Energy Coach | SDG 7 • 12 • 13")

# ================== CITY DATA ==================
city_data = {
    "Delhi": {"tariff": [(0,200,3.0),(201,400,5.0),(401,800,6.5),(801,1200,7.0),(1201,float('inf'),8.0)], "co2": 0.73, "note": "Subsidy up to 200 units common"},
    "Mumbai": {"tariff": [(0,100,4.0),(101,300,6.0),(301,500,7.5),(501,float('inf'),9.0)], "co2": 0.75, "note": "High urban demand"},
    "Bangalore": {"tariff": [(0,50,3.5),(51,100,5.0),(101,200,6.5),(201,float('inf'),8.0)], "co2": 0.72, "note": "Good solar incentives"},
    "Hyderabad": {"tariff": [(0,100,3.5),(101,200,5.0),(201,400,6.5),(401,float('inf'),8.0)], "co2": 0.74, "note": "Subsidized for some categories"},
    "Chennai": {"tariff": [(0,100,4.0),(101,200,5.5),(201,500,7.0),(501,float('inf'),8.5)], "co2": 0.76, "note": "Strong renewable push"}
}

selected_city = st.selectbox("🌆 Select Your City", list(city_data.keys()), index=0)
city_info = city_data[selected_city]
tariff_slabs = city_info["tariff"]
CO2_FACTOR = city_info["co2"]

st.info(f"📍 Working for *{selected_city}* • {city_info['note']}")

# ================== IMPROVED APPLIANCES WITH VARIANTS ==================
appliances = {
    # AC Variants
    "AC 1 Ton (5-star)": 800,
    "AC 1.5 Ton (5-star)": 1200,
    "AC 2 Ton (5-star)": 1600,
    
    # Washing Machine Variants
    "Washing Machine 6kg (Semi-auto)": 350,
    "Washing Machine 7kg (Fully-auto)": 450,
    "Washing Machine 8kg (Fully-auto)": 550,
    
    # Refrigerator Variants
    "Refrigerator 190L (5-star)": 120,
    "Refrigerator 250L (5-star)": 150,
    "Refrigerator 320L (5-star)": 180,
    
    # Geyser Variants
    "Geyser 15L Instant": 2500,
    "Geyser 25L Storage": 2000,
    
    # Common ones
    "Ceiling Fan (60W)": 60,
    "LED Bulb (9W)": 9,
    "Tube Light (40W)": 40,
    "TV (LED 55\")": 100,
    "Laptop Charger": 65,
    "Microwave": 1200,
    "Water Pump (0.5 HP)": 750,
    "Desktop PC": 300
}

# Sidebar
st.sidebar.header("📋 Your Home Details")
monthly_units = st.sidebar.number_input("Monthly electricity units (from bill)", min_value=50, value=300, step=10)
num_people = st.sidebar.number_input("Number of people in house", min_value=1, value=4)

st.sidebar.subheader("🛠️ Select Your Appliances")
selected_appliances = st.sidebar.multiselect(
    "Choose appliances you have",
    options=list(appliances.keys()),
    default=["Ceiling Fan (60W)", "Refrigerator 250L (5-star)", "AC 1.5 Ton (5-star)", "TV (LED 55\")", "Washing Machine 7kg (Fully-auto)"]
)

# Base Calculation
base_breakdown = {}
total_monthly = 0.0

for app in selected_appliances:
    hours = st.sidebar.slider(f"Hours/day - {app}", 0.0, 24.0, 8.0 if "AC" in app else 6.0 if "Washing" in app else 4.0, 0.5)
    monthly_kwh = round((appliances[app] * hours * 30) / 1000, 1)
    base_breakdown[app] = monthly_kwh
    total_monthly += monthly_kwh

def calculate_bill(units, slabs):
    cost = 0.0
    rem = units
    for min_u, max_u, rate in slabs:
        if rem <= 0: break
        slab_u = min(rem, max_u - min_u if max_u != float('inf') else rem)
        cost += slab_u * rate
        rem -= slab_u
    return round(cost)

base_bill = calculate_bill(total_monthly, tariff_slabs)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ Energy & Cost", 
    "🔄 What-If Simulator", 
    "🧠 Energy Personality",
    "🌟 Smart Suggestions", 
    "📊 Energy Breakdown"
])

with tab1:
    st.subheader(f"Energy & Bill - {selected_city}")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Monthly Consumption", f"{total_monthly:.1f} kWh")
    with col2: st.metric("Estimated Bill", f"₹{base_bill}")
    with col3: st.metric("People", f"{num_people}")

with tab2:
    st.subheader("🔄 What-If Simulator")
    sim_apps = st.multiselect("Choose appliances to change", selected_appliances, default=selected_appliances)
    sim_total = 0.0
    for app in sim_apps:
        hrs = st.slider(f"New hours for {app}", 0.0, 24.0, 8.0 if "AC" in app else 6.0, 0.5, key=f"sim_{app}")
        sim_total += (appliances[app] * hrs * 30) / 1000
    new_monthly = round(sim_total, 1)
    savings = int((total_monthly - new_monthly) * 6.5)
    st.success(f"New Usage: {new_monthly} kWh | *Potential Savings: ₹{savings}* 💰")

with tab3:
    st.subheader("🧠 Energy Personality Score")
    q1 = st.slider("Leave chargers on standby?", 1, 10, 5)
    q2 = st.slider("Turn off AC/fan when leaving room?", 1, 10, 5)
    q3 = st.slider("Unnecessary appliances running?", 0, 10, 3)
    score = max(20, 100 - (q1*4 + (10-q2)*5 + q3*7))
    st.metric("Your Score", f"{score}/100")

with tab4:
    st.subheader("🌟 Smart Suggestions (Our Main Novelty)")
    st.write("AI-powered personalized recommendations based on your usage")

    suggestions = []

    # Find top consumer
    if base_breakdown:
        top_app = max(base_breakdown, key=base_breakdown.get)
        top_kwh = base_breakdown[top_app]
        percent = round(top_kwh / total_monthly * 100)

        suggestions.append({
            "icon": "🔥",
            "title": f"{top_app} is your highest consumer ({percent}%)",
            "desc": f"Consuming {top_kwh} kWh per month.",
            "action": "Service regularly, use efficiently, consider upgrading to higher star rating",
            "saving": f"Potential saving: ₹{int(top_kwh * 0.35 * 6.5)}/month"
        })

    # AC specific suggestions
    ac_apps = [app for app in selected_appliances if "AC" in app]
    if ac_apps:
        for ac in ac_apps:
            ac_kwh = base_breakdown[ac]
            if ac_kwh > 80:
                suggestions.append({
                    "icon": "❄️",
                    "title": f"Optimize {ac}",
                    "desc": "Air conditioners are major power consumers in summer.",
                    "action": "Set temperature to 24-26°C, use with fan, clean filters monthly",
                    "saving": f"Save up to ₹{int(ac_kwh*0.3*6.5)}/month"
                })

    # Washing Machine
    if any("Washing" in app for app in selected_appliances):
        suggestions.append({
            "icon": "🧼",
            "title": "Washing Machine Tips",
            "desc": "Washing machines consume more when overloaded or using hot water.",
            "action": "Run full loads, use eco mode, avoid hot water cycles",
            "saving": "Save ₹200-450/month"
        })

    # General high-impact suggestions
    if total_monthly > 350:
        suggestions.append({
            "icon": "☀️",
            "title": f"Go Solar in {selected_city}",
            "desc": "With current government subsidies, solar is very beneficial.",
            "action": "Install 2-3 kW rooftop solar system",
            "saving": f"Can reduce your bill by 50-70% (₹{int(total_monthly*0.6*6.5)}/month)"
        })

    suggestions.append({
        "icon": "🔌",
        "title": "Eliminate Vampire Power",
        "desc": "Devices on standby (TV, chargers, routers) waste 5-8% energy.",
        "action": "Use smart plugs or switch off at mains",
        "saving": "Save ₹150-350/month"
    })

    # Display suggestions
    for sug in suggestions:
        st.markdown(f"""
        <div class="suggestion">
            <h4>{sug['icon']} {sug['title']}</h4>
            <p><strong>Why:</strong> {sug['desc']}</p>
            <p><strong>Recommended Action:</strong> {sug['action']}</p>
            <p><strong>Estimated Monthly Saving:</strong> <span style="color:#4ade80">{sug['saving']}</span></p>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.subheader("📊 How & Where Energy is Consumed")
    if base_breakdown:
        df = pd.DataFrame(list(base_breakdown.items()), columns=["Appliance", "Monthly kWh"])
        fig = px.pie(df, values="Monthly kWh", names="Appliance", title=f"Energy Breakdown - {selected_city}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

st.caption(f"Built by *Code Encoders* | Enhanced Appliance Models + Smart Suggestions | {selected_city}")