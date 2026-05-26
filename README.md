# Agentic Workflow & Academic Tools

A comprehensive collection of tools for academic writing automation and workflow orchestration.

## � Project Structure

```
.
├── thesis_editor/          # Academic thesis editing tools
├── orchestration_system/   # Local workflow automation (n8n + Prefect)
├── docs/                   # Documentation
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🎯 What's Included

### 1. **Thesis Editor** (`thesis_editor/`)
A specialized tool for editing academic theses and research papers.

**Features:**
- Fix punctuation (em-dashes, semicolons)
- Remove AI-generated tone
- Humanize text with Superhumanizer AI integration
- Work paragraph-by-paragraph with approval
- Preserves original files, creates backups

**Quick Start:**
```bash
cd thesis_editor
python thesis_editor.py
```

### 2. **Orchestration System** (`orchestration_system/`)
A complete local workflow automation system using n8n and Prefect.

**Components:**
- **n8n**: Visual workflow automation (like Zapier, but local)
- **Prefect**: Python workflow orchestration with scheduling
- **Docker Compose**: Easy service management
- **Example workflows**: Data pipelines, ML training, ETL processes

**Quick Start:**
```bash
cd orchestration_system
make start  # or .\start.ps1 on Windows
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/scod-code/engineering_portfolio.git
cd engineering_portfolio/agentic-workflow
```

2. **Set up Thesis Editor:**
```bash
cd thesis_editor
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Linux/Mac
pip install python-docx
```

3. **Set up Orchestration System:**
```bash
cd orchestration_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 Documentation

- **Thesis Editor Guide**: `thesis_editor/QUICK_START_GUIDE.md`
- **Orchestration Guide**: `orchestration_system/SIMPLE_GUIDE.md`
- **Full Documentation**: `docs/`

## 🛠️ Usage Examples

### Academic Thesis Editing
```python
# Edit your MSc thesis
cd thesis_editor
python thesis_editor.py
# Follow the interactive menu to fix em-dashes, week ranges, and AI phrases
```

### Workflow Automation
```bash
# Start all services
cd orchestration_system
.\start.ps1  # Windows
# or make start  # Linux/Mac

# Access dashboards:
# - n8n: http://localhost:5678 (admin/password123)
# - Prefect: http://localhost:4200
```

### Run Example Pipelines
```bash
cd orchestration_system
.\run-pipeline.ps1 -Pipeline data  # Data quality pipeline
.\run-pipeline.ps1 -Pipeline ml    # ML training pipeline
.\run-pipeline.ps1 -Pipeline etl   # ETL pipeline
```

## 🎓 Use Cases

### For Students & Researchers
- **Thesis editing**: Fix formatting, remove AI tone, improve readability
- **Report generation**: Automate weekly/monthly academic reports
- **Data analysis**: Process research data with automated pipelines

### For Developers & Engineers
- **Local automation**: Schedule tasks, connect APIs, process data
- **ML workflows**: Train, evaluate, and deploy models locally
- **Data pipelines**: Extract, transform, and load data automatically

## � Technical Details

### Thesis Editor
- **Language**: Python
- **Dependencies**: python-docx
- **Input**: .docx files (Microsoft Word)
- **Output**: Edited .docx with change log

### Orchestration System
- **Services**: n8n, Prefect, PostgreSQL
- **Orchestration**: Docker Compose
- **Workflows**: Python + Prefect flows
- **Monitoring**: Web dashboards for both n8n and Prefect

## 📄 License

This project is provided as-is for educational and practical use.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the documentation in `docs/`
- Review the guides in each subdirectory
- Open an issue on GitHub

---

**Happy automating and writing!** 🎓🚀