from database import Booking, Event, TicketType


def test_event_can_add_ticket_type():
    event = Event(
        "evt_test",
        "Test Event",
        "Test description",
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

    assert len(event.ticket_types) == 1
    assert event.ticket_types[0].name == "General Admission"


def test_ticket_type_starts_with_full_availability():
    ticket = TicketType(
        "ticket_1",
        "General Admission",
        45.0,
        100,
    )

    assert ticket.quantity == 100
    assert ticket.available_quantity == 100


def test_ticket_availability_decreases_after_purchase():
    ticket = TicketType(
        "ticket_1",
        "General Admission",
        45.0,
        100,
    )

    ticket.available_quantity -= 2

    assert ticket.available_quantity == 98


def test_booking_contains_multiple_ticket_items():
    items = [
        {
            "ticket_type_id": "ticket_1",
            "ticket_type_name": "General Admission",
            "count": 2,
            "line_total": 90.0,
        },
        {
            "ticket_type_id": "ticket_2",
            "ticket_type_name": "VIP Pass",
            "count": 1,
            "line_total": 95.0,
        },
    ]

    booking = Booking(
        booking_id="bkg_test",
        attendee_id="att1",
        event_id="evt_test",
        event_title="Test Event",
        items=items,
        total_price=187.0,
    )

    assert booking.booking_id == "bkg_test"
    assert booking.attendee_id == "att1"
    assert len(booking.items) == 2
    assert booking.total_price == 187.0


def test_booking_cancel_changes_status():
    booking = Booking(
        booking_id="bkg_test",
        attendee_id="att1",
        event_id="evt_test",
        event_title="Test Event",
        items=[],
        total_price=0.0,
    )

    assert booking.status == "Confirmed"

    booking.cancel_booking()

    assert booking.status == "Cancelled"