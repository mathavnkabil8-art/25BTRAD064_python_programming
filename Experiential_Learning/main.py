"""RouteIQ — Intelligent Commute and Multi-Modal Route Optimization System.

Primary application entry point with automatic SQLite migration and backward-compatible interfaces.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path to enable direct execution
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import config
from src.routeiq.analytics.commute_analytics import CommuteAnalyticsService
from src.routeiq.core.constants import (
    DEFAULT_CONGESTION_MULTIPLIER,
    DEFAULT_ROAD_VEHICLES,
    DEFAULT_RUSH_HOURS,
)
from src.routeiq.core.models import TripRecord
from src.routeiq.optimization.multi_criteria import MultiCriteriaOptimizer
from src.routeiq.routing.offline_router import OfflineRouter
from src.routeiq.routing.route_optimizer import RouteOptimizer
from src.routeiq.services.trip_service import TripService
from src.routeiq.ui.app import TravelApp
from src.routeiq.utils.logging_config import configure_logging, get_logger

# Configure security-conscious logging
configure_logging()
logger = get_logger("RouteIQ.Main")

# Backward compatibility alias for TransitNetwork
TransitNetwork = OfflineRouter


class LogEngine:
    """Backward-compatible wrapper around TripService."""

    def __init__(self, filename: str = "commute_history.csv"):
        self.service = TripService()

    def log_commute(self, origin, destination, mode, duration, cost):
        self.service.record_commute(origin, destination, mode, duration, cost)
        return True

    def read_all_logs(self):
        trips = self.service.get_all_trips()
        return [
            {
                "timestamp": t.timestamp,
                "origin": t.origin,
                "destination": t.destination,
                "mode": t.mode,
                "duration": t.effective_duration,
                "cost": t.cost_inr,
            }
            for t in trips
        ]


class CommuteAnalytics:
    """Backward-compatible wrapper around CommuteAnalyticsService."""

    @staticmethod
    def generate_dashboard(logs):
        if not logs:
            return {"total_trips": 0, "total_spend": 0.0, "total_time": 0.0, "popular_mode": "None"}
        trips = [
            TripRecord(
                origin=l["origin"],
                destination=l["destination"],
                mode=l["mode"],
                estimated_duration_min=float(l["duration"]),
                actual_duration_min=float(l["duration"]),
                cost_inr=float(l["cost"]),
                timestamp=l["timestamp"],
            )
            for l in logs
        ]
        s = CommuteAnalyticsService.compute_summary(trips)
        return {
            "total_trips": s.total_trips,
            "total_spend": s.total_spend_inr,
            "total_time": s.total_time_min,
            "popular_mode": s.popular_mode,
        }


def main() -> None:
    """Application main execution entry point."""
    logger.info("Initializing RouteIQ Commute Optimization System...")

    trip_service = TripService()
    try:
        migrated = trip_service.run_startup_migration()
        if migrated > 0:
            logger.info(f"Safely preserved and migrated {migrated} historical records into SQLite.")
    except Exception as e:
        logger.warning(f"Startup migration notice: {e}")

    logger.info("Starting Desktop Graphical Interface...")
    app = TravelApp()
    app.mainloop()


if __name__ == "__main__":
    main()