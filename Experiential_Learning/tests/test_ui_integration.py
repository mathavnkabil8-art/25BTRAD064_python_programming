"""Integration test for Tkinter TravelApp initialization, tabs, and queue processing."""

import pytest
from src.routeiq.ui.app import TravelApp


def test_travel_app_initialization_and_tabs():
    app = TravelApp()
    try:
        assert "RouteIQ" in app.title()
        tab_names = [app.notebook.tab(i, "text") for i in range(app.notebook.index("end"))]
        assert "Find Best Route" in tab_names
        assert "Log a Trip" in tab_names
        assert "Analytics Dashboard" in tab_names

        # Trigger background offline route calculation
        app.route_tab.origin_var.set("Hostel_Block")
        app.route_tab.dest_var.set("Campus_Gate")
        app.route_tab.hour_var.set(9)
        app.route_tab.mode_choice_var.set("offline")
        app.find_route()

        # Let Tkinter event loop process queue messages
        for _ in range(25):
            app.update()
            app.process_queue()

        rows = app.route_tab.route_table.get_children()
        assert len(rows) > 0

        res_text = app.route_tab.route_result.get("1.0", "end")
        assert "ROUTE" in res_text or "RECOMMENDATION" in res_text
    finally:
        app.destroy()
