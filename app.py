# app.py - Main entry point for the Event Booking Portal
import streamlit as st

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
    ("logged_in_user", None),
    ("user_role", None),
    ("last_booking_success", None),
    ("nav_choice", "🔥 Explore Events"),
    ("redirect_to_dashboard", False),
    ("redirect_to_bookings", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

current_user = st.session_state.get("logged_in_user")

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

    if st.session_state["nav_choice"] not in menu:
        st.session_state["nav_choice"] = menu[0]

    # --- CRITICAL: Handle dashboard redirection BEFORE rendering the sidebar widget ---
    if st.session_state.get("redirect_to_dashboard", False):
        st.session_state["nav_choice"] = "📊 Dashboard & Manage"
        st.session_state["nav_radio"] = "📊 Dashboard & Manage"
        st.session_state["redirect_to_dashboard"] = False

    if st.session_state.get("redirect_to_bookings", False):
        st.session_state["nav_choice"] = "🎟️ My Bookings"
        st.session_state["nav_radio"] = "🎟️ My Bookings"
        st.session_state["redirect_to_bookings"] = False

    # Ensure the choice is valid in the menu before finding its index
    if st.session_state["nav_choice"] not in menu:
        st.session_state["nav_choice"] = menu[0]

    default_index = menu.index(st.session_state["nav_choice"])
    choice = st.sidebar.radio("Navigation", menu, index=default_index, key="nav_radio")

    st.session_state["nav_choice"] = choice

    # --- PAGE ROUTING ---
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