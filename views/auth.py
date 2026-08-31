# views/auth.py - Strict validation matching Use Cases 1 and 2
import streamlit as st

import database as db


def render_login_register():
    st.subheader("🔑 Account Access")
    tab_login, tab_reg = st.tabs(["🔐 Log In", "📝 Register"])

    with tab_login:
        st.info("Demo Accounts: john@test.com (Attendee) | org@test.com (Organiser)")
        c1, c2 = st.columns(2)
        email = c1.text_input("Email", key="l_email")
        password = c2.text_input("Password", type="password", key="l_pass")

        if st.button("Log In", use_container_width=True, key="btn_login"):
            if not email or not password:
                st.error("Please fill in all required fields.")
            else:
                authenticated = False
                for u in db.users.values():
                    if u.email == email and u.password == password:
                        st.session_state["logged_in_user"] = u
                        st.session_state["user_role"] = (
                            "Organiser"
                            if isinstance(u, db.EventOrganiser)
                            else "Attendee"
                        )
                        st.session_state["nav_choice"] = (
                            "📊 Dashboard & Manage"
                            if st.session_state["user_role"] == "Organiser"
                            else "🔥 Explore Events"
                        )
                        authenticated = True
                        st.success("Authentication successful! Redirecting...")
                        st.rerun()
                if not authenticated:
                    st.error(
                        "Authentication failure: Invalid email or incorrect password."
                    )

    with tab_reg:
        c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])
        r_name = c1.text_input("Name", key="r_name")
        r_email = c2.text_input("Reg Email", key="r_email")
        r_pass = c3.text_input("Reg Pass", type="password", key="r_pass")
        r_role = c4.selectbox("Role", ["Attendee", "Organiser"], key="r_role")

        if st.button("Register Account", use_container_width=True, key="btn_register"):
            if not r_name or not r_email or not r_pass:
                st.error("Error: Required fields cannot be empty.")
            elif any(u.email == r_email for u in db.users.values()):
                st.error(f"Error: An account with email '{r_email}' already exists.")
            elif len(r_pass) < 4:
                st.error("Password must be at least 4 characters long.")
            else:
                u_id = f"usr_{len(db.users) + 1}"
                new_u = (
                    db.EventOrganiser(u_id, r_name, r_email, r_pass)
                    if r_role == "Organiser"
                    else db.Attendee(u_id, r_name, r_email, r_pass)
                )
                db.users[u_id] = new_u
                st.session_state["logged_in_user"] = new_u
                st.session_state["user_role"] = r_role
                st.session_state["nav_choice"] = (
                    "📊 Dashboard & Manage" if r_role == "Organiser" else "🔥 Explore Events"
                )
                st.success("Account successfully created!")
                st.rerun()


def logout():
    st.session_state["logged_in_user"] = None
    st.session_state["user_role"] = None
    st.session_state["nav_choice"] = "🔥 Explore Events"
    if "form_tiers" in st.session_state:
        del st.session_state["form_tiers"]
    st.rerun()