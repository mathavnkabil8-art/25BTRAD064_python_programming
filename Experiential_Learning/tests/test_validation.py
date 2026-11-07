"""Unit tests for user input and domain metric validators."""

import pytest

from src.routeiq.core.exceptions import ValidationError
from src.routeiq.utils.validators import (
    validate_address,
    validate_departure_hour,
    validate_numeric_metric,
    validate_origin_destination,
    validate_transport_mode,
)


def test_validate_origin_destination():
    # Valid pair
    validate_origin_destination("Origin Hub", "Destination Hub")

    # Identical
    with pytest.raises(ValidationError):
        validate_origin_destination("Campus_Gate", "Campus_Gate")

    # Empty
    with pytest.raises(ValidationError):
        validate_origin_destination("", "Campus_Gate")
    with pytest.raises(ValidationError):
        validate_origin_destination("Hostel_Block", "   ")


def test_validate_departure_hour():
    assert validate_departure_hour(0) == 0
    assert validate_departure_hour(23) == 23
    assert validate_departure_hour("9") == 9

    with pytest.raises(ValidationError):
        validate_departure_hour(-1)
    with pytest.raises(ValidationError):
        validate_departure_hour(24)
    with pytest.raises(ValidationError):
        validate_departure_hour("invalid_hour")


def test_validate_numeric_metric():
    assert validate_numeric_metric(15.5, "Duration") == 15.5
    assert validate_numeric_metric(0, "Cost", allow_zero=True) == 0.0

    with pytest.raises(ValidationError):
        validate_numeric_metric(-5, "Cost", allow_zero=True)
    with pytest.raises(ValidationError):
        validate_numeric_metric(0, "Duration", allow_zero=False)
    with pytest.raises(ValidationError):
        validate_numeric_metric("not_a_number", "Cost")


def test_validate_transport_mode():
    assert validate_transport_mode("Metro_Train") == "Metro_Train"
    assert validate_transport_mode("public bus") == "Public_Bus"
    assert validate_transport_mode("driving") == "Driving"

    with pytest.raises(ValidationError):
        validate_transport_mode("   ")


def test_validate_address():
    assert validate_address("Connaught Place") == "Connaught Place"

    with pytest.raises(ValidationError):
        validate_address(" ")
    with pytest.raises(ValidationError):
        validate_address("a")
