# Data Engineering: Scalable Analytics Infrastructure

**Production-grade data pipelines and analytics systems**

[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-blue)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/NumPy-1.x-orange)](https://numpy.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-red)](https://matplotlib.org)

---

## Overview

This portfolio demonstrates expertise in building scalable data processing infrastructure, from ETL pipelines handling large datasets to optimized analytics engines. Projects showcase performance optimization, data quality assurance, and production-ready visualization systems.

### Key Competencies
- **ETL Pipeline Design**: Extract, Transform, Load systems for large datasets
- **Performance Optimization**: Pandas/NumPy optimization for 10x+ speedups
- **Data Quality**: Automated validation and cleansing pipelines
- **Analytics Engines**: Scalable computation frameworks
- **Visualization Systems**: Production-ready dashboards and reporting

---

## Portfolio Structure

```
data-engineering/
├── README.md                    # This overview
├── etl-pipelines/              # Data pipeline engineering
│   ├── batch-processing/        # Large-scale batch ETL systems
│   ├── streaming/               # Real-time data processing
│   ├── data-validation/         # Quality assurance frameworks
│   └── README.md
├── analytics-engines/           # Optimized computation systems
│   ├── pandas-optimization/     # High-performance data manipulation
│   ├── numpy-acceleration/      # Vectorized computation
│   ├── memory-management/       # Efficient large dataset handling
│   └── README.md
├── visualization/               # Production dashboards
│   ├── executive-dashboards/    # Business intelligence reporting
│   ├── real-time-monitoring/    # Live data visualization
│   ├── interactive-analytics/   # Exploratory data analysis tools
│   └── README.md
└── requirements.txt             # Dependencies
```

---

## ETL Pipeline Engineering

### Scalable Batch Processing System
```python
class ProductionETLPipeline:
    """High-performance ETL pipeline for large datasets."""
    
    def __init__(self, chunk_size=10000, n_workers=4):
        self.chunk_size = chunk_size
        self.n_workers = n_workers
        self.logger = self._setup_logging()
        
    def extract_data(self, source_config):
        """Extract data from multiple sources with error handling."""
        extractors = {
            'csv': self._extract_csv,
            'json': self._extract_json,
            'database': self._extract_database,
            'api': self._extract_api
        }
        
        source_type = source_config['type']
        if source_type not in extractors:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        self.logger.info(f"Extracting data from {source_type} source")
        return extractors[source_type](source_config)
    
    def _extract_csv(self, config):
        """Extract from CSV with chunked reading for memory efficiency."""
        file_path = config['path']
        
        # Read in chunks to handle large files
        chunks = []
        for chunk in pd.read_csv(file_path, chunksize=self.chunk_size):
            chunks.append(chunk)
        
        return pd.concat(chunks, ignore_index=True)
    
    def transform_data(self, df, transformations):
        """Apply transformations with performance optimization."""
        self.logger.info("Starting data transformations")
        
        for transform in transformations:
            transform_type = transform['type']
            
            if transform_type == 'clean':
                df = self._clean_data(df, transform['config'])
            elif transform_type == 'aggregate':
                df = self._aggregate_data(df, transform['config'])
            elif transform_type == 'enrich':
                df = self._enrich_data(df, transform['config'])
            elif transform_type == 'validate':
                df = self._validate_data(df, transform['config'])
        
        return df
    
    def _clean_data(self, df, config):
        """Comprehensive data cleaning with vectorized operations."""
        # Remove duplicates
        if config.get('remove_duplicates', True):
            initial_rows = len(df)
            df = df.drop_duplicates()
            self.logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Handle missing values
        missing_strategy = config.get('missing_strategy', 'drop')
        if missing_strategy == 'drop':
            df = df.dropna()
        elif missing_strategy == 'fill':
            fill_values = config.get('fill_values', {})
            df = df.fillna(fill_values)
        
        # Data type optimization
        df = self._optimize_dtypes(df)
        
        return df
    
    def _optimize_dtypes(self, df):
        """Optimize data types for memory efficiency."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to category if low cardinality
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'int64':
                # Downcast integers
                df[col] = pd.to_numeric(df[col], downcast='integer')
            elif df[col].dtype == 'float64':
                # Downcast floats
                df[col] = pd.to_numeric(df[col], downcast='float')
        
        return df
```
    def load_data(self, df, destination_config):
        """Load data to destination with batch optimization."""
        dest_type = destination_config['type']
        
        if dest_type == 'csv':
            self._load_to_csv(df, destination_config)
        elif dest_type == 'database':
            self._load_to_database(df, destination_config)
        elif dest_type == 'parquet':
            self._load_to_parquet(df, destination_config)
        
        self.logger.info(f"Successfully loaded {len(df)} rows to {dest_type}")
    
    def _load_to_parquet(self, df, config):
        """Load to Parquet with compression and partitioning."""
        output_path = config['path']
        partition_cols = config.get('partition_cols', None)
        
        df.to_parquet(
            output_path,
            partition_cols=partition_cols,
            compression='snappy',
            index=False
        )

### Data Quality Framework
class DataQualityValidator:
    """Comprehensive data quality validation system."""
    
    def __init__(self):
        self.validation_rules = []
        self.quality_report = {}
    
    def add_rule(self, rule_name, validation_func, severity='error'):
        """Add custom validation rule."""
        self.validation_rules.append({
            'name': rule_name,
            'func': validation_func,
            'severity': severity
        })
    
    def validate_dataset(self, df):
        """Run all validation rules and generate quality report."""
        self.quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'validation_results': [],
            'overall_score': 0
        }
        
        passed_rules = 0
        
        for rule in self.validation_rules:
            try:
                result = rule['func'](df)
                self.quality_report['validation_results'].append({
                    'rule': rule['name'],
                    'passed': result['passed'],
                    'message': result['message'],
                    'severity': rule['severity'],
                    'details': result.get('details', {})
                })
                
                if result['passed']:
                    passed_rules += 1
                    
            except Exception as e:
                self.quality_report['validation_results'].append({
                    'rule': rule['name'],
                    'passed': False,
                    'message': f"Validation error: {str(e)}",
                    'severity': 'error'
                })
        
        # Calculate overall quality score
        if self.validation_rules:
            self.quality_report['overall_score'] = passed_rules / len(self.validation_rules)
        
        return self.quality_report
    
    def generate_quality_report(self):
        """Generate detailed quality report."""
        report = f"""
        DATA QUALITY REPORT
        ==================
        Dataset Size: {self.quality_report['total_rows']:,} rows × {self.quality_report['total_columns']} columns
        Overall Quality Score: {self.quality_report['overall_score']:.2%}
        
        Validation Results:
        """
        
        for result in self.quality_report['validation_results']:
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            report += f"  {status} {result['rule']}: {result['message']}\n"
        
        return report

# Example validation rules
def validate_no_nulls(df):
    """Validate that critical columns have no null values."""
    critical_columns = ['id', 'timestamp', 'amount']
    null_counts = df[critical_columns].isnull().sum()
    
    if null_counts.sum() == 0:
        return {'passed': True, 'message': 'No null values in critical columns'}
    else:
        return {
            'passed': False, 
            'message': f'Found null values in critical columns',
            'details': null_counts.to_dict()
        }

def validate_data_types(df):
    """Validate expected data types."""
    expected_types = {
        'id': 'int64',
        'amount': 'float64',
        'category': 'object'
    }
    
    type_mismatches = []
    for col, expected_type in expected_types.items():
        if col in df.columns and str(df[col].dtype) != expected_type:
            type_mismatches.append(f"{col}: expected {expected_type}, got {df[col].dtype}")
    
    if not type_mismatches:
        return {'passed': True, 'message': 'All data types match expectations'}
    else:
        return {
            'passed': False,
            'message': 'Data type mismatches found',
            'details': type_mismatches
        }