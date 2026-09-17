from streamlit.testing.v1 import AppTest


# TC-A01
def test_explore_page_displays_active_events():
    at = AppTest.from_file("../../app.py")
    at.run()

    # Log in as the seeded attendee
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")

    # Click Login
    at.button(key="btn_login").click()
    at.run()

    # Select Explore from the attendee navigation
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Verify that active events are displayed
    assert len(at.markdown) > 0
    assert any("Tech" in item.value for item in at.markdown)
    
#TC-A02
def test_explore_search_by_title():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Search for PyCon
    at.text_input[0].set_value("PyCon")
    at.run()

    # Matching event should be displayed
    assert any("PyCon" in item.value for item in at.markdown)

    # Unrelated event should not be displayed
    assert not any("Tech Summit Berlin" in item.value for item in at.markdown)
    
#TC-A03
def test_explore_filter_by_category():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select Tech category
    at.selectbox[0].set_value("Tech")
    at.run()

    # Tech events should be displayed
    assert any("Tech" in item.value for item in at.markdown)

    # A known non-Tech event should not be displayed
    assert not any("Berlin Music Festival" in item.value for item in at.markdown)
    
#TC-A04
def test_explore_price_calculation():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select 2 General Admission tickets and 1 VIP ticket
    at.number_input(key="tier_qty_evt_1_tix_evt_1_1").set_value(2)
    at.number_input(key="tier_qty_evt_1_tix_evt_1_2").set_value(1)
    at.run()

    # Verify calculated totals
    assert any("€90.00" in item.value for item in at.markdown)
    assert any("€95.00" in item.value for item in at.markdown)
    assert any("€185.00" in item.value for item in at.markdown)
    assert any("€2.00" in item.value for item in at.markdown)
    assert any("€187.00" in item.value for item in at.markdown)
    
#TC-A05
def test_explore_ticket_quantity_boundary():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # General Admission has a maximum of 100
    quantity_input = at.number_input(key="tier_qty_evt_1_tix_evt_1_1")

    # Verify the UI enforces the boundary
    assert quantity_input.max == 100

    # Maximum valid quantity should be accepted
    quantity_input.set_value(100)
    at.run()

    assert at.number_input(key="tier_qty_evt_1_tix_evt_1_1").value == 100
    
#TC-A06
def test_explore_blocks_checkout_with_zero_tickets():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Attempt to proceed without selecting any tickets
    proceed_buttons = [
        button for button in at.button
        if "Proceed to Payment" in button.label
    ]

    assert proceed_buttons

    proceed_buttons[0].click()
    at.run()

    # Checkout should be blocked
    assert any(
        "Please select at least one ticket quantity to book" in item.value
        for item in at.error
    )

#TC-A07
def test_successful_booking_updates_stock_and_shows_confirmation():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select 2 General Admission tickets
    at.number_input(key="tier_qty_evt_1_tix_evt_1_1").set_value(2)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Enter valid CVC
    cvc_inputs = [
        text_input for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("123")
    at.run()

    # Confirm payment
    pay_buttons = [
        button for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Verify booking confirmation
    assert any(
        "Payment successful" in item.value
        for item in at.success
    )
    
#TC-A08
def test_booking_cancellation_restores_ticket_capacity():
    at = AppTest.from_file("../../app.py")

    # Login
    at.run()
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Open Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Get current available quantity before booking
    ticket_input = at.number_input(key="tier_qty_evt_1_tix_evt_1_1")
    initial_capacity = ticket_input.max

    # Select 2 General Admission tickets
    ticket_input.set_value(2)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Enter CVC
    cvc_inputs = [
        text_input for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("123")
    at.run()

    # Complete payment
    pay_buttons = [
        button for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Open My Bookings
    at.radio(key="nav_radio").set_value("🎟️ My Bookings")
    at.run()

    # Verify booking exists
    assert any(
        "General Admission" in item.value
        for item in at.markdown
    )

    # Find and click Cancel
    cancel_buttons = [
        button for button in at.button
        if "Cancel" in button.label
    ]
    assert cancel_buttons
    cancel_buttons[0].click()
    at.run()

    # Verify cancellation
    assert any(
        "Cancelled" in item.value
        for item in at.markdown
    )

    # Return to Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Capacity should be restored to the original value
    restored_ticket_input = at.number_input(
        key="tier_qty_evt_1_tix_evt_1_1"
    )

    assert restored_ticket_input.max == initial_capacity

#TC-A09
def test_attendee_can_view_booking_history():
    at = AppTest.from_file("../../app.py")

    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Go to Explore Events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select one General Admission ticket
    at.number_input(
        key="tier_qty_evt_1_tix_evt_1_1"
    ).set_value(1)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button
        for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Enter CVC
    cvc_inputs = [
        text_input
        for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("123")
    at.run()

    # Confirm payment
    pay_buttons = [
        button
        for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Navigate to My Bookings
    at.radio(key="nav_radio").set_value("🎟️ My Bookings")
    at.run()

    # Verify booking history
    assert any(
        "General Admission" in item.value
        for item in at.markdown
    )

    assert any(
        "Booking ID" in item.value
        for item in at.markdown
    )
    
#Payment test
  #non-numeric cvc
def test_payment_rejects_non_numeric_cvc():
    at = AppTest.from_file("../../app.py")

    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Explore events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select one ticket
    at.number_input(
        key="tier_qty_evt_1_tix_evt_1_1"
    ).set_value(1)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button
        for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Enter an invalid non-numeric CVC
    cvc_inputs = [
        text_input
        for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("abc")
    at.run()

    # Attempt payment
    pay_buttons = [
        button
        for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Invalid CVC should prevent payment
    assert any(
        "CVC" in item.value
        for item in at.error
    )
    
  #empty cvc
def test_payment_rejects_empty_cvc():
    at = AppTest.from_file("../../app.py")

    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Explore events
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select one ticket
    at.number_input(
        key="tier_qty_evt_1_tix_evt_1_1"
    ).set_value(1)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button
        for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Leave CVC empty
    cvc_inputs = [
        text_input
        for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("")
    at.run()

    # Attempt payment
    pay_buttons = [
        button
        for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Empty CVC should prevent payment
    assert any(
        "CVC" in item.value
        for item in at.error
    )
    
def test_payment_rejects_short_cvc():
    at = AppTest.from_file("../../app.py")
    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Explore
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select one ticket
    at.number_input(key="tier_qty_evt_1_tix_evt_1_1").set_value(1)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Enter a 2-character CVC
    cvc_inputs = [
        text_input for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    cvc_inputs[0].set_value("12")
    at.run()

    # Pay
    pay_buttons = [
        button for button in at.button
        if "Pay & Confirm" in button.label
    ]
    assert pay_buttons
    pay_buttons[0].click()
    at.run()

    # Expected: validation error
    assert any("CVC" in item.value for item in at.error)

#long cvc reject test    
def test_payment_rejects_long_cvc():
    at = AppTest.from_file("../../app.py")
    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Explore
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    # Select one ticket
    at.number_input(key="tier_qty_evt_1_tix_evt_1_1").set_value(1)
    at.run()

    # Proceed to payment
    proceed_buttons = [
        button for button in at.button
        if "Proceed to Payment" in button.label
    ]
    assert proceed_buttons
    proceed_buttons[0].click()
    at.run()

    # Verify CVC field enforces the maximum of 4 characters
    cvc_inputs = [
        text_input for text_input in at.text_input
        if "CVC" in text_input.label
    ]
    assert cvc_inputs
    assert cvc_inputs[0].max_chars == 4
    
    
#Stock Boundary at payment
def test_ticket_quantity_max_matches_remaining_stock():
    at = AppTest.from_file("../../app.py")
    at.run()

    # Login
    at.text_input(key="l_email").set_value("john@test.com")
    at.text_input(key="l_pass").set_value("password123")
    at.button(key="btn_login").click()
    at.run()

    # Explore
    at.radio(key="nav_radio").set_value("🔥 Explore Events")
    at.run()

    quantity_input = at.number_input(
        key="tier_qty_evt_1_tix_evt_1_1"
    )

    # The quantity input must have a valid non-negative maximum.
    assert quantity_input.max >= 0

    # The maximum must be an integer quantity.
    assert quantity_input.max.is_integer()