# views/bookings.py
from datetime import datetime

import streamlit as st

import database as db


def _get_event(event_id):
    """Find and return an event using its ID."""
    return next(
        (e for e in db.events if e.event_id == event_id),
        None,
    )


def _get_ticket_type(ev, ticket_type_id):
    """Find and return a ticket tier using its ID."""
    if not ev:
        return None

    return next(
        (
            t
            for t in ev.ticket_types
            if t.ticket_type_id == ticket_type_id
        ),
        None,
    )


def _event_has_passed(ev):
    """Return True if the event date is in the past."""
    if ev is None:
        return True

    try:
        event_date = datetime.strptime(
            ev.date,
            "%Y-%m-%d"
        ).date()
    except (ValueError, TypeError):
        return False

    return event_date < datetime.now().date()


def _display_booking(booking, category):
    """Display one booking with information based on its category."""

    ev = _get_event(booking.event_id)

    with st.container():

        # CURRENT BOOKING
        if category == "current":
            st.markdown(
                f"""
                ### 🎟️ {booking.event_title}

                - **Booking ID:** `{booking.booking_id}`
                - **Ticket Tier:** {booking.ticket_type_name}
                - **Quantity:** {booking.count}
                - **Total Paid:** €{booking.total_price:.2f}
                - **Date Booked:** {booking.booking_date}
                - **Status:** 🟢 {booking.status}
                """
            )

            if st.button(
                "❌ Cancel Booking",
                key=f"cancel_{booking.booking_id}",
            ):
                booking.cancel_booking()

                # Return the tickets to the available inventory
                tier = _get_ticket_type(
                    ev,
                    booking.ticket_type_id,
                )

                if tier is not None:
                    tier.available_quantity = min(
                        tier.available_quantity + booking.count,
                        tier.quantity,
                    )

                st.session_state["last_booking_success"] = (
                    f"Booking {booking.booking_id} has been cancelled."
                )

                st.rerun()

        # PAST EVENT
        elif category == "past":
            st.markdown(
                f"""
                ### 🕘 {booking.event_title}

                - **Booking ID:** `{booking.booking_id}`
                - **Ticket Tier:** {booking.ticket_type_name}
                - **Quantity:** {booking.count}
                - **Total Paid:** €{booking.total_price:.2f}
                - **Date Booked:** {booking.booking_date}
                - **Status:** 🕘 Event Completed
                """
            )

            st.caption(
                "This event has already taken place. "
                "The booking can no longer be cancelled."
            )

        # CANCELLED BOOKING
        elif category == "cancelled":
            st.markdown(
                f"""
                ### 🗑️ {booking.event_title}

                - **Booking ID:** `{booking.booking_id}`
                - **Ticket Tier:** {booking.ticket_type_name}
                - **Quantity:** {booking.count}
                - **Total Paid:** €{booking.total_price:.2f}
                - **Date Booked:** {booking.booking_date}
                - **Status:** 🔴 Cancelled
                """
            )

            st.info(
                "This booking has been cancelled. "
                "The tickets have been returned to the event inventory."
            )




def render():
    """Render the attendee's My Bookings page."""

    st.markdown(
        "<div class='main-header'><h1>🎟️ My Bookings</h1></div>",
        unsafe_allow_html=True,
    )

    # Display cancellation success message
    if st.session_state.get("last_booking_success"):
        st.success(
            st.session_state["last_booking_success"]
        )

        # Clear message after displaying it once
        st.session_state["last_booking_success"] = None

    user = st.session_state["logged_in_user"]

    # Get all bookings belonging to the logged-in attendee
    user_bookings = [
        b
        for b in db.bookings
        if b.attendee_id == user.user_id
    ]

    if not user_bookings:
        st.info(
            "You haven't booked any tickets yet. "
            "Explore events to get started!"
        )
        return

    # Separate bookings into three categories

    current_bookings = []
    past_bookings = []
    cancelled_bookings = []

    for booking in user_bookings:

        # Cancelled bookings always go into the
        # cancelled section.
        if booking.status == "Cancelled":
            cancelled_bookings.append(booking)
            continue

        event = _get_event(booking.event_id)

        # Confirmed bookings are divided according
        # to whether the event has already happened.
        if _event_has_passed(event):
            past_bookings.append(booking)
        else:
            current_bookings.append(booking)

    # Create the three booking tabs
    tab_current, tab_past, tab_cancelled = st.tabs(
        [
            f"🟢 Current Bookings ({len(current_bookings)})",
            f"🕘 Past Events ({len(past_bookings)})",
            f"🗑️ Cancelled ({len(cancelled_bookings)})",
        ]
    )

    # CURRENT BOOKINGS
    with tab_current:

        if not current_bookings:
            st.info(
                "You don't have any current bookings."
            )
        else:
            for booking in current_bookings:
                _display_booking(
                    booking,
                    "current",
                )
                st.write("---")

    # PAST EVENTS
    with tab_past:

        if not past_bookings:
            st.info(
                "You don't have any past event bookings."
            )
        else:
            for booking in past_bookings:
                _display_booking(
                    booking,
                    "past",
                )
                st.write("---")

  
    # CANCELLED BOOKINGS
    with tab_cancelled:

        if not cancelled_bookings:
            st.info(
                "You don't have any cancelled bookings."
            )
        else:
            for booking in cancelled_bookings:
                _display_booking(
                    booking,
                    "cancelled",
                )
                st.write("---")

