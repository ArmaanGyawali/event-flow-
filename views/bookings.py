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
        # If the date can't be parsed, don't block on a bad assumption
        return False
    return event_date < datetime.now().date()


def _render_active_booking(b, ev, event_passed):
    """Render a non-cancelled booking, with a Cancel button if the event hasn't happened yet."""
    ticket_lines = "\n".join(
        f"    - {i['ticket_type_name']}: {i['count']} × (subtotal €{i['line_total']:.2f})"
        for i in b.items
    )
    st.markdown(f"""
    ### Event: {b.event_title}
    - **Booking ID:** {b.booking_id}
    - **Tickets:**
{ticket_lines}
    - **Total Paid:** €{b.total_price:.2f}
    - **Date Booked:** {b.booking_date}
    - **Status:** {b.status}
    """)

    if not event_passed:
        if st.button("❌ Cancel Booking", key=f"cancel_{b.booking_id}"):
            b.cancel_booking()

            # Restore ticket availability for EVERY tier in this booking
            for i in b.items:
                tier = _get_ticket_type(ev, i["ticket_type_id"])
                if tier is not None:
                    tier.available_quantity = min(
                        tier.available_quantity + i["count"], tier.quantity
                    )

            st.session_state["last_booking_success"] = (
                f"Booking {b.booking_id} has been cancelled."
            )
            st.rerun()

    st.write("---")


def _render_greyed_booking(b, tag):
    """Render a cancelled or past booking in a greyed-out style with a status tag."""
    ticket_lines = "".join(
        f"<li>{i['ticket_type_name']}: {i['count']} × (subtotal €{i['line_total']:.2f})</li>"
        for i in b.items
    )
    st.markdown(
        f"""
        <div style='opacity: 0.5;'>
        <h3>Event: {b.event_title} <span style='font-size: 0.6em;'>({tag})</span></h3>
        <ul>
        <li><b>Booking ID:</b> {b.booking_id}</li>
        <li><b>Tickets:</b></li>
        <ul>{ticket_lines}</ul>
        <li><b>Total Paid:</b> €{b.total_price:.2f}</li>
        <li><b>Date Booked:</b> {b.booking_date}</li>
        <li><b>Status:</b> {b.status}</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")


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

    # Sort bookings into buckets: cancelled, past (event already happened), current (upcoming, active)
    current_bookings = []
    past_bookings = []
    cancelled_bookings = []

    for b in user_bookings:
        ev = _get_event(b.event_id)
        event_passed = _event_has_passed(ev)

        if b.status == "Cancelled":
            cancelled_bookings.append((b, ev, event_passed))
        elif event_passed:
            past_bookings.append((b, ev, event_passed))
        else:
            current_bookings.append((b, ev, event_passed))

    tab_current, tab_past, tab_cancelled = st.tabs(
        [
            f"🎫 Current Bookings ({len(current_bookings)})",
            f"📅 Past Events ({len(past_bookings)})",
            f"🗑️ Cancelled ({len(cancelled_bookings)})",
        ]
    )

    with tab_current:
        if not current_bookings:
            st.info("No upcoming bookings.")
        else:
            for b, ev, event_passed in current_bookings:
                with st.container():
                    _render_active_booking(b, ev, event_passed)

    with tab_past:
        if not past_bookings:
            st.info("No past events yet.")
        else:
            for b, ev, event_passed in past_bookings:
                with st.container():
                    _render_greyed_booking(b, "Past Event")

    with tab_cancelled:
        if not cancelled_bookings:
            st.info("No cancelled bookings.")
        else:
            for b, ev, event_passed in cancelled_bookings:
                with st.container():
                    _render_greyed_booking(b, "Cancelled")