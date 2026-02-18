import streamlit as st
import random
import re
import time
import pandas as pd
import os
import matplotlib.pyplot as plt

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="CyberShield V4", page_icon="🛡️", layout="centered")

# -----------------------------------
# STYLING (DIGITAL BLUE THEME)
# -----------------------------------
st.markdown("""
<style>
    body {
        background: radial-gradient(circle at top, #0b2a4a, #050b1e, #020512);
        color: white;
    }
    .title {
        font-size: 55px;
        font-weight: 900;
        text-align: center;
        color: #00fff2;
        text-shadow: 0px 0px 30px rgba(0,255,242,0.8);
        margin-bottom: -10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #b0b0b0;
        margin-bottom: 30px;
    }
    .panel {
        padding: 20px;
        border-radius: 18px;
        background-color: rgba(255,255,255,0.04);
        border: 1px solid rgba(0,255,242,0.25);
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 0px 20px rgba(0,255,242,0.15);
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
        background-color: rgba(0,255,242,0.08);
        border: 1px solid rgba(0,255,242,0.35);
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .scan {
        font-family: monospace;
        color: #00fff2;
        font-size: 16px;
        text-shadow: 0px 0px 10px rgba(0,255,242,0.6);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# LEADERBOARD FILE
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
        return data.sort_values(by="Score", ascending=False).head(10)
    return pd.DataFrame(columns=["Name", "Score"])

# -----------------------------------
# SESSION STATE INIT
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

if "deepfake_correct" not in st.session_state:
    st.session_state.deepfake_correct = 0

if "password_success" not in st.session_state:
    st.session_state.password_success = 0

if "current_msg" not in st.session_state:
    st.session_state.current_msg = None

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "saved" not in st.session_state:
    st.session_state.saved = False

if "sound_on" not in st.session_state:
    st.session_state.sound_on = True

# -----------------------------------
# GAME FUNCTIONS
# -----------------------------------
def restart_game():
    for key in list(st.session_state.keys()):
        if key not in ["sound_on"]:
            del st.session_state[key]
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.hints_used = 0
    st.session_state.phish_round = 1
    st.session_state.phish_correct = 0
    st.session_state.deepfake_correct = 0
    st.session_state.password_success = 0
    st.session_state.current_msg = None
    st.session_state.player_name = ""
    st.session_state.saved = False

def aura_hint(text):
    st.session_state.hints_used += 1
    st.markdown(f"<div class='aura'>🤖 <b>AURA:</b> {text}</div>", unsafe_allow_html=True)

def password_strength(password):
    points = 0
    if len(password) >= 10: points += 1
    if re.search(r"[A-Z]", password): points += 1
    if re.search(r"[a-z]", password): points += 1
    if re.search(r"[0-9]", password): points += 1
    if re.search(r"[@$!%*?&]", password): points += 1
    return points

def risk_score(message):
    risk = 0
    suspicious_words = ["urgent", "verify", "password", "locked", "click", "winner", "free", "claim", "confirm", "payment"]
    for word in suspicious_words:
        if word in message.lower():
            risk += 15
    if "http" in message.lower() or ".com" in message.lower() or ".net" in message.lower():
        risk += 25
    if "!!!" in message:
        risk += 15
    if len(message) > 80:
        risk += 10
    return min(risk, 100)

def terminal_typing(text):
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"<p class='scan'>{output}</p>", unsafe_allow_html=True)
        time.sleep(0.02)

def scan_animation():
    lines = [
        "[AURA SCAN] Booting AI security scanner...",
        "[AURA SCAN] Running pattern detection...",
        "[AURA SCAN] Checking suspicious domains...",
        "[AURA SCAN] Detecting urgency manipulation...",
        "[AURA SCAN] Applying neural phishing classifier...",
        "[AURA SCAN] Generating risk score..."
    ]
    for line in lines:
        st.markdown(f"<p class='scan'>{line}</p>", unsafe_allow_html=True)
        time.sleep(0.35)

def play_sound(effect="success"):
    if not st.session_state.sound_on:
        return
    if effect == "success":
        st.toast("🔊 *Beep!* (Success Sound)")
    elif effect == "fail":
        st.toast("🔊 *Buzz!* (Fail Sound)")
    elif effect == "scan":
        st.toast("🔊 *Scanning...*")

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown('<div class="title">🛡️ CyberShield V4</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI + Cybersecurity Game | Dark Digital Blue Edition</div>', unsafe_allow_html=True)

colA, colB = st.columns(2)
with colA:
    st.write(f"### ⭐ Score: {st.session_state.score}")
with colB:
    st.session_state.sound_on = st.toggle("🔊 Sound Effects", value=st.session_state.sound_on)

progress_value = st.session_state.level / 7
st.progress(progress_value)

st.divider()

# -----------------------------------
# LEVEL 0 INTRO
# -----------------------------------
if st.session_state.level == 0:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("📖 Mission Briefing")
    st.write("""
    Your identity has been stolen by **PHANTOM AI**.
    
    You are trapped inside the Digital World.
    
    Complete cybersecurity challenges to escape.
    
    Your AI assistant: **AURA** 🤖
    """)
    st.session_state.player_name = st.text_input("Enter your Agent Name:", value=st.session_state.player_name)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Start Mission"):
        if st.session_state.player_name.strip() == "":
            st.error("Enter a name first.")
        else:
            terminal_typing("ACCESS GRANTED... ENTERING CYBERSPACE...")
            st.session_state.level = 1
            st.rerun()

# -----------------------------------
# LEVEL 1 PASSWORD
# -----------------------------------
elif st.session_state.level == 1:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🔐 Level 1: Password Panic")
    st.write("Create a password strong enough to survive PHANTOM AI's brute-force attack.")
    st.markdown("</div>", unsafe_allow_html=True)

    password = st.text_input("Enter your password:")

    if st.button("🧪 Test Password"):
        strength = password_strength(password)
        st.write("Strength Meter:")
        st.progress(strength / 5)

        if strength <= 2:
            play_sound("fail")
            st.markdown("<div class='danger'>❌ Weak password. Hacker cracked it.</div>", unsafe_allow_html=True)
            st.session_state.score -= 5
        elif strength == 3:
            st.warning("⚠️ Medium password. Better, but risky.")
            st.session_state.score += 5
        else:
            play_sound("success")
            st.success("✅ Strong password! Firewall secured.")
            st.session_state.score += 35
            st.session_state.password_success = 1
            st.session_state.level = 2
            st.rerun()

    if st.button("🤖 Ask AURA"):
        aura_hint("Use 10+ characters with uppercase, lowercase, numbers, and symbols like @ or !")

# -----------------------------------
# LEVEL 2 PHISHING (3 ROUNDS)
# -----------------------------------
elif st.session_state.level == 2:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader(f"🎣 Level 2: Phishing Trap (Round {st.session_state.phish_round}/3)")
    st.write("Identify if the message is SAFE or PHISHING.")
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
        play_sound("scan")
        scan_animation()
        score = risk_score(msg)
        st.write("AURA Risk Meter:")
        st.progress(score / 100)
        st.caption(f"Risk Score: {score}/100")

    col1, col2 = st.columns(2)

    def handle_answer(choice):
        if choice == correct:
            play_sound("success")
            st.success("✅ Correct decision!")
            st.session_state.score += 25
            st.session_state.phish_correct += 1
        else:
            play_sound("fail")
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
        aura_hint("Phishing uses urgency + fake links + asks for private information.")

# -----------------------------------
# LEVEL 3 DEEPFAKE
# -----------------------------------
elif st.session_state.level == 3:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🎭 Level 3: Deepfake Danger")
    st.write("Someone uploaded a fake video pretending to be you.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("""
    **Clues:**
    - Robotic voice  
    - Lips slightly off  
    - Unnatural blinking  
    - Shadows inconsistent  
    """)

    choice = st.radio("REAL or DEEPFAKE?", ["REAL", "DEEPFAKE"])

    if st.button("Submit Answer"):
        if choice == "DEEPFAKE":
            play_sound("success")
            st.success("✅ Correct! It was AI-generated.")
            st.session_state.score += 35
            st.session_state.deepfake_correct = 1
            st.session_state.level = 4
            st.rerun()
        else:
            play_sound("fail")
            st.error("❌ Wrong! It was a deepfake.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA"):
        aura_hint("Deepfakes often have mismatched lip sync, robotic audio, and unnatural facial movement.")

# -----------------------------------
# LEVEL 4 CREATOR PROTECTION
# -----------------------------------
elif st.session_state.level == 4:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🎨 Level 4: Creator Protection")
    st.write("PHANTOM AI is stealing your artwork. Choose the best defense.")
    st.markdown("</div>", unsafe_allow_html=True)

    option = st.radio("What protects your creativity the MOST?", [
        "Post art with no watermark",
        "Add watermark + keep original files + copyright proof",
        "Send your art to random people for attention"
    ])

    if st.button("Protect Artwork"):
        if option == "Add watermark + keep original files + copyright proof":
            play_sound("success")
            st.success("✅ Correct! You protected your digital creativity.")
            st.session_state.score += 30
            st.session_state.level = 5
            st.rerun()
        else:
            play_sound("fail")
            st.error("❌ That makes stealing easier.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA"):
        aura_hint("Creators should watermark work, save originals, and use copyright proof like timestamps.")

# -----------------------------------
# LEVEL 5 SECRET LEVEL (UNLOCK CONDITION)
# -----------------------------------
elif st.session_state.level == 5:
    if st.session_state.phish_correct == 3 and st.session_state.deepfake_correct == 1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("🕵️ SECRET LEVEL: Data Leak Detector")
        st.write("AURA found a hidden data leak in your profile. Fix it to earn a bonus.")

        option = st.radio("Which info is MOST dangerous to share publicly?", [
            "Favorite movie",
            "Home address + school name",
            "Favorite color"
        ])

        if st.button("Fix Leak"):
            if option == "Home address + school name":
                play_sound("success")
                st.success("✅ Leak patched! Bonus points earned.")
                st.session_state.score += 40
                st.session_state.level = 6
                st.rerun()
            else:
                play_sound("fail")
                st.error("❌ Wrong. That leak could lead to stalking/identity theft.")
                st.session_state.score -= 10

        if st.button("🤖 Ask AURA"):
            aura_hint("Never share location details, addresses, or school names publicly.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.session_state.level = 6
        st.rerun()

# -----------------------------------
# LEVEL 6 FINAL BOSS
# -----------------------------------
elif st.session_state.level == 6:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("💀 FINAL BOSS: PHANTOM AI")
    st.write("PHANTOM AI launches an AI-powered attack on your identity.")
    st.write("Choose your best defense strategy.")
    st.markdown("</div>", unsafe_allow_html=True)

    boss_choice = st.radio("Choose your defense move:", [
        "Ignore security updates",
        "Enable encryption + 2FA + strong passwords + updates",
        "Share passwords with friends",
        "Click random links to confuse the hacker"
    ])

    if st.button("⚔️ Execute Defense"):
        if boss_choice == "Enable encryption + 2FA + strong passwords + updates":
            play_sound("success")
            st.success("🏆 You defeated PHANTOM AI and reclaimed your identity!")
            st.session_state.score += 70
            st.session_state.level = 7
            st.rerun()
        else:
            play_sound("fail")
            st.markdown("<div class='danger'>💥 PHANTOM AI hacked you. Wrong move.</div>", unsafe_allow_html=True)
            st.session_state.score -= 20

    if st.button("🤖 Ask AURA"):
        aura_hint("Layered security is strongest: updates + encryption + 2FA + strong passwords.")

# -----------------------------------
# LEVEL 7 WIN SCREEN + DASHBOARD
# -----------------------------------
elif st.session_state.level == 7:
    st.subheader("🎉 MISSION COMPLETE")
    st.write(f"Agent **{st.session_state.player_name}**, you escaped the Digital World.")

    st.write(f"### ⭐ Final Score: {st.session_state.score}")
    st.write(f"### 🎣 Phishing Accuracy: {st.session_state.phish_correct}/3")
    st.write(f"### 🤖 Hints Used: {st.session_state.hints_used}")

    # RANKING + SECRET ENDING
    if st.session_state.score >= 200:
        st.success("👑 SECRET ENDING UNLOCKED: CYBER LEGEND")
        st.balloons()
        st.write("🔥 AURA upgrades you into the *Digital Guardian Council*.")
    elif st.session_state.score >= 150:
        st.success("🥇 Rank: DIGITAL GUARDIAN")
    elif st.session_state.score >= 100:
        st.warning("🥈 Rank: FIREWALL FIGHTER")
    else:
        st.error("🥉 Rank: CYBER ROOKIE")

    st.info("🧠 Final Tip: Cybersecurity = strong passwords + 2FA + phishing awareness + privacy protection.")

    # DASHBOARD CHART
    st.subheader("📊 Mission Stats Dashboard")

    labels = ["Phishing Correct", "Phishing Wrong", "Hints Used"]
    phishing_wrong = 3 - st.session_state.phish_correct
    values = [st.session_state.phish_correct, phishing_wrong, st.session_state.hints_used]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)

    # LEADERBOARD SAVE
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

