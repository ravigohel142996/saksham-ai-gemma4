# 🎓 SakshamAI — AI Career Counselor for First-Generation College Students

> **Gemma 4 Good Hackathon Submission | Digital Equity & Inclusivity Track**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](YOUR_DEMO_LINK)
[![Powered by](https://img.shields.io/badge/Powered%20by-Gemma%204-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/gemma)
[![Track](https://img.shields.io/badge/Track-Digital%20Equity-orange?style=for-the-badge)](https://kaggle.com/competitions/gemma-4-good-hackathon)

---

## 🇮🇳 The Problem

India has **600 million+** students who are the first in their families to attend college. Their parents — farmers, laborers, small business owners — have no knowledge of:
- Which career to choose after 12th
- Which scholarships exist
- How to write a resume
- Which entrance exams to appear for

**These students have no mentor. SakshamAI becomes that mentor.**

---

## 💡 What is SakshamAI?

SakshamAI is an AI-powered career counselor built on **Google Gemma 4**, designed specifically for first-generation college students in India. It speaks their language — Hindi, Gujarati, English, or Hinglish.

### Features:
| Feature | Description |
|---------|-------------|
| 🗣️ **Multilingual Chat** | Career guidance in Hindi, Gujarati, English, Hinglish |
| 📄 **Marksheet Analysis** | Upload marksheet photo → Get personalized career roadmap |
| 🏆 **Scholarship Finder** | Find government scholarships based on category, state, income |
| 📝 **Resume Builder** | Generate ATS-friendly resume with project suggestions |

---

## 🏗️ Architecture

```
User Input (Text/Image)
        ↓
Streamlit Frontend (Python)
        ↓
Google Gemma 4 API (gemma-3-27b-it)
  - Text: Career counseling, scholarships, resume
  - Multimodal: Marksheet image analysis
        ↓
Structured Response in User's Language
        ↓
Streamlit UI Display
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/saksham-ai-gemma4
cd saksham-ai-gemma4

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API key
# Create .streamlit/secrets.toml and add:
# GOOGLE_API_KEY = "your_key_here"

# 4. Run
streamlit run app.py
```

**Get free API key:** [aistudio.google.com](https://aistudio.google.com)

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GOOGLE_API_KEY` in Secrets
5. Deploy!

---

## 🎯 Impact

- **Target Users:** 600M+ first-generation college students in India
- **Languages Supported:** Hindi, Gujarati, English, Hinglish
- **Cost:** Free forever
- **Internet Required:** Yes (minimal bandwidth)
- **Device:** Works on any smartphone browser

---

## 🔧 Tech Stack

- **AI Model:** Google Gemma 4 (gemma-3-27b-it) via Google AI Studio API
- **Frontend:** Streamlit
- **Image Processing:** PIL (Python Imaging Library)
- **Deployment:** Streamlit Community Cloud
- **Language:** Python 3.10+

---

## 📹 Demo Video

[Watch on YouTube](YOUR_YOUTUBE_LINK)

---

## 👤 Author

**Ravi Gohel**  
B.Tech CSE (AI & ML) | Rajkot, Gujarat  
[LinkedIn](https://www.linkedin.com/in/ravi-gohel-733172245/)

---

## 📄 License

CC-BY 4.0 — Open Source

---

*Built with ❤️ for India's first-generation college students | Gemma 4 Good Hackathon 2026*
