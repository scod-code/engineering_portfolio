"""
Tests for example Prefect flows.
"""

import pytest
from prefect_flows.example_flows import (
    extract_data,
    transform_data,
    load_data,
    train_model,
    evaluate_model
)
import pandas as pd
import numpy as np
from datetime import datetime


def test_extract_data():
    """Test data extraction task."""
    # Test CSV source
    data = extract_data.fn("csv")
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert "id" in data.columns
    assert "value" in data.columns
    
    # Test API source
    data = extract_data.fn("api")
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0


def test_transform_data():
    """Test data transformation task."""
    # Create test data
    test_data = pd.DataFrame({
        "value": np.random.randn(100),
        "id": range(100)
    })
    
    # Apply transformation
    transformed = transform_data.fn(test_data)
    
    # Check results
    assert isinstance(transformed, pd.DataFrame)
    assert "value_squared" in transformed.columns
    assert "value_normalized" in transformed.columns
    assert len(transformed) <= len(test_data)  # Some outliers may be filtered


def test_load_data():
    """Test data loading task."""
    # Create test data
    test_data = pd.DataFrame({
        "id": [1, 2, 3],
        "value": [0.1, 0.2, 0.3]
    })
    
    # Test CSV load
    result = load_data.fn(test_data, "csv")
    assert isinstance(result, dict)
    assert "rows_loaded" in result
    assert result["rows_loaded"] == 3
    assert result["destination"] == "csv"
    
    # Test database load
    result = load_data.fn(test_data, "database")
    assert result["destination"] == "database"


def test_train_model():
    """Test model training task."""
    # Create test data
    test_data = pd.DataFrame({
        "feature1": np.random.randn(50),
        "feature2": np.random.randn(50)
    })
    
    # Train model
    metrics = train_model.fn(test_data, "linear")
    
    # Check metrics
    assert isinstance(metrics, dict)
    assert "model_type" in metrics
    assert "accuracy" in metrics["metrics"]
    assert "precision" in metrics["metrics"]
    assert "recall" in metrics["metrics"]
    assert "f1_score" in metrics["metrics"]
    assert 0 <= metrics["metrics"]["accuracy"] <= 1


def test_evaluate_model():
    """Test model evaluation task."""
    # Create test metrics
    test_metrics = {
        "model_type": "random_forest",
        "metrics": {
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.80,
            "f1_score": 0.81
        }
    }
    
    # Evaluate with threshold
    evaluation = evaluate_model.fn(test_metrics, threshold=0.80)
    
    # Check evaluation
    assert isinstance(evaluation, dict)
    assert "passed" in evaluation
    assert "accuracy" in evaluation
    assert "threshold" in evaluation
    assert "meets_requirements" in evaluation
    
    # Test with higher threshold (should fail)
    evaluation = evaluate_model.fn(test_metrics, threshold=0.90)
    assert evaluation["passed"] == False


if __name__ == "__main__":
    # Run tests
    test_extract_data()
    test_transform_data()
    test_load_data()
    test_train_model()
    test_evaluate_model()
    print("All tests passed!")