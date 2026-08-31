# views/organiser.py - Event creation with external image uploader & dynamic tiers
import os

import streamlit as st

import database as db


def render_dashboard():
    st.subheader("📊 Organiser Dashboard & Event Management")
    u_id = st.session_state["logged_in_user"].user_id

    for e in db.events:
        if not hasattr(e, "is_deleted"):
            e.is_deleted = False

    my_events = [
        e
        for e in db.events
        if getattr(e, "organiser_id", None) == u_id and not e.is_deleted
    ]
    trash_events = [
        e for e in db.events if getattr(e, "organiser_id", None) == u_id and e.is_deleted
    ]

    tab_active, tab_trash = st.tabs(["Active Events", "🗑️ Deleted Events Archive"])

    with tab_active:
        if not my_events:
            st.info("You haven't created any events yet.")
        else:
            for ev in my_events:
                c1, c2 = st.columns([1, 3])
                with c1:
                    img_src = ev.image_url
                    if img_src and not img_src.startswith("http") and os.path.exists(img_src):
                        st.image(img_src, use_container_width=True)
                    else:
                        st.image(img_src if img_src and img_src.startswith("http") else "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800", use_container_width=True)
                with c2:
                    st.markdown(f"### {ev.title} (`{ev.category}`)")
                    st.write(
                        f"📍 **Venue:** {ev.location} | 📅 **Date:** {ev.date} | ⏱️ **Time:** {ev.time}"
                    )
                    
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        new_status = st.selectbox(
                            "Status",
                            ["Active", "Cancelled"],
                            index=0 if ev.status == "Active" else 1,
                            key=f"stat_{ev.event_id}",
                        )
                        if new_status != ev.status:
                            ev.status = new_status
                            st.success("Event status updated!")
                            st.rerun()
                    with col_act2:
                        if st.button("Delete Event", key=f"del_{ev.event_id}"):
                            ev.is_deleted = True
                            st.success("Event deleted and hidden from attendees.")
                            st.rerun()
                st.write("---")

    with tab_trash:
        if not trash_events:
            st.info("Trash bin is empty.")
        else:
            for ev in trash_events:
                st.markdown(f"### 🗑️ {ev.title} (Deleted)")
                if st.button("Restore Event", key=f"rest_{ev.event_id}"):
                    ev.is_deleted = False
                    st.success("Event restored successfully.")
                    st.rerun()
                st.write("---")


def render_create_event():
    st.subheader("➕ Publish New Event")

    if "form_tiers" not in st.session_state:
        st.session_state["form_tiers"] = [{"name": "General Admission", "price": 49.0, "qty": 100}]

    # Image setup outside the form for full interactivity
    st.markdown("### 🖼️ Event Image Setup")
    img_source_type = st.radio("Select Image Input Method", ["Paste Image URL", "Upload Image File"], horizontal=True)
    
    final_image_url = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"
    
    if img_source_type == "Paste Image URL":
        final_image_url = st.text_input("Image URL", value="https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800")
    else:
        uploaded_file = st.file_uploader("Upload Image File", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            final_image_url = file_path
            st.success(f"Image uploaded successfully: {uploaded_file.name}")

    with st.form("c_event_form"):
        title = st.text_input("Event Name")
        desc = st.text_area("Description")
        cat = st.selectbox("Category", ["Tech", "Music", "Conference", "Sports"])
        date = st.text_input("Date (YYYY-MM-DD)", "2026-11-10")
        time = st.text_input("Time", "18:00")
        location = st.text_input("Location")
        artist = st.text_input("Artist / Speaker", "N/A")

        st.markdown("### 🎫 Ticket Tiers Configuration")
        
        updated_tiers = []
        for i, tier in enumerate(st.session_state["form_tiers"]):
            cols = st.columns([2, 1, 1])
            t_name = cols[0].text_input(f"Tier Name {i+1}", value=tier["name"], key=f"t_name_{i}")
            t_price = cols[1].number_input(f"Price (€) {i+1}", min_value=0.0, value=float(tier["price"]), key=f"t_price_{i}")
            t_qty = cols[2].number_input(f"Qty {i+1}", min_value=1, value=int(tier["qty"]), key=f"t_qty_{i}")
            updated_tiers.append({"name": t_name, "price": t_price, "qty": t_qty})

        st.session_state["form_tiers"] = updated_tiers

        submitted = st.form_submit_button("Publish Event", use_container_width=True)

        if submitted:
            if not title or not location or not date:
                st.error("Error: Required event information cannot be empty.")
            elif not st.session_state["form_tiers"]:
                st.error("Error: Please include at least one ticket tier.")
            else:
                new_ev = db.Event(
                    f"evt_{len(db.events) + 1}",
                    title,
                    desc,
                    cat,
                    date,
                    time,
                    location,
                    final_image_url,
                    organiser_id=st.session_state["logged_in_user"].user_id,
                    artist=artist if artist else "N/A",
                )
                
                for idx, tier in enumerate(st.session_state["form_tiers"]):
                    new_ev.add_ticket_type(
                        db.TicketType(
                            f"tix_{new_ev.event_id}_{idx + 1}",
                            tier["name"],
                            tier["price"],
                            int(tier["qty"])
                        )
                    )

                db.events.append(new_ev)
                st.session_state["form_tiers"] = [{"name": "General Admission", "price": 49.0, "qty": 100}]
                st.session_state["nav"] = "📊 Dashboard & Manage"
                st.success("Event successfully created and published! Redirecting to dashboard...")
                st.rerun()

    if st.button("➕ Add Another Tier Field"):
        st.session_state["form_tiers"].append({"name": "", "price": 0.0, "qty": 50})
        st.rerun()


def render_manage_tiers():
    st.subheader("🏷️ Manage Ticket Tiers")
    u_id = st.session_state["logged_in_user"].user_id
    my_events = [
        e
        for e in db.events
        if getattr(e, "organiser_id", None) == u_id and not getattr(e, "is_deleted", False)
    ]

    if not my_events:
        st.info("Please create an active event first.")
        return

    sel_title = st.selectbox("Select Event", [e.title for e in my_events])
    ev = next(e for e in my_events if e.title == sel_title)

    st.write("Current Ticket Tiers:")
    for t in ev.ticket_types:
        st.markdown(f"- **{t.name}**: €{t.price:.2f} ({t.available_quantity}/{t.quantity} available)")

    with st.form("add_tier"):
        st.markdown("### Add New Tier")
        t_name = st.text_input("New Tier Name")
        t_price = st.number_input("Price (€)", min_value=0.0)
        t_qty = st.number_input("Quantity", min_value=1)

        if st.form_submit_button("Add Tier", use_container_width=True):
            if t_name:
                ev.add_ticket_type(
                    db.TicketType(
                        f"tix_{ev.event_id}_{len(ev.ticket_types) + 1}",
                        t_name,
                        t_price,
                        int(t_qty),
                    )
                )
                st.success("Ticket tier added successfully!")
                st.rerun()
            else:
                st.error("Please enter a valid tier name.")


def render_view_bookings():
    st.subheader("📋 View Event Bookings")
    u_id = st.session_state["logged_in_user"].user_id
    my_events = [e for e in db.events if getattr(e, "organiser_id", None) == u_id]

    if not my_events:
        st.info("You have not created any events yet.")
        return

    sel_title = st.selectbox("Select Event to Inspect", [e.title for e in my_events])
    event_bookings = [b for b in db.bookings if b.event_title == sel_title]

    if not event_bookings:
        st.info(f"No bookings found for '{sel_title}'.")
        return

    for b in event_bookings:
        status_color = "green" if b.status == "Confirmed" else "red"
        st.markdown(
            f"**Booking ID:** `{b.booking_id}` | **Attendee ID:** `{b.attendee_id}`"
        )
        st.markdown(
            f"**Tier:** {b.ticket_type_name} | **Qty:** {b.count} | **Total:** €{b.total_price:.2f}"
        )
        st.markdown(
            f"**Status:** :{status_color}[{b.status}] | **Date:** {b.booking_date}"
        )
        st.write("---")