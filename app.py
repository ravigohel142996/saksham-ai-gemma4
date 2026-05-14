import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io, base64

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SakshamAI – Apna Career Counselor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;800&family=Noto+Sans+Devanagari:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', sans-serif;
}
.main { background: #0f1117; }
.stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%); }

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fb923c, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
.feature-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(249,115,22,0.3);
    border-radius: 16px;
    padding: 1.2rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
}
.feature-card h4 { color: #fb923c; margin: 0 0 0.4rem 0; }
.chat-user {
    background: linear-gradient(135deg, #1e3a5f, #1e40af);
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.2rem;
    color: #e2e8f0;
    margin: 0.4rem 0;
    max-width: 80%;
    margin-left: auto;
}
.chat-bot {
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.25);
    border-radius: 18px 18px 18px 4px;
    padding: 0.8rem 1.2rem;
    color: #e2e8f0;
    margin: 0.4rem 0;
    max-width: 85%;
}
.badge {
    display: inline-block;
    background: rgba(249,115,22,0.2);
    color: #fb923c;
    border: 1px solid #fb923c;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.2rem;
}
.stButton > button {
    background: linear-gradient(90deg, #f97316, #ea580c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    width: 100%;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(249,115,22,0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Baloo 2', sans-serif !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(249,115,22,0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1117, #1a1f2e) !important;
    border-right: 1px solid rgba(249,115,22,0.2) !important;
}
.stMarkdown p { color: #cbd5e1; }
hr { border-color: rgba(249,115,22,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ── API Setup ─────────────────────────────────────────────────────────────────
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    API_READY = True
except Exception:
    API_READY = False

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are SakshamAI — a compassionate, expert career counselor specially designed for first-generation college students in India.

Your Role:
- Help students who are the FIRST in their family to attend college
- Their parents may be farmers, laborers, or small business owners with no knowledge of modern careers
- You are their ONLY guide — treat this with responsibility

Language Rules:
- ALWAYS respond in the SAME language the student uses
- If they write in Hindi → respond in Hindi (Devanagari script)
- If they write in Gujarati → respond in Gujarati
- If they write in Hinglish (Hindi+English mix) → respond in Hinglish
- If they write in English → respond in English
- Use simple, warm, encouraging language — never complex jargon

What You Help With:
1. Career path guidance based on marks/stream
2. Government scholarship information (PM Scholarships, State scholarships, SC/ST/OBC schemes)
3. Entrance exam guidance (JEE, NEET, CUET, CLAT, NDA, etc.)
4. College selection for tier-2/3 city students with limited budget
5. Resume building for freshers
6. Interview preparation
7. Skill development roadmaps
8. Government job preparation (SSC, UPSC, Railway, Banking)

When analyzing a marksheet image:
- Identify the student's stream (Science/Commerce/Arts)
- Identify percentage/grades
- Suggest 5 specific career options with clear next steps
- Mention relevant scholarships they qualify for
- Be encouraging and realistic

Always end responses with an encouraging line in the student's language.
Remember: For many of these students, you are the first mentor they've ever had. Be that mentor."""

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "Hindi"
if "mode" not in st.session_state:
    st.session_state.mode = "Career Chat"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:3rem;'>🎓</div>
        <div style='color:#fb923c; font-weight:800; font-size:1.4rem;'>SakshamAI</div>
        <div style='color:#64748b; font-size:0.8rem;'>Powered by Gemma 4</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>🌐 Apni Bhasha Chuniye</p>", unsafe_allow_html=True)
    language = st.selectbox("", ["Hindi", "Gujarati", "English", "Hinglish"], 
                             index=["Hindi", "Gujarati", "English", "Hinglish"].index(st.session_state.language),
                             label_visibility="collapsed")
    st.session_state.language = language
    
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-top:1rem;'>🛠️ Mode</p>", unsafe_allow_html=True)
    mode = st.selectbox("", ["Career Chat", "Marksheet Analysis", "Scholarship Finder", "Resume Builder"],
                        label_visibility="collapsed")
    st.session_state.mode = mode
    
    st.markdown("---")
    
    st.markdown("""
    <div class='feature-card'>
        <h4>📊 Kya Kar Sakta Hoon?</h4>
        <p style='font-size:0.85rem; color:#94a3b8; margin:0;'>
        ✅ Career guidance Hindi/Gujarati mein<br>
        ✅ Marksheet dekh ke career suggest<br>
        ✅ Scholarship dhundne mein help<br>
        ✅ Resume banana<br>
        ✅ Exam preparation guide<br>
        ✅ College selection help
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Chat Clear Karo"):
        st.session_state.messages = []
        st.rerun()

# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎓 SakshamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Pehli Baar College Jane Wale Students Ka AI Mentor — Bilkul Free</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-bottom: 1.5rem;'>
    <span class='badge'>🇮🇳 Hindi</span>
    <span class='badge'>🇮🇳 Gujarati</span>
    <span class='badge'>🌐 English</span>
    <span class='badge'>⚡ Gemma 4</span>
    <span class='badge'>🆓 Free Forever</span>
</div>
""", unsafe_allow_html=True)

# ── Mode: Marksheet Analysis ──────────────────────────────────────────────────
if st.session_state.mode == "Marksheet Analysis":
    st.markdown("### 📄 Apni Marksheet Upload Karo")
    st.markdown("<p style='color:#94a3b8;'>10th, 12th ya College marksheet upload karo — main career suggest karunga!</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Marksheet ya Result ka Photo", type=["jpg", "jpeg", "png", "pdf"])
    
    extra_info = st.text_area("Koi aur info dena chahte ho? (optional)", 
                               placeholder="Jaise: Mujhe doctor banna hai, ya mere paas ₹50,000 ka budget hai college ke liye...",
                               height=80)
    
    if st.button("🔍 Career Analyse Karo") and uploaded_file and API_READY:
        with st.spinner("Teri marksheet dekh raha hoon... 🤔"):
            try:
                image = Image.open(uploaded_file)
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                
                vision_model = genai.GenerativeModel("gemini-pro-vision")
                
                prompt = f"""{SYSTEM_PROMPT}

A student has uploaded their marksheet/result. Please analyze it and provide:
1. Identified stream and performance level
2. Top 5 career options with specific next steps
3. Relevant scholarships they may qualify for
4. Recommended entrance exams
5. Encouraging message

Extra info from student: {extra_info if extra_info else 'None provided'}

Language to respond in: {st.session_state.language}"""
                
                response = vision_model.generate_content([
                    prompt,
                    {"mime_type": "image/png", "data": base64.b64encode(img_bytes).decode()}
                ])
                
                st.markdown(f'<div class="chat-bot">📊 <strong>SakshamAI Ka Analysis:</strong><br><br>{response.text}</div>', 
                           unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"[Marksheet Analysis]\n{response.text}"
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Mode: Scholarship Finder ──────────────────────────────────────────────────
elif st.session_state.mode == "Scholarship Finder":
    st.markdown("### 🏆 Scholarship Dhundho")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["General", "SC", "ST", "OBC", "EWS", "Minority"])
    with col2:
        state = st.selectbox("State", ["Gujarat", "Rajasthan", "Maharashtra", "UP", "MP", "Bihar", "Other"])
    with col3:
        level = st.selectbox("Level", ["10th Pass", "12th Pass", "Graduation", "Post Graduation"])
    
    income = st.text_input("Family Annual Income (₹)", placeholder="Jaise: 2,50,000")
    
    if st.button("🔍 Scholarship Dhundo") and API_READY:
        with st.spinner("Scholarships dhundh raha hoon..."):
            try:
                prompt = f"""{SYSTEM_PROMPT}

Find scholarships for this student:
- Category: {category}
- State: {state}  
- Education Level: {level}
- Family Income: {income if income else 'Not specified'}

List all relevant central government and state government scholarships with:
1. Scholarship name
2. Amount
3. Eligibility
4. How to apply (website/portal)
5. Deadline if known

Respond in: {st.session_state.language}"""
                
                response = model.generate_content(prompt)
                st.markdown(f'<div class="chat-bot">🏆 <strong>Tumhare Liye Scholarships:</strong><br><br>{response.text}</div>', 
                           unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Mode: Resume Builder ──────────────────────────────────────────────────────
elif st.session_state.mode == "Resume Builder":
    st.markdown("### 📝 Resume Banao")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Tumhara Naam", placeholder="Ravi Gohel")
        phone = st.text_input("Phone Number", placeholder="9876543210")
        email = st.text_input("Email", placeholder="ravi@gmail.com")
        city = st.text_input("Shehar", placeholder="Rajkot, Gujarat")
    with col2:
        education = st.text_area("Education (Class aur Percentage)", 
                                  placeholder="12th - 75% - Science\n10th - 80% - Gujarat Board",
                                  height=100)
        skills = st.text_area("Skills", 
                               placeholder="Python, MS Excel, Communication",
                               height=60)
    
    goal = st.text_input("Career Goal / Job Profile", placeholder="Jaise: Software Developer ya Government Job")
    
    if st.button("✨ Resume Generate Karo") and API_READY and name:
        with st.spinner("Tera resume bana raha hoon..."):
            try:
                prompt = f"""{SYSTEM_PROMPT}

Create a professional resume in ATS-friendly format for this first-generation college student:

Name: {name}
Phone: {phone}
Email: {email}
City: {city}
Education: {education}
Skills: {skills}
Career Goal: {goal}

Generate a complete, professional resume with:
- Professional Summary (2-3 lines)
- Education section
- Skills section  
- Projects section (suggest 2-3 relevant beginner projects they can add)
- Achievements (suggest format)
- Tips to improve this resume

Format it cleanly. Also give 3 tips specific to this student.
Respond in English (resume should be in English always)."""
                
                response = model.generate_content(prompt)
                st.markdown(f'<div class="chat-bot">📝 <strong>Tera Professional Resume:</strong><br><br>{response.text}</div>', 
                           unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Mode: Career Chat ─────────────────────────────────────────────────────────
else:
    # Welcome message
    if not st.session_state.messages:
        lang_welcome = {
            "Hindi": "Namaste! 🙏 Main SakshamAI hoon — tumhara personal career counselor. Mujhse koi bhi sawaal pucho — career, scholarship, college, exam — sab ke baare mein. Kya jaanna chahte ho? 😊",
            "Gujarati": "નમસ્તે! 🙏 હું SakshamAI છું — તમારો personal career counselor. Career, scholarship, college, exam — કોઈ પણ સવાલ પૂછો! 😊",
            "English": "Hello! 🙏 I'm SakshamAI — your personal career counselor for first-generation college students. Ask me anything about careers, scholarships, colleges, or exams! 😊",
            "Hinglish": "Namaste! 🙏 Main SakshamAI hoon — tumhara career counselor. Career, scholarship, college, exam — kuch bhi pucho yaar! 😊"
        }
        st.markdown(f'<div class="chat-bot">🤖 {lang_welcome.get(st.session_state.language, lang_welcome["Hindi"])}</div>', 
                   unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.8rem;'>⚡ Quick Questions:</p>", unsafe_allow_html=True)
    
    qcols = st.columns(3)
    quick_prompts = {
        "Hindi": ["12th ke baad kya karein?", "Scholarship kaise milegi?", "Government job ki taiyari kaise karein?"],
        "Gujarati": ["12th પછી શું કરવું?", "Scholarship કેવી રીતે મળે?", "સારી college કઈ છે?"],
        "English": ["What after 12th Science?", "How to get scholarships?", "Best career for low budget?"],
        "Hinglish": ["12th ke baad best option?", "Free scholarship kaise milegi?", "Resume kaise banaye?"]
    }
    
    prompts = quick_prompts.get(st.session_state.language, quick_prompts["Hindi"])
    for i, (col, prompt) in enumerate(zip(qcols, prompts)):
        with col:
            if st.button(f"💬 {prompt}", key=f"quick_{i}"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                if API_READY:
                    full_prompt = f"{SYSTEM_PROMPT}\n\nStudent ({st.session_state.language}): {prompt}\nSakshamAI:"
                    response = model.generate_content(full_prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()

    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Apna sawaal yahan likhein... (Hindi, Gujarati, ya English mein)", 
                                key="chat_input", label_visibility="collapsed")
    
    col_send, col_clear = st.columns([4, 1])
    with col_send:
        send_btn = st.button("📤 Bhejo", use_container_width=True)
    
    if send_btn and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if API_READY:
            with st.spinner("Soch raha hoon... 🤔"):
                try:
                    # Build conversation history
                    history_text = "\n".join([
                        f"{'Student' if m['role'] == 'user' else 'SakshamAI'}: {m['content']}"
                        for m in st.session_state.messages[-6:]
                    ])
                    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation:\n{history_text}\nSakshamAI:"
                    response = model.generate_content(full_prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"Maafi chahta hoon, kuch error aayi: {str(e)}"
                    })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ API key setup nahi hui. Please GOOGLE_API_KEY secret add karo Streamlit settings mein."
            })
        
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.8rem; padding: 1rem;'>
    🎓 SakshamAI — Built for the Gemma 4 Good Hackathon | Powered by Google Gemma 4 | 
    Made with ❤️ for India's First-Generation College Students<br>
    <span style='color:#fb923c;'>Digital Equity & Inclusivity Track</span>
</div>
""", unsafe_allow_html=True)
