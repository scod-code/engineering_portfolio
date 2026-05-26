#!/usr/bin/env python3
"""
ETL (Extract, Transform, Load) Pipeline using Prefect.
Demonstrates a complete data pipeline with error handling and monitoring.
"""

from prefect import flow, task
from prefect.logging import get_run_logger
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import sqlite3
import hashlib


@task(retries=3, retry_delay_seconds=10)
def extract_from_source(source_type: str, source_config: Dict[str, Any]) -> pd.DataFrame:
    """Extract data from various sources."""
    logger = get_run_logger()
    logger.info(f"Extracting from {source_type} source")
    
    try:
        if source_type == "csv":
            filepath = source_config.get("filepath", "data/source.csv")
            logger.info(f"Reading CSV from {filepath}")
            
            # Simulate reading CSV
            time.sleep(1)
            
            # Generate sample data if file doesn't exist
            if not Path(filepath).exists():
                logger.warning(f"File {filepath} not found, generating sample data")
                data = generate_sample_data(100)
                Path("data").mkdir(exist_ok=True)
                data.to_csv(filepath, index=False)
            else:
                data = pd.read_csv(filepath)
            
            logger.info(f"Extracted {len(data)} rows from CSV")
            
        elif source_type == "api":
            url = source_config.get("url", "https://api.example.com/data")
            params = source_config.get("params", {})
            
            logger.info(f"Calling API: {url}")
            time.sleep(2)  # Simulate API call
            
            # Simulate API response
            data = pd.DataFrame({
                "id": range(50),
                "api_value": np.random.randn(50),
                "timestamp": [datetime.now() - timedelta(minutes=i) for i in range(50)],
                "source": "api"
            })
            
            logger.info(f"Extracted {len(data)} rows from API")
            
        elif source_type == "database":
            query = source_config.get("query", "SELECT * FROM data")
            db_path = source_config.get("db_path", "data/source.db")
            
            logger.info(f"Querying database: {query[:50]}...")
            time.sleep(1.5)
            
            # Simulate database query
            data = pd.DataFrame({
                "db_id": range(75),
                "db_value": np.random.randn(75),
                "extracted_at": datetime.now().isoformat(),
                "source": "database"
            })
            
            logger.info(f"Extracted {len(data)} rows from database")
            
        else:
            raise ValueError(f"Unknown source type: {source_type}")
        
        # Add extraction metadata
        data["_extracted_at"] = datetime.now().isoformat()
        data["_source_type"] = source_type
        data["_extraction_id"] = hashlib.md5(
            f"{source_type}_{datetime.now().timestamp()}".encode()
        ).hexdigest()[:8]
        
        return data
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


@task
def validate_data(data: pd.DataFrame, validation_rules: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data quality and integrity."""
    logger = get_run_logger()
    logger.info("Validating data")
    
    validation_results = {
        "total_rows": len(data),
        "validation_passed": True,
        "issues": [],
        "metrics": {}
    }
    
    # Check for null values
    null_counts = data.isnull().sum()
    total_nulls = null_counts.sum()
    
    if total_nulls > 0:
        validation_results["issues"].append({
            "type": "null_values",
            "count": int(total_nulls),
            "columns": null_counts[null_counts > 0].to_dict()
        })
    
    # Check data types
    expected_types = validation_rules.get("expected_types", {})
    for col, expected_type in expected_types.items():
        if col in data.columns:
            actual_type = str(data[col].dtype)
            if expected_type not in actual_type:
                validation_results["issues"].append({
                    "type": "type_mismatch",
                    "column": col,
                    "expected": expected_type,
                    "actual": actual_type
                })
    
    # Check value ranges
    range_rules = validation_rules.get("value_ranges", {})
    for col, (min_val, max_val) in range_rules.items():
        if col in data.columns:
            out_of_range = ((data[col] < min_val) | (data[col] > max_val)).sum()
            if out_of_range > 0:
                validation_results["issues"].append({
                    "type": "out_of_range",
                    "column": col,
                    "count": int(out_of_range),
                    "range": [min_val, max_val]
                })
    
    # Calculate data quality metrics
    validation_results["metrics"] = {
        "completeness": 1.0 - (total_nulls / (len(data) * len(data.columns))),
        "unique_rows": len(data.drop_duplicates()) / len(data),
        "column_count": len(data.columns),
        "memory_usage_mb": data.memory_usage(deep=True).sum() / 1024 / 1024
    }
    
    # Determine if validation passed
    critical_issues = [issue for issue in validation_results["issues"] 
                      if issue["type"] in ["type_mismatch", "out_of_range"]]
    
    if critical_issues:
        validation_results["validation_passed"] = False
        logger.warning(f"Validation failed with {len(critical_issues)} critical issues")
    else:
        logger.info(f"Validation passed with {len(validation_results['issues'])} minor issues")
    
    return validation_results


@task
def transform_data(data: pd.DataFrame, transformations: List[Dict[str, Any]]) -> pd.DataFrame:
    """Apply transformations to data."""
    logger = get_run_logger()
    logger.info("Transforming data")
    
    transformed_data = data.copy()
    
    for transform in transformations:
        transform_type = transform.get("type")
        
        if transform_type == "rename_columns":
            column_map = transform.get("mapping", {})
            transformed_data = transformed_data.rename(columns=column_map)
            logger.info(f"Renamed columns: {list(column_map.keys())}")
            
        elif transform_type == "add_derived_columns":
            for col_config in transform.get("columns", []):
                name = col_config["name"]
                expression = col_config["expression"]
                
                # Simple expression evaluation (in real scenario, use safer method)
                if expression == "value_squared":
                    transformed_data[name] = transformed_data["value"] ** 2
                elif expression == "normalized":
                    col = col_config.get("source_column", "value")
                    mean = transformed_data[col].mean()
                    std = transformed_data[col].std()
                    transformed_data[name] = (transformed_data[col] - mean) / std
                elif expression == "timestamp_to_date":
                    col = col_config.get("source_column", "timestamp")
                    transformed_data[name] = pd.to_datetime(transformed_data[col]).dt.date
                
                logger.info(f"Added derived column: {name}")
            
        elif transform_type == "filter":
            condition = transform.get("condition")
            if condition == "remove_nulls":
                before = len(transformed_data)
                transformed_data = transformed_data.dropna()
                after = len(transformed_data)
                logger.info(f"Filtered nulls: {before - after} rows removed")
            
        elif transform_type == "aggregate":
            group_by = transform.get("group_by", [])
            aggregations = transform.get("aggregations", {})
            
            if group_by and aggregations:
                aggregated = transformed_data.groupby(group_by).agg(aggregations).reset_index()
                transformed_data = aggregated
                logger.info(f"Aggregated by {group_by}")
    
    # Add transformation metadata
    transformed_data["_transformed_at"] = datetime.now().isoformat()
    transformed_data["_transformation_id"] = hashlib.md5(
        f"transform_{datetime.now().timestamp()}".encode()
    ).hexdigest()[:8]
    
    logger.info(f"Transformation complete: {len(transformed_data)} rows")
    return transformed_data


@task
def load_to_destination(data: pd.DataFrame, destination_type: str, 
                       destination_config: Dict[str, Any]) -> Dict[str, Any]:
    """Load data to destination."""
    logger = get_run_logger()
    logger.info(f"Loading to {destination_type}")
    
    load_result = {
        "destination_type": destination_type,
        "rows_loaded": len(data),
        "success": True,
        "errors": [],
        "files_created": []
    }
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if destination_type == "csv":
            output_dir = destination_config.get("output_dir", "output")
            filename = destination_config.get("filename", f"etl_output_{timestamp}.csv")
            filepath = f"{output_dir}/{filename}"
            
            Path(output_dir).mkdir(exist_ok=True)
            data.to_csv(filepath, index=False)
            
            load_result["files_created"].append(filepath)
            logger.info(f"Loaded {len(data)} rows to CSV: {filepath}")
            
        elif destination_type == "database":
            table_name = destination_config.get("table_name", "etl_results")
            db_path = destination_config.get("db_path", "data/etl_database.db")
            
            # Simulate database load
            Path("data").mkdir(exist_ok=True)
            conn = sqlite3.connect(db_path)
            data.to_sql(table_name, conn, if_exists="append", index=False)
            conn.close()
            
            load_result["database_info"] = {
                "database": db_path,
                "table": table_name,
                "rows_inserted": len(data)
            }
            logger.info(f"Loaded {len(data)} rows to database table: {table_name}")
            
        elif destination_type == "json":
            output_dir = destination_config.get("output_dir", "output")
            filename = destination_config.get("filename", f"etl_output_{timestamp}.json")
            filepath = f"{output_dir}/{filename}"
            
            Path(output_dir).mkdir(exist_ok=True)
            data.to_json(filepath, orient="records", indent=2)
            
            load_result["files_created"].append(filepath)
            logger.info(f"Loaded {len(data)} rows to JSON: {filepath}")
            
        else:
            raise ValueError(f"Unknown destination type: {destination_type}")
            
    except Exception as e:
        load_result["success"] = False
        load_result["errors"].append(str(e))
        logger.error(f"Load failed: {e}")
    
    return load_result


@task
def generate_etl_report(
    extraction_result: pd.DataFrame,
    validation_result: Dict[str, Any],
    transformation_result: pd.DataFrame,
    load_result: Dict[str, Any],
    pipeline_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate comprehensive ETL pipeline report."""
    logger = get_run_logger()
    logger.info("Generating ETL report")
    
    report = {
        "pipeline_id": hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:12],
        "execution_timestamp": datetime.now().isoformat(),
        "pipeline_config": pipeline_config,
        "extraction": {
            "source_type": pipeline_config.get("source_type"),
            "rows_extracted": len(extraction_result),
            "columns_extracted": list(extraction_result.columns)
        },
        "validation": validation_result,
        "transformation": {
            "rows_transformed": len(transformation_result),
            "columns_transformed": list(transformation_result.columns),
            "transformations_applied": len(pipeline_config.get("transformations", []))
        },
        "load": load_result,
        "summary": {
            "total_processing_time": None,  # Would be calculated from task durations
            "success": validation_result.get("validation_passed", False) and load_result.get("success", False),
            "data_quality_score": validation_result.get("metrics", {}).get("completeness", 0),
            "throughput_rows_per_second": len(transformation_result) / 10  # Simplified
        }
    }
    
    # Save report to file
    output_dir = "reports"
    Path(output_dir).mkdir(exist_ok=True)
    
    report_file = f"{output_dir}/etl_report_{report['pipeline_id']}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"ETL report saved to {report_file}")
    return report


def generate_sample_data(n_rows: int = 100) -> pd.DataFrame:
    """Generate sample data for demonstration."""
    dates = [datetime.now() - timedelta(hours=i) for i in range(n_rows)]
    
    data = pd.DataFrame({
        "id": range(n_rows),
        "timestamp": dates,
        "value": np.random.randn(n_rows),
        "category": np.random.choice(["A", "B", "C", "D"], n_rows),
        "status": np.random.choice(["active", "inactive", "pending"], n_rows),
        "amount": np.random.uniform(10, 1000, n_rows),
        "quantity": np.random.randint(1, 100, n_rows)
    })
    
    # Add some null values for testing
    null_indices = np.random.choice(n_rows, size=int(n_rows * 0.05), replace=False)
    data.loc[null_indices, "value"] = np.nan
    
    return data


@flow(name="ETL Pipeline")
def etl_pipeline(
    source_type: str = "csv",
    source_config: Optional[Dict[str, Any]] = None,
    destination_type: str = "csv",
    destination_config: Optional[Dict[str, Any]] = None,
    validation_rules: Optional[Dict[str, Any]] = None,
    transformations: Optional[List[Dict[str, Any]]] = None
):
    """
    Complete ETL pipeline.
    
    Args:
        source_type: Type of source (csv, api, database)
        source_config: Configuration for source
        destination_type: Type of destination (csv, database, json)
        destination_config: Configuration for destination
        validation_rules: Data validation rules
        transformations: List of transformations to apply
    """
    logger = get_run_logger()
    logger.info("Starting ETL pipeline")
    
    # Default configurations
    if source_config is None:
        source_config = {"filepath": "data/source.csv"}
    
    if destination_config is None:
        destination_config = {"output_dir": "output", "filename": "etl_output.csv"}
    
    if validation_rules is None:
        validation_rules = {
            "expected_types": {
                "id": "int",
                "value": "float",
                "timestamp": "datetime"
            },
            "value_ranges": {
                "amount": [0, 10000],
                "quantity": [0, 1000]
            }
        }
    
    if transformations is None:
        transformations = [
            {
                "type": "rename_columns",
                "mapping": {"id": "record_id", "value": "measurement"}
            },
            {
                "type": "add_derived_columns",
                "columns": [
                    {"name": "value_squared", "expression": "value_squared"},
                    {"name": "normalized_value", "expression": "normalized"}
                ]
            },
            {
                "type": "filter",
                "condition": "remove_nulls"
            }
        ]
    
    pipeline_config = {
        "source_type": source_type,
        "source_config": source_config,
        "destination_type": destination_type,
        "destination_config": destination_config,
        "validation_rules": validation_rules,
        "transformations": transformations,
        "started_at": datetime.now().isoformat()
    }
    
    # Extract
    extracted_data = extract_from_source(source_type, source_config)
    
    # Validate
    validation_result = validate_data(extracted_data, validation_rules)
    
    # Transform (only if validation passed)
    if validation_result["validation_passed"]:
        transformed_data = transform_data(extracted_data, transformations)
    else:
        logger.error("Validation failed, skipping transformation")
        transformed_data = extracted_data
    
    # Load
    load_result = load_to_destination(transformed_data, destination_type, destination_config)
    
    # Generate report
    report = generate_etl_report(
        extracted_data,
        validation_result,
        transformed_data,
        load_result,
        pipeline_config
    )
    
    # Pipeline summary
    summary = {
        "pipeline": "etl",
        "source": source_type,
        "destination": destination_type,
        "rows_processed": len(extracted_data),
        "validation_passed": validation_result["validation_passed"],
        "load_successful": load_result["success"],
        "report_generated": True,
        "report_id": report["pipeline_id"],
        "completed_at": datetime.now().isoformat()
    }
    
    logger.info(f"ETL pipeline completed: {summary}")
    return summary


if __name__ == "__main__":
    # Run the pipeline directly
    print("Running ETL Pipeline...")
    
    # Create sample data directory
    Path("data").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    result = etl_pipeline(
        source_type="csv",
        source_config={"filepath": "data/sample_data.csv"},
        destination_type="csv",
        destination_config={
            "output_dir": "etl_output",
            "filename": "processed_data.csv"
        }
    )
    
    print(f"\nETL Pipeline completed successfully!")
    print(f"Summary: {json.dumps(result, indent=2)}")