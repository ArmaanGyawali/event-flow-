# views/bookings.py
import streamlit as st
import database as db

def render():
    st.markdown("<div class='main-header'><h1>🎟️ My Bookings</h1></div>", unsafe_allow_html=True)

    if st.session_state.get("last_booking_success"):
        st.success(st.session_state["last_booking_success"])
        # Clear it so it doesn't persist forever on reload
        st.session_state["last_booking_success"] = None

    user = st.session_state["logged_in_user"]
    user_bookings = [b for b in db.bookings if b.attendee_id == user.user_id]

    if not user_bookings:
        st.info("You haven't booked any tickets yet. Explore events to get started!")
        return

    for b in user_bookings:
        with st.container():
            st.markdown(f"""
            ### Event: {b.event_title}
            - **Booking ID:** `{b.booking_id}`
            - **Ticket Tier:** {b.ticket_type_name}
            - **Quantity:** {b.count}
            - **Total Paid:** €{b.total_price:.2f}
            - **Date Booked:** {b.booking_date}
            - **Status:** `{b.status}`
            """)
            st.write("---")