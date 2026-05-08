import streamlit as st
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from docx import Document
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart Resume Screener")
st.markdown("*AI-powered resume screening using TF-IDF and Cosine Similarity*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎯 How It Works")
    st.markdown("""
    1. **Paste or upload** a job description
    2. **Upload resumes** (PDF, DOCX, or TXT)
    3. **Click Screen** to get ranked results
    
    The app uses **TF-IDF Vectorization** and **Cosine Similarity** to match resumes with job descriptions.
    
    ### Match Categories:
    - 🏆 **70-100%** : Strong Match
    - 📌 **50-69%** : Good Match  
    - ⚠️ **30-49%** : Consider
    - ❌ **0-29%** : Low Match
    """)
    
    st.divider()
    st.caption("Made with ❤️ using Streamlit & scikit-learn")
    st.caption("No APIs needed - 100% free & local")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    text = ""
    try:
        doc = Document(docx_file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
    return text

# Function to extract text from TXT
def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode('utf-8')
    except:
        try:
            return txt_file.read().decode('latin-1')
        except:
            return ""

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to extract keywords
def extract_keywords(text, top_n=10):
    from collections import Counter
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stop_words = {'the', 'and', 'for', 'that', 'this', 'with', 'are', 'was', 'were', 'from', 'have', 'has', 'had', 'but', 'not', 'you', 'your', 'our', 'their', 'will', 'can', 'all', 'about', 'what', 'when', 'where', 'who', 'which', 'why', 'how', 'experience', 'skills', 'years', 'ability', 'strong', 'using', 'including', 'such', 'like', 'well', 'working', 'knowledge', 'proven', 'demonstrated'}
    words = [w for w in words if w not in stop_words]
    return Counter(words).most_common(top_n)

# Calculate match scores
def calculate_match_scores(job_description, resumes_text):
    job_cleaned = preprocess_text(job_description)
    resumes_cleaned = [preprocess_text(resume) for resume in resumes_text if resume]
    
    if not resumes_cleaned:
        return []
    
    all_texts = [job_cleaned] + resumes_cleaned
    
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=1000
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        job_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        similarity_scores = cosine_similarity(job_vector, resume_vectors).flatten()
        percentages = similarity_scores * 100
        return percentages
    except:
        return []

# Main content - Two columns
col1, col2 = st.columns(2, gap="large")

# COLUMN 1: Job Description
with col1:
    st.subheader("📌 Job Description")
    
    job_input_method = st.radio(
        "Choose input method:",
        ["✏️ Paste Text", "📁 Upload File"],
        horizontal=True
    )
    
    job_description = ""
    
    if job_input_method == "✏️ Paste Text":
        job_description = st.text_area(
            "Paste the job description here:",
            height=400,
            placeholder="""Example:
We are looking for a Python Developer with 2+ years of experience.
Required Skills: Python, Django, SQL, Git, REST APIs
Good to have: Flask, Docker, AWS
Responsibilities: Build scalable web applications, write clean code"""
        )
    else:
        uploaded_job = st.file_uploader(
            "Upload Job Description (TXT file)",
            type=['txt']
        )
        if uploaded_job:
            job_description = uploaded_job.read().decode('utf-8')
            st.success("✅ Job description loaded!")

# COLUMN 2: Resumes
with col2:
    st.subheader("📄 Candidate Resumes")
    
    uploaded_resumes = st.file_uploader(
        "Upload resumes (PDF, DOCX, or TXT)",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_resumes:
        st.success(f"✅ {len(uploaded_resumes)} resume(s) uploaded")
        with st.expander("📋 Uploaded files"):
            for resume in uploaded_resumes:
                st.write(f"• {resume.name}")

# Screen button
st.markdown("---")
col_button1, col_button2, col_button3 = st.columns([2, 1, 2])
with col_button2:
    screen_button = st.button("🎯 SCREEN RESUMES", type="primary", use_container_width=True)

if screen_button:
    if not job_description:
        st.error("❌ Please provide a job description")
    elif not uploaded_resumes:
        st.error("❌ Please upload at least one resume")
    else:
        with st.spinner("🔍 Analyzing resumes..."):
            resumes_text = []
            resume_names = []
            
            for resume in uploaded_resumes:
                try:
                    if resume.name.endswith('.pdf'):
                        text = extract_text_from_pdf(resume)
                    elif resume.name.endswith('.docx'):
                        text = extract_text_from_docx(resume)
                    else:
                        text = extract_text_from_txt(resume)
                    
                    if text and len(text.strip()) > 50:
                        resumes_text.append(text)
                        resume_names.append(resume.name)
                    else:
                        st.warning(f"⚠️ {resume.name} has very little text. Skipping...")
                except Exception as e:
                    st.warning(f"⚠️ Could not read {resume.name}")
            
            if not resumes_text:
                st.error("❌ No valid resumes found")
                st.stop()
            
            scores = calculate_match_scores(job_description, resumes_text)
            results = list(zip(resume_names, scores))
            results.sort(key=lambda x: x[1], reverse=True)
            
            # Display results
            st.divider()
            st.subheader("📊 Screening Results")
            st.markdown(f"**{len(results)} candidate(s) screened**")
            
            # Show job keywords
            job_keywords = extract_keywords(job_description)
            with st.expander("🔑 Key Skills from Job Description"):
                st.markdown(", ".join([f"**{word}**" for word, count in job_keywords[:15]]))
            
            st.divider()
            st.subheader("🏆 Candidate Ranking")
            
            # Display ranking cards
            for i, (name, score) in enumerate(results, 1):
                if score >= 70:
                    color = "#28a745"
                    emoji = "🏆"
                    status = "Strong Match"
                elif score >= 50:
                    color = "#ffc107"
                    emoji = "📌"
                    status = "Good Match"
                elif score >= 30:
                    color = "#fd7e14"
                    emoji = "⚠️"
                    status = "Consider"
                else:
                    color = "#dc3545"
                    emoji = "❌"
                    status = "Low Match"
                
                st.markdown(f"""
                <div style='border: 2px solid {color}; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;'>
                    <h2>{emoji} #{i} - {name}</h2>
                    <h1 style='color: {color};'>{score:.1f}% Match</h1>
                    <p><strong>Status:</strong> {status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Shortlisted candidates
            st.divider()
            st.subheader("🎯 Shortlisted Candidates")
            shortlisted = [(name, score) for name, score in results if score >= 50]
            
            if shortlisted:
                for name, score in shortlisted:
                    st.success(f"✅ **{name}** - {score:.1f}% match")
            else:
                st.warning("No candidates above 50% match. Try adjusting expectations.")

st.divider()
st.caption("💡 **Pro tip:** For best results, ensure resumes contain the keywords from the job description.")