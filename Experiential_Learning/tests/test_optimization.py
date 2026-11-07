"""Unit tests for Multi-Criteria Route Optimization and Recommendation Engine."""

import pytest
from src.routeiq.optimization.multi_criteria import MultiCriteriaOptimizer
from src.routeiq.optimization.recommendation import RecommendationEngine
from src.routeiq.routing.offline_router import OfflineRouter


@pytest.fixture
def sample_options():
    router = OfflineRouter()
    return router.find_all_paths("Hostel_Block", "City_Center", departure_hour=9)


def test_multi_criteria_comparison(sample_options):
    optimizer = MultiCriteriaOptimizer()
    comparison = optimizer.compare_all(sample_options)

    assert comparison.fastest is not None
    assert comparison.cheapest is not None
    assert comparison.greenest is not None
    assert comparison.balanced is not None

    for opt in sample_options:
        assert comparison.fastest.total_duration_minutes <= opt.total_duration_minutes
        assert comparison.cheapest.total_cost_inr <= opt.total_cost_inr
        assert comparison.greenest.total_carbon_kg <= opt.total_carbon_kg


def test_pick_best_priorities(sample_options):
    optimizer = MultiCriteriaOptimizer()

    best_fast = optimizer.pick_best(sample_options, priority="Fastest")
    assert best_fast.total_duration_minutes == 42.0

    best_cheap = optimizer.pick_best(sample_options, priority="Cheapest")
    assert best_cheap.total_cost_inr == 55.0

    best_eco = optimizer.pick_best(sample_options, priority="Eco-Friendly")
    assert best_eco.total_carbon_kg == 0.7

    best_bal = optimizer.pick_best(sample_options, priority="Balanced")
    assert best_bal is not None


def test_recommendation_explanation(sample_options):
    optimizer = MultiCriteriaOptimizer()
    comparison = optimizer.compare_all(sample_options)

    exp_fast = RecommendationEngine.generate_explanation(comparison, user_priority="Fastest")
    assert "FASTEST ROUTE" in exp_fast
    assert "mins" in exp_fast

    exp_cheap = RecommendationEngine.generate_explanation(comparison, user_priority="Cheapest")
    assert "CHEAPEST ROUTE" in exp_cheap
    assert "₹" in exp_cheap

    exp_balanced = RecommendationEngine.generate_explanation(comparison, user_priority="Balanced")
    assert "BALANCED RECOMMENDATION" in exp_balanced
    assert "Rationale" in exp_balanced


def test_empty_options_handling():
    optimizer = MultiCriteriaOptimizer()
    comparison = optimizer.compare_all([])
    assert comparison.fastest is None
    assert comparison.balanced is None

    exp = RecommendationEngine.generate_explanation(comparison)
    assert "No viable route options" in exp
