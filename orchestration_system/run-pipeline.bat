@echo off
echo 🚀 Running Local Orchestration Pipelines
echo ========================================

REM Check for pipeline argument
if "%1"=="" (
    echo Usage: %~n0 [data^|ml^|etl^|all]
    echo.
    echo Examples:
    echo   %~n0 data    - Run data quality pipeline
    echo   %~n0 ml      - Run ML training pipeline
    echo   %~n0 etl     - Run ETL pipeline
    echo   %~n0 all     - Run all pipelines
    pause
    exit /b 1
)

set PIPELINE=%1

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️  Virtual environment not activated
    echo    Attempting to activate...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ Could not activate virtual environment
        echo    Please activate manually: venv\Scripts\activate.bat
        pause
        exit /b 1
    )
    echo ✅ Virtual environment activated
)

REM Create output directories
set DIRECTORIES=output data models reports ml_pipeline_output etl_output
for %%d in (%DIRECTORIES%) do (
    if not exist "%%d" (
        mkdir "%%d" >nul 2>&1
        echo 📁 Created directory: %%d
    )
)

REM Run selected pipeline
if "%PIPELINE%"=="data" (
    echo.
    echo 📊 Running Data Quality Pipeline...
    python prefect_flows/data_pipeline.py
) else if "%PIPELINE%"=="ml" (
    echo.
    echo 🤖 Running ML Training Pipeline...
    python prefect_flows/ml_pipeline.py
) else if "%PIPELINE%"=="etl" (
    echo.
    echo 🔄 Running ETL Pipeline...
    python prefect_flows/etl_pipeline.py
) else if "%PIPELINE%"=="all" (
    echo.
    echo 🎯 Running all pipelines...
    
    echo.
    echo 1. Data Quality Pipeline:
    python prefect_flows/data_pipeline.py
    
    echo.
    echo 2. ML Training Pipeline:
    python prefect_flows/ml_pipeline.py
    
    echo.
    echo 3. ETL Pipeline:
    python prefect_flows/etl_pipeline.py
) else (
    echo ❌ Invalid pipeline: %PIPELINE%
    echo    Valid options: data, ml, etl, all
    pause
    exit /b 1
)

echo.
echo ✅ Pipeline execution completed!
echo.
echo 📁 Check output in these directories:
echo    • output\ - Data pipeline results
echo    • ml_pipeline_output\ - ML model artifacts
echo    • etl_output\ - ETL processed data
echo    • reports\ - Generated reports
echo.
echo 💡 Run other pipelines:
echo    %~n0 ml    - Run ML pipeline
echo    %~n0 etl   - Run ETL pipeline
echo    %~n0 all   - Run all pipelines
pause