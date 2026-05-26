#!/usr/bin/env python3
"""
Demonstration of the integrated orchestration system.
Shows how n8n, Prefect, and Makefile work together.
"""

import subprocess
import time
import json
from pathlib import Path
import requests
from datetime import datetime


def check_docker_services():
    """Check if Docker services are running."""
    print("🔍 Checking Docker services...")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            check=True
        )
        
        services = []
        for line in result.stdout.split('\n')[2:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    service = {
                        "name": parts[0],
                        "status": parts[3],
                        "ports": " ".join(parts[5:]) if len(parts) > 5 else ""
                    }
                    services.append(service)
        
        print(f"Found {len(services)} services:")
        for service in services:
            status_icon = "✅" if "Up" in service["status"] else "❌"
            print(f"  {status_icon} {service['name']}: {service['status']}")
        
        return services
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking Docker services: {e}")
        return []


def test_n8n_connection():
    """Test connection to n8n."""
    print("\n🔗 Testing n8n connection...")
    
    try:
        response = requests.get("http://localhost:5678/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ n8n is accessible at http://localhost:5678")
            print(f"   Default credentials: admin / password123")
            return True
        else:
            print(f"❌ n8n returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n. Make sure it's running with 'make start'")
        return False
    except Exception as e:
        print(f"❌ Error testing n8n: {e}")
        return False


def test_prefect_connection():
    """Test connection to Prefect."""
    print("\n🔗 Testing Prefect connection...")
    
    try:
        response = requests.get("http://localhost:4200/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Prefect is accessible at http://localhost:4200")
            return True
        else:
            print(f"❌ Prefect returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Prefect. Make sure it's running with 'make start'")
        return False
    except Exception as e:
        print(f"❌ Error testing Prefect: {e}")
        return False


def run_make_command(command):
    """Run a make command and return output."""
    try:
        result = subprocess.run(
            ["make", command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


def demonstrate_pipelines():
    """Demonstrate running the example pipelines."""
    print("\n🚀 Demonstrating pipelines...")
    
    # Create output directories
    Path("output").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # 1. Data Pipeline
    print("\n1. Running Data Quality Pipeline...")
    data_output = run_make_command("data-pipeline")
    if "Pipeline completed successfully" in data_output:
        print("✅ Data pipeline completed")
        
        # Find output files
        output_files = list(Path("output").glob("*.csv"))
        if output_files:
            print(f"   Output files: {[f.name for f in output_files[:3]]}")
    else:
        print("❌ Data pipeline failed")
    
    # 2. ETL Pipeline
    print("\n2. Running ETL Pipeline...")
    etl_output = run_make_command("etl-pipeline")
    if "ETL Pipeline completed successfully" in etl_output:
        print("✅ ETL pipeline completed")
        
        # Check for reports
        report_files = list(Path("reports").glob("*.json"))
        if report_files:
            print(f"   Reports generated: {[f.name for f in report_files[:2]]}")
    else:
        print("❌ ETL pipeline failed")
    
    # 3. ML Pipeline
    print("\n3. Running ML Training Pipeline...")
    ml_output = run_make_command("ml-pipeline")
    if "ML training pipeline completed" in ml_output or "Pipeline completed successfully" in ml_output:
        print("✅ ML pipeline completed")
        
        # Check for model files
        model_files = list(Path("ml_pipeline_output").glob("*.json"))
        if model_files:
            print(f"   Model artifacts: {[f.name for f in model_files[:2]]}")
    else:
        print("❌ ML pipeline failed")


def show_system_summary():
    """Show summary of the orchestration system."""
    print("\n" + "="*60)
    print("🎯 LOCAL ORCHESTRATION SYSTEM SUMMARY")
    print("="*60)
    
    print("\n📊 Services Status:")
    services = check_docker_services()
    
    print("\n🔗 Access Points:")
    print("  • n8n:      http://localhost:5678")
    print("  • Prefect:  http://localhost:4200")
    
    print("\n🛠️ Available Commands:")
    print("  • make start          - Start all services")
    print("  • make stop           - Stop all services")
    print("  • make data-pipeline  - Run data quality pipeline")
    print("  • make ml-pipeline    - Run ML training pipeline")
    print("  • make etl-pipeline   - Run ETL pipeline")
    print("  • make logs           - View service logs")
    print("  • make test           - Run tests")
    
    print("\n📁 Project Structure:")
    project_files = [
        "docker-compose.yml",
        "Makefile",
        "requirements.txt",
        "prefect_flows/",
        "tests/",
        "README.md"
    ]
    
    for file in project_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
    
    print("\n🎯 Next Steps:")
    print("  1. Review the README.md for detailed instructions")
    print("  2. Explore n8n workflows at http://localhost:5678")
    print("  3. Check Prefect dashboard at http://localhost:4200")
    print("  4. Run 'make test' to verify everything works")
    print("  5. Create your own workflows in prefect_flows/")
    
    print("\n" + "="*60)
    print("✅ Setup complete! Happy automating! 🚀")
    print("="*60)


def main():
    """Main demonstration function."""
    print("🔧 Local Machine Orchestration System Demo")
    print("="*60)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    
    # Check Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✅ Docker is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not in PATH")
        print("   Please install Docker from: https://docs.docker.com/get-docker/")
        return
    
    # Check Docker Compose
    try:
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print("✅ Docker Compose is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker Compose is not installed")
        print("   Please install Docker Compose from: https://docs.docker.com/compose/install/")
        return
    
    # Check Python
    try:
        subprocess.run(["python", "--version"], capture_output=True, check=True)
        print("✅ Python is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Python is not installed")
        print("   Please install Python from: https://www.python.org/downloads/")
        return
    
    # Check services
    services_running = False
    services = check_docker_services()
    if services:
        running_services = [s for s in services if "Up" in s["status"]]
        if len(running_services) >= 2:  # At least n8n and Prefect
            services_running = True
    
    if not services_running:
        print("\n⚠️ Services are not running. Starting them now...")
        start_output = run_make_command("start")
        print(start_output)
        time.sleep(10)  # Give services time to start
    
    # Test connections
    n8n_ok = test_n8n_connection()
    prefect_ok = test_prefect_connection()
    
    if n8n_ok and prefect_ok:
        # Demonstrate pipelines
        demonstrate_pipelines()
        
        # Show summary
        show_system_summary()
    else:
        print("\n❌ Some services are not accessible.")
        print("   Try running 'make start' to start all services")
        print("   Then run this demo again")


if __name__ == "__main__":
    main()