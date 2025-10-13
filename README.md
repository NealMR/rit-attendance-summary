# 🧾 RIT Attendance Summary Generator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Selenium](https://img.shields.io/badge/Automation-Selenium-brightgreen?logo=selenium)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

---

### 📚 Overview

**RIT Attendance Summary Generator** is a **Python + Selenium** automation tool that logs into the **RIT CMS portal**, fetches your subject-wise attendance, calculates percentages, and generates a clean **CSV summary file** — all automatically.

---

## 🚀 Features

✅ Auto-detects working RIT CMS URL  
✅ Secure login with up to 3 attempts  
✅ Scrapes complete attendance details per subject  
✅ Calculates:
- Total classes
- Attendance %
- Classes needed to reach 75%  
✅ Exports to `attendance_summary.csv`  
✅ Displays overall and per-subject analysis in the console  

---

## 🧠 How It Works

1. Connects automatically to the correct RIT CMS URL.  
2. Logs in securely with your credentials.  
3. Navigates to the attendance dashboard.  
4. Scrapes all subjects’ attendance using **Selenium**.  
5. Parses data using **BeautifulSoup** and **Pandas**.  
6. Exports a CSV summary to your current directory.

---

## 🧩 Requirements

Install dependencies:

```bash
pip install selenium pandas beautifulsoup4
Also required:

Google Chrome

ChromeDriver (compatible with your Chrome version)
🔗 Download here

⚙️ Setup & Run
Clone the repository

bash
Copy code
git clone https://github.com/yourusername/rit-attendance-summary.git
cd rit-attendance-summary
Run the script

bash
Copy code
python attendance_summary.py
Follow the prompts

Enter your User ID and Password

Wait for data extraction

Find your summary in attendance_summary.csv

📂 Output Example
Generated file: attendance_summary.csv

Subject	SubjectCode	TotalClasses	Present	Absent	AttendancePercentage	LatestAttendanceDate	ClassesNeededFor75
Data Structures	CS201	42	36	6	85.71	12/10/2025	0
DBMS	CS202	40	26	14	65.00	10/10/2025	5

🧑‍💻 Technologies Used
🐍 Python 3

🧭 Selenium WebDriver

📊 Pandas

🧠 BeautifulSoup

🌐 ChromeDriver

⚠️ Important Notes
Use this tool only for personal/educational purposes.

Do not share credentials or spam the RIT server.

Ensure a stable internet connection.

Tested on Windows 10 with Python 3.11 + Chrome 128.

🏁 Example Console Output
markdown
Copy code
============================================================
RIT ATTENDANCE SUMMARY GENERATOR
============================================================

🔌 Connecting to RIT CMS...
📡 Attempting 1/3: 210.212.171.172 ✅

🔐 LOGIN ATTEMPT 1/3
📝 Entering credentials... ⏳ Verifying...
✅ Login successful!

📊 Opening Attendance Dashboard...
🤖 Extracting attendance data...
✓ Found 5 subjects

✅ SUMMARY GENERATED!
📈 Overall Attendance: 78.45%
✅ Great! You're above 75%

📄 File saved: attendance_summary.csv
👨‍🎓 Author
Neal Rankhambe
📍 B.Tech | RIT India
💻 Passionate about automation, AI, and productivity tools



🪪 License
This project is licensed under the MIT License — feel free to use, modify, and distribute with attribution.

⭐ If you like this project, don’t forget to star the repo and share it with your friends!