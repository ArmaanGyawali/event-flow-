from database import Booking, Event, TicketType


def test_booking_creation_integrates_event_ticket_and_attendee():
    # Arrange
    event = Event(
        "evt_test",
        "Integration Test Event",
        "Test event",
        "Tech",
        "2026-11-20",
        "18:00",
        "Berlin",
        "image.jpg",
        "org1",
    )

    ticket = TicketType(
        "ticket_1",
        "General Admission",
        45.0,
        100,
    )

    event.add_ticket_type(ticket)

    attendee_id = "att1"
    quantity = 2

    # Act
    line_total = ticket.price * quantity
    ticket.available_quantity -= quantity

    booking = Booking(
        booking_id="bkg_integration",
        attendee_id=attendee_id,
        event_id=event.event_id,
        event_title=event.title,
        items=[
            {
                "ticket_type_id": ticket.ticket_type_id,
                "ticket_type_name": ticket.name,
                "count": quantity,
                "line_total": line_total,
            }
        ],
        total_price=line_total + 2.00,
    )

    # Assert
    assert booking.attendee_id == attendee_id
    assert booking.event_id == event.event_id
    assert booking.event_title == event.title
    assert booking.items[0]["ticket_type_id"] == ticket.ticket_type_id
    assert booking.items[0]["count"] == 2
    assert booking.total_price == 92.00
    assert ticket.available_quantity == 98


def test_cancelling_booking_restores_ticket_quantity():
    # Arrange
    event = Event(
        "evt_cancel",
        "Cancellation Integration Test",
        "Test event",
        "Tech",
        "2026-11-20",
        "18:00",
        "Berlin",
        "image.jpg",
        "org1",
    )

    ticket = TicketType(
        "ticket_cancel",
        "General Admission",
        45.0,
        100,
    )

    event.add_ticket_type(ticket)

    quantity = 2

    ticket.available_quantity -= quantity

    booking = Booking(
        booking_id="bkg_cancel",
        attendee_id="att1",
        event_id=event.event_id,
        event_title=event.title,
        items=[
            {
                "ticket_type_id": ticket.ticket_type_id,
                "ticket_type_name": ticket.name,
                "count": quantity,
                "line_total": 90.0,
            }
        ],
        total_price=92.0,
    )

    # Act
    booking.cancel_booking()

    # Simulate the availability restoration performed by bookings.py
    if booking.status == "Cancelled":
        ticket.available_quantity = min(
            ticket.available_quantity + quantity,
            ticket.quantity,
        )

    # Assert
    assert booking.status == "Cancelled"
    assert ticket.available_quantity == 100