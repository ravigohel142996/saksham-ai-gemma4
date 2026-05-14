import streamlit as st
import requests
from PIL import Image
import io
import base64

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="SakshamAI", page_icon="🎓", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Baloo 2', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%); }
.hero-title {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center;
}
.hero-sub { text-align:center; color:#94a3b8; font-size:1.1rem; margin-bottom:1.5rem; }
.chat-user {
    background: linear-gradient(135deg,#1e3a5f,#1e40af);
    border-radius:18px 18px 4px 18px; padding:0.8rem 1.2rem;
    color:#e2e8f0; margin:0.4rem 0; max-width:80%; margin-left:auto;
}
.chat-bot {
    background:rgba(249,115,22,0.12); border:1px solid rgba(249,115,22,0.25);
    border-radius:18px 18px 18px 4px; padding:0.8rem 1.2rem;
    color:#e2e8f0; margin:0.4rem 0; max-width:85%;
}
.badge {
    display:inline-block; background:rgba(249,115,22,0.2); color:#fb923c;
    border:1px solid #fb923c; border-radius:20px;
    padding:0.2rem 0.8rem; font-size:0.75rem; font-weight:600; margin:0.2rem;
}
.stButton>button {
    background:linear-gradient(90deg,#f97316,#ea580c) !important;
    color:white !important; border:none !important;
    border-radius:12px !important; font-weight:600 !important; width:100%;
}
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0f1117,#1a1f2e) !important;
    border-right:1px solid rgba(249,115,22,0.2) !important;
}
.stMarkdown p { color:#cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ── API (REST — no gRPC!) ─────────────────────────────────────────────────────
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
MODEL   = "gemini-1.5-flash"
URL     = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"
API_READY = bool(API_KEY)

SYSTEM_PROMPT = """You are SakshamAI — a compassionate career counselor for first-generation college students in India.
Language rules: Hindi input→Hindi reply, Gujarati→Gujarati, English→English, Hinglish→Hinglish.
Help with: careers, scholarships, entrance exams, college selection, resume, govt jobs.
Always be warm, simple, encouraging."""

def ask_gemini(prompt_text, image_bytes=None):
    if not API_READY:
        return "⚠️ API key missing. Please add GOOGLE_API_KEY in Streamlit Secrets."
    try:
        parts = [{"text": f"{SYSTEM_PROMPT}\n\n{prompt_text}"}]
        if image_bytes:
            b64 = base64.b64encode(image_bytes).decode()
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64}})
        payload = {"contents": [{"parts": parts}]}
        r = requests.post(URL, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        # Try flash-002 if flash fails
        try:
            url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={API_KEY}"
            r2 = requests.post(url2, json={"contents":[{"parts":[{"text":f"{SYSTEM_PROMPT}\n\n{prompt_text}"}]}]}, timeout=30)
            r2.raise_for_status()
            return r2.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Session ───────────────────────────────────────────────────────────────────
for k,v in [("messages",[]),("language","Hindi"),("mode","Career Chat")]:
    if k not in st.session_state: st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:1rem 0'><div style='font-size:3rem'>🎓</div><div style='color:#fb923c;font-weight:800;font-size:1.4rem'>SakshamAI</div><div style='color:#64748b;font-size:0.8rem'>Powered by Gemini AI</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color:#94a3b8;font-size:0.85rem'>🌐 Bhasha Chuniye</p>", unsafe_allow_html=True)
    st.session_state.language = st.selectbox("lang", ["Hindi","Gujarati","English","Hinglish"], label_visibility="collapsed")
    st.markdown("<p style='color:#94a3b8;font-size:0.85rem;margin-top:1rem'>🛠️ Mode</p>", unsafe_allow_html=True)
    st.session_state.mode = st.selectbox("mode", ["Career Chat","Marksheet Analysis","Scholarship Finder","Resume Builder"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(249,115,22,0.3);border-radius:16px;padding:1.2rem'><p style='color:#fb923c;font-weight:700;margin:0 0 0.5rem'>📊 Features</p><p style='font-size:0.85rem;color:#94a3b8;margin:0'>✅ Career guidance<br>✅ Marksheet analysis<br>✅ Scholarship finder<br>✅ Resume builder<br>✅ Hindi / Gujarati</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ Chat Clear"):
        st.session_state.messages = []
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎓 SakshamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Pehli Baar College Jane Wale Students Ka AI Mentor — Bilkul Free</div>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center;margin-bottom:1.5rem'><span class='badge'>🇮🇳 Hindi</span><span class='badge'>🇮🇳 Gujarati</span><span class='badge'>🌐 English</span><span class='badge'>⚡ Gemini AI</span><span class='badge'>🆓 Free</span></div>", unsafe_allow_html=True)

mode = st.session_state.mode
lang = st.session_state.language

# ── MARKSHEET ─────────────────────────────────────────────────────────────────
if mode == "Marksheet Analysis":
    st.markdown("### 📄 Marksheet Upload Karo")
    f = st.file_uploader("Photo upload karo", type=["jpg","jpeg","png"])
    extra = st.text_area("Extra info (optional)", placeholder="Doctor banna chahta hoon...", height=80)
    if st.button("🔍 Analyse Karo") and f:
        with st.spinner("Dekh raha hoon... 🤔"):
            prompt = f"Marksheet analyse karo. Career options do. Scholarships batao. Language: {lang}. Extra: {extra or 'None'}"
            result = ask_gemini(prompt, image_bytes=f.read())
        st.markdown(f'<div class="chat-bot">📊 <b>Analysis:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ── SCHOLARSHIP ───────────────────────────────────────────────────────────────
elif mode == "Scholarship Finder":
    st.markdown("### 🏆 Scholarship Dhundho")
    c1,c2,c3 = st.columns(3)
    cat   = c1.selectbox("Category", ["General","SC","ST","OBC","EWS","Minority"])
    state = c2.selectbox("State",    ["Gujarat","Rajasthan","Maharashtra","UP","MP","Bihar","Other"])
    level = c3.selectbox("Level",    ["10th Pass","12th Pass","Graduation","Post Graduation"])
    income = st.text_input("Family Income (₹)", placeholder="2,50,000")
    if st.button("🔍 Dhundo"):
        with st.spinner("Dhundh raha hoon..."):
            prompt = f"Scholarships for: Category={cat}, State={state}, Level={level}, Income={income or 'unknown'}. List all central+state schemes with links. Language: {lang}"
            result = ask_gemini(prompt)
        st.markdown(f'<div class="chat-bot">🏆 <b>Scholarships:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ── RESUME ────────────────────────────────────────────────────────────────────
elif mode == "Resume Builder":
    st.markdown("### 📝 Resume Banao")
    c1,c2 = st.columns(2)
    name  = c1.text_input("Naam",   placeholder="Ravi Gohel")
    phone = c1.text_input("Phone",  placeholder="9876543210")
    email = c1.text_input("Email",  placeholder="ravi@gmail.com")
    city  = c1.text_input("Shehar", placeholder="Rajkot, Gujarat")
    edu   = c2.text_area("Education", placeholder="12th-75%-Science\n10th-80%", height=100)
    skills= c2.text_area("Skills",   placeholder="Python, Excel", height=60)
    goal  = st.text_input("Career Goal", placeholder="Software Developer")
    if st.button("✨ Resume Banao") and name:
        with st.spinner("Bana raha hoon..."):
            prompt = f"ATS resume for: Name={name}, Phone={phone}, Email={email}, City={city}, Edu={edu}, Skills={skills}, Goal={goal}. Add project suggestions. English only."
            result = ask_gemini(prompt)
        st.markdown(f'<div class="chat-bot">📝 <b>Resume:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ── CHAT ──────────────────────────────────────────────────────────────────────
else:
    welcome = {"Hindi":"Namaste! 🙏 Main SakshamAI — career, scholarship, college sab ke liye! Kya poochna hai? 😊",
               "Gujarati":"નમસ્તે! 🙏 SakshamAI — career counselor. સવાલ પૂછો! 😊",
               "English":"Hello! 🙏 I'm SakshamAI — ask me about careers, scholarships, colleges! 😊",
               "Hinglish":"Namaste yaar! 🙏 Career, scholarship, college — sab bataunga! 😊"}
    if not st.session_state.messages:
        st.markdown(f'<div class="chat-bot">🤖 {welcome.get(lang, welcome["Hindi"])}</div>', unsafe_allow_html=True)

    for m in st.session_state.messages:
        css = "chat-user" if m["role"]=="user" else "chat-bot"
        ico = "👤" if m["role"]=="user" else "🤖"
        st.markdown(f'<div class="{css}">{ico} {m["content"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    quick = {"Hindi":["12th ke baad kya karein?","Scholarship kaise milegi?","Government job ki taiyari?"],
             "Gujarati":["12th પછી શું?","Scholarship કેવી?","Govt job?"],
             "English":["What after 12th?","How to get scholarships?","Best low-budget career?"],
             "Hinglish":["12th ke baad best?","Free scholarship?","Resume kaise?"]}
    qs = quick.get(lang, quick["Hindi"])
    for col,qp in zip(st.columns(3), qs):
        with col:
            if st.button(f"💬 {qp}", key=qp):
                st.session_state.messages.append({"role":"user","content":qp})
                with st.spinner("..."):
                    r = ask_gemini(f"Student ({lang}): {qp}")
                st.session_state.messages.append({"role":"assistant","content":r})
                st.rerun()

    user_input = st.text_input("", placeholder="Sawaal likhein...", key="inp", label_visibility="collapsed")
    if st.button("📤 Bhejo") and user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        history = "\n".join([f"{'Student' if m['role']=='user' else 'SakshamAI'}: {m['content']}" for m in st.session_state.messages[-6:]])
        with st.spinner("Soch raha hoon... 🤔"):
            reply = ask_gemini(f"Conversation:\n{history}\nSakshamAI:")
        st.session_state.messages.append({"role":"assistant","content":reply})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div style='text-align:center;color:#475569;font-size:0.8rem'>🎓 SakshamAI | Gemma 4 Good Hackathon | <span style='color:#fb923c'>Digital Equity & Inclusivity</span></div>", unsafe_allow_html=True)
