import streamlit as st
import random
import re
import time
import pandas as pd
import os

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="CyberShield V3", page_icon="🛡️", layout="centered")

# -----------------------------------
# STYLING (HACKER THEME)
# -----------------------------------
st.markdown("""
<style>
    body {
        background-color: #0b0f19;
        color: white;
    }
    .title {
        font-size: 55px;
        font-weight: 900;
        text-align: center;
        color: #00ffb3;
        text-shadow: 0px 0px 25px rgba(0,255,179,0.7);
        margin-bottom: -10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #bbbbbb;
        margin-bottom: 30px;
    }
    .panel {
        padding: 20px;
        border-radius: 18px;
        background-color: rgba(255,255,255,0.04);
        border: 1px solid rgba(0,255,179,0.25);
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 0px 18px rgba(0,255,179,0.1);
    }
    .danger {
        padding: 15px;
        border-radius: 14px;
        background-color: rgba(255,0,0,0.08);
        border: 1px solid rgba(255,0,0,0.35);
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .aura {
        padding: 15px;
        border-radius: 14px;
        background-color: rgba(0,255,179,0.08);
        border: 1px solid rgba(0,255,179,0.35);
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .scan {
        font-family: monospace;
        color: #00ffb3;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# FILE SETUP FOR LEADERBOARD
# -----------------------------------
LEADERBOARD_FILE = "leaderboard.csv"

def save_score(name, score):
    new_data = pd.DataFrame([[name, score]], columns=["Name", "Score"])

    if os.path.exists(LEADERBOARD_FILE):
        old_data = pd.read_csv(LEADERBOARD_FILE)
        combined = pd.concat([old_data, new_data], ignore_index=True)
    else:
        combined = new_data

    combined.to_csv(LEADERBOARD_FILE, index=False)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        data = pd.read_csv(LEADERBOARD_FILE)
        data = data.sort_values(by="Score", ascending=False).head(10)
        return data
    return pd.DataFrame(columns=["Name", "Score"])

# -----------------------------------
# SESSION STATE
# -----------------------------------
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

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "saved" not in st.session_state:
    st.session_state.saved = False

# -----------------------------------
# GAME FUNCTIONS
# -----------------------------------
def restart_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.hints_used = 0
    st.session_state.phish_round = 1
    st.session_state.phish_correct = 0
    st.session_state.current_msg = None
    st.session_state.saved = False


def aura_hint(text):
    st.session_state.hints_used += 1
    st.markdown(f"""
    <div class="aura">
        🤖 <b>AURA:</b> {text}
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


def scan_animation():
    lines = [
        "[AURA SCAN] Initializing AI scanner...",
        "[AURA SCAN] Checking message structure...",
        "[AURA SCAN] Detecting suspicious keywords...",
        "[AURA SCAN] Analyzing link patterns...",
        "[AURA SCAN] Running neural safety model...",
        "[AURA SCAN] Generating risk score..."
    ]
    for line in lines:
        st.markdown(f"<p class='scan'>{line}</p>", unsafe_allow_html=True)
        time.sleep(0.4)


# -----------------------------------
# HEADER
# -----------------------------------
st.markdown('<div class="title">🛡️ CyberShield V3</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI + Cybersecurity Story Game | Protect Your Identity Online</div>', unsafe_allow_html=True)

st.write(f"### ⭐ Score: {st.session_state.score}   |   🤖 Hints: {st.session_state.hints_used}")

progress_value = st.session_state.level / 6
st.progress(progress_value)

st.divider()

# -----------------------------------
# LEVEL 0 INTRO + NAME
# -----------------------------------
if st.session_state.level == 0:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📖 Mission Briefing")

    st.write("""
    You are trapped inside the Digital World.
    
    Your identity was stolen by **PHANTOM AI**, a hacker powered by artificial intelligence.
    
    Your goal is to defeat cyber threats and recover your digital identity.
    
    Your AI assistant is **AURA**.
    """)

    st.session_state.player_name = st.text_input("Enter your agent name:", value=st.session_state.player_name)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Start Mission"):
        if st.session_state.player_name.strip() == "":
            st.error("Please enter your agent name first.")
        else:
            st.session_state.level = 1
            st.rerun()

# -----------------------------------
# LEVEL 1 PASSWORD
# -----------------------------------
elif st.session_state.level == 1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🔐 Level 1: Password Panic")
    st.write("Build a strong password before PHANTOM AI brute-forces your account.")
    st.markdown("</div>", unsafe_allow_html=True)

    password = st.text_input("Enter a password:")

    if st.button("🧪 Test Password"):
        strength = password_strength(password)

        st.write("🔎 Strength Meter:")
        st.progress(strength / 5)

        if strength <= 2:
            st.markdown("<div class='danger'>❌ Weak password. Hacker cracked it.</div>", unsafe_allow_html=True)
        elif strength == 3:
            st.warning("⚠️ Medium password. Better, but still risky.")
        else:
            st.success("✅ Strong password! Firewall secured.")
            st.session_state.score += 30
            st.session_state.level = 2
            st.rerun()

    if st.button("🤖 Ask AURA"):
        aura_hint("Use 10+ characters and mix uppercase, lowercase, numbers, and symbols like @ or !")

# -----------------------------------
# LEVEL 2 PHISHING (3 ROUNDS)
# -----------------------------------
elif st.session_state.level == 2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader(f"🎣 Level 2: Phishing Trap (Round {st.session_state.phish_round}/3)")
    st.write("Decide if the message is SAFE or PHISHING.")
    st.markdown("</div>", unsafe_allow_html=True)

    phishing_messages = [
        ("URGENT!!! Your bank account is locked. Verify now: bank-secure-login.net", "PHISHING"),
        ("Hey, are you free later? We need your help on the science project.", "SAFE"),
        ("Congratulations! You won a FREE gift card. Claim here: giftcard-winner.com", "PHISHING"),
        ("Reminder: School starts at 8:00 AM tomorrow.", "SAFE"),
        ("Security Alert: Suspicious login detected. Confirm your password immediately!", "PHISHING"),
        ("Your teacher posted new homework on Google Classroom.", "SAFE"),
        ("Your Netflix payment failed. Update your card here: netflix-billing-support.net", "PHISHING"),
    ]

    if st.session_state.current_msg is None:
        st.session_state.current_msg = random.choice(phishing_messages)

    msg, correct = st.session_state.current_msg

    st.write(f"📩 **Message:** {msg}")

    if st.button("🧠 Run AURA Scan"):
        scan_animation()
        score = risk_score(msg)
        st.write("AURA Risk Meter:")
        st.progress(score / 100)
        st.caption(f"Risk Score: {score}/100")

    col1, col2 = st.columns(2)

    def handle_answer(choice):
        if choice == correct:
            st.success("✅ Correct decision!")
            st.session_state.score += 20
            st.session_state.phish_correct += 1
        else:
            st.error("❌ Wrong decision!")
            st.session_state.score -= 10

        st.session_state.phish_round += 1
        st.session_state.current_msg = None

        if st.session_state.phish_round > 3:
            st.session_state.level = 3

        st.rerun()

    with col1:
        if st.button("✅ SAFE"):
            handle_answer("SAFE")

    with col2:
        if st.button("🚨 PHISHING"):
            handle_answer("PHISHING")

    if st.button("🤖 Ask AURA"):
        aura_hint("Phishing messages often pressure you, use suspicious links, or ask for passwords.")

# -----------------------------------
# LEVEL 3 DEEPFAKE
# -----------------------------------
elif st.session_state.level == 3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🎭 Level 3: Deepfake Danger")
    st.write("Someone uploaded a video of you saying something harmful. Detect if it's fake.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("""
    **Video Evidence:**
    - Voice sounds robotic  
    - Lips slightly misaligned  
    - Blinking is unnatural  
    - Lighting flickers  
    """)

    choice = st.radio("Is this video REAL or a DEEPFAKE?", ["REAL", "DEEPFAKE"])

    if st.button("Submit Answer"):
        if choice == "DEEPFAKE":
            st.success("✅ Correct! It was a deepfake.")
            st.session_state.score += 30
            st.session_state.level = 4
            st.rerun()
        else:
            st.error("❌ Wrong! It was a deepfake.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA"):
        aura_hint("Deepfakes often have weird blinking, inconsistent shadows, and robotic audio.")

# -----------------------------------
# LEVEL 4 CREATOR PROTECTION (WATERMARK MINI GAME)
# -----------------------------------
elif st.session_state.level == 4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🎨 Level 4: Creator Protection")
    st.write("PHANTOM AI is stealing your artwork. Choose the best defense.")
    st.markdown("</div>", unsafe_allow_html=True)

    option = st.radio("What protects your digital art the MOST?", [
        "Post the artwork with no watermark",
        "Add a visible watermark + keep original files",
        "Send your art to strangers to prove ownership"
    ])

    if st.button("Protect Artwork"):
        if option == "Add a visible watermark + keep original files":
            st.success("✅ Correct! Watermarks + original files help prove ownership.")
            st.session_state.score += 25
            st.session_state.level = 5
            st.rerun()
        else:
            st.error("❌ That makes stealing easier.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA"):
        aura_hint("Creators should watermark art, save originals, and use copyright tools when possible.")

# -----------------------------------
# LEVEL 5 FINAL BOSS
# -----------------------------------
elif st.session_state.level == 5:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("💀 Final Level: Boss Fight — PHANTOM AI")
    st.write("PHANTOM AI launches an AI-driven cyberattack on your identity.")
    st.write("Choose the best defense strategy.")
    st.markdown("</div>", unsafe_allow_html=True)

    boss_choice = st.radio("Choose your defense move:", [
        "Ignore software updates",
        "Enable encryption + 2FA + strong passwords + updates",
        "Share your password with friends",
        "Click random links to confuse the hacker"
    ])

    if st.button("⚔️ Execute Defense"):
        if boss_choice == "Enable encryption + 2FA + strong passwords + updates":
            st.success("🏆 You defeated PHANTOM AI and reclaimed your identity!")
            st.session_state.score += 60
            st.session_state.level = 6
            st.rerun()
        else:
            st.markdown("<div class='danger'>💥 PHANTOM AI hacked you. Wrong move.</div>", unsafe_allow_html=True)
            st.session_state.score -= 20

    if st.button("🤖 Ask AURA"):
        aura_hint("The best defense is layered: updates + encryption + 2FA + strong passwords.")

# -----------------------------------
# LEVEL 6 WIN SCREEN + LEADERBOARD
# -----------------------------------
elif st.session_state.level == 6:
    st.subheader("🎉 MISSION COMPLETE")
    st.write(f"Agent **{st.session_state.player_name}**, you escaped the Digital World.")

    st.write(f"### ⭐ Final Score: {st.session_state.score}")
    st.write(f"### 🎣 Phishing Accuracy: {st.session_state.phish_correct}/3")
    st.write(f"### 🤖 Hints Used: {st.session_state.hints_used}")

    if st.session_state.score >= 160:
        st.success("🥇 Rank: DIGITAL LEGEND")
        st.balloons()
    elif st.session_state.score >= 120:
        st.success("🥈 Rank: DIGITAL GUARDIAN")
    elif st.session_state.score >= 80:
        st.warning("🥉 Rank: FIREWALL FIGHTER")
    else:
        st.error("🔰 Rank: CYBER ROOKIE")

    st.info("🧠 Final Tip: Strong passwords + 2FA + phishing awareness protect your identity and creativity online.")

    # Save Score Button
    if not st.session_state.saved:
        if st.button("💾 Save Score to Leaderboard"):
            save_score(st.session_state.player_name, st.session_state.score)
            st.session_state.saved = True
            st.success("Saved successfully!")

    st.subheader("🏆 Top Agents Leaderboard")
    leaderboard = load_leaderboard()
    st.dataframe(leaderboard, use_container_width=True)

    if st.button("🔄 Restart Game"):
        restart_game()
        st.rerun()
