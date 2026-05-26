# Instructions to Update scod-code Repository

Since I cannot directly edit the `scod-code/scod-code.git` repository, here are the instructions to update it:

## 🎯 What to Add

Add a new section to your `scod-code` repository README or portfolio page:

### **New Project: Agentic Workflow & Academic Tools**

**Location**: `engineering_portfolio/agentic-workflow/`

**Description**: A comprehensive collection of tools for academic writing automation and workflow orchestration, developed during my MSc in Robotics and Intelligent Systems.

**Components**:

1. **Thesis Editor** (`thesis_editor/`)
   - Fixes punctuation (em-dashes, semicolons)
   - Removes AI-generated tone
   - Humanizes text with Superhumanizer AI integration
   - Works paragraph-by-paragraph with approval
   - Preserves original files, creates backups

2. **Orchestration System** (`orchestration_system/`)
   - n8n: Visual workflow automation (like Zapier, but local)
   - Prefect: Python workflow orchestration with scheduling
   - Docker Compose: Easy service management
   - Example workflows: Data pipelines, ML training, ETL processes

**Use Cases**:
- Academic thesis editing (MSc research papers)
- Workflow automation for research projects
- ML pipeline scheduling and monitoring
- Data processing and ETL workflows

**Technical Skills Demonstrated**:
- Python development with python-docx
- Workflow orchestration (n8n, Prefect)
- Docker containerization
- API integration (Superhumanizer AI)
- Automation and scheduling

**Academic Context**:
- Developed for COMP40321 Research Methods submission
- Used for AdaptLearn project (hyperheuristic-orchestrated intelligent tutoring system)
- Supervised by Dr Jordan Bird at NTU

## 🔗 Links to Add

1. **Repository**: `https://github.com/scod-code/engineering_portfolio/tree/main/agentic-workflow`
2. **Thesis Editor**: `https://github.com/scod-code/engineering_portfolio/tree/main/agentic-workflow/thesis_editor`
3. **Orchestration System**: `https://github.com/scod-code/engineering_portfolio/tree/main/agentic-workflow/orchestration_system`

## 📝 Suggested README Update

Add this to your `scod-code` repository README:

```markdown
## 🚀 Recent Projects

### Agentic Workflow & Academic Tools
A comprehensive suite of tools for academic writing automation and workflow orchestration.

**Features**:
- Thesis editing with AI-tone removal
- Workflow automation with n8n and Prefect
- ML pipeline scheduling and monitoring
- Data processing workflows

**Repository**: [engineering_portfolio/agentic-workflow](https://github.com/scod-code/engineering_portfolio/tree/main/agentic-workflow)

**Technologies**: Python, n8n, Prefect, Docker, python-docx

**Context**: Developed during MSc in Robotics and Intelligent Systems at NTU for research paper editing and workflow automation.
```

## 🛠️ How to Update

1. Clone your `scod-code` repository:
   ```bash
   git clone https://github.com/scod-code/scod-code.git
   cd scod-code
   ```

2. Edit the README.md file to add the new project section.

3. Commit and push:
   ```bash
   git add README.md
   git commit -m "Add agentic-workflow project to portfolio"
   git push origin main
   ```

## 📊 Project Impact

This project demonstrates:
- **Practical application** of automation tools in academic research
- **Cross-disciplinary skills** combining software engineering with academic writing
- **Real-world problem solving** for common academic challenges
- **Professional tool development** with user-friendly interfaces

The tools have been **tested and used** for editing actual MSc thesis submissions, proving their practical utility in academic contexts.