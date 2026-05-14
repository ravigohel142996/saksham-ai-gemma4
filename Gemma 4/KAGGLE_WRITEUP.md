# SakshamAI: Empowering India's First-Generation College Students with Gemma 4

**Subtitle:** A multilingual AI career counselor that speaks Hindi, Gujarati, and English — giving 600 million underserved Indian students their first-ever mentor.

**Track:** Digital Equity & Inclusivity

---

## The Problem: 600 Million Students With No Guide

In India, over 600 million students are the first in their families to attend college. Their parents are farmers, daily wage laborers, or small shop owners. When these students finish their 12th grade exams, they face a wall of questions:

- *"Science liya hai — kya karun ab?"* (I took Science — what do I do now?)
- *"Koi scholarship milegi mujhe?"* (Will I get any scholarship?)
- *"Resume kaise banate hain?"* (How do you make a resume?)

They cannot afford career counselors. Their schools have one overworked teacher for 80 students. Their parents don't know what JEE or NEET is. They rely on neighbors, rumors, and luck.

**SakshamAI was built to change this.** It gives every first-generation college student access to a knowledgeable, compassionate, always-available AI mentor — in their own language, for free.

---

## The Solution: SakshamAI

SakshamAI is a multilingual AI career counseling application powered by Google Gemma 4. It addresses the specific, acute needs of first-generation college students in India across four core capabilities:

### 1. Multilingual Career Chat
Students converse in Hindi, Gujarati, English, or Hinglish. The model detects language automatically and responds in kind. This is critical — many rural students are more comfortable in their native language and feel intimidated by English-only interfaces.

### 2. Marksheet Analysis (Multimodal)
Students upload a photo of their 10th or 12th marksheet. Gemma 4's multimodal capability analyzes the image, identifies their stream and performance, and generates a personalized career roadmap with 5 specific options, relevant scholarships, and entrance exam guidance.

### 3. Scholarship Finder
India has dozens of central and state government scholarships — PM Scholarship, NSP, state-specific schemes for SC/ST/OBC/EWS students — but most students don't know they exist. SakshamAI asks for category, state, education level, and family income, then lists every applicable scholarship with application links and deadlines.

### 4. Resume Builder
For students applying to their first job or internship, SakshamAI generates an ATS-friendly resume using their basic details, suggests relevant beginner projects to add, and provides personalized improvement tips.

---

## Why Gemma 4?

Gemma 4 was the ideal choice for three reasons:

**Multimodal Understanding:** The marksheet analysis feature requires reading handwritten or printed text from a photo and understanding educational context. Gemma 4's vision capabilities handle this reliably without fine-tuning.

**Multilingual Competence:** Gemma 4 demonstrates strong performance in Indian languages including Hindi and Gujarati, enabling natural, contextually appropriate responses that feel genuine rather than translated.

**Open and Accessible:** Gemma 4 is available via Google AI Studio at no cost for prototyping, making SakshamAI itself free to build and free for users — which is non-negotiable for our target audience.

The application uses `gemma-3-27b-it` via the Google Generative AI Python SDK, with carefully engineered system prompts that establish the counselor persona, language-switching rules, and domain expertise.

---

## Technical Architecture

```
User (Smartphone Browser)
         ↓
  Streamlit Web App (Python)
         ↓
  Google Gemma 4 API
  (gemma-3-27b-it)
    - Text completion for chat, scholarships, resume
    - Multimodal for marksheet image analysis
         ↓
  Structured response in user's language
         ↓
  Streamlit UI (dark theme, mobile-friendly)
```

**Key technical decisions:**
- **Streamlit** for rapid deployment with zero frontend overhead
- **PIL** for image preprocessing before sending to the vision model
- **Session state management** for multi-turn conversation continuity
- **System prompt engineering** for consistent persona, language detection, and domain focus
- **Streamlit Community Cloud** for free, always-on hosting

---

## Challenges and Solutions

**Challenge 1: Language switching reliability**
Early versions would sometimes mix languages mid-response. Solution: explicit language instruction in every prompt, including the detected language as a parameter.

**Challenge 2: Marksheet variety**
Indian marksheets vary enormously — CBSE, GSEB, RBSE, Maharashtra Board all have different formats. Solution: prompt engineering to instruct the model to extract key fields (stream, percentage, board) regardless of format, rather than looking for specific layouts.

**Challenge 3: Scholarship accuracy**
Government scholarship details change yearly. Solution: the model is instructed to provide the scheme name and official portal URL so students can verify current details, rather than presenting potentially outdated figures as absolute facts.

---

## Real-World Impact

SakshamAI is designed to scale. The marginal cost of each conversation is near zero. The application requires only a smartphone and basic internet — conditions met by 400+ million Indians today, a number growing daily.

Consider the impact: a student in a village in Gujarat who scored 72% in 12th Science previously had no way to know that she qualifies for the MYSY scholarship, that she can appear for GUJCET for pharmacy admissions, or that her marks qualify her for a B.Sc. in a state university where fees are under ₹10,000/year. SakshamAI tells her all of this in Gujarati, in under two minutes, for free.

---

## Future Roadmap

- **Voice interface** for students with low literacy using Gemma 4's multimodal pipeline
- **Offline mode** using Gemma 4's edge-optimized E4B model via Ollama for areas with no internet
- **WhatsApp integration** since most rural students access internet primarily through WhatsApp
- **Fine-tuning** on Indian career counseling datasets for higher accuracy on domain-specific queries

---

## Conclusion

Digital equity is not just about access to devices and internet. It is about access to knowledge, guidance, and opportunity. SakshamAI uses the power of Gemma 4 to give India's most underserved students something they have never had before: a mentor who knows them, speaks their language, and is available at 2 AM the night before they have to fill out their college application form.

That is the promise of AI for good. That is SakshamAI.

---

**Live Demo:** [YOUR_STREAMLIT_LINK]  
**Code Repository:** [YOUR_GITHUB_LINK]  
**Video:** [YOUR_YOUTUBE_LINK]  

*Author: Ravi Gohel | B.Tech CSE (AI & ML) | Rajkot, Gujarat, India*
