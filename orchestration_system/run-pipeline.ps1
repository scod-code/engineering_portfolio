# PowerShell script to run example pipelines
# Equivalent to 'make data-pipeline', 'make ml-pipeline', etc.

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("data", "ml", "etl", "all")]
    [string]$Pipeline = "data"
)

Write-Host "🚀 Running $Pipeline pipeline..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan

# Check if virtual environment is activated
$venvPath = "venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    $pythonExe = $venvPath
    Write-Host "✅ Using virtual environment Python" -ForegroundColor Green
} else {
    $pythonExe = "python"
    Write-Host "⚠️  Using system Python (virtual environment not found)" -ForegroundColor Yellow
}

# Create output directories
$directories = @("output", "data", "models", "reports", "ml_pipeline_output", "etl_output")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Created directory: $dir" -ForegroundColor Cyan
    }
}

# Run selected pipeline
switch ($Pipeline) {
    "data" {
        Write-Host "`n📊 Running Data Quality Pipeline..." -ForegroundColor Cyan
        & $pythonExe prefect_flows/data_pipeline.py
    }
    "ml" {
        Write-Host "`n🤖 Running ML Training Pipeline..." -ForegroundColor Cyan
        & $pythonExe prefect_flows/ml_pipeline.py
    }
    "etl" {
        Write-Host "`n🔄 Running ETL Pipeline..." -ForegroundColor Cyan
        & $pythonExe prefect_flows/etl_pipeline.py
    }
    "all" {
        Write-Host "`n🎯 Running all pipelines..." -ForegroundColor Cyan
        
        Write-Host "`n1. Data Quality Pipeline:" -ForegroundColor Yellow
        & $pythonExe prefect_flows/data_pipeline.py
        
        Write-Host "`n2. ML Training Pipeline:" -ForegroundColor Yellow
        & $pythonExe prefect_flows/ml_pipeline.py
        
        Write-Host "`n3. ETL Pipeline:" -ForegroundColor Yellow
        & $pythonExe prefect_flows/etl_pipeline.py
    }
}

Write-Host "`n✅ Pipeline execution completed!" -ForegroundColor Green
Write-Host "`n📁 Check output in these directories:" -ForegroundColor Cyan
Write-Host "   • output/ - Data pipeline results" -ForegroundColor White
Write-Host "   • ml_pipeline_output/ - ML model artifacts" -ForegroundColor White
Write-Host "   • etl_output/ - ETL processed data" -ForegroundColor White
Write-Host "   • reports/ - Generated reports" -ForegroundColor White

Write-Host "`n💡 Run other pipelines:" -ForegroundColor Cyan
Write-Host "   .\run-pipeline.ps1 -Pipeline ml    # Run ML pipeline" -ForegroundColor White
Write-Host "   .\run-pipeline.ps1 -Pipeline etl   # Run ETL pipeline" -ForegroundColor White
Write-Host "   .\run-pipeline.ps1 -Pipeline all   # Run all pipelines" -ForegroundColor White