# views/bookings.py - Attendee Booking Management & State Chart Lifecycle
import streamlit as st

import database as db


def render():
    st.markdown(
        """
        <div class="main-header">
            <h1>🎟️ Your Ticket Reservations</h1>
            <p>Manage active bookings or review your cancellation history.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    u_id = st.session_state["logged_in_user"].user_id
    user_bk = [b for b in db.bookings if b.attendee_id == u_id]

    if not user_bk:
        st.info("You have no ticket reservations in your history.")
        return

    tab_active, tab_trash = st.tabs(["🎫 Active Bookings", "🗑️ Cancelled / History"])

    with tab_active:
        active_bookings = [b for b in user_bk if b.status == "Confirmed"]
        if not active_bookings:
            st.info("No active confirmed bookings found.")
        else:
            for b in active_bookings:
                matching_event = next(
                    (e for e in db.events if e.title == b.event_title), None
                )
                image_url = (
                    matching_event.image_url
                    if matching_event
                    else "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"
                )

                col_img, col_info = st.columns([1, 2])
                with col_img:
                    st.image(image_url, use_container_width=True)
                with col_info:
                    st.markdown(f"### {b.event_title}")
                    if matching_event:
                        st.write(
                            f"📍 **Venue:** {matching_event.location} | 📅 **Date:** {matching_event.date}"
                        )
                    st.write(
                        f"**Tier:** {b.ticket_type_name} | **Qty:** {b.count} | **Total Paid:** €{b.total_price:.2f}"
                    )
                    st.write(f"📅 Booked On: {b.booking_date}")

                    if st.button("Cancel Booking", key=f"cncl_{b.booking_id}"):
                        b.cancel_booking()
                        if matching_event:
                            t_tier = next(
                                (
                                    t
                                    for t in matching_event.ticket_types
                                    if t.name == b.ticket_type_name
                                ),
                                None,
                            )
                            if t_tier:
                                t_tier.available_quantity += b.count
                        st.success(
                            "Booking status changed to 'Cancelled' and ticket quantities restored."
                        )
                        st.rerun()
                st.write("---")

    with tab_trash:
        trash_bookings = [b for b in user_bk if b.status == "Cancelled"]
        if not trash_bookings:
            st.info("No cancelled bookings in your history.")
        else:
            st.warning("Cancelled bookings are preserved for traceability.")
            for b in trash_bookings:
                st.markdown(f"### 🗑️ {b.event_title} (Status: Cancelled)")
                st.write(
                    f"**Tier:** {b.ticket_type_name} | **Qty:** {b.count} | **Paid:** €{b.total_price:.2f}"
                )
                st.write(f"📅 Booked On: {b.booking_date}")
                st.write("---")