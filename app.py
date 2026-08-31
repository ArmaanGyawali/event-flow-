# app.py - Main Router with Persistent Test Mode Switcher
import streamlit as st

import database as db
from views import auth, bookings, explore, organiser

st.set_page_config(page_title="Event Booking Portal", page_icon="🎫", layout="wide")

st.markdown(
    """
    <style>
    .main-header {
        text-align: center; padding: 2rem 1rem;
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
        color: white; border-radius: 12px; margin-bottom: 1.5rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

for key, default in [
    ("logged_in_user", db.users["att1"]),  # Default to attendee on fresh load
    ("user_role", "Attendee"),
    ("last_booking_success", None),
    ("nav", "🔥 Explore Events"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# --- Always Accessible Test Mode Switcher in Sidebar ---
st.sidebar.markdown("### 🛠️ Test Mode Role Switcher")
current_role_index = 0 if st.session_state["user_role"] == "Attendee" else 1
selected_role = st.sidebar.radio("Switch Role As:", ["Attendee", "Organiser"], index=current_role_index)

if selected_role == "Attendee" and st.session_state["user_role"] == "Organiser":
    st.session_state["logged_in_user"] = db.users["att1"]
    st.session_state["user_role"] = "Attendee"
    st.session_state["nav"] = "🔥 Explore Events"
    st.rerun()
elif selected_role == "Organiser" and st.session_state["user_role"] == "Attendee":
    st.session_state["logged_in_user"] = db.users["org1"]
    st.session_state["user_role"] = "Organiser"
    st.session_state["nav"] = "📊 Dashboard & Manage"
    st.rerun()

# If explicitly logged out or cleared, show auth view
if not st.session_state["logged_in_user"]:
    auth.render_login_register()
else:
    menu = (
        [
            "📊 Dashboard & Manage",
            "➕ Create Event",
            "🏷️ Manage Ticket Tiers",
            "📋 View Bookings",
            "🚪 Logout",
        ]
        if st.session_state["user_role"] == "Organiser"
        else ["🔥 Explore Events", "🎟️ My Bookings", "🚪 Logout"]
    )

    if st.session_state["nav"] not in menu:
        st.session_state["nav"] = menu[0]

    default_index = menu.index(st.session_state["nav"])
    choice = st.sidebar.radio("Navigation", menu, index=default_index)
    st.session_state["nav"] = choice

    if choice == "🔥 Explore Events":
        explore.render()
    elif choice == "🎟️ My Bookings":
        bookings.render()
    elif choice == "📊 Dashboard & Manage":
        organiser.render_dashboard()
    elif choice == "➕ Create Event":
        organiser.render_create_event()
    elif choice == "🏷️ Manage Ticket Tiers":
        organiser.render_manage_tiers()
    elif choice == "📋 View Bookings":
        organiser.render_view_bookings()
    elif choice == "🚪 Logout":
        auth.logout()