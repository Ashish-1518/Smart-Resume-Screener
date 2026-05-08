# 📄 Smart Resume Screener

An AI-powered resume screening tool that ranks candidates based on job description relevance using **TF-IDF Vectorization** and **Cosine Similarity**.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57.0-red.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📝 **Job Description Input** | Paste text directly or upload .txt files |
| 📄 **Resume Upload** | Support for PDF, DOCX, and TXT formats |
| 🏆 **Smart Ranking** | Get match percentages for each candidate |
| 🔑 **Keyword Extraction** | Automatically identify key skills from job descriptions |
| 📊 **Visual Results** | Color-coded rankings with match categories |
| ✅ **Auto-Shortlisting** | Instantly highlights candidates above 50% match |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Interactive web framework |
| **scikit-learn** | TF-IDF vectorization & cosine similarity |
| **PyPDF2** | PDF text extraction |
| **python-docx** | DOCX text extraction |
| **pandas** | Data manipulation and analysis |

---

## 📊 How It Works

### The Algorithm Explained

1. **Text Extraction** - Extracts raw text from PDF, DOCX, and TXT files
2. **Preprocessing** - Converts to lowercase, removes special characters and stop words
3. **TF-IDF Vectorization** - Converts text documents into numerical feature vectors
4. **Cosine Similarity** - Calculates similarity between job description and each resume
5. **Ranking** - Sorts candidates by match percentage (0-100%)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### How to Use
Step 1: Enter Job Description
Option A: Paste text directly into the text area

Option B: Upload a .txt file containing the job description

Step 2: Upload Resumes
Upload one or more resume files (PDF, DOCX, or TXT)

Supports batch upload for multiple candidates

Step 3: Screen Resumes
Click "SCREEN RESUMES" button

View ranked results with match percentages

🎯 Use Cases
HR Departments - Screen hundreds of resumes quickly

Recruitment Agencies - Filter candidates before manual review

Job Seekers - Check resume strength against job descriptions

Career Services - Help students improve their resumes

👨‍💻 Author
Ashish

GitHub: @Ashish-1518

Project Link: Smart Resume Screener

⭐ Show Your Support
If you found this project helpful, please give it a ⭐ on GitHub!

Happy Screening! 🎯
