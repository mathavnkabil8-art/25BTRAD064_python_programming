"""Unit and integration tests for InteractiveMapView, LocalMapServer, and Google Maps JS API visualization."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from src.routeiq.core.models import RouteOption, RouteSegment
from src.routeiq.maps.map_server import LocalMapServer
from src.routeiq.maps.map_view import InteractiveMapView


def _create_sample_route(
    summary: str = "Fastest Route via NH 48",
    origin: str = "Campus Gate",
    destination: str = "City Center",
    distance_km: float = 12.5,
    duration_min: float = 25.0,
    geometry=None,
) -> RouteOption:
    """Helper to create a RouteOption instance for testing."""
    if geometry is None:
        geometry = [(28.5450, 77.1925), (28.5800, 77.2000), (28.6304, 77.2177)]

    segments = [
        RouteSegment(
            origin=origin,
            destination=destination,
            mode="Drive",
            distance_km=distance_km,
            duration_minutes=duration_min,
            cost_inr=150.0,
            carbon_kg=1.8,
        )
    ]
    return RouteOption(
        origin=origin,
        destination=destination,
        summary=summary,
        segments=segments,
        total_duration_minutes=duration_min,
        total_distance_km=distance_km,
        total_cost_inr=150.0,
        total_carbon_kg=1.8,
        raw_geometry=geometry,
        is_traffic_aware=True,
        traffic_delay_minutes=5.0,
    )


def test_map_html_generation_with_google_key(tmp_path: Path):
    """Verify that with an API key, Google Maps JavaScript API is embedded and OSM/Leaflet are absent."""
    route1 = _create_sample_route("Primary Via Highway", distance_km=12.0, duration_min=24.0)
    route2 = _create_sample_route("Alternative Via City Road", distance_km=14.0, duration_min=32.0)

    out_file = tmp_path / "test_map.html"

    mock_cfg = MagicMock()
    mock_cfg.BASE_DIR = tmp_path
    mock_cfg.GOOGLE_MAPS_JS_API_KEY = "AIzaSyFakeKeyForTesting1234567890"

    with patch("src.routeiq.maps.map_view.config", mock_cfg):
        saved_path = InteractiveMapView.generate_map_html(
            selected_route=route1,
            all_routes=[route1, route2],
            output_path=out_file,
        )

        assert saved_path.exists()
        content = saved_path.read_text(encoding="utf-8")

        # 1. Must use Google Maps JavaScript API
        assert "https://maps.googleapis.com/maps/api/js?key=AIzaSyFakeKeyForTesting1234567890" in content
        assert "libraries=geometry" in content
        assert '<meta name="referrer" content="origin">' in content

        # 2. Must NOT contain OpenStreetMap or Leaflet references
        assert "openstreetmap" not in content.lower()
        assert "leaflet" not in content.lower()
        assert "tile.openstreetmap.org" not in content

        # 3. Must contain required controls and layers
        assert "mapTypeControl: true" in content
        assert "fullscreenControl: true" in content
        assert "new google.maps.TrafficLayer()" in content
        assert "window.gm_authFailure" in content

        # 4. Markers and polylines
        assert "google.maps.Polyline" in content
        assert "google.maps.Marker" in content
        assert "Campus Gate" in content
        assert "City Center" in content

        # 5. Alternative routes support
        assert "Primary Via Highway" in content
        assert "Alternative Via City Road" in content
        assert "setActiveRoute" in content


def test_map_html_strict_key_segregation_no_backend_key_leak(tmp_path: Path):
    """Verify that backend GOOGLE_ROUTES_API_KEY is NEVER leaked into HTML/JS when GOOGLE_MAPS_JS_API_KEY is unset."""
    route = _create_sample_route()
    out_file = tmp_path / "segregation_test_map.html"

    mock_cfg = MagicMock()
    mock_cfg.BASE_DIR = tmp_path
    mock_cfg.GOOGLE_MAPS_JS_API_KEY = ""
    # Backend key exists, but must NOT be used for frontend
    mock_cfg.GOOGLE_ROUTES_API_KEY = "AIzaSySecretBackendRoutesKey987654321"

    with patch("src.routeiq.maps.map_view.config", mock_cfg):
        saved_path = InteractiveMapView.generate_map_html(
            selected_route=route,
            all_routes=[route],
            output_path=out_file,
        )

        assert saved_path.exists()
        content = saved_path.read_text(encoding="utf-8")

        # Backend key MUST NOT be present in client HTML/JS
        assert "AIzaSySecretBackendRoutesKey987654321" not in content
        assert "https://maps.googleapis.com/maps/api/js" not in content
        # Must show configuration instructions
        assert "GOOGLE_MAPS_JS_API_KEY" in content
        assert "Security Key Segregation Enforced" in content


def test_map_html_generation_fallback_when_no_key(tmp_path: Path):
    """Verify clean setup guidance when no Google API key is configured without requesting OSM tiles."""
    route = _create_sample_route()
    out_file = tmp_path / "no_key_map.html"

    mock_cfg = MagicMock()
    mock_cfg.BASE_DIR = tmp_path
    mock_cfg.GOOGLE_MAPS_JS_API_KEY = ""
    mock_cfg.GOOGLE_ROUTES_API_KEY = ""

    with patch("src.routeiq.maps.map_view.config", mock_cfg):
        saved_path = InteractiveMapView.generate_map_html(
            selected_route=route,
            all_routes=[route],
            output_path=out_file,
        )

        assert saved_path.exists()
        content = saved_path.read_text(encoding="utf-8")

        # Must not call OSM tiles
        assert "tile.openstreetmap.org" not in content
        assert "leaflet" not in content.lower()
        # Must show configuration instructions
        assert "GOOGLE_MAPS_JS_API_KEY" in content
        assert "Google Cloud Console" in content


def test_offline_hub_route_coordinate_extraction():
    """Verify that offline routes without raw geometry properly map known campus hubs to coordinates."""
    offline_route = RouteOption(
        origin="Hostel_Block",
        destination="Tech_Park_Metro",
        summary="Offline Campus Route",
        segments=[
            RouteSegment(
                origin="Hostel_Block",
                destination="Campus_Gate",
                mode="Walk",
                distance_km=0.8,
                duration_minutes=10.0,
                cost_inr=0.0,
                carbon_kg=0.0,
            ),
            RouteSegment(
                origin="Campus_Gate",
                destination="Tech_Park_Metro",
                mode="Public_Bus",
                distance_km=3.2,
                duration_minutes=15.0,
                cost_inr=15.0,
                carbon_kg=0.2,
            ),
        ],
        total_duration_minutes=25.0,
        total_distance_km=4.0,
        total_cost_inr=15.0,
        total_carbon_kg=0.2,
        raw_geometry=[],
    )

    coords = InteractiveMapView._extract_coordinates(offline_route)
    assert len(coords) >= 3
    # Check that coordinates are float pairs
    for lat, lng in coords:
        assert isinstance(lat, float)
        assert isinstance(lng, float)
        assert 20.0 < lat < 35.0
        assert 70.0 < lng < 85.0


def test_local_map_server_lifecycle():
    """Verify that LocalMapServer starts, returns valid local origin and port, and shuts down."""
    server = LocalMapServer(host="127.0.0.1", port=24869)
    try:
        base_url = server.start()
        assert base_url.startswith("http://127.0.0.1:")
        assert server.is_running() is True
        origin = server.get_origin()
        assert origin == base_url
        map_url = server.get_map_url("route_map.html")
        assert map_url == f"{base_url}/route_map.html"
    finally:
        server.shutdown()
        assert server.is_running() is False
