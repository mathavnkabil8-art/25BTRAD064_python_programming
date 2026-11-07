"""Unit tests for GeocodingService and address resolution."""

from unittest.mock import MagicMock, patch
import pytest

from src.routeiq.core.exceptions import APIAuthenticationError, GeocodingError
from src.routeiq.routing.geocoding import GeocodingService


def test_geocoding_known_offline_hubs():
    geocoder = GeocodingService(api_key="")
    lat, lng, name = geocoder.geocode("Hostel_Block")
    assert round(lat, 2) == 28.55
    assert round(lng, 2) == 77.19
    assert "Hostel" in name


def test_geocoding_empty_address():
    geocoder = GeocodingService(api_key="")
    with pytest.raises(GeocodingError):
        geocoder.geocode("   ")


@patch("requests.get")
def test_google_geocoding_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": "OK",
        "results": [
            {
                "formatted_address": "Connaught Place, New Delhi, Delhi, India",
                "geometry": {"location": {"lat": 28.6315, "lng": 77.2167}},
            }
        ],
    }
    mock_get.return_value = mock_resp

    geocoder = GeocodingService(api_key="AIzaSyMockedKey12345678901234567890")
    lat, lng, name = geocoder.geocode("Random Place Name Query")
    assert round(lat, 2) == 28.63
    assert round(lng, 2) == 77.22
    assert "Connaught Place" in name


@patch("requests.get")
def test_google_geocoding_auth_error(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": "REQUEST_DENIED",
        "error_message": "The provided API key is invalid.",
    }
    mock_get.return_value = mock_resp

    geocoder = GeocodingService(api_key="AIzaSyMockedInvalidKey1234567890")
    with pytest.raises(APIAuthenticationError):
        geocoder.geocode("Some Street Address")
