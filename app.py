import json
import streamlit as st

st.set_page_config(
    page_title="Dehradun Smart AI Tour Planner", page_icon="🗺️"
)

st.title("🗺️ Dehradun Smart AI Tour Planner")
st.caption(
    "Science Exhibition Prototype | Hyper-Local Rules Engine & Budget Optimizer"
)


# 1. Load Custom Dehradun Dataset
@st.cache_data
def load_data():
  with open("dehradun_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
  return data


places = load_data()

# Sidebar User Inputs
st.sidebar.header("⚙️ Tour Parameters")
budget = st.sidebar.slider(
    "Maximum Ticket/Entry Budget (₹)", min_value=0, max_value=300, value=200
)
days = st.sidebar.radio("Trip Duration", [1, 2])
categories = st.sidebar.multiselect(
    "Select Interests", ["Nature", "Heritage"], default=["Nature", "Heritage"]
)
pacing = st.sidebar.selectbox(
    "Pacing Preference", ["Relaxed (Max 2 spots/day)", "Active"]
)


# 2. Logic Engine (Filter & Optimize)
def generate_itinerary(places, budget, categories, pacing, days):
  # Filter by category and entry fee budget
  filtered = [
      p
      for p in places
      if p["category"] in categories and p["entry_fee"] <= budget
  ]

  # Sort by entry fee
  filtered = sorted(filtered, key=lambda x: x["entry_fee"])

  # Determine max spots based on duration and pacing
  max_spots = days * 2 if "Relaxed" in pacing else days * 4
  selected = filtered[:max_spots]

  total_cost = sum(p["entry_fee"] for p in selected)
  return selected, total_cost


selected_spots, total_cost = generate_itinerary(
    places, budget, categories, pacing, days
)

st.subheader(f"Total Estimated Entry Cost: ₹{total_cost} / ₹{budget}")

if not selected_spots:
  st.warning(
      "Koi bhi spot aapke budget ya category match nahi kar raha. Parameters"
      " change karein!"
  )
else:
  for i, spot in enumerate(selected_spots, 1):
    with st.expander(f"Spot {i}: {spot['name']} ({spot['category']})"):
      st.write(f"💸 **Entry Fee:** ₹{spot['entry_fee']}")
      st.write(f"⭐ **Rating:** {spot['rating']}")
      st.write(f"⏰ **Best Time:** {spot['best_time']}")
      st.write(f"🍽️ **Food Spot:** {spot['food_spot']}")
      st.write(f"💡 **Weather Tip:** {spot['weather_tip']}")