# views/bookings.py
from datetime import datetime

import streamlit as st

import database as db


def _get_event(event_id):
    return next((e for e in db.events if e.event_id == event_id), None)


def _get_ticket_type(ev, ticket_type_id):
    if not ev:
        return None
    return next((t for t in ev.ticket_types if t.ticket_type_id == ticket_type_id), None)


def _event_has_passed(ev):
    """Return True if the event's date is in the past (or event no longer exists)."""
    if ev is None:
        return True
    try:
        event_date = datetime.strptime(ev.date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        # If the date can't be parsed, don't block cancellation on a bad assumption
        return False
    return event_date < datetime.now().date()


def render():
    st.markdown(
        "<div class='main-header'><h1>🎟️ My Bookings</h1></div>",
        unsafe_allow_html=True,
    )

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
        ev = _get_event(b.event_id)
        is_cancelled = b.status == "Cancelled"
        event_passed = _event_has_passed(ev)

        with st.container():
            if is_cancelled:
                # Greyed-out styling for cancelled bookings
                st.markdown(
                    f"""
                    <div style='opacity: 0.5;'>
                    <h3>Event: {b.event_title} <span style='font-size: 0.6em;'>(Cancelled)</span></h3>
                    <ul>
                    <li><b>Booking ID:</b> {b.booking_id}</li>
                    <li><b>Ticket Tier:</b> {b.ticket_type_name}</li>
                    <li><b>Quantity:</b> {b.count}</li>
                    <li><b>Total Paid:</b> €{b.total_price:.2f}</li>
                    <li><b>Date Booked:</b> {b.booking_date}</li>
                    <li><b>Status:</b> Cancelled</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"""
                ### Event: {b.event_title}
                - **Booking ID:** {b.booking_id}
                - **Ticket Tier:** {b.ticket_type_name}
                - **Quantity:** {b.count}
                - **Total Paid:** €{b.total_price:.2f}
                - **Date Booked:** {b.booking_date}
                - **Status:** {b.status}
                """)

                if event_passed:
                    st.caption("This event has already taken place — cancellation is no longer available.")
                else:
                    if st.button("❌ Cancel Booking", key=f"cancel_{b.booking_id}"):
                        b.cancel_booking()

                        # Restore ticket availability back to the event's tier
                        tier = _get_ticket_type(ev, b.ticket_type_id)
                        if tier is not None:
                            tier.available_quantity = min(
                                tier.available_quantity + b.count, tier.quantity
                            )

                        st.session_state["last_booking_success"] = (
                            f"Booking {b.booking_id} has been cancelled."
                        )
                        st.rerun()

        st.write("---")