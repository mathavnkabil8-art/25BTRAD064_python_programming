"""Unit tests for Statistical Commute Analytics and Matplotlib visualization."""

from matplotlib.figure import Figure
import pytest

from src.routeiq.analytics.commute_analytics import CommuteAnalyticsService
from src.routeiq.analytics.visualization import ChartVisualizer
from src.routeiq.core.models import TripRecord


def test_empty_analytics_summary():
    summary = CommuteAnalyticsService.compute_summary([])
    assert summary.total_trips == 0
    assert summary.total_spend_inr == 0.0
    assert summary.average_duration_min == 0.0
    assert summary.average_cost_inr == 0.0
    assert summary.popular_mode == "None"

    fig = ChartVisualizer.create_analytics_figure(summary)
    assert isinstance(fig, Figure)


def test_full_analytics_calculations():
    trips = [
        TripRecord("Hostel_Block", "City_Center", "Metro_Train", 20.0, 40.0, distance_km=15.0, carbon_kg=0.2, timestamp="2026-10-15 09:00:00"),
        TripRecord("Hostel_Block", "City_Center", "Premium_Cab", 35.0, 220.0, distance_km=15.0, carbon_kg=2.5, timestamp="2026-10-20 18:00:00"),
        TripRecord("Campus_Gate", "Tech_Park_Metro", "Public_Bus", 25.0, 15.0, distance_km=6.0, carbon_kg=0.3, timestamp="2026-11-01 08:30:00"),
        TripRecord("Campus_Gate", "Tech_Park_Metro", "Auto_Rickshaw", 15.0, 60.0, distance_km=6.0, carbon_kg=0.5, timestamp="2026-11-03 17:15:00"),
    ]

    summary = CommuteAnalyticsService.compute_summary(trips)

    assert summary.total_trips == 4
    assert summary.total_spend_inr == 335.0
    assert summary.total_distance_km == 42.0
    assert summary.total_carbon_kg == 3.5
    assert summary.average_duration_min == 23.8
    assert summary.average_cost_inr == 83.75
    assert len(summary.mode_counts) == 4

    assert summary.fastest_trip is not None
    assert summary.fastest_trip.effective_duration == 15.0

    assert summary.cheapest_trip is not None
    assert summary.cheapest_trip.cost_inr == 15.0

    assert "2026-10" in summary.monthly_spend
    assert "2026-11" in summary.monthly_spend
    assert summary.monthly_spend["2026-10"] == 260.0
    assert summary.monthly_spend["2026-11"] == 75.0
    assert summary.time_saved_min == 25.0

    fig = ChartVisualizer.create_analytics_figure(summary)
    assert isinstance(fig, Figure)
    assert len(fig.axes) == 2
