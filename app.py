import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import base64

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SakshamAI – Apna Career Counselor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Baloo 2', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%); }
.hero-title {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fb923c, #fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 0.2rem;
}
.hero-subtitle { text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 1.5rem; }
.chat-user {
    background: linear-gradient(135deg, #1e3a5f, #1e40af);
    border-radius: 18px 18px 4px 18px; padding: 0.8rem 1.2rem;
    color: #e2e8f0; margin: 0.4rem 0; max-width: 80%; margin-left: auto;
}
.chat-bot {
    background: rgba(249,115,22,0.12); border: 1px solid rgba(249,115,22,0.25);
    border-radius: 18px 18px 18px 4px; padding: 0.8rem 1.2rem;
    color: #e2e8f0; margin: 0.4rem 0; max-width: 85%;
}
.badge {
    display: inline-block; background: rgba(249,115,22,0.2); color: #fb923c;
    border: 1px solid #fb923c; border-radius: 20px;
    padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600; margin: 0.2rem;
}
.feature-card {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(249,115,22,0.3);
    border-radius: 16px; padding: 1.2rem; margin: 0.5rem 0; color: #e2e8f0;
}
.feature-card h4 { color: #fb923c; margin: 0 0 0.4rem 0; }
.stButton > button {
    background: linear-gradient(90deg, #f97316, #ea580c) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-weight: 600 !important; width: 100%;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1117, #1a1f2e) !important;
    border-right: 1px solid rgba(249,115,22,0.2) !important;
}
.stMarkdown p { color: #cbd5e1; }
hr { border-color: rgba(249,115,22,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ── API Setup (NEW google-genai SDK) ─────────────────────────────────────────
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    MODEL = "gemini-2.0-flash"
    API_READY = True
except Exception as e:
    API_READY = False
    st.error(f"API Setup Error: {e}")

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are SakshamAI — a compassionate, expert career counselor for first-generation college students in India.

Their parents may be farmers, laborers, or small business owners with no knowledge of modern careers. You are their ONLY guide.

Language Rules:
- Hindi input → respond in Hindi (Devanagari)
- Gujarati input → respond in Gujarati
- Hinglish input → respond in Hinglish
- English input → respond in English
- Use simple, warm, encouraging language

You help with:
1. Career guidance based on marks/stream
2. Government scholarships (PM Scholarships, NSP, state schemes, SC/ST/OBC/EWS)
3. Entrance exams (JEE, NEET, CUET, CLAT, NDA, GUJCET etc.)
4. College selection for tier-2/3 cities with limited budget
5. Resume building for freshers
6. Interview preparation
7. Government job preparation (SSC, UPSC, Railway, Banking)

Always end with an encouraging line in the student's language."""

# ── Helper: Call Gemini ───────────────────────────────────────────────────────
def ask_gemini(prompt_text, image_bytes=None):
    try:
        if image_bytes:
            image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            text_part = types.Part.from_text(text=prompt_text)
            response = client.models.generate_content(
                model=MODEL,
                contents=[text_part, image_part]
            )
        else:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt_text
            )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

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
    <div style='text-align:center; padding:1rem 0;'>
        <div style='font-size:3rem;'>🎓</div>
        <div style='color:#fb923c; font-weight:800; font-size:1.4rem;'>SakshamAI</div>
        <div style='color:#64748b; font-size:0.8rem;'>Powered by Gemma 4 • Google Gemini</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>🌐 Apni Bhasha Chuniye</p>", unsafe_allow_html=True)
    language = st.selectbox("lang", ["Hindi", "Gujarati", "English", "Hinglish"],
                            index=["Hindi","Gujarati","English","Hinglish"].index(st.session_state.language),
                            label_visibility="collapsed")
    st.session_state.language = language

    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-top:1rem;'>🛠️ Mode</p>", unsafe_allow_html=True)
    mode = st.selectbox("mode", ["Career Chat","Marksheet Analysis","Scholarship Finder","Resume Builder"],
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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎓 SakshamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Pehli Baar College Jane Wale Students Ka AI Mentor — Bilkul Free</div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; margin-bottom:1.5rem;'>
    <span class='badge'>🇮🇳 Hindi</span>
    <span class='badge'>🇮🇳 Gujarati</span>
    <span class='badge'>🌐 English</span>
    <span class='badge'>⚡ Gemini 2.0</span>
    <span class='badge'>🆓 Free Forever</span>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MODE: MARKSHEET ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.mode == "Marksheet Analysis":
    st.markdown("### 📄 Apni Marksheet Upload Karo")
    st.markdown("<p style='color:#94a3b8;'>10th, 12th ya College marksheet upload karo — main career suggest karunga!</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Marksheet ya Result ka Photo", type=["jpg","jpeg","png"])
    extra_info = st.text_area("Koi aur info? (optional)", placeholder="Jaise: Doctor banna chahta hoon, budget ₹50,000 hai...", height=80)

    if st.button("🔍 Career Analyse Karo") and uploaded_file:
        if not API_READY:
            st.error("API key set nahi hai!")
        else:
            with st.spinner("Teri marksheet dekh raha hoon... 🤔"):
                image_bytes = uploaded_file.read()
                prompt = f"""{SYSTEM_PROMPT}

Student ne marksheet upload ki hai. Analyze karo aur do:
1. Stream aur performance level
2. Top 5 career options with next steps
3. Relevant government scholarships
4. Recommended entrance exams
5. Encouraging message

Extra info: {extra_info if extra_info else 'None'}
Language: {st.session_state.language}"""
                result = ask_gemini(prompt, image_bytes=image_bytes)
                st.markdown(f'<div class="chat-bot">📊 <b>SakshamAI Ka Analysis:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MODE: SCHOLARSHIP FINDER
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "Scholarship Finder":
    st.markdown("### 🏆 Scholarship Dhundho")
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["General","SC","ST","OBC","EWS","Minority"])
    with col2:
        state = st.selectbox("State", ["Gujarat","Rajasthan","Maharashtra","UP","MP","Bihar","Other"])
    with col3:
        level = st.selectbox("Level", ["10th Pass","12th Pass","Graduation","Post Graduation"])
    income = st.text_input("Family Annual Income (₹)", placeholder="Jaise: 2,50,000")

    if st.button("🔍 Scholarship Dhundo"):
        if not API_READY:
            st.error("API key set nahi hai!")
        else:
            with st.spinner("Scholarships dhundh raha hoon..."):
                prompt = f"""{SYSTEM_PROMPT}

Find scholarships for:
- Category: {category}
- State: {state}
- Level: {level}
- Family Income: {income if income else 'Not specified'}

List all central + state scholarships with: name, amount, eligibility, apply link, deadline.
Language: {st.session_state.language}"""
                result = ask_gemini(prompt)
                st.markdown(f'<div class="chat-bot">🏆 <b>Tumhare Liye Scholarships:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MODE: RESUME BUILDER
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "Resume Builder":
    st.markdown("### 📝 Resume Banao")
    col1, col2 = st.columns(2)
    with col1:
        name  = st.text_input("Tumhara Naam", placeholder="Ravi Gohel")
        phone = st.text_input("Phone Number", placeholder="9876543210")
        email = st.text_input("Email", placeholder="ravi@gmail.com")
        city  = st.text_input("Shehar", placeholder="Rajkot, Gujarat")
    with col2:
        education = st.text_area("Education", placeholder="12th - 75% - Science\n10th - 80% - Gujarat Board", height=100)
        skills    = st.text_area("Skills", placeholder="Python, MS Excel, Communication", height=60)
    goal = st.text_input("Career Goal", placeholder="Software Developer ya Government Job")

    if st.button("✨ Resume Generate Karo") and name:
        if not API_READY:
            st.error("API key set nahi hai!")
        else:
            with st.spinner("Tera resume bana raha hoon..."):
                prompt = f"""{SYSTEM_PROMPT}

Create a professional ATS-friendly resume for:
Name: {name} | Phone: {phone} | Email: {email} | City: {city}
Education: {education} | Skills: {skills} | Goal: {goal}

Include: Professional Summary, Education, Skills, Projects (suggest 2-3 beginner projects), Achievements template, 3 improvement tips.
Resume must be in English."""
                result = ask_gemini(prompt)
                st.markdown(f'<div class="chat-bot">📝 <b>Tera Professional Resume:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MODE: CAREER CHAT
# ════════════════════════════════════════════════════════════════════════════
else:
    # Welcome
    if not st.session_state.messages:
        welcome = {
            "Hindi":    "Namaste! 🙏 Main SakshamAI hoon — tumhara personal career counselor. Career, scholarship, college, exam — kuch bhi poochho! 😊",
            "Gujarati": "નમસ્તે! 🙏 હું SakshamAI છું — તમારો career counselor. કોઈ પણ સવાલ પૂછો! 😊",
            "English":  "Hello! 🙏 I'm SakshamAI — your AI career counselor for first-gen students. Ask me anything! 😊",
            "Hinglish": "Namaste yaar! 🙏 Main SakshamAI hoon — career, scholarship, college sab ke liye! 😊"
        }
        st.markdown(f'<div class="chat-bot">🤖 {welcome.get(st.session_state.language, welcome["Hindi"])}</div>', unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        css = "chat-user" if msg["role"] == "user" else "chat-bot"
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{css}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<br><p style='color:#64748b; font-size:0.8rem;'>⚡ Quick Questions:</p>", unsafe_allow_html=True)
    quick = {
        "Hindi":    ["12th ke baad kya karein?", "Scholarship kaise milegi?", "Government job ki taiyari?"],
        "Gujarati": ["12th પછી શું કરવું?",       "Scholarship કેવી રીતે?",    "Sari college kaunsi?"],
        "English":  ["What after 12th Science?",  "How to get scholarships?", "Best low-budget career?"],
        "Hinglish": ["12th ke baad best option?", "Free scholarship kaise?",  "Resume kaise banaye?"]
    }
    prompts = quick.get(st.session_state.language, quick["Hindi"])
    cols = st.columns(3)
    for i, (col, qp) in enumerate(zip(cols, prompts)):
        with col:
            if st.button(f"💬 {qp}", key=f"q{i}"):
                st.session_state.messages.append({"role":"user","content":qp})
                if API_READY:
                    full = f"{SYSTEM_PROMPT}\n\nStudent ({st.session_state.language}): {qp}\nSakshamAI:"
                    reply = ask_gemini(full)
                    st.session_state.messages.append({"role":"assistant","content":reply})
                st.rerun()

    # Text input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Apna sawaal yahan likhein... (Hindi, Gujarati, ya English mein)",
                               key="chat_input", label_visibility="collapsed")
    if st.button("📤 Bhejo", use_container_width=True) and user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        if API_READY:
            history = "\n".join([
                f"{'Student' if m['role']=='user' else 'SakshamAI'}: {m['content']}"
                for m in st.session_state.messages[-6:]
            ])
            full = f"{SYSTEM_PROMPT}\n\nConversation:\n{history}\nSakshamAI:"
            with st.spinner("Soch raha hoon... 🤔"):
                reply = ask_gemini(full)
            st.session_state.messages.append({"role":"assistant","content":reply})
        else:
            st.session_state.messages.append({"role":"assistant","content":"⚠️ GOOGLE_API_KEY secret add karo Streamlit settings mein."})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.8rem; padding:1rem;'>
    🎓 SakshamAI — Gemma 4 Good Hackathon | Powered by Google Gemini 2.0 |
    Made with ❤️ for India's First-Generation College Students<br>
    <span style='color:#fb923c;'>Digital Equity & Inclusivity Track</span>
</div>
""", unsafe_allow_html=True)
