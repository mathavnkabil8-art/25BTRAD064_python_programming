"""Unit tests for SQLite database operations, CSV repository, and migration."""

import tempfile
from pathlib import Path
import pytest

from src.routeiq.core.models import TripRecord
from src.routeiq.database.database import DatabaseManager
from src.routeiq.database.migration import MigrationService
from src.routeiq.database.repository import CSVRepository


@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_commute.db"
        csv_path = Path(tmpdir) / "test_commute.csv"
        db = DatabaseManager(db_path)
        csv_repo = CSVRepository(csv_path)
        yield db, csv_repo, csv_path


def test_sqlite_insert_and_retrieve(temp_storage):
    db, _, _ = temp_storage
    trip = TripRecord(
        origin="Campus_Gate",
        destination="Tech_Park_Metro",
        mode="Public_Bus",
        estimated_duration_min=25.0,
        cost_inr=15.0,
        distance_km=6.5,
        carbon_kg=0.3,
    )
    trip_id = db.add_trip(trip)
    assert trip_id > 0
    assert db.get_trip_count() == 1

    trips = db.get_all_trips()
    assert len(trips) == 1
    t = trips[0]
    assert t.origin == "Campus_Gate"
    assert t.destination == "Tech_Park_Metro"
    assert t.mode == "Public_Bus"
    assert t.effective_duration == 25.0
    assert t.cost_inr == 15.0
    assert t.distance_km == 6.5
    assert t.carbon_kg == 0.3


def test_csv_append_and_read(temp_storage):
    _, csv_repo, _ = temp_storage
    trip = TripRecord(
        origin="Hostel_Block",
        destination="Campus_Gate",
        mode="Walking",
        estimated_duration_min=12.0,
        cost_inr=0.0,
    )
    csv_repo.append_trip(trip)

    trips = csv_repo.read_all_trips()
    assert len(trips) == 1
    assert trips[0].origin == "Hostel_Block"
    assert trips[0].mode == "Walking"
    assert trips[0].cost_inr == 0.0


def test_safe_csv_migration_without_duplication(temp_storage):
    db, csv_repo, csv_path = temp_storage

    t1 = TripRecord("Hostel_Block", "Campus_Gate", "Walking", 12.0, 0.0, timestamp="2026-11-01 10:00:00")
    t2 = TripRecord("Campus_Gate", "Tech_Park_Metro", "Auto_Rickshaw", 15.0, 60.0, timestamp="2026-11-01 10:15:00")
    csv_repo.append_trip(t1)
    csv_repo.append_trip(t2)

    migrated_first = MigrationService.migrate_csv_to_sqlite(csv_path=csv_path, db_manager=db)
    assert migrated_first == 2
    assert db.get_trip_count() == 2

    migrated_second = MigrationService.migrate_csv_to_sqlite(csv_path=csv_path, db_manager=db)
    assert migrated_second == 0
    assert db.get_trip_count() == 2

    trips = db.get_all_trips()
    for t in trips:
        assert t.distance_km is None
        assert t.carbon_kg is None
