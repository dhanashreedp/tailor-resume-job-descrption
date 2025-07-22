import streamlit as st
import requests
import json
import PyPDF2
import io
import re
import nltk
import os
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

class ResumeProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english')) if 'stopwords' in dir(nltk.corpus) else set()
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    
    def extract_experience_sections(self, pdf_text):
        """Extract specific experience sections from resume"""
        exp_sections = {"ipsos": "", "route": ""}
        lines = pdf_text.split("\n")
        current = None
        
        for line in lines:
            line = line.strip()
            if "Ipsos" in line or "Software Engineer" in line:
                current = "ipsos"
                exp_sections[current] += line + "\n"
            elif "Route Mobile" in line or "Software Developer" in line:
                current = "route"
                exp_sections[current] += line + "\n"
            elif current and line:
                exp_sections[current] += line + "\n"
                # Stop if we hit another major section
                if any(keyword in line.lower() for keyword in ["skills", "education", "project"]):
                    current = None
        
        return exp_sections
    
    def extract_current_summary(self, pdf_text):
        """Extract current summary from resume"""
        lines = pdf_text.split("\n")
        summary = ""
        in_summary = False
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ["summary", "objective", "profile"]):
                in_summary = True
                continue
            elif in_summary and line:
                if any(keyword in line.lower() for keyword in ["experience", "skills", "education"]):
                    break
                summary += line + " "
        
        return summary.strip()
    
    def extract_keywords_from_jd(self, jd_text):
        """Extract relevant keywords from job description"""
        if not jd_text:
            return []
        
        # Common tech keywords to look for
        tech_keywords = [
            "python", "django", "flask", "fastapi", "api", "rest", "sql", "postgresql", 
            "mysql", "aws", "docker", "kubernetes", "redis", "celery", "git", "ci/cd",
            "machine learning", "ml", "ai", "javascript", "react", "microservices",
            "cloud", "backend", "frontend", "database", "nosql", "mongodb", "java",
            "spring", "nodejs", "vue", "angular", "kubernetes", "jenkins", "devops"
        ]
        
        jd_lower = jd_text.lower()
        found_keywords = []
        
        for keyword in tech_keywords:
            if keyword in jd_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def generate_tailored_summary(self, current_summary, jd_keywords, api_choice="Smart/Local"):
        """Generate tailored summary based on current summary and JD keywords"""
        if api_choice == "Smart/Local":
            # Enhanced local generation
            base = "Innovative Software Developer with 2.5+ years of experience in creating secure and scalable applications. Developed backend services using Python, Django, and Flask, improving system performance and user engagement."
            
            # Customize based on JD keywords
            if jd_keywords:
                if any(kw in jd_keywords for kw in ["aws", "cloud"]):
                    base += " Experienced with AWS cloud services and containerization technologies."
                if any(kw in jd_keywords for kw in ["api", "rest"]):
                    base += " Specialized in RESTful API development and microservices architecture."
                if any(kw in jd_keywords for kw in ["machine learning", "ml", "ai"]):
                    base += " Interested in applying AI/ML technologies to solve complex problems."
                if any(kw in jd_keywords for kw in ["java", "spring"]):
                    base += " Adaptable to Java and Spring framework development."
                if any(kw in jd_keywords for kw in ["devops", "ci/cd"]):
                    base += " Experienced with DevOps practices and CI/CD pipeline implementation."
            
            base += " Seeking a Software Developer role to enhance software solutions through expertise in Python, RESTful API development, and cloud integration."
            return base
        
        elif api_choice == "Groq":
            prompt = f"""Rewrite this professional summary to match the job requirements. Keep it 3-4 sentences and ATS-friendly:

Current Summary: {current_summary}

Job Keywords: {', '.join(jd_keywords)}

Focus on: Python, Django, Flask, and relevant skills from the job keywords."""
            
            return self.call_groq_api(prompt)
        
        else:  # Ollama
            prompt = f"Rewrite professional summary for Software Developer. Include these keywords: {', '.join(jd_keywords[:5])}. Current: {current_summary[:200]}"
            return self.call_ollama_api(prompt)
    
    def generate_tailored_experience(self, experience_text, company_name, jd_keywords, api_choice="Smart/Local"):
        """Generate tailored experience description"""
        if api_choice == "Smart/Local":
            if "ipsos" in company_name.lower():
                base_points = [
                    "Developed backend services using Python with Django and Flask for unified data platform",
                    "Designed and implemented scalable features for data ingestion and ETL pipelines",
                    "Built RESTful APIs using Flask and Django REST Framework for data management",
                    "Enhanced resource efficiency by designing distributed task workflows with Celery",
                    "Reduced manual configuration by 40% through automated end-to-end workflows"
                ]
                
                # Customize based on JD keywords
                if jd_keywords:
                    if "aws" in jd_keywords:
                        base_points.insert(2, "Deployed applications on AWS using containerization and cloud services")
                    if "microservices" in jd_keywords:
                        base_points.insert(1, "Architected microservices-based solutions for improved scalability")
                    if "java" in jd_keywords:
                        base_points.insert(3, "Collaborated on Java-based integrations and cross-platform development")
                
                return "\n".join(f"• {point}" for point in base_points[:5])
            
            elif "route" in company_name.lower():
                base_points = [
                    "Implemented secure authentication mechanisms using JWT tokens and OAuth",
                    "Analyzed and optimized source code improving performance by 25%",
                    "Integrated PostgreSQL and MySQL databases using SQLAlchemy",
                    "Automated deployment pipelines using CI/CD tools like Jenkins and GitLab",
                    "Managed datasets with over 1 million records and reduced deployment time by 30%"
                ]
                
                # Customize based on JD keywords
                if jd_keywords:
                    if "docker" in jd_keywords:
                        base_points.insert(3, "Containerized applications using Docker for consistent deployment")
                    if "api" in jd_keywords:
                        base_points.insert(1, "Developed and maintained RESTful APIs serving millions of requests")
                    if "devops" in jd_keywords:
                        base_points.insert(4, "Implemented DevOps best practices for continuous integration and deployment")
                
                return "\n".join(f"• {point}" for point in base_points[:5])
        
        elif api_choice == "Groq":
            prompt = f"""Rewrite this work experience with 4-5 bullet points. Make it ATS-friendly and highlight skills relevant to the job:

Company: {company_name}
Experience: {experience_text}
Job Keywords: {', '.join(jd_keywords)}

Focus on technical achievements and quantifiable results."""
            
            return self.call_groq_api(prompt)
        
        else:  # Ollama
            prompt = f"Rewrite {company_name} experience in 4 bullet points. Include: {', '.join(jd_keywords[:3])}. Text: {experience_text[:300]}"
            return self.call_ollama_api(prompt)
    
    def call_groq_api(self, prompt):
        """Call Groq API"""
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        # GROQ_API_KEY = ""
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": "You are a professional resume writer. Be concise and professional."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                return "❌ Groq API error. Please try Smart/Local mode."
                
        except Exception as e:
            return f"❌ Groq API failed: {str(e)}"
    
    def call_ollama_api(self, prompt):
        """Call Ollama API with optimized settings"""
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "top_p": 0.8,
                    "top_k": 20,
                    "num_predict": 200,
                    "num_ctx": 1024,
                    "stop": ["###", "---", "\n\n\n"]
                }
            }, timeout=30)
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return "❌ Ollama API error. Please try Smart/Local mode."
        
        except Exception as e:
            return f"❌ Ollama failed: {str(e)}"

def main():
    st.set_page_config(page_title="Quick Resume Tailor", layout="wide")
    st.title("🚀 Quick Resume Tailor")
    st.write("Upload your PDF resume → Paste job description → Get tailored content for Canva")
    
    processor = ResumeProcessor()
    
    # Step 1: Upload PDF Resume
    st.subheader("📄 Step 1: Upload Your Current Resume (PDF)")
    pdf_file = st.file_uploader("Upload your resume", type=["pdf"])
    
    if pdf_file:
        # Extract text from PDF
        pdf_text = processor.extract_text_from_pdf(pdf_file)
        
        if pdf_text:
            # Extract current summary and experiences
            current_summary = processor.extract_current_summary(pdf_text)
            experience_sections = processor.extract_experience_sections(pdf_text)
            
            st.success("✅ Resume uploaded and processed successfully!")
            
            with st.expander("📋 View Extracted Content"):
                st.write("**Current Summary:**")
                st.write(current_summary or "No summary found")
                
                st.write("**Ipsos Experience:**")
                st.write(experience_sections.get("ipsos", "Not found"))
                
                st.write("**Route Mobile Experience:**")
                st.write(experience_sections.get("route", "Not found"))
            
            # Step 2: Job Description
            st.subheader("📋 Step 2: Paste Job Description")
            jd_input = st.text_area("Paste the job description here", height=200)
            
            if jd_input:
                # Extract keywords
                jd_keywords = processor.extract_keywords_from_jd(jd_input)
                
                if jd_keywords:
                    st.write("**🔍 Extracted Keywords:**")
                    st.write(", ".join(jd_keywords))
                
                # Step 3: AI Processing
                st.subheader("🤖 Step 3: Generate Tailored Content")
                
                # API Selection
                api_choice = st.selectbox(
                    "Choose processing method:",
                    ["Smart/Local (Instant)", "Groq (Fast API)", "Ollama (Local AI)"],
                    index=0
                )
                
                col1, col2, col3 = st.columns(3)
                
                # Generate Summary
                with col1:
                    if st.button("📝 Generate Summary", use_container_width=True):
                        if api_choice == "Smart/Local (Instant)":
                            summary = processor.generate_tailored_summary(current_summary, jd_keywords, "Smart/Local")
                            st.session_state.tailored_summary = summary
                            st.success("✅ Summary generated!")
                        
                        elif api_choice == "Groq (Fast API)":
                            with st.spinner("Generating with Groq..."):
                                summary = processor.generate_tailored_summary(current_summary, jd_keywords, "Groq")
                                st.session_state.tailored_summary = summary
                        
                        else:  # Ollama
                            with st.spinner("Generating with Ollama..."):
                                summary = processor.generate_tailored_summary(current_summary, jd_keywords, "Ollama")
                                st.session_state.tailored_summary = summary
                
                # Generate Ipsos Experience
                with col2:
                    if st.button("🏢 Generate Ipsos Experience", use_container_width=True):
                        if experience_sections.get("ipsos"):
                            if api_choice == "Smart/Local (Instant)":
                                exp = processor.generate_tailored_experience(experience_sections["ipsos"], "Ipsos", jd_keywords, "Smart/Local")
                                st.session_state.ipsos_exp = exp
                                st.success("✅ Ipsos experience generated!")
                            
                            elif api_choice == "Groq (Fast API)":
                                with st.spinner("Generating with Groq..."):
                                    exp = processor.generate_tailored_experience(experience_sections["ipsos"], "Ipsos", jd_keywords, "Groq")
                                    st.session_state.ipsos_exp = exp
                            
                            else:  # Ollama
                                with st.spinner("Generating with Ollama..."):
                                    exp = processor.generate_tailored_experience(experience_sections["ipsos"], "Ipsos", jd_keywords, "Ollama")
                                    st.session_state.ipsos_exp = exp
                        else:
                            st.error("❌ Ipsos experience not found in resume")
                
                # Generate Route Experience
                with col3:
                    if st.button("🚀 Generate Route Experience", use_container_width=True):
                        if experience_sections.get("route"):
                            if api_choice == "Smart/Local (Instant)":
                                exp = processor.generate_tailored_experience(experience_sections["route"], "Route Mobile", jd_keywords, "Smart/Local")
                                st.session_state.route_exp = exp
                                st.success("✅ Route experience generated!")
                            
                            elif api_choice == "Groq (Fast API)":
                                with st.spinner("Generating with Groq..."):
                                    exp = processor.generate_tailored_experience(experience_sections["route"], "Route Mobile", jd_keywords, "Groq")
                                    st.session_state.route_exp = exp
                            
                            else:  # Ollama
                                with st.spinner("Generating with Ollama..."):
                                    exp = processor.generate_tailored_experience(experience_sections["route"], "Route Mobile", jd_keywords, "Ollama")
                                    st.session_state.route_exp = exp
                        else:
                            st.error("❌ Route Mobile experience not found in resume")
                
                # Display Generated Content
                st.subheader("📋 Step 4: Copy Content for Canva")
                
                if hasattr(st.session_state, 'tailored_summary'):
                    st.write("**📝 Tailored Summary:**")
                    st.text_area("Summary (Copy this)", st.session_state.tailored_summary, height=100)
                
                if hasattr(st.session_state, 'ipsos_exp'):
                    st.write("**🏢 Ipsos Experience:**")
                    st.text_area("Ipsos Experience (Copy this)", st.session_state.ipsos_exp, height=150)
                
                if hasattr(st.session_state, 'route_exp'):
                    st.write("**🚀 Route Mobile Experience:**")
                    st.text_area("Route Mobile Experience (Copy this)", st.session_state.route_exp, height=150)
                
                # Quick Generate All
                st.subheader("⚡ Quick Generate All")
                if st.button("🚀 Generate All Content", use_container_width=True):
                    with st.spinner("Generating all content..."):
                        # Generate summary
                        summary = processor.generate_tailored_summary(current_summary, jd_keywords, api_choice.split('(')[0].strip())
                        st.session_state.tailored_summary = summary
                        
                        # Generate experiences
                        if experience_sections.get("ipsos"):
                            ipsos_exp = processor.generate_tailored_experience(experience_sections["ipsos"], "Ipsos", jd_keywords, api_choice.split('(')[0].strip())
                            st.session_state.ipsos_exp = ipsos_exp
                        
                        if experience_sections.get("route"):
                            route_exp = processor.generate_tailored_experience(experience_sections["route"], "Route Mobile", jd_keywords, api_choice.split('(')[0].strip())
                            st.session_state.route_exp = route_exp
                    
                    st.success("✅ All content generated! Copy and paste into your Canva template.")
                    st.rerun()
            
            else:
                st.info("👆 Please paste the job description to continue")
        
        else:
            st.error("❌ Could not extract text from PDF. Please try a different file.")
    
    else:
        st.info("👆 Please upload your resume PDF to get started")
    
    # Add help section
    with st.expander("💡 How to Use"):
        st.write("""
        **Simple 4-step process:**
        
        1. **Upload PDF**: Upload your current resume in PDF format
        2. **Paste JD**: Copy and paste the job description you're applying for
        3. **Generate**: Click buttons to generate tailored content (or use "Generate All")
        4. **Copy**: Copy the generated content and paste into your Canva resume template
        
        **Processing Options:**
        - **Smart/Local**: Instant results, no API needed
        - **Groq**: Fast AI processing with API
        - **Ollama**: Local AI (requires Ollama installed)
        
        **Tips:**
        - Use Smart/Local for fastest results
        - The content is optimized for ATS (Applicant Tracking Systems)
        - Copy each section separately into your Canva template
        """)

if __name__ == "__main__":
    main()