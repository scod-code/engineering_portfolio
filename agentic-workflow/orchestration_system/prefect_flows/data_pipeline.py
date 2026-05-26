#!/usr/bin/env python3
"""
Data pipeline example using Prefect.
This demonstrates a real-world data processing workflow.
"""

from prefect import flow, task
from prefect.logging import get_run_logger
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from pathlib import Path


@task
def generate_sample_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate sample time series data."""
    logger = get_run_logger()
    logger.info(f"Generating {n_samples} samples of time series data")
    
    dates = [datetime.now() - timedelta(hours=i) for i in range(n_samples)]
    
    data = pd.DataFrame({
        "timestamp": dates,
        "sensor_id": np.random.choice(["A", "B", "C", "D"], n_samples),
        "temperature": np.random.normal(22.5, 2.5, n_samples),
        "humidity": np.random.normal(45, 10, n_samples),
        "pressure": np.random.normal(1013, 5, n_samples),
        "quality_score": np.random.uniform(0.7, 1.0, n_samples)
    })
    
    # Add some anomalies
    anomaly_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    data.loc[anomaly_indices, "temperature"] *= 1.5
    data.loc[anomaly_indices, "quality_score"] *= 0.5
    
    logger.info(f"Generated data with shape: {data.shape}")
    return data


@task
def detect_anomalies(data: pd.DataFrame) -> pd.DataFrame:
    """Detect anomalies in the data."""
    logger = get_run_logger()
    logger.info("Detecting anomalies")
    
    # Simple anomaly detection based on z-score
    for column in ["temperature", "humidity", "pressure"]:
        mean = data[column].mean()
        std = data[column].std()
        data[f"{column}_zscore"] = (data[column] - mean) / std
        data[f"{column}_anomaly"] = abs(data[f"{column}_zscore"]) > 3
    
    # Overall anomaly flag
    data["is_anomaly"] = (
        data["temperature_anomaly"] | 
        data["humidity_anomaly"] | 
        data["pressure_anomaly"] |
        (data["quality_score"] < 0.8)
    )
    
    anomalies = data[data["is_anomaly"]]
    logger.info(f"Detected {len(anomalies)} anomalies")
    
    return data


@task
def calculate_statistics(data: pd.DataFrame) -> dict:
    """Calculate statistics for the data."""
    logger = get_run_logger()
    logger.info("Calculating statistics")
    
    stats = {
        "total_samples": len(data),
        "anomaly_count": int(data["is_anomaly"].sum()),
        "anomaly_percentage": float(data["is_anomaly"].mean() * 100),
        "sensor_counts": data["sensor_id"].value_counts().to_dict(),
        "temperature_stats": {
            "mean": float(data["temperature"].mean()),
            "std": float(data["temperature"].std()),
            "min": float(data["temperature"].min()),
            "max": float(data["temperature"].max())
        },
        "humidity_stats": {
            "mean": float(data["humidity"].mean()),
            "std": float(data["humidity"].std()),
            "min": float(data["humidity"].min()),
            "max": float(data["humidity"].max())
        },
        "pressure_stats": {
            "mean": float(data["pressure"].mean()),
            "std": float(data["pressure"].std()),
            "min": float(data["pressure"].min()),
            "max": float(data["pressure"].max())
        },
        "processing_timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Statistics calculated: {stats['anomaly_count']} anomalies found")
    return stats


@task
def save_results(data: pd.DataFrame, stats: dict, output_dir: str = "output"):
    """Save processed data and statistics."""
    logger = get_run_logger()
    logger.info("Saving results")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save processed data
    data_filename = f"{output_dir}/processed_data_{timestamp}.csv"
    data.to_csv(data_filename, index=False)
    
    # Save statistics
    stats_filename = f"{output_dir}/statistics_{timestamp}.json"
    with open(stats_filename, "w") as f:
        json.dump(stats, f, indent=2)
    
    # Save anomaly report
    anomalies = data[data["is_anomaly"]]
    if len(anomalies) > 0:
        anomaly_filename = f"{output_dir}/anomalies_{timestamp}.csv"
        anomalies.to_csv(anomaly_filename, index=False)
    
    logger.info(f"Results saved to {output_dir}/")
    return {
        "data_file": data_filename,
        "stats_file": stats_filename,
        "anomaly_file": anomaly_filename if len(anomalies) > 0 else None,
        "anomaly_count": len(anomalies)
    }


@task
def send_alert_if_needed(stats: dict, threshold: float = 5.0):
    """Send alert if anomaly percentage exceeds threshold."""
    logger = get_run_logger()
    
    anomaly_percentage = stats["anomaly_percentage"]
    
    if anomaly_percentage > threshold:
        alert_message = (
            f"⚠️ HIGH ANOMALY RATE DETECTED ⚠️\n"
            f"Anomaly percentage: {anomaly_percentage:.1f}% (threshold: {threshold}%)\n"
            f"Total anomalies: {stats['anomaly_count']}\n"
            f"Time: {stats['processing_timestamp']}"
        )
        logger.warning(alert_message)
        return {
            "alert_sent": True,
            "message": alert_message,
            "anomaly_percentage": anomaly_percentage
        }
    else:
        logger.info(f"Anomaly rate normal: {anomaly_percentage:.1f}%")
        return {
            "alert_sent": False,
            "anomaly_percentage": anomaly_percentage
        }


@flow(name="Data Quality Pipeline")
def data_quality_pipeline(
    n_samples: int = 1000,
    anomaly_threshold: float = 5.0,
    output_dir: str = "output"
):
    """
    Complete data quality pipeline.
    
    Args:
        n_samples: Number of samples to generate
        anomaly_threshold: Percentage threshold for alerts
        output_dir: Directory to save output files
    """
    logger = get_run_logger()
    logger.info("Starting data quality pipeline")
    
    # Generate sample data
    raw_data = generate_sample_data(n_samples)
    
    # Detect anomalies
    processed_data = detect_anomalies(raw_data)
    
    # Calculate statistics
    stats = calculate_statistics(processed_data)
    
    # Save results
    save_results(processed_data, stats, output_dir)
    
    # Check for alerts
    alert = send_alert_if_needed(stats, anomaly_threshold)
    
    # Return summary
    summary = {
        "pipeline": "data_quality",
        "samples_processed": n_samples,
        "anomalies_detected": stats["anomaly_count"],
        "anomaly_percentage": stats["anomaly_percentage"],
        "alert_triggered": alert["alert_sent"],
        "output_directory": output_dir,
        "completed_at": datetime.now().isoformat()
    }
    
    logger.info(f"Data quality pipeline completed: {summary}")
    return summary


if __name__ == "__main__":
    # Run the pipeline directly
    print("Running Data Quality Pipeline...")
    result = data_quality_pipeline(
        n_samples=500,
        anomaly_threshold=3.0,
        output_dir="data_pipeline_output"
    )
    print(f"\nPipeline completed successfully!")
    print(f"Summary: {json.dumps(result, indent=2)}")