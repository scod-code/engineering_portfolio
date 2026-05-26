#!/usr/bin/env python3
"""
Machine Learning Pipeline using Prefect.
Demonstrates a complete ML workflow with model training, evaluation, and deployment.
"""

from prefect import flow, task
from prefect.logging import get_run_logger
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json
import pickle
from pathlib import Path
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Simulated ML imports (in real scenario, import actual libraries)
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report


@task
def load_and_prepare_data(dataset_name: str = "sample") -> Tuple[pd.DataFrame, pd.Series]:
    """Load and prepare dataset for ML training."""
    logger = get_run_logger()
    logger.info(f"Loading dataset: {dataset_name}")
    
    # Simulate data loading
    time.sleep(1)
    
    # Generate synthetic classification data
    n_samples = 1000
    n_features = 20
    
    # Features
    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f"feature_{i}" for i in range(n_features)]
    )
    
    # Add some meaningful patterns
    X["feature_0"] = X["feature_0"] * 2 + np.random.randn(n_samples) * 0.5
    X["feature_1"] = X["feature_1"] * 1.5 - np.random.randn(n_samples) * 0.3
    
    # Target (binary classification)
    y = pd.Series(
        (X["feature_0"] + X["feature_1"] + np.random.randn(n_samples) * 0.2) > 0,
        name="target"
    ).astype(int)
    
    # Add some noise
    noise_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
    y.iloc[noise_indices] = 1 - y.iloc[noise_indices]
    
    logger.info(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    logger.info(f"Class distribution: {y.value_counts().to_dict()}")
    
    return X, y


@task
def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
    """Split data into training and testing sets."""
    logger = get_run_logger()
    logger.info(f"Splitting data with test_size={test_size}")
    
    # Simulate train-test split
    n_samples = len(X)
    n_test = int(n_samples * test_size)
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    X_train = X.iloc[train_indices]
    X_test = X.iloc[test_indices]
    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]
    
    split_info = {
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "train_test_ratio": len(X_train) / len(X_test),
        "features": X.shape[1]
    }
    
    logger.info(f"Split complete: {split_info['train_samples']} train, {split_info['test_samples']} test")
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "split_info": split_info
    }


@task
def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = "random_forest",
    hyperparams: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Train a machine learning model."""
    logger = get_run_logger()
    logger.info(f"Training {model_type} model")
    
    if hyperparams is None:
        hyperparams = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        }
    
    # Simulate training (in real scenario, use actual ML library)
    time.sleep(2)
    
    # Generate mock model metrics
    np.random.seed(42)
    
    # Simulate predictions for metrics calculation
    n_train = len(X_train)
    y_pred_train = (np.random.rand(n_train) > 0.3).astype(int)
    y_pred_proba_train = np.random.rand(n_train)
    
    # Calculate mock metrics
    accuracy = np.random.uniform(0.85, 0.95)
    precision = np.random.uniform(0.82, 0.92)
    recall = np.random.uniform(0.80, 0.90)
    f1 = 2 * (precision * recall) / (precision + recall)
    
    # Feature importance (mock)
    feature_importance = {
        f"feature_{i}": float(np.random.uniform(0, 1))
        for i in range(min(10, X_train.shape[1]))
    }
    
    model_info = {
        "model_type": model_type,
        "hyperparameters": hyperparams,
        "training_samples": n_train,
        "training_time": np.random.uniform(1.5, 3.0),
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "auc_roc": float(np.random.uniform(0.88, 0.96))
        },
        "feature_importance": feature_importance,
        "model_size_mb": np.random.uniform(5, 20)
    }
    
    logger.info(f"Model trained: accuracy={model_info['metrics']['accuracy']:.3f}")
    return model_info


@task
def evaluate_model(
    model_info: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Any]:
    """Evaluate model on test set."""
    logger = get_run_logger()
    logger.info("Evaluating model on test set")
    
    # Simulate evaluation
    time.sleep(1)
    
    n_test = len(X_test)
    
    # Generate mock test predictions
    y_pred_test = (np.random.rand(n_test) > 0.3).astype(int)
    y_pred_proba_test = np.random.rand(n_test)
    
    # Calculate test metrics (slightly worse than training)
    test_accuracy = model_info["metrics"]["accuracy"] * np.random.uniform(0.95, 0.98)
    test_precision = model_info["metrics"]["precision"] * np.random.uniform(0.94, 0.97)
    test_recall = model_info["metrics"]["recall"] * np.random.uniform(0.93, 0.96)
    test_f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall)
    
    # Confusion matrix (mock)
    tp = int(n_test * test_accuracy * 0.6)
    tn = int(n_test * test_accuracy * 0.4)
    fp = int(n_test * (1 - test_accuracy) * 0.3)
    fn = int(n_test * (1 - test_accuracy) * 0.7)
    
    evaluation = {
        "test_samples": n_test,
        "metrics": {
            "accuracy": float(test_accuracy),
            "precision": float(test_precision),
            "recall": float(test_recall),
            "f1_score": float(test_f1),
            "auc_roc": float(model_info["metrics"]["auc_roc"] * np.random.uniform(0.97, 0.99))
        },
        "confusion_matrix": {
            "true_positive": tp,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn
        },
        "overfitting_check": {
            "accuracy_drop": float(model_info["metrics"]["accuracy"] - test_accuracy),
            "acceptable": (model_info["metrics"]["accuracy"] - test_accuracy) < 0.05
        }
    }
    
    logger.info(f"Test evaluation: accuracy={evaluation['metrics']['accuracy']:.3f}")
    return evaluation


@task
def save_model(
    model_info: Dict[str, Any],
    evaluation: Dict[str, Any],
    output_dir: str = "models"
) -> Dict[str, Any]:
    """Save model artifacts and metadata."""
    logger = get_run_logger()
    logger.info("Saving model artifacts")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_id = f"model_{timestamp}"
    
    # Save model metadata
    metadata = {
        "model_id": model_id,
        "created_at": datetime.now().isoformat(),
        "model_info": model_info,
        "evaluation": evaluation,
        "performance_summary": {
            "train_accuracy": model_info["metrics"]["accuracy"],
            "test_accuracy": evaluation["metrics"]["accuracy"],
            "overfitting": evaluation["overfitting_check"]["acceptable"],
            "model_size_mb": model_info["model_size_mb"]
        }
    }
    
    metadata_file = f"{output_dir}/{model_id}_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Save mock model file
    model_file = f"{output_dir}/{model_id}.pkl"
    with open(model_file, "wb") as f:
        pickle.dump({"mock": "model", "timestamp": timestamp}, f)
    
    # Save evaluation report
    report_file = f"{output_dir}/{model_id}_report.txt"
    with open(report_file, "w") as f:
        f.write(f"Model Training Report\n")
        f.write(f"=====================\n\n")
        f.write(f"Model ID: {model_id}\n")
        f.write(f"Created: {metadata['created_at']}\n\n")
        f.write(f"Training Metrics:\n")
        for metric, value in model_info["metrics"].items():
            f.write(f"  {metric}: {value:.4f}\n")
        f.write(f"\nTest Metrics:\n")
        for metric, value in evaluation["metrics"].items():
            f.write(f"  {metric}: {value:.4f}\n")
        f.write(f"\nOverfitting Check: {'PASS' if evaluation['overfitting_check']['acceptable'] else 'FAIL'}\n")
    
    logger.info(f"Model artifacts saved to {output_dir}/")
    
    return {
        "model_id": model_id,
        "metadata_file": metadata_file,
        "model_file": model_file,
        "report_file": report_file,
        "output_dir": output_dir
    }


@task
def deploy_model_if_good(
    model_artifacts: Dict[str, Any],
    accuracy_threshold: float = 0.85,
    overfitting_threshold: float = 0.05
) -> Dict[str, Any]:
    """Check if model meets deployment criteria."""
    logger = get_run_logger()
    logger.info("Checking deployment criteria")
    
    # Load metadata
    metadata_file = model_artifacts["metadata_file"]
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    
    test_accuracy = metadata["evaluation"]["metrics"]["accuracy"]
    accuracy_drop = metadata["evaluation"]["overfitting_check"]["accuracy_drop"]
    
    meets_accuracy = test_accuracy >= accuracy_threshold
    meets_overfitting = abs(accuracy_drop) <= overfitting_threshold
    
    deployable = meets_accuracy and meets_overfitting
    
    deployment_decision = {
        "deployable": deployable,
        "test_accuracy": test_accuracy,
        "accuracy_threshold": accuracy_threshold,
        "accuracy_met": meets_accuracy,
        "overfitting_drop": accuracy_drop,
        "overfitting_threshold": overfitting_threshold,
        "overfitting_met": meets_overfitting,
        "decision_reason": (
            "Model meets all criteria" if deployable else
            f"Accuracy too low: {test_accuracy:.3f} < {accuracy_threshold}" if not meets_accuracy else
            f"Overfitting detected: drop={accuracy_drop:.3f} > {overfitting_threshold}"
        )
    }
    
    if deployable:
        logger.info(f"✅ Model approved for deployment: accuracy={test_accuracy:.3f}")
        # Simulate deployment steps
        deployment_decision.update({
            "deployment_steps": [
                "Model validated",
                "Artifacts packaged",
                "API endpoint created",
                "Monitoring configured"
            ],
            "deployment_status": "ready"
        })
    else:
        logger.warning(f"❌ Model rejected: {deployment_decision['decision_reason']}")
        deployment_decision.update({
            "deployment_steps": ["Model rejected - requires retraining"],
            "deployment_status": "rejected"
        })
    
    return deployment_decision


@flow(name="ML Training Pipeline")
def ml_training_pipeline(
    dataset_name: str = "sample",
    test_size: float = 0.2,
    model_type: str = "random_forest",
    accuracy_threshold: float = 0.85,
    output_dir: str = "ml_models"
):
    """
    Complete ML training pipeline.
    
    Args:
        dataset_name: Name of dataset to use
        test_size: Proportion of data for testing
        model_type: Type of model to train
        accuracy_threshold: Minimum accuracy for deployment
        output_dir: Directory to save model artifacts
    """
    logger = get_run_logger()
    logger.info("Starting ML training pipeline")
    
    # Load and prepare data
    X, y = load_and_prepare_data(dataset_name)
    
    # Split data
    split_data_result = split_data(X, y, test_size)
    
    # Train model
    model_info = train_model(
        split_data_result["X_train"],
        split_data_result["y_train"],
        model_type=model_type
    )
    
    # Evaluate model
    evaluation = evaluate_model(
        model_info,
        split_data_result["X_test"],
        split_data_result["y_test"]
    )
    
    # Save model artifacts
    model_artifacts = save_model(model_info, evaluation, output_dir)
    
    # Check deployment criteria
    deployment_decision = deploy_model_if_good(model_artifacts, accuracy_threshold)
    
    # Pipeline summary
    summary = {
        "pipeline": "ml_training",
        "dataset": dataset_name,
        "model_type": model_type,
        "training_samples": split_data_result["split_info"]["train_samples"],
        "test_samples": split_data_result["split_info"]["test_samples"],
        "final_accuracy": evaluation["metrics"]["accuracy"],
        "deployment_approved": deployment_decision["deployable"],
        "model_id": model_artifacts["model_id"],
        "output_directory": output_dir,
        "completed_at": datetime.now().isoformat()
    }
    
    logger.info(f"ML training pipeline completed: {summary}")
    return summary


if __name__ == "__main__":
    # Run the pipeline directly
    print("Running ML Training Pipeline...")
    result = ml_training_pipeline(
        dataset_name="sample_classification",
        test_size=0.25,
        model_type="random_forest",
        accuracy_threshold=0.82,
        output_dir="ml_pipeline_output"
    )
    print(f"\nPipeline completed successfully!")
    print(f"Summary: {json.dumps(result, indent=2)}")