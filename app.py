import streamlit as st
import random
import re
import time
import base64

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="CyberShield", page_icon="🛡️", layout="centered")

# ------------------------------
# SOUND SYSTEM (FIXED FOR INSTANT PLAY)
# ------------------------------
if "muted" not in st.session_state:
    st.session_state.muted = False

def play_sound(filename):
    if st.session_state.muted:
        return

    try:
        with open(filename, "rb") as f:
            data = f.read()

        b64 = base64.b64encode(data).decode()

        sound_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """

        st.markdown(sound_html, unsafe_allow_html=True)

    except:
        pass


# ------------------------------
# CSS / DESIGN (FULL V4 THEME)
# ------------------------------
st.markdown("""
<style>

@keyframes glowPulse {
  0% { text-shadow: 0px 0px 10px rgba(0,255,255,0.3); }
  50% { text-shadow: 0px 0px 25px rgba(0,255,255,0.8); }
  100% { text-shadow: 0px 0px 10px rgba(0,255,255,0.3); }
}

@keyframes floatBox {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
  100% { transform: translateY(0px); }
}

body {
    background: radial-gradient(circle at top, #0b2a4a, #050b1e, #020512);
    color: white;
}

.big-title {
    font-size: 80px;
    font-weight: 1000;
    text-align: center;
    color: #00fff7;
    animation: glowPulse 2s infinite;
}

.subtitle {
    font-size: 19px;
    text-align: center;
    color: #b3b3b3;
    margin-top: -15px;
}

.desc {
    font-size: 15px;
    text-align: center;
    color: #bfbfbf;
    margin-top: 8px;
    margin-bottom: 15px;
}

.level-box {
    padding: 22px;
    border-radius: 22px;
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,255,247,0.35);
    margin-top: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 0px 20px rgba(0,255,247,0.12);
    animation: floatBox 3s infinite;
}

.aura-box {
    padding: 15px;
    border-radius: 18px;
    background-color: rgba(0,255,247,0.08);
    border: 1px solid rgba(0,255,247,0.4);
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 0px 15px rgba(0,255,247,0.15);
}

.danger-box {
    padding: 15px;
    border-radius: 18px;
    background-color: rgba(255,50,80,0.10);
    border: 1px solid rgba(255,50,80,0.5);
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 0px 18px rgba(255,50,80,0.15);
}

div.stButton > button {
    background: linear-gradient(90deg, #00fff7, #6d28d9);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 16px;
    font-weight: bold;
    font-size: 16px;
    box-shadow: 0px 0px 18px rgba(0,255,247,0.25);
    transition: 0.25s;
    width: 100%;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 30px rgba(109,40,217,0.55);
    cursor: pointer;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# SESSION STATE
# ------------------------------
if "level" not in st.session_state:
    st.session_state.level = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0

if "phish_round" not in st.session_state:
    st.session_state.phish_round = 1

if "phish_correct" not in st.session_state:
    st.session_state.phish_correct = 0

if "current_msg" not in st.session_state:
    st.session_state.current_msg = None


# ------------------------------
# GAME FUNCTIONS
# ------------------------------
def restart_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.hints_used = 0
    st.session_state.phish_round = 1
    st.session_state.phish_correct = 0
    st.session_state.current_msg = None


def aura_hint(text):
    st.session_state.hints_used += 1
    st.markdown(f"""
    <div class="aura-box">
        🤖 <b>AURA Hint:</b> {text}
    </div>
    """, unsafe_allow_html=True)


def password_strength(password):
    points = 0
    if len(password) >= 10:
        points += 1
    if re.search(r"[A-Z]", password):
        points += 1
    if re.search(r"[a-z]", password):
        points += 1
    if re.search(r"[0-9]", password):
        points += 1
    if re.search(r"[@$!%*?&]", password):
        points += 1
    return points


def risk_score(message):
    risk = 0
    suspicious_words = ["urgent", "verify", "password", "locked", "click", "winner", "free", "claim", "confirm"]
    for word in suspicious_words:
        if word in message.lower():
            risk += 15

    if "http" in message.lower() or ".com" in message.lower() or ".net" in message.lower():
        risk += 20

    if "!!!" in message:
        risk += 15

    if len(message) > 80:
        risk += 10

    return min(risk, 100)


def transition(text):
    with st.spinner(text):
        time.sleep(1.2)


# ------------------------------
# HEADER
# ------------------------------
st.markdown('<div class="big-title">🛡️ CyberShield V4</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI + Cybersecurity Adventure Game</div>', unsafe_allow_html=True)

st.markdown("""
<div class="desc">
CyberShield V4 is an interactive cybersecurity game where players learn how to stop phishing scams, detect deepfakes, 
secure passwords, and protect their digital identity using real-world online safety skills.
</div>
""", unsafe_allow_html=True)

# MUTE BUTTON
colA, colB = st.columns([1, 1])
with colA:
    if st.button("🔊 Toggle Sound"):
        st.session_state.muted = not st.session_state.muted
        st.rerun()

with colB:
    st.write("")

if not st.session_state.muted:
    st.caption("🔊 Sound is ON")
else:
    st.caption("🔇 Sound is OFF")

# BACKGROUND MUSIC (UNCHANGED)
if not st.session_state.muted:
    try:
        music_file = open("music.mp3", "rb")
        music_bytes = music_file.read()
        st.audio(music_bytes, format="audio/mp3", loop=True)
    except:
        pass

st.write(f"### ⭐ Score: {st.session_state.score} | 🤖 Hints Used: {st.session_state.hints_used}")

progress_value = st.session_state.level / 6
st.progress(progress_value)

st.divider()


# ------------------------------
# LEVEL 0 INTRO
# ------------------------------
if st.session_state.level == 0:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader("📖 Welcome, Agent.")
    st.write("""
Your identity has been stolen by **PHANTOM AI**, a hacker that uses artificial intelligence to manipulate and attack users.

You are trapped inside the internet.

Complete cybersecurity challenges, earn points, and escape the digital world.

Your AI assistant **AURA** will guide you.
""")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Begin Mission"):
        play_sound("click.mp3")
        transition("Booting into the Digital World...")
        st.session_state.level = 1
        st.rerun()


# ------------------------------
# LEVEL 1 PASSWORD
# ------------------------------
elif st.session_state.level == 1:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader("🔐 Level 1: Password Panic")
    st.write("Create a strong password to block brute-force attacks.")
    st.markdown("</div>", unsafe_allow_html=True)

    password = st.text_input("Enter your password:")

    if st.button("Check Strength"):
        play_sound("click.mp3")
        strength = password_strength(password)

        if strength <= 2:
            play_sound("fail.mp3")
            st.markdown('<div class="danger-box">❌ Weak password. Hacker cracked it.</div>', unsafe_allow_html=True)
        elif strength == 3:
            st.warning("⚠️ Medium password. Better, but still risky.")
        else:
            play_sound("success.mp3")
            st.success("✅ Strong password! Access protected.")
            st.session_state.score += 25
            transition("Firewall secured...")
            st.session_state.level = 2
            st.rerun()

    if st.button("🤖 Ask AURA"):
        play_sound("click.mp3")
        aura_hint("Use 10+ characters, mix uppercase, lowercase, numbers, and symbols like @ or !")


# ------------------------------
# LEVEL 2 PHISHING MULTI ROUND
# ------------------------------
elif st.session_state.level == 2:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader(f"🎣 Level 2: Phishing Trap (Round {st.session_state.phish_round}/3)")
    st.write("Decide if the message is SAFE or PHISHING.")
    st.markdown("</div>", unsafe_allow_html=True)

    phishing_messages = [
        ("URGENT!!! Your bank account has been locked. Verify now: bank-secure-login.net", "PHISHING"),
        ("Hey! Are you coming to the robotics club meeting tomorrow?", "SAFE"),
        ("Your package delivery failed. Confirm address here: fedex-support-delivery.com", "PHISHING"),
        ("Reminder: Science fair projects due Friday.", "SAFE"),
        ("Congratulations!!! You won a FREE iPhone. Click to claim now!", "PHISHING"),
        ("Your teacher posted new homework on Google Classroom.", "SAFE"),
        ("Security alert: suspicious login detected. Confirm password immediately!", "PHISHING"),
    ]

    if st.session_state.current_msg is None:
        st.session_state.current_msg = random.choice(phishing_messages)

    msg, correct = st.session_state.current_msg

    st.write(f"📩 **Message:** {msg}")

    r_score = risk_score(msg)
    st.write("🤖 AURA Risk Scanner:")
    st.progress(r_score / 100)
    st.caption(f"Risk Score: {r_score}/100")

    col1, col2 = st.columns(2)

    def handle_answer(choice):
        play_sound("click.mp3")

        if choice == correct:
            play_sound("success.mp3")
            st.success("✅ Correct!")
            st.session_state.score += 15
            st.session_state.phish_correct += 1
        else:
            play_sound("fail.mp3")
            st.error("❌ Wrong!")
            st.session_state.score -= 5

        st.session_state.phish_round += 1
        st.session_state.current_msg = None

        if st.session_state.phish_round > 3:
            transition("Phishing firewall activated...")
            st.session_state.level = 3

        st.rerun()

    with col1:
        if st.button("✅ SAFE"):
            handle_answer("SAFE")

    with col2:
        if st.button("🚨 PHISHING"):
            handle_answer("PHISHING")

    if st.button("🤖 Ask AURA"):
        play_sound("click.mp3")
        aura_hint("Check for urgency, weird links, spelling mistakes, or requests for passwords/personal info.")


# ------------------------------
# LEVEL 3 DEEPFAKE
# ------------------------------
elif st.session_state.level == 3:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader("🎭 Level 3: Deepfake Danger")
    st.write("Someone posted a fake video pretending to be you.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("""
**Clues:**
- The voice sounds robotic  
- Lips don’t match perfectly  
- Lighting flickers strangely  
- The video looks slightly blurred  
""")

    choice = st.radio("Is the video REAL or a DEEPFAKE?", ["REAL", "DEEPFAKE"])

    if st.button("Submit"):
        play_sound("click.mp3")
        if choice == "DEEPFAKE":
            play_sound("success.mp3")
            st.success("✅ Correct! It was AI-generated.")
            st.session_state.score += 25
            transition("Deepfake removed...")
            st.session_state.level = 4
            st.rerun()
        else:
            play_sound("fail.mp3")
            st.error("❌ Wrong! It was a deepfake.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA"):
        play_sound("click.mp3")
        aura_hint("Deepfakes often have weird blinking, lip-sync errors, robotic audio, and inconsistent shadows.")


# ------------------------------
# LEVEL 4 PRIVACY
# ------------------------------
elif st.session_state.level == 4:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader("👁️ Level 4: Privacy Settings Maze")
    st.write("Your profile is leaking personal info. Choose the BEST privacy defense.")
    st.markdown("</div>", unsafe_allow_html=True)

    option = st.radio("Which choice protects you the most?", [
        "Keep location tagging ON",
        "Enable Two-Factor Authentication (2FA)",
        "Make profile public"
    ])

    if st.button("Lock It In"):
        play_sound("click.mp3")
        if option == "Enable Two-Factor Authentication (2FA)":
            play_sound("success.mp3")
            st.success("✅ Correct! 2FA blocks hackers even if they steal your password.")
            st.session_state.score += 25
            transition("Privacy locked...")
            st.session_state.level = 5
            st.rerun()
        else:
            play_sound("fail.mp3")
            st.error("❌ That increases risk.")
            st.session_state.score -= 5

    if st.button("🤖 Ask AURA"):
        play_sound("click.mp3")
        aura_hint("2FA is one of the best cybersecurity tools because it adds an extra layer of security.")


# ------------------------------
# LEVEL 5 FINAL BOSS
# ------------------------------
elif st.session_state.level == 5:
    st.markdown('<div class="level-box">', unsafe_allow_html=True)
    st.subheader("💀 Level 5: Boss Fight — PHANTOM AI")
    st.write("PHANTOM AI is attacking with advanced AI hacking techniques.")
    st.write("Choose your defense strategy carefully.")
    st.markdown("</div>", unsafe_allow_html=True)

    boss_choice = st.radio("Choose your defense move:", [
        "Share your password with a trusted friend",
        "Enable encryption + 2FA + strong passwords",
        "Click random links to confuse the hacker",
        "Turn off security updates"
    ])

    if st.button("⚔️ Attack!"):
        play_sound("click.mp3")
        if boss_choice == "Enable encryption + 2FA + strong passwords":
            play_sound("success.mp3")
            st.success("🏆 You defeated PHANTOM AI!")
            st.session_state.score += 50
            transition("Identity restored...")
            st.session_state.level = 6
            st.rerun()
        else:
            play_sound("fail.mp3")
            st.error("💥 Wrong move! PHANTOM AI hacked you.")
            st.session_state.score -= 15

    if st.button("🤖 Ask AURA"):
        play_sound("click.mp3")
        aura_hint("The strongest defense is layered security: encryption + 2FA + strong passwords + updates.")


# ------------------------------
# WIN SCREEN
# ------------------------------
elif st.session_state.level == 6:
    st.subheader("🎉 MISSION COMPLETE!")
    st.write("You recovered your identity and escaped the Digital World.")

    st.write(f"### ⭐ Final Score: {st.session_state.score}")
    st.write(f"### 🎣 Phishing Accuracy: {st.session_state.phish_correct}/3")
    st.write(f"### 🤖 Hints Used: {st.session_state.hints_used}")

    if st.session_state.score >= 120:
        st.success("🥇 Rank: DIGITAL GUARDIAN")
        st.balloons()
    elif st.session_state.score >= 80:
        st.warning("🥈 Rank: FIREWALL FIGHTER")
    else:
        st.error("🥉 Rank: CYBER ROOKIE")

    st.info("🧠 Cyber Tip: Strong passwords + 2FA + avoiding phishing links are your best online defenses.")

    if st.button("🔄 Restart Game"):
        play_sound("click.mp3")
        restart_game()
        st.rerun()
