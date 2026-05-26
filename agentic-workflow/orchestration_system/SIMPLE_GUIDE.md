# Simple Guide to Your Local Orchestration System

## 🎯 **What Is This System?**

Think of it as your **personal automation assistant** that can:
- **Run tasks automatically** (like a smart scheduler)
- **Process data** (clean, transform, analyze)
- **Create documents** (Word, reports, summaries)
- **Send notifications** (alerts, updates)
- **Connect different tools** (APIs, databases, files)

---

## 🏠 **The 3 Tools - Simple Explanation**

### **1. n8n - The Visual Builder**
**What it is**: A drag-and-drop automation tool (like Zapier, but free and on your computer)

**When to use it**:
- You want to click buttons to create workflows
- You need simple triggers (email, webhook, timer)
- You want to connect apps without coding
- You prefer visual over code

**Example use**:
```
"When I receive an email → save attachment → run a script → send me a notification"
```

---

### **2. Prefect - The Code-Based Automation**
**What it is**: A Python library that runs and monitors your scripts

**When to use it**:
- You need complex data processing
- You want to chain multiple steps together
- You need error handling and retries
- You want to monitor progress in a dashboard
- You're comfortable with Python code

**Example use**:
```
"Extract data from API → Clean it → Generate report → Save to file"
```

---

### **3. Makefile/Batch - The Task Runner**
**What it is**: One command that runs multiple commands

**When to use it**:
- You want to run several steps with one command
- You need simple development automation
- You want to standardize commands across your team

**Example use**:
```
"make start" → Starts all services
"make test" → Runs all tests
```

---

## 🔄 **How They Work Together**

```
You run a command (like "run-pipeline.ps1")
         ↓
Prefect executes Python scripts
         ↓
Scripts process data, create documents, etc.
         ↓
n8n can trigger workflows or send notifications
         ↓
Everything shows up in dashboards for monitoring
```

---

## 📝 **Practical Word Document Automation**

### **Scenario 1: Create a Weekly Report Automatically**

**What you want**:
Every Friday, automatically generate a Word document with:
- This week's tasks completed
- Current project status
- Next week's goals

**How to do it**:

**Step 1**: Run the Word automation script
```powershell
# PowerShell
.\run-pipeline.ps1 -Pipeline word
```

**Step 2**: Or run directly with Python
```powershell
.\venv\Scripts\Activate.ps1
python prefect_flows/word_automation.py
```

**What happens**:
- Script creates a Word document
- Adds formatted sections (Tasks, Status, Goals)
- Saves it to `output/weekly_report_*.docx`

---

### **Scenario 2: Update an Existing Document**

**What you want**:
Automatically update a "Status Report" document with new data every day

**How to do it**:
```python
# In your Python script
from prefect_flows.word_automation import update_word_document

# Update a specific section
update_word_document(
    filename="reports/Status_Report.docx",
    section="Current Status",
    new_content="Project is 75% complete. On track for deadline."
)
```

---

### **Scenario 3: Generate Multiple Documents from Data**

**What you want**:
Take data from Excel/CSV and create individual Word documents for each entry

**Example**:
```python
# Read data from file
data = [
    {"name": "John", "report": "Excellent performance this quarter"},
    {"name": "Jane", "report": "Met all targets, needs improvement in communication"},
    {"name": "Bob", "report": "Outstanding results, promoted to senior role"}
]

# Create a document for each person
for person in data:
    create_word_document(
        filename=f"reports/{person['name']}_report.docx",
        content=f"""
        Employee: {person['name']}
        
        Performance Review:
        {person['report']}
        
        Date: {datetime.now().strftime('%Y-%m-%d')}
        """
    )
```

---

### **Scenario 4: Merge Multiple Documents**

**What you want**:
Combine several Word documents into one master document

**Example**:
```python
merge_documents(
    sources=[
        "reports/January_Report.docx",
        "reports/February_Report.docx", 
        "reports/March_Report.docx"
    ],
    output="reports/Q1_Combined_Report.docx"
)
```

---

### **Scenario 5: Add Tables to Documents**

**What you want**:
Create a Word document with a formatted table of data

**Example**:
```python
add_table_to_document(
    filename="reports/Project_Status.docx",
    headers=["Task", "Status", "Owner", "Due Date"],
    data=[
        ["Design Review", "Complete", "Alice", "2024-01-15"],
        ["Development", "In Progress", "Bob", "2024-01-20"],
        ["Testing", "Pending", "Charlie", "2024-01-25"],
        ["Deployment", "Pending", "Dave", "2024-02-01"]
    ]
)
```

---

## 🎯 **When to Use What - Quick Reference**

| Task | Tool | Example |
|------|------|---------|
| **Simple document creation** | Prefect + Python | "Create a report from template" |
| **Update existing document** | Prefect + Python | "Replace section X with new content" |
| **Create table in Word** | Prefect + Python | "Add data table to document" |
| **Merge documents** | Prefect + Python | "Combine multiple reports" |
| **Schedule daily reports** | Prefect + n8n | "Every morning at 9 AM, generate report" |
| **Send email with document** | n8n | "When report created → send email with attachment" |
| **Trigger from webhook** | n8n | "When API called → create document" |
| **Multiple steps in sequence** | Prefect | "Extract → Transform → Create Document → Save → Notify" |
| **One command to do everything** | Makefile/Batch | "make generate-reports" |

---

## 🚀 **How to Get Started - Step by Step**

### **Step 1: Start the System**
```powershell
# PowerShell
.\start.ps1
```

This starts:
- n8n dashboard (http://localhost:5678)
- Prefect dashboard (http://localhost:4200)

---

### **Step 2: Set Up Python**
```powershell
.\setup.ps1
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### **Step 3: Install Word Support**
```powershell
pip install python-docx
```

This library lets Python create and edit Word documents.

---

### **Step 4: Run Your First Word Automation**
```powershell
python prefect_flows/word_automation.py
```

This creates sample documents in the `output` folder.

---

### **Step 5: Customize for Your Needs**

Edit `prefect_flows/word_automation.py` to:
- Change the report format
- Add your own templates
- Connect to your data sources
- Modify the content structure

---

## 📁 **File Structure - What Each Does**

```
prefect_flows/
├── word_automation.py    # Word document creation/editing
├── example_flows.py      # Basic examples (ETL, ML, etc.)
├── data_pipeline.py      # Data quality monitoring
├── ml_pipeline.py        # Machine learning workflows
└── etl_pipeline.py       # Data extraction & transformation

output/                   # Where documents are saved
reports/                  # Generated reports go here
```

---

## 💡 **Simple Workflow Examples**

### **Example A: Daily Status Report**
```
Every morning at 8 AM:
1. Prefect runs word_automation.py
2. Script creates "Daily_Status_YYYY-MM-DD.docx"
3. Document contains:
   - Yesterday's accomplishments
   - Today's priorities
   - Blockers/risks
4. Saves to reports/ folder
5. n8n sends email with document attached
```

### **Example B: Weekly Performance Summary**
```
Every Friday at 5 PM:
1. Prefect extracts data from database
2. Calculates metrics (tasks completed, etc.)
3. Generates Word document with charts/tables
4. Saves as "Weekly_Performance_YYYY-WW.docx"
5. Uploads to shared folder
6. n8n notifies team on Slack
```

### **Example C: On-Demand Document Generation**
```
When manager requests a report:
1. Manager clicks button in n8n dashboard
2. n8n triggers Prefect workflow
3. Prefect creates document with latest data
4. Document sent back to n8n
5. n8n emails document to manager
```

---

## 🔧 **Customization - Change the Content**

To customize what goes in your Word documents, edit `word_automation.py`:

```python
# Find this section and change it:
content = f"""
Weekly Progress Report
======================

Date: {datetime.now().strftime('%Y-%m-%d')}

# CHANGE THIS SECTION TO YOUR NEEDS
Tasks Completed: {data.get('tasks_completed', 0)}
Tasks In Progress: {data.get('tasks_in_progress', 0)}
Pending Tasks: {data.get('pending_tasks', 0)}

Highlights:
{data.get('highlights', 'No highlights this week.')}

Challenges:
{data.get('challenges', 'No challenges reported.')}

Next Week's Goals:
{data.get('next_goals', 'Continue current progress.')}
"""
```

---

## 🎓 **Learning Path**

### **Beginner (Start Here)**
1. Run `python prefect_flows/word_automation.py`
2. Check the `output` folder for created documents
3. Open a .docx file in Microsoft Word
4. Modify the content in the Python script
5. Run again and see changes

### **Intermediate**
1. Add your own sections to the report
2. Connect to real data (Excel, CSV, database)
3. Add formatting (bold, colors, tables)
4. Schedule automatic generation

### **Advanced**
1. Create n8n workflows to trigger document creation
2. Add email/Slack notifications
3. Connect to external APIs
4. Build complex multi-step pipelines

---

## ❓ **Common Questions**

**Q: Do I need to know Python?**
A: Basic Python helps, but you can start by just running the scripts. The examples are designed to be "copy-paste-run".

**Q: Can I use this with existing Word templates?**
A: Yes! You can modify the script to load existing .docx files and update specific sections.

**Q: How do I schedule automatic generation?**
A: Use Prefect's scheduling features or n8n's cron triggers.

**Q: Can I create PDFs instead?**
A: Yes, install `python-docx` and use additional libraries like `pdf2docx` or `weasyprint`.

**Q: How do I stop the services?**
A: Run `.\stop.ps1` in PowerShell or `stop.bat` in Command Prompt.

---

## 📚 **Next Steps**

1. **Try it now**: Run `python prefect_flows/word_automation.py`
2. **Check output**: Look in the `output` folder for created documents
3. **Open in Word**: Double-click a .docx file to see the result
4. **Modify it**: Change some text in the Python script
5. **Run again**: See your changes reflected in the new document

---

## 🆘 **Troubleshooting**

**"python-docx not installed"**
```powershell
pip install python-docx
```

**"No module named prefect"**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**"File not found"**
- Make sure you're in the right directory
- Check that the `output` folder exists
- Verify the filename path is correct

**"Permission denied"**
- Close the Word document if it's open
- Make sure you have write permissions to the folder

---

## ✅ **Summary**

- **n8n**: Visual automation (drag & drop)
- **Prefect**: Code-based automation (Python scripts)
- **Makefile/Batch**: Task runner (one command, many steps)
- **Word Automation**: Use `prefect_flows/word_automation.py`
- **Start**: `.\start.ps1`
- **Run**: `python prefect_flows/word_automation.py`
- **Output**: Check the `output` folder

Start simple, experiment, and gradually add more complexity as you get comfortable!