"""RouteIQ Configuration and Environment Management.

Loads settings from environment variables and provides centralized access
to operational constants, fare calculations, and carbon emission factors.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from dotenv import load_dotenv

    _project_root = Path(__file__).resolve().parent.parent
    load_dotenv(_project_root / ".env")
except ImportError:
    pass

from src.routeiq.core.constants import (
    DEFAULT_CONGESTION_MULTIPLIER,
    DEFAULT_EMISSION_FACTORS,
    DEFAULT_FARE_RATES,
    DEFAULT_ROAD_VEHICLES,
    DEFAULT_RUSH_HOURS,
)


@dataclass(frozen=True)
class AppConfig:
    """Central immutable configuration for RouteIQ."""

    # Project directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    ASSETS_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "assets")

    # API Keys & Endpoints (with key segregation for backend vs frontend)
    # Server-side Routes API Key (used only in Python requests)
    GOOGLE_ROUTES_API_KEY: str = field(
        default_factory=lambda: (
            os.getenv("GOOGLE_ROUTES_API_KEY", "")
            or os.getenv("GOOGLE_MAPS_API_KEY", "")
        ).strip()
    )

    # Server-side Geocoding API Key (used only in Python requests)
    GOOGLE_GEOCODING_API_KEY: str = field(
        default_factory=lambda: (
            os.getenv("GOOGLE_GEOCODING_API_KEY", "")
            or os.getenv("GOOGLE_ROUTES_API_KEY", "")
            or os.getenv("GOOGLE_MAPS_API_KEY", "")
        ).strip()
    )

    # Client-side JavaScript API Key (safe to use in frontend HTML map; loaded EXCLUSIVELY from dedicated env var)
    GOOGLE_MAPS_JS_API_KEY: str = field(
        default_factory=lambda: os.getenv("GOOGLE_MAPS_JS_API_KEY", "").strip()
    )

    # Local Map Server Settings for deterministic HTTP origin & port
    MAP_SERVER_HOST: str = field(default_factory=lambda: os.getenv("MAP_SERVER_HOST", "127.0.0.1").strip())
    MAP_SERVER_PORT: int = field(default_factory=lambda: int(os.getenv("MAP_SERVER_PORT", "24860")))

    GOOGLE_ROUTES_API_URL: str = "https://routes.googleapis.com/directions/v2:computeRoutes"
    GOOGLE_GEOCODE_API_URL: str = "https://maps.googleapis.com/maps/api/geocode/json"
    REQUEST_TIMEOUT_SECONDS: int = 6

    # Persistence paths (defaulting to data/ directory while maintaining root backward compatibility)
    DATABASE_PATH: Path = field(
        default_factory=lambda: (
            Path(__file__).resolve().parent.parent / "data" / os.getenv("DATABASE_NAME", "commute_history.db")
            if (Path(__file__).resolve().parent.parent / "data").exists()
            else Path(__file__).resolve().parent.parent / os.getenv("DATABASE_NAME", "commute_history.db")
        )
    )
    CSV_PATH: Path = field(
        default_factory=lambda: (
            Path(__file__).resolve().parent.parent / "data" / os.getenv("CSV_FILENAME", "commute_history.csv")
            if (Path(__file__).resolve().parent.parent / "data").exists()
            else Path(__file__).resolve().parent.parent / os.getenv("CSV_FILENAME", "commute_history.csv")
        )
    )

    # Traffic & Congestion Constants
    RUSH_HOURS: List[Tuple[int, int]] = field(default_factory=lambda: list(DEFAULT_RUSH_HOURS))
    DEFAULT_CONGESTION_MULTIPLIER: float = DEFAULT_CONGESTION_MULTIPLIER
    ROAD_VEHICLES: List[str] = field(default_factory=lambda: list(DEFAULT_ROAD_VEHICLES))

    # Estimated Carbon Emissions per passenger-km (kg CO2 / km)
    EMISSION_FACTORS: Dict[str, float] = field(default_factory=lambda: dict(DEFAULT_EMISSION_FACTORS))

    # Estimated Fare Rates: (Base Fare INR, Per-Km Fare INR)
    FARE_RATES: Dict[str, Tuple[float, float]] = field(default_factory=lambda: dict(DEFAULT_FARE_RATES))

    @property
    def is_live_api_configured(self) -> bool:
        """Return True if a valid server-side Google Routes API key is configured."""
        key = self.GOOGLE_ROUTES_API_KEY
        return bool(key and len(key) > 10 and not key.startswith("YOUR_"))

    @property
    def is_frontend_maps_key_configured(self) -> bool:
        """Return True if a separate client-side Maps JS API key is configured."""
        key = self.GOOGLE_MAPS_JS_API_KEY
        return bool(key and len(key) > 10 and not key.startswith("YOUR_"))


# Global singleton instance
config = AppConfig()
