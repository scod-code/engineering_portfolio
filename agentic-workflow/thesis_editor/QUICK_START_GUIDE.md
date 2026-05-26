# Quick Start Guide: Academic Thesis Editor

## 🎯 **What This Tool Does**

This is a **focused tool** for editing your MSc thesis (COMP40321 Research Methods submission). It specifically addresses:

1. **Punctuation fixes** - Em-dashes, semicolons, spacing
2. **AI-tone removal** - Makes text sound more human/academic
3. **Section-by-section editing** - You approve each change
4. **Superhumanizer AI integration** - Optional AI-powered humanization

---

## 🚀 **How to Use - 3 Simple Steps**

### **Step 1: Prepare Your Document**
1. Save your thesis as a **.txt or .md file** (Word → Save As → Plain Text)
2. Place it in this folder
3. Note the filename (e.g., `thesis.txt`)

### **Step 2: Run the Editor**
```cmd
thesis_editor.bat
```

Or directly with Python:
```cmd
python academic_editor.py
```

### **Step 3: Follow the Menu**
The editor will show you a menu:
```
1. Fix em-dashes
2. Fix semicolons  
3. Humanize specific section
4. Humanize entire document
5. Show changes summary
6. Save and exit
7. Exit without saving
```

---

## 🎯 **Your Specific Editing Tasks**

### **Task 1: Fix Em-dashes**
**What it does**: Replaces `—` with appropriate punctuation (`:` or `,`)

**Example**:
```
Before: The system—which uses reinforcement learning—will adapt.
After:  The system, which uses reinforcement learning, will adapt.
```

**How to use**: Select option `1` from menu

---

### **Task 2: Fix Semicolon Overuse**
**What it does**: Breaks long semicolon chains into separate sentences

**Example**:
```
Before: The system learns from data; it adapts to students; it improves over time.
After:  The system learns from data. It adapts to students. It improves over time.
```

**How to use**: Select option `2` from menu

---

### **Task 3: Humanize Specific Section**
**What it does**: Removes AI-generated phrases from a section you choose

**Example**:
```
Before: It is important to note that this study aims to leverage...
After:  This study uses...
```

**How to use**: 
1. Select option `3`
2. Choose a section (e.g., "2.2 Objectives")
3. Enter Superhumanizer API key (optional)
4. Review changes before applying

---

### **Task 4: Use Superhumanizer AI**
**What it does**: Uses https://superhumanizer.ai/ to humanize text

**How to get API key**:
1. Go to https://superhumanizer.ai/
2. Sign up for an account
3. Get your API key
4. Enter it when prompted

**Cost**: Check their website for pricing (often free tier available)

---

## 📝 **Your Document Structure**

Based on your description, your thesis has:

```
1. Title: AdaptLearn - hyperheuristic-orchestrated intelligent tutoring system
2. Section 2.2: Objectives (already partially edited)
3. Section 4: Resources Required (already partially edited)
4. Other sections to edit
```

---

## 🔧 **How the Editor Works**

### **1. It Creates Backups**
```
thesis.txt → thesis.txt.backup_20250126_143022
```
- **Always keeps original safe**
- **Never overwrites your file**

### **2. It Shows You Changes**
For each change:
```
Found em-dash at position 1250:
  Context: ...system—which uses...
  Proposed replacement: ','
  Apply? (y/n)
```

### **3. It Logs Everything**
```
thesis.txt.edited_20250126_143022.changes.json
```
- **Lists every change made**
- **Shows before/after text**
- **Tracks who made what change**

---

## 🎯 **Your Editing Workflow**

### **Option A: Section-by-Section (Recommended)**
```
1. Run: thesis_editor.bat
2. Select: "3. Humanize specific section"
3. Choose: "2.2 Objectives"
4. Review changes → Approve
5. Choose: "4. Resources Required"
6. Review changes → Approve
7. Save when done
```

### **Option B: Fix Specific Issues**
```
1. Run: thesis_editor.bat  
2. Select: "1. Fix em-dashes"
3. Select: "2. Fix semicolons"
4. Save when done
```

### **Option C: Full AI Humanization**
```
1. Get Superhumanizer API key
2. Run: thesis_editor.bat
3. Select: "4. Humanize entire document"
4. Enter API key
5. Review all changes
6. Save when done
```

---

## 📁 **Files Created**

After editing, you'll have:
```
thesis.txt                    (your original - UNCHANGED)
thesis.txt.backup_TIMESTAMP   (exact copy of original)
thesis.txt.edited_TIMESTAMP   (your edited version)
thesis.txt.changes.json       (list of all changes made)
```

---

## 💡 **Tips for Your Thesis**

### **Common Issues to Fix:**
1. **Em-dashes**: Replace with colons or commas
2. **Semicolon chains**: Break into separate sentences
3. **AI phrases**: Remove "leveraging", "harnessing", "utilizing"
4. **Redundancies**: "computational compute" → "computational resources"
5. **Typos**: "fort weekly" → "fortnightly"
6. **Ranges**: Use en-dash: "weeks 1–8" not "weeks 1-8"

### **Academic Tone:**
- **Use active voice**: "This study examines" not "It was examined"
- **Be specific**: "The system adapts" not "The system will adapt"
- **Avoid jargon**: "Using" not "leveraging"
- **Clear structure**: Short sentences, logical flow

---

## 🆘 **Troubleshooting**

### **"File not found"**
- Make sure file is in same folder as `academic_editor.py`
- Check filename spelling
- Use full path: `C:\Users\...\thesis.txt`

### **"No sections found"**
- Your document needs section headers like:
  - `2.2 Objectives`
  - `## Resources Required`
  - `4. METHODOLOGY`

### **"Superhumanizer API failed"**
- Check internet connection
- Verify API key is correct
- Use local humanization (option 3 without API key)

### **"Changes not saving"**
- Make sure to select "6. Save and exit"
- Check you have write permissions
- Look for `*.edited_*` files

---

## ✅ **Before You Submit**

### **Final Checklist:**
1. [ ] All em-dashes fixed
2. [ ] Semicolon chains broken up
3. [ ] AI-generated phrases removed
4. [ ] Typos corrected ("fortnightly")
5. [ ] Week ranges use en-dash (Weeks 1–8)
6. [ ] Read entire document aloud
7. [ ] Check with supervisor (Dr Jordan Bird)

### **Quality Check:**
- Does it sound like **you** wrote it?
- Is the **academic tone** maintained?
- Are **technical terms** used correctly?
- Is the **structure** logical?

---

## 🎓 **For Your Specific Thesis**

### **AdaptLearn Project Terms:**
- **Hyperheuristic-orchestrated**: Keep this term
- **Multimodal learner perception**: Keep this term  
- **Continual reinforcement learning**: Keep this term
- **Intelligent tutoring system**: Keep this term

### **What to Humanize:**
- **Remove**: "leveraging", "harnessing", "utilizing"
- **Simplify**: "computational compute" → "resources"
- **Clarify**: "n = 100" → "100 samples"
- **Fix**: "access to an institution" → "institutional support"

---

## 📚 **Example Editing Session**

```
C:\> thesis_editor.bat
Enter path to your document: thesis.txt

🔍 Analyzing document...
  • Em-dashes: 15 found
  • Semicolons: 8 found
  • Sections: 12 found

📝 EDITING MENU
1. Fix em-dashes
2. Fix semicolons
3. Humanize specific section
...

Select: 1
Replace em-dashes with: :

Found em-dash at position 1250:
  Context: ...system—which uses...
  Proposed replacement: ','
  Apply? (y/n): y

✅ Replaced 15 em-dashes

Select: 3
Available sections:
  1. 2.2 Objectives
  2. 4. Resources Required
  ...

Enter section number: 1
Superhumanizer API key: [your-key]

📝 Original: It is important to note that this study aims to...
📝 Humanized: This study examines...
Apply? (y/n): y

✅ Section humanized

Select: 6
Save as: thesis_final.txt

💾 Saved: thesis_final.txt
📋 Changes log: thesis_final.txt.changes.json
```

---

## 🎯 **Start Now**

1. **Save your thesis as .txt**
2. **Run `thesis_editor.bat`**
3. **Start with section 2.2 (Objectives)**
4. **Review each change carefully**
5. **Save when satisfied**

This tool gives you **control** while doing the **tedious work** of punctuation and tone fixes. You focus on **content**, let the tool handle **formatting**.

Good luck with your MSc submission! 🎓