# app.py - Main Router with Conditional Test Mode Switcher
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
    ("logged_in_user", db.users["att1"]),  # Default to demo attendee on fresh load
    ("user_role", "Attendee"),
    ("last_booking_success", None),
    ("nav_choice", "🔥 Explore Events"),
    ("redirect_to_bookings", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

current_user = st.session_state.get("logged_in_user")

# --- Conditional Test Mode Switcher ---
# Only show the test switcher if no custom user is logged in, 
# or if it's explicitly using one of the default mock accounts ("att1" / "org1")
is_default_test_user = current_user and current_user.user_id in ["att1", "org1"]

if not current_user or is_default_test_user:
    st.sidebar.markdown("### 🛠️ Test Mode Role Switcher")
    current_role_index = 0 if st.session_state["user_role"] == "Attendee" else 1
    selected_role = st.sidebar.radio("Switch Role As:", ["Attendee", "Organiser"], index=current_role_index, key="role_switcher")

    if selected_role == "Attendee" and st.session_state["user_role"] == "Organiser":
        st.session_state["logged_in_user"] = db.users["att1"]
        st.session_state["user_role"] = "Attendee"
        st.session_state["nav_choice"] = "🔥 Explore Events"
        st.rerun()
    elif selected_role == "Organiser" and st.session_state["user_role"] == "Attendee":
        st.session_state["logged_in_user"] = db.users["org1"]
        st.session_state["user_role"] = "Organiser"
        st.session_state["nav_choice"] = "📊 Dashboard & Manage"
        st.rerun()

# If explicitly logged out or cleared, show auth view
if not current_user:
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

    # Handle redirection request BEFORE rendering the sidebar radio widget
    if st.session_state.get("redirect_to_bookings", False):
        st.session_state["nav_choice"] = "🎟️ My Bookings"
        st.session_state["redirect_to_bookings"] = False

    if st.session_state["nav_choice"] not in menu:
        st.session_state["nav_choice"] = menu[0]

    # Force the radio widget to respect st.session_state["nav_choice"] via index matching
    default_index = menu.index(st.session_state["nav_choice"])
    choice = st.sidebar.radio("Navigation", menu, index=default_index, key="nav_radio")
    
    # Keep nav_choice synced if user manually clicks sidebar
    st.session_state["nav_choice"] = choice

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