# views/explore.py - Two-step checkout flow with complete state cleanup & safe redirection flag
import os
from datetime import datetime, timezone

import streamlit as st

import database as db


def render():
    st.markdown(
        "<div class='main-header'><h1>🔥 Explore Events & Book Tickets</h1></div>",
        unsafe_allow_html=True,
    )

    # Search & Filter Controls
    c1, c2 = st.columns([2, 1])
    search_query = c1.text_input("Search events by title or artist...", "").lower()

    categories = ["All"] + list(set(e.category for e in db.events))
    selected_cat = c2.selectbox("Filter by Category", categories)

    # Filter events logic
    active_events = []
    for ev in db.events:
        if getattr(ev, "is_deleted", False):
            continue
        if getattr(ev, "status", "Active") != "Active":
            continue

        matches_search = (
            search_query in ev.title.lower()
            or search_query in getattr(ev, "artist", "").lower()
            or search_query in ev.location.lower()
        )
        matches_cat = selected_cat == "All" or ev.category == selected_cat

        if matches_search and matches_cat:
            active_events.append(ev)

    if not active_events:
        st.info("No events found matching your criteria.")
        return

    # Display Event Feed
    for ev in active_events:
        with st.container():
            col_img, col_info = st.columns([1, 3])
            with col_img:
                img_src = ev.image_url
                if (
                    img_src
                    and not img_src.startswith("http")
                    and os.path.exists(img_src)
                ):
                    st.image(img_src, use_container_width=True)
                else:
                    st.image(
                        img_src
                        if img_src and img_src.startswith("http")
                        else "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",
                        use_container_width=True,
                    )

            with col_info:
                st.markdown(f"### {ev.title} (`{ev.category}`)")
                st.markdown(
                    f"📍 **Venue:** {ev.location} | 📅 **Date:** {ev.date} at {ev.time}"
                )
                if getattr(ev, "artist", "N/A") != "N/A":
                    st.markdown(f"🎤 **Featured:** {ev.artist}")
                st.write(ev.description)

                # Track checkout step per event using session state
                step_key = f"checkout_step_{ev.event_id}"
                if step_key not in st.session_state:
                    st.session_state[step_key] = "selecting"

                # Multi-tier reservation expander
                with st.expander(f"🎟️ Reserve Tickets for {ev.title}"):
                    if not ev.ticket_types:
                        st.warning("No ticket tiers currently available for this event.")
                    else:
                        # --- STEP 1: Select Quantities ---
                        if st.session_state[step_key] == "selecting":
                            st.markdown("Configure quantities for any/all tiers you want to book:")

                            selected_selections = []
                            total_booking_cost = 0.0
                            platform_fee = 2.00  # Flat service fee per ticket

                            for tier in ev.ticket_types:
                                cols = st.columns([2, 1, 1])
                                cols[0].markdown(
                                    f"**{tier.name}** (€{tier.price:.2f} + €2 fee)"
                                )
                                cols[1].markdown(f"Left: {tier.available_quantity}")
                                qty = cols[2].number_input(
                                    "Qty",
                                    min_value=0,
                                    max_value=int(tier.available_quantity),
                                    value=0,
                                    key=f"tier_qty_{ev.event_id}_{tier.ticket_type_id}",
                                )

                                if qty > 0:
                                    line_price = (tier.price + platform_fee) * qty
                                    selected_selections.append(
                                        {"tier": tier, "qty": qty, "line_total": line_price}
                                    )
                                    total_booking_cost += line_price

                            if selected_selections:
                                st.markdown(
                                    f"### 💶 Combined Total Cost: **€{total_booking_cost:.2f}** (Includes €2.00 fee per ticket)"
                                )

                            if st.button("Proceed to Payment", key=f"proceed_btn_{ev.event_id}"):
                                if not selected_selections:
                                    st.error("Please select at least one ticket quantity to book.")
                                else:
                                    st.session_state[f"pending_sel_{ev.event_id}"] = selected_selections
                                    st.session_state[f"pending_cost_{ev.event_id}"] = total_booking_cost
                                    st.session_state[step_key] = "paying"
                                    st.rerun()

                        # --- STEP 2: Payment Screen ---
                        elif st.session_state[step_key] == "paying":
                            st.markdown("### 💳 Secure Checkout & Payment")
                            total_cost = st.session_state.get(f"pending_cost_{ev.event_id}", 0.0)
                            st.info(f"Amount Due: **€{total_cost:.2f}**")

                            pay_method = st.selectbox(
                                "Select Payment Method",
                                ["Credit Card (**** **** **** 4242)", "PayPal", "Apple Pay"],
                                key=f"pay_meth_{ev.event_id}"
                            )
                            card_cvc = st.text_input(
                                "Enter CVC / PIN",
                                type="password",
                                key=f"cvc_{ev.event_id}",
                                max_chars=4
                            )

                            col_back, col_pay = st.columns(2)
                            with col_back:
                                if st.button("⬅️ Back", key=f"back_btn_{ev.event_id}"):
                                    st.session_state[step_key] = "selecting"
                                    st.rerun()

                            with col_pay:
                                if st.button("Pay & Confirm Booking", key=f"pay_btn_{ev.event_id}"):
                                    if not card_cvc or len(card_cvc) < 3:
                                        st.error("Please enter a valid CVC/PIN to authorize payment.")
                                    else:
                                        selected_selections = st.session_state.get(f"pending_sel_{ev.event_id}", [])
                                        booking_summary_ids = []

                                        for item in selected_selections:
                                            t = item["tier"]
                                            q = item["qty"]
                                            t.available_quantity -= q

                                            b_id = f"bkg_{len(db.bookings) + 1}"
                                            new_b = db.Booking(
                                                booking_id=b_id,
                                                attendee_id=st.session_state["logged_in_user"].user_id,
                                                event_id=ev.event_id,
                                                event_title=ev.title,
                                                ticket_type_id=t.ticket_type_id,
                                                ticket_type_name=t.name,
                                                count=q,
                                                total_price=item["line_total"],
                                                booking_date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                                                status="Confirmed",
                                            )
                                            db.bookings.append(new_b)
                                            booking_summary_ids.append(b_id)

                                        # Clean up checkout states completely
                                        del st.session_state[step_key]
                                        if f"pending_sel_{ev.event_id}" in st.session_state:
                                            del st.session_state[f"pending_sel_{ev.event_id}"]
                                        if f"pending_cost_{ev.event_id}" in st.session_state:
                                            del st.session_state[f"pending_cost_{ev.event_id}"]
                                        if f"cvc_{ev.event_id}" in st.session_state:
                                            del st.session_state[f"cvc_{ev.event_id}"]
                                        
                                        # Reset quantity inputs back to 0
                                        for tier in ev.ticket_types:
                                            qty_key = f"tier_qty_{ev.event_id}_{tier.ticket_type_id}"
                                            if qty_key in st.session_state:
                                                st.session_state[qty_key] = 0

                                        st.success(f"Payment successful! Bookings confirmed: {', '.join(booking_summary_ids)}")
                                        
                                        # Trigger safe navigation flag and rerun
                                        st.session_state["redirect_to_bookings"] = True
                                        st.rerun()

        st.write("---")