"""
Example Prefect flows for local machine orchestration.
These demonstrate common automation patterns.
"""

from prefect import flow, task
from prefect.logging import get_run_logger
import time
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import requests
import json


@task
def extract_data(source: str) -> pd.DataFrame:
    """Extract data from source."""
    logger = get_run_logger()
    logger.info(f"Extracting data from {source}")
    
    # Simulate data extraction
    time.sleep(1)
    
    if source == "csv":
        data = pd.DataFrame({
            "id": range(100),
            "value": np.random.randn(100),
            "timestamp": [datetime.now() - timedelta(hours=i) for i in range(100)]
        })
    elif source == "api":
        # Simulate API call
        response = {"data": [{"id": i, "value": random.random()} for i in range(50)]}
        data = pd.DataFrame(response["data"])
    else:
        data = pd.DataFrame({"id": [1, 2, 3], "value": [0.1, 0.2, 0.3]})
    
    logger.info(f"Extracted {len(data)} rows")
    return data


@task
def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Transform and clean data."""
    logger = get_run_logger()
    logger.info("Transforming data")
    
    # Add derived columns
    data["value_squared"] = data["value"] ** 2
    data["value_normalized"] = (data["value"] - data["value"].mean()) / data["value"].std()
    
    # Filter outliers
    q_low = data["value"].quantile(0.01)
    q_high = data["value"].quantile(0.99)
    filtered_data = data[(data["value"] >= q_low) & (data["value"] <= q_high)]
    
    logger.info(f"Filtered {len(data) - len(filtered_data)} outliers")
    return filtered_data


@task
def load_data(data: pd.DataFrame, destination: str):
    """Load data to destination."""
    logger = get_run_logger()
    logger.info(f"Loading data to {destination}")
    
    if destination == "csv":
        filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        data.to_csv(filename, index=False)
        logger.info(f"Saved to {filename}")
    elif destination == "database":
        # Simulate database insert
        logger.info(f"Would insert {len(data)} rows to database")
    elif destination == "api":
        # Simulate API call
        logger.info(f"Would send {len(data)} rows to API")
    
    return {"rows_loaded": len(data), "destination": destination}


@flow(name="ETL Pipeline")
def etl_pipeline(source: str = "csv", destination: str = "csv"):
    """Complete ETL pipeline flow."""
    logger = get_run_logger()
    logger.info("Starting ETL pipeline")
    
    # Extract
    raw_data = extract_data(source)
    
    # Transform
    transformed_data = transform_data(raw_data)
    
    # Load
    result = load_data(transformed_data, destination)
    
    logger.info(f"ETL pipeline completed: {result}")
    return result


@task
def train_model(data: pd.DataFrame, model_type: str = "linear"):
    """Train a machine learning model."""
    logger = get_run_logger()
    logger.info(f"Training {model_type} model")
    
    # Simulate training
    time.sleep(2)
    
    # Create mock model metrics
    metrics = {
        "model_type": model_type,
        "accuracy": random.uniform(0.8, 0.95),
        "precision": random.uniform(0.75, 0.9),
        "recall": random.uniform(0.7, 0.88),
        "f1_score": random.uniform(0.8, 0.92),
        "training_time": random.uniform(1.5, 3.0),
        "samples": len(data)
    }
    
    logger.info(f"Model trained with accuracy: {metrics['accuracy']:.3f}")
    return metrics


@task
def evaluate_model(metrics: Dict[str, Any], threshold: float = 0.85):
    """Evaluate model performance."""
    logger = get_run_logger()
    logger.info("Evaluating model")
    
    passed = metrics["accuracy"] >= threshold
    evaluation = {
        "passed": passed,
        "accuracy": metrics["accuracy"],
        "threshold": threshold,
        "meets_requirements": passed
    }
    
    if passed:
        logger.info(f"Model meets accuracy threshold ({metrics['accuracy']:.3f} >= {threshold})")
    else:
        logger.warning(f"Model below accuracy threshold ({metrics['accuracy']:.3f} < {threshold})")
    
    return evaluation


@flow(name="ML Training Pipeline")
def ml_training_pipeline():
    """Machine learning training pipeline."""
    logger = get_run_logger()
    logger.info("Starting ML training pipeline")
    
    # Extract and prepare data
    data = extract_data("csv")
    transformed_data = transform_data(data)
    
    # Train model
    model_metrics = train_model(transformed_data, model_type="random_forest")
    
    # Evaluate
    evaluation = evaluate_model(model_metrics, threshold=0.82)
    
    # Save results
    results = {
        "model_metrics": model_metrics,
        "evaluation": evaluation,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to file
    filename = f"model_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"ML pipeline completed. Results saved to {filename}")
    return results


@task
def call_webhook(url: str, payload: Dict[str, Any]):
    """Call a webhook URL."""
    logger = get_run_logger()
    logger.info(f"Calling webhook: {url}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Webhook call successful: {response.status_code}")
        return {"success": True, "status_code": response.status_code}
    except Exception as e:
        logger.error(f"Webhook call failed: {e}")
        return {"success": False, "error": str(e)}


@task
def send_notification(message: str, channel: str = "log"):
    """Send notification to channel."""
    logger = get_run_logger()
    
    if channel == "log":
        logger.info(f"Notification: {message}")
    elif channel == "console":
        print(f"[NOTIFICATION] {message}")
    
    return {"channel": channel, "message": message, "sent_at": datetime.now().isoformat()}


@flow(name="Event-Driven Automation")
def event_driven_automation(event_type: str, event_data: Dict[str, Any]):
    """Event-driven automation flow."""
    logger = get_run_logger()
    logger.info(f"Processing {event_type} event")
    
    # Process based on event type
    if event_type == "data_ready":
        # Extract and transform
        data = extract_data("api")
        transformed = transform_data(data)
        
        # Send notification
        notification = send_notification(
            f"Data processed: {len(transformed)} rows",
            channel="log"
        )
        
        # Call webhook
        webhook_result = call_webhook(
            "http://localhost:5678/webhook/test",
            {"event": "data_processed", "rows": len(transformed)}
        )
        
        return {
            "event_type": event_type,
            "data_rows": len(transformed),
            "notification": notification,
            "webhook": webhook_result
        }
    
    elif event_type == "model_trained":
        # Train model
        data = extract_data("csv")
        metrics = train_model(data, model_type="gradient_boosting")
        
        # Evaluate
        evaluation = evaluate_model(metrics)
        
        # Send notification
        notification = send_notification(
            f"Model trained with accuracy: {metrics['accuracy']:.3f}",
            channel="console"
        )
        
        return {
            "event_type": event_type,
            "model_metrics": metrics,
            "evaluation": evaluation,
            "notification": notification
        }
    
    else:
        # Default event processing
        notification = send_notification(
            f"Unknown event type: {event_type}",
            channel="log"
        )
        
        return {
            "event_type": event_type,
            "processed": False,
            "notification": notification
        }


@flow(name="Scheduled Daily Report")
def scheduled_daily_report():
    """Generate and send daily report."""
    logger = get_run_logger()
    logger.info("Generating daily report")
    
    # Collect data from multiple sources
    data_sources = ["csv", "api"]
    all_data = []
    
    for source in data_sources:
        data = extract_data(source)
        transformed = transform_data(data)
        all_data.append(transformed)
    
    # Combine data
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Generate statistics
    stats = {
        "total_rows": len(combined_data),
        "sources": data_sources,
        "mean_value": float(combined_data["value"].mean()),
        "std_value": float(combined_data["value"].std()),
        "min_value": float(combined_data["value"].min()),
        "max_value": float(combined_data["value"].max()),
        "generated_at": datetime.now().isoformat()
    }
    
    # Save report
    report_filename = f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_filename, "w") as f:
        json.dump(stats, f, indent=2)
    
    # Send notification
    notification = send_notification(
        f"Daily report generated: {stats['total_rows']} rows from {len(data_sources)} sources",
        channel="log"
    )
    
    logger.info(f"Daily report saved to {report_filename}")
    return {"report": stats, "notification": notification, "filename": report_filename}


def deploy_all():
    """Deploy all example flows."""
    from prefect.deployments import Deployment
    
    # Deploy ETL pipeline
    etl_deployment = Deployment.build_from_flow(
        flow=etl_pipeline,
        name="etl-pipeline-deployment",
        parameters={"source": "csv", "destination": "csv"},
        tags=["etl", "data", "pipeline"]
    )
    etl_deployment.apply()
    
    # Deploy ML training pipeline
    ml_deployment = Deployment.build_from_flow(
        flow=ml_training_pipeline,
        name="ml-training-deployment",
        tags=["ml", "training", "ai"]
    )
    ml_deployment.apply()
    
    # Deploy scheduled daily report
    report_deployment = Deployment.build_from_flow(
        flow=scheduled_daily_report,
        name="daily-report-deployment",
        schedule={"cron": "0 9 * * *"},  # Run daily at 9 AM
        tags=["scheduled", "report", "daily"]
    )
    report_deployment.apply()
    
    print("All example flows deployed successfully!")
    print("Run 'prefect deployment run <deployment-name>' to execute them.")


if __name__ == "__main__":
    # Run examples directly
    print("Running example flows...")
    
    # Run ETL pipeline
    print("\n1. Running ETL Pipeline:")
    etl_result = etl_pipeline()
    print(f"   Result: {etl_result}")
    
    # Run ML training pipeline
    print("\n2. Running ML Training Pipeline:")
    ml_result = ml_training_pipeline()
    print(f"   Result saved to JSON file")
    
    # Run event-driven automation
    print("\n3. Running Event-Driven Automation:")
    event_result = event_driven_automation("data_ready", {"test": "data"})
    print(f"   Result: {event_result}")
    
    print("\nAll example flows completed successfully!")