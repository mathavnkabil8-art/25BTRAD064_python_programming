"""Unit tests for offline Dijkstra graph routing and live Google Routes API client."""

from unittest.mock import MagicMock, patch
import pytest
import requests

from src.routeiq.core.exceptions import (
    APIAuthenticationError,
    APIQuotaExceededError,
    RouteNotFoundError,
    RouteIQError,
    ValidationError,
)
from src.routeiq.routing.google_routes import GoogleRoutesService, decode_polyline
from src.routeiq.routing.offline_router import OfflineRouter
from src.routeiq.routing.route_provider import LiveRouteProvider, OfflineRouteProvider


def test_offline_router_locations():
    router = OfflineRouter()
    locations = router.get_locations()
    assert "Hostel_Block" in locations
    assert "Campus_Gate" in locations
    assert "Tech_Park_Metro" in locations
    assert "City_Center" in locations


def test_multi_hop_dijkstra_traversal():
    router = OfflineRouter()
    paths = router.find_all_paths("Hostel_Block", "City_Center", departure_hour=9)
    assert len(paths) == 6

    for p in paths:
        assert len(p.segments) == 3
        assert p.segments[0].origin == "Hostel_Block"
        assert p.segments[-1].destination == "City_Center"
        assert p.total_duration_minutes > 0
        assert p.total_cost_inr > 0
        assert p.total_carbon_kg >= 0


def test_dijkstra_optimization_criteria():
    router = OfflineRouter()
    fastest = router.dijkstra_shortest_path("Hostel_Block", "City_Center", departure_hour=9, criterion="time")
    assert fastest is not None
    assert "Premium_Cab" in fastest.summary

    cheapest = router.dijkstra_shortest_path("Hostel_Block", "City_Center", departure_hour=9, criterion="cost")
    assert cheapest is not None
    assert cheapest.total_cost_inr == 55.0
    assert "Public_Bus" in cheapest.summary

    greenest = router.dijkstra_shortest_path("Hostel_Block", "City_Center", departure_hour=9, criterion="carbon")
    assert greenest is not None
    assert greenest.total_carbon_kg == 0.7


def test_rush_hour_congestion_slowdown():
    router = OfflineRouter()
    peak_paths = router.find_all_paths("Campus_Gate", "Tech_Park_Metro", departure_hour=9)
    offpeak_paths = router.find_all_paths("Campus_Gate", "Tech_Park_Metro", departure_hour=14)

    cab_peak = next(p for p in peak_paths if p.primary_mode == "Premium_Cab")
    cab_offpeak = next(p for p in offpeak_paths if p.primary_mode == "Premium_Cab")

    assert cab_peak.total_duration_minutes == 18.0
    assert cab_offpeak.total_duration_minutes == 12.0
    assert cab_peak.is_traffic_aware is True


def test_offline_provider_validation_and_errors():
    provider = OfflineRouteProvider()

    with pytest.raises(ValidationError):
        provider.get_routes("Campus_Gate", "Campus_Gate", departure_hour=9)

    with pytest.raises(RouteNotFoundError):
        provider.get_routes("City_Center", "Hostel_Block", departure_hour=9)


def test_decode_polyline():
    encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
    decoded = decode_polyline(encoded)
    assert len(decoded) > 0
    assert isinstance(decoded[0], tuple)
    assert len(decoded[0]) == 2


@patch("requests.post")
def test_google_routes_success_with_traffic(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "routes": [
            {
                "description": "Via NH 48",
                "distanceMeters": 15400,
                "duration": "1800s",
                "staticDuration": "1200s",
                "polyline": {"encodedPolyline": "_p~iF~ps|U_ulLnnqC"},
            },
            {
                "description": "Via MG Road",
                "distanceMeters": 17200,
                "duration": "2100s",
                "staticDuration": "1500s",
                "polyline": {"encodedPolyline": "_p~iF~ps|U_ulLnnqC"},
            },
        ]
    }
    mock_post.return_value = mock_resp

    service = GoogleRoutesService(api_key="AIzaSyMockedKeyForTestingPurposes1234")
    routes = service.compute_routes(
        origin_coords=(28.545, 77.192),
        dest_coords=(28.630, 77.217),
        origin_name="Connaught Place",
        dest_name="Cyber Hub",
    )

    assert len(routes) == 2
    primary = routes[0]
    assert primary.total_distance_km == 15.4
    assert primary.total_duration_minutes == 30.0
    assert primary.static_duration_minutes == 20.0
    assert primary.traffic_delay_minutes == 10.0
    assert primary.is_traffic_aware is True
    assert primary.total_cost_inr > 0
    assert primary.total_carbon_kg > 0


@patch("requests.post")
def test_google_routes_auth_failure(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {
        "error": {"message": "API key not valid. Please pass a valid API key."}
    }
    mock_post.return_value = mock_resp

    service = GoogleRoutesService(api_key="InvalidKey123")
    with pytest.raises(APIAuthenticationError) as exc_info:
        service.compute_routes((28.5, 77.1), (28.6, 77.2), "Origin", "Dest")
    assert "Authentication Failed" in str(exc_info.value)


@patch("requests.post")
def test_google_routes_quota_exceeded(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_post.return_value = mock_resp

    service = GoogleRoutesService(api_key="ValidKeyOverQuota")
    with pytest.raises(APIQuotaExceededError):
        service.compute_routes((28.5, 77.1), (28.6, 77.2), "Origin", "Dest")


@patch("requests.post")
def test_google_routes_timeout(mock_post):
    mock_post.side_effect = requests.Timeout("Connection timed out")

    service = GoogleRoutesService(api_key="ValidKey")
    with pytest.raises(RouteIQError) as exc_info:
        service.compute_routes((28.5, 77.1), (28.6, 77.2), "Origin", "Dest")
    assert "timed out" in str(exc_info.value)


@patch("requests.post")
def test_google_routes_empty(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"routes": []}
    mock_post.return_value = mock_resp

    service = GoogleRoutesService(api_key="ValidKey")
    with pytest.raises(RouteNotFoundError):
        service.compute_routes((28.5, 77.1), (28.6, 77.2), "Origin", "Dest")
