"""Live End-to-End Integration Verification Script for RouteIQ.

Performs live end-to-end testing against Google Maps Platform services:
1. Google Routes API v2 (live driving calculation & traffic delay)
2. Geocoding API (address-to-coordinate resolution)
3. Maps JavaScript API script fetching with local HTTP referrer
4. Tkinter application lifecycle (Offline Dijkstra & Live Google Routes)
5. Interactive Map generation, polyline extraction, markers, controls, and alternatives
6. Strict key segregation check
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import config
from src.routeiq.maps.map_server import LocalMapServer
from src.routeiq.maps.map_view import InteractiveMapView
from src.routeiq.routing.geocoding import GeocodingService
from src.routeiq.routing.google_routes import GoogleRoutesService
from src.routeiq.routing.offline_router import OfflineRouter
from src.routeiq.routing.route_provider import LiveRouteProvider, OfflineRouteProvider
from src.routeiq.ui.app import TravelApp


def run_live_tests():
    print("=" * 70)
    print("ROUTEIQ LIVE INTEGRATION VERIFICATION RUNNER")
    print("=" * 70)

    results = {}

    # -------------------------------------------------------------------------
    # TEST 1: Live Geocoding Service
    # -------------------------------------------------------------------------
    print("\n[1/6] Testing Live Geocoding API...")
    geocoder = GeocodingService()
    try:
        lat1, lng1, addr1 = geocoder.geocode("Connaught Place, New Delhi")
        lat2, lng2, addr2 = geocoder.geocode("Cyber City, Gurugram")
        print(f"  Origin Geocoded: {addr1} -> ({lat1:.4f}, {lng1:.4f})")
        print(f"  Destination Geocoded: {addr2} -> ({lat2:.4f}, {lng2:.4f})")
        assert 28.0 < lat1 < 29.0 and 76.0 < lng1 < 78.0
        assert 28.0 < lat2 < 29.0 and 76.0 < lng2 < 78.0
        results["geocoding"] = "PASSED (Live Google Geocoding API)"
    except Exception as e:
        print(f"  Geocoding failed: {e}")
        results["geocoding"] = f"FAILED: {e}"

    # -------------------------------------------------------------------------
    # TEST 2: Live Google Routes API v2
    # -------------------------------------------------------------------------
    print("\n[2/6] Testing Live Google Routes API v2...")
    routes_service = GoogleRoutesService()
    live_routes = []
    try:
        live_routes = routes_service.compute_routes(
            origin_coords=(lat1, lng1),
            dest_coords=(lat2, lng2),
            origin_name=addr1,
            dest_name=addr2,
        )
        print(f"  Computed {len(live_routes)} route option(s):")
        for i, r in enumerate(live_routes):
            print(f"    Option {i+1}: {r.summary} | {r.total_distance_km:.1f} km | {r.total_duration_minutes:.1f} min (Traffic delay: {r.traffic_delay_minutes:.1f} min) | Geometry points: {len(r.raw_geometry)}")
        assert len(live_routes) >= 1
        assert len(live_routes[0].raw_geometry) > 10
        results["routes_api"] = f"PASSED ({len(live_routes)} live routes retrieved with traffic ETA)"
    except Exception as e:
        print(f"  Routes API failed: {e}")
        results["routes_api"] = f"FAILED: {e}"

    # -------------------------------------------------------------------------
    # TEST 3: Google Maps JavaScript API with Local HTTP Referrer
    # -------------------------------------------------------------------------
    print("\n[3/6] Testing Google Maps JavaScript API loader with Local HTTP Referrer...")
    server = LocalMapServer.get_instance()
    origin_url = server.get_origin()
    print(f"  Local Map Server Origin: {origin_url}")
    print(f"  Local Map Server Port: {server.actual_port}")

    js_key = config.GOOGLE_MAPS_JS_API_KEY
    js_url = f"https://maps.googleapis.com/maps/api/js?key={js_key}&libraries=geometry"
    req = urllib.request.Request(
        js_url,
        headers={"Referer": f"{origin_url}/route_map.html", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            print(f"  Google Maps JS HTTP Status: {status}")
            print(f"  Downloaded JS Script Size: {len(content):,} bytes")
            # Verify script is valid Google Maps bootstrap
            assert "google.maps" in content or "window.google" in content
            assert "error" not in content[:300].lower()
            results["maps_js_api"] = f"PASSED (HTTP {status}, {len(content):,} bytes received)"
    except Exception as e:
        print(f"  Maps JS API fetch failed: {e}")
        results["maps_js_api"] = f"FAILED: {e}"

    # -------------------------------------------------------------------------
    # TEST 4: Generate Map HTML & Local Server Verification
    # -------------------------------------------------------------------------
    print("\n[4/6] Generating and Verifying Interactive Map HTML...")
    if live_routes:
        out_html = InteractiveMapView.generate_map_html(live_routes[0], all_routes=live_routes)
        html_text = out_html.read_text(encoding="utf-8")

        # Verify key elements
        has_js_key = js_key in html_text
        has_backend_key_leaked = bool(config.GOOGLE_ROUTES_API_KEY != js_key and config.GOOGLE_ROUTES_API_KEY in html_text)
        has_referrer_meta = '<meta name="referrer" content="origin">' in html_text
        has_markers = 'google.maps.Marker' in html_text
        has_polylines = 'google.maps.Polyline' in html_text
        has_traffic_layer = 'new google.maps.TrafficLayer()' in html_text
        has_satellite_control = 'mapTypeControl: true' in html_text
        has_fullscreen_control = 'fullscreenControl: true' in html_text
        has_switcher = 'setActiveRoute' in html_text
        has_auth_failure_handler = 'window.gm_authFailure' in html_text
        has_no_osm = 'openstreetmap' not in html_text.lower() and 'leaflet' not in html_text.lower()

        print(f"  Contains Client JS API Key: {has_js_key}")
        print(f"  Backend Key Leak Detected: {has_backend_key_leaked}")
        print(f"  Contains Meta Referrer: {has_referrer_meta}")
        print(f"  Contains Origin & Destination Markers: {has_markers}")
        print(f"  Contains Route Polylines: {has_polylines}")
        print(f"  Contains Traffic Layer: {has_traffic_layer}")
        print(f"  Contains Satellite / Map Control: {has_satellite_control}")
        print(f"  Contains Fullscreen Control: {has_fullscreen_control}")
        print(f"  Contains Route Switcher Logic: {has_switcher}")
        print(f"  Contains gm_authFailure Handler: {has_auth_failure_handler}")
        print(f"  Leaflet / OpenStreetMap Completely Absent: {has_no_osm}")

        assert has_js_key
        assert not has_backend_key_leaked
        assert has_referrer_meta
        assert has_markers
        assert has_polylines
        assert has_traffic_layer
        assert has_satellite_control
        assert has_fullscreen_control
        assert has_switcher
        assert has_auth_failure_handler
        assert has_no_osm

        # Test fetching through the local server
        map_http_url = server.get_map_url("route_map.html")
        with urllib.request.urlopen(map_http_url, timeout=5) as map_resp:
            assert map_resp.status == 200
            assert map_resp.headers.get("Referrer-Policy") == "origin"
            print(f"  Local HTTP Server Delivery: HTTP {map_resp.status} at {map_http_url}")

        results["interactive_map"] = "PASSED (Full Google Maps JS integration verified)"
    else:
        results["interactive_map"] = "SKIPPED (No live routes)"

    # -------------------------------------------------------------------------
    # TEST 5: Offline Mode Verification
    # -------------------------------------------------------------------------
    print("\n[5/6] Testing Offline Dijkstra Hub Routing Mode...")
    offline_provider = OfflineRouteProvider()
    offline_routes = offline_provider.get_routes("Hostel_Block", "City_Center", departure_hour=9)
    print(f"  Offline provider found {len(offline_routes)} multi-hop route option(s):")
    for r in offline_routes:
        print(f"    - {r.summary} ({r.total_duration_minutes:.1f}m, ₹{r.total_cost_inr:.1f}, {r.total_carbon_kg:.2f}kg CO2)")
    assert len(offline_routes) > 0
    results["offline_mode"] = f"PASSED ({len(offline_routes)} paths resolved via offline Dijkstra graph)"

    # -------------------------------------------------------------------------
    # TEST 6: Tkinter App Lifecycle & UI Tab Integration
    # -------------------------------------------------------------------------
    print("\n[6/6] Testing Tkinter Application Lifecycle & Queue Processing...")
    app = TravelApp()
    try:
        # Check tabs
        tab_names = [app.notebook.tab(i, "text") for i in range(app.notebook.index("end"))]
        print(f"  Detected Tkinter tabs: {tab_names}")
        assert "Find Best Route" in tab_names
        assert "Log a Trip" in tab_names
        assert "Analytics Dashboard" in tab_names

        # Test offline query in Tkinter
        app.route_tab.origin_var.set("Hostel_Block")
        app.route_tab.dest_var.set("City_Center")
        app.route_tab.hour_var.set(9)
        app.route_tab.mode_choice_var.set("offline")
        app.find_route()

        # Pump Tkinter event loop
        for _ in range(30):
            app.update()
            app.process_queue()

        offline_rows = app.route_tab.route_table.get_children()
        print(f"  Offline route table populated with {len(offline_rows)} rows.")
        assert len(offline_rows) > 0

        # Test live query in Tkinter
        app.latest_options = None
        app.route_tab.origin_var.set("Campus Gate")
        app.route_tab.dest_var.set("City Center")
        app.route_tab.hour_var.set(9)
        app.route_tab.mode_choice_var.set("live")
        app.find_route()

        # Pump Tkinter event loop for live API response
        import time
        t_start = time.time()
        while time.time() - t_start < 10:
            app.update()
            app.process_queue()
            if app.latest_options is not None and not app.is_calculating:
                break
            time.sleep(0.1)

        live_rows = app.route_tab.route_table.get_children()
        print(f"  Live route table populated with {len(live_rows)} rows.")
        assert len(live_rows) > 0

        # Trigger map generation from UI
        app.open_interactive_map()
        for _ in range(10):
            app.update()

        print("  UI Interactive Map opened successfully via Local Map Server.")
        results["tkinter_ui"] = "PASSED (All 3 tabs, offline Dijkstra, live routing, and map trigger verified)"
    finally:
        app.destroy()

    # -------------------------------------------------------------------------
    # SUMMARY REPORT
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("LIVE INTEGRATION TEST RESULTS SUMMARY")
    print("=" * 70)
    all_passed = True
    for test_name, status in results.items():
        print(f"  {test_name.upper():<20}: {status}")
        if not status.startswith("PASSED"):
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("ALL LIVE INTEGRATION TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED OR SKIPPED.")
    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    success = run_live_tests()
    sys.exit(0 if success else 1)
