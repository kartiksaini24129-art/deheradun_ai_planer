import streamlit as st
import json
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Dehradun AI Tour Planner", page_icon="🗺️", layout="wide")

st.title("🗺️ Dehradun Smart AI Tour Planner")
st.caption("Science Exhibition Prototype | Hyper-Local Rules Engine & Budget Optimizer")

# 1. Load Custom Dehradun Dataset
@st.cache_data
def load_data():
    with open('dehradun_data.json', 'r') as f:
        return json.load(f)

places = load_data()

# Sidebar User Inputs
st.sidebar.header("⚙️ Tour Parameters")
budget = st.sidebar.slider("Maximum Ticket/Entry Budget (₹)", min_value=0, max_value=500, value=200, step=10)
days = st.sidebar.radio("Trip Duration", [1, 2])
categories = st.sidebar.multiselect("Select Interests", ["Nature", "Heritage", "Peace"], default=["Nature", "Heritage"])
pacing = st.sidebar.selectbox("Pacing Preference", ["Relaxed (Max 2 spots/day)", "Explorer (Max 4 spots/day)"])

# 2. Logic Engine (Custom Algorithm - Non-ChatGPT)
def generate_itinerary(places, budget, categories, pacing, days):
    max_spots_per_day = 2 if "Relaxed" in pacing else 4
    total_allowed_spots = max_spots_per_day * days
    
    # Filter 1: Preference Matching
    filtered = [p for p in places if p["category"] in categories]
    
    # Filter 2: Sort by Value/Cost Ratio
    filtered = sorted(filtered, key=lambda x: x["ticket_cost"])
    
    # Filter 3: Budget Constraint Solver
    selected = []
    current_cost = 0
    
    for spot in filtered:
        if len(selected) < total_allowed_spots:
            if current_cost + spot["ticket_cost"] <= budget:
                selected.append(spot)
                current_cost += spot["ticket_cost"]
                
    return selected, current_cost

# Generate Itinerary Button Action
if st.sidebar.button("🚀 Generate Itinerary"):
    selected_spots, total_cost = generate_itinerary(places, budget, categories, pacing, days)
    
    if not selected_spots:
        st.warning("No spots match your exact budget and preference filters. Try increasing budget or selecting more interests.")
    else:
        # Layout Columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📌 Optimized Itinerary")
            st.write(f"**Total Estimated Entry Cost:** ₹{total_cost} / ₹{budget}")
            
            for idx, spot in enumerate(selected_spots, 1):
                with st.expander(f"Spot {idx}: {spot['name']} ({spot['category']})"):
                    st.write(f"**Description:** {spot['description']}")
                    st.write(f"**Entry Fee:** ₹{spot['ticket_cost']}")
                    st.write(f"**Est. Time Required:** {spot['time_hrs']} hrs")

        with col2:
            st.subheader("📍 Real-Time Location Map")
            # Create Pandas DataFrame for Streamlit Map
            map_data = pd.DataFrame([
                {"name": s["name"], "lat": s["lat"], "lon": s["lon"]} for s in selected_spots
            ])
            st.map(map_data, zoom=11)

else:
    st.info("👈 Set your preferences in the sidebar and click **Generate Itinerary** to test the prototype.")