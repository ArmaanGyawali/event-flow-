# views/auth.py - Multi-step registration flow
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
        # Initialize multi-step state flags for registration
        if "reg_step" not in st.session_state:
            st.session_state["reg_step"] = "details"

        # --- STEP 1: Enter Name, Email, Password ---
        if st.session_state["reg_step"] == "details":
            c1, c2, c3 = st.columns(3)
            r_name = c1.text_input("Full Name", key="r_name")
            r_email = c2.text_input("Email Address", key="r_email")
            r_pass = c3.text_input("Password", type="password", key="r_pass")

            st.write("")
            if st.button("Next: Choose Role ➡️", use_container_width=True, key="btn_next_role"):
                if not r_name or not r_email or not r_pass:
                    st.error("Error: Required fields cannot be empty.")
                elif any(u.email == r_email for u in db.users.values()):
                    st.error(f"Error: An account with email '{r_email}' already exists.")
                elif len(r_pass) < 4:
                    st.error("Password must be at least 4 characters long.")
                else:
                    # Save details temporarily in session state and move to role selection step
                    st.session_state["temp_reg_name"] = r_name
                    st.session_state["temp_reg_email"] = r_email
                    st.session_state["temp_reg_pass"] = r_pass
                    st.session_state["reg_step"] = "role_selection"
                    st.rerun()

        # --- STEP 2: Choose Role & Finalize Account Creation ---
        elif st.session_state["reg_step"] == "role_selection":
            st.markdown("### 🛠️ Select Your Account Role")
            st.info(f"Registering account for: **{st.session_state.get('temp_reg_email')}**")
            
            chosen_role = st.radio(
                "What type of account would you like to create?",
                ["Attendee", "Organiser"],
                key="final_chosen_role"
            )

            col_back, col_create = st.columns(2)
            with col_back:
                if st.button("⬅️ Back", use_container_width=True, key="btn_back_details"):
                    st.session_state["reg_step"] = "details"
                    st.rerun()

            with col_create:
                if st.button("✅ Complete Registration", use_container_width=True, key="btn_complete_reg"):
                    r_name = st.session_state.get("temp_reg_name")
                    r_email = st.session_state.get("temp_reg_email")
                    r_pass = st.session_state.get("temp_reg_pass")
                    r_role = chosen_role

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

                    # Cleanup temp reg states
                    del st.session_state["reg_step"]
                    if "temp_reg_name" in st.session_state:
                        del st.session_state["temp_reg_name"]
                    if "temp_reg_email" in st.session_state:
                        del st.session_state["temp_reg_email"]
                    if "temp_reg_pass" in st.session_state:
                        del st.session_state["temp_reg_pass"]

                    st.success("Account successfully created!")
                    st.rerun()


def logout():
    st.session_state["logged_in_user"] = None
    st.session_state["user_role"] = None
    st.session_state["nav_choice"] = "🔥 Explore Events"
    if "form_tiers" in st.session_state:
        del st.session_state["form_tiers"]
    if "reg_step" in st.session_state:
        del st.session_state["reg_step"]
    st.rerun()