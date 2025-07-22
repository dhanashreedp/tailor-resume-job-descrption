# 🚀 Quick Resume Tailor

Quick Resume Tailor is a Streamlit-based AI assistant that analyzes your resume (in PDF format) and a job description, then instantly generates a tailored professional summary and experience sections optimized for ATS and Canva resumes.

---

## ✨ Features

- 📄 Upload your current **PDF resume**
- 📋 Paste any **job description**
- 🔍 Extract keywords from the JD automatically
- 🧠 Generate **tailored professional summary** based on JD
- 🏢 Generate customized **experience descriptions** (Ipsos & Route Mobile as examples)
- ⚡ Choose from:
  - **Smart/Local** (Instant generation)
  - **Groq API** (Online AI model)
  - **Ollama** (Offline AI via localhost)
- 📤 Copy and paste the final content into your Canva or ATS-ready resume

---

## 🛠️ Tech Stack

- **Python 3.9+**
- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [NLTK](https://www.nltk.org/)
- [Requests](https://pypi.org/project/requests/)

---

## 🚀 Setup Instructions

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/resume-tailor.git
cd resume-tailor
````

2. **Create and activate virtual environment**

```bash
python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, use:

```bash
pip install streamlit PyPDF2 nltk requests
```

4. **Download NLTK stopwords and punkt tokenizer**
   These are automatically downloaded on first run, but you can pre-install:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

---

## 📦 Running the App

```bash
streamlit run app.py
```

---

## ⚙️ API Keys & Configuration

* To use **Groq API**, update your API key in the code:

```python
GROQ_API_KEY = "your_actual_api_key"
```

* To use **Ollama (offline AI)**, install [Ollama](https://ollama.com/) and run:

```bash
ollama run phi3:mini
```

Make sure Ollama is accessible at `http://localhost:11434`.

---

## 🧪 Sample Workflow

1. Upload your **resume PDF**
2. Paste the **job description**
3. Choose an AI mode (Smart/Local, Groq, or Ollama)
4. Click **Generate Summary / Experience**
5. Copy output content and update your resume!

---

## 🧠 Customization

* Modify experience extraction by editing keywords in:

```python
def extract_experience_sections(self, pdf_text):
```

* Add more JD keyword patterns in:

```python
def extract_keywords_from_jd(self, jd_text):
```

---

## ✅ To-Do
* [ ] Support for other companies besides Ipsos and Route Mobile
* [ ] Export Word/Canva templates directly

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Feel free to fork this project and submit PRs for improvements, bug fixes, or new features!

---

## 🙋‍♀️ Author

Built by **Dhanashree Patil**
📧 [Email](mailto:your-email@example.com)
🔗 [LinkedIn](https://linkedin.com/in/your-profile)
💻 [GitHub](https://github.com/yourusername)
