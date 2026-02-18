import streamlit as st
import random
import re

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="CyberShield: Identity Rescue", page_icon="🛡️", layout="centered")

# -------------------------------
# SESSION STATE SETUP
# -------------------------------
if "level" not in st.session_state:
    st.session_state.level = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# -------------------------------
# FUNCTIONS
# -------------------------------
def restart_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.hints_used = 0
    st.session_state.game_over = False


def aura_hint(text):
    st.session_state.hints_used += 1
    st.info(f"🤖 AURA Hint: {text}")


def password_strength(password):
    score = 0
    if len(password) >= 10:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[@$!%*?&]", password):
        score += 1
    return score


# -------------------------------
# HEADER
# -------------------------------
st.title("🛡️ CyberShield: Identity Rescue")
st.write("**Theme:** AI + Cybersecurity — Protect your identity and creativity online.")
st.write(f"### ⭐ Score: {st.session_state.score} | 🤖 Hints Used: {st.session_state.hints_used}")

st.divider()

# -------------------------------
# INTRO SCREEN
# -------------------------------
if st.session_state.level == 0:
    st.subheader("📖 Story Intro")
    st.write("""
    You wake up inside the **Digital World**.
    
    Your online identity has been stolen by a hacker called **PHANTOM AI**.
    
    Luckily, you have an AI assistant named **AURA**.
    
    To escape, you must defeat cyber threats through challenges.
    """)

    if st.button("🚀 Start Mission"):
        st.session_state.level = 1
        st.rerun()


# -------------------------------
# LEVEL 1: PASSWORD PANIC
# -------------------------------
elif st.session_state.level == 1:
    st.subheader("🔐 Level 1: Password Panic")
    st.write("A hacker is trying to brute-force your password. Create a strong password to survive.")

    password = st.text_input("Enter a password:")

    if st.button("Check Password Strength"):
        strength = password_strength(password)

        if strength <= 2:
            st.error("❌ Weak password! Hacker cracked it.")
            st.write("Try again with more symbols, numbers, and length.")
        elif strength == 3:
            st.warning("⚠️ Medium password. Better, but still risky.")
            st.write("Add more symbols or make it longer.")
        else:
            st.success("✅ Strong password! You blocked the hacker.")
            st.session_state.score += 20
            st.session_state.level = 2
            st.rerun()

    if st.button("🤖 Ask AURA for help"):
        aura_hint("Use at least 10 characters, include uppercase, lowercase, numbers, and symbols like @ or !.")


# -------------------------------
# LEVEL 2: PHISHING TRAP
# -------------------------------
elif st.session_state.level == 2:
    st.subheader("🎣 Level 2: Phishing Trap")
    st.write("You received a suspicious message. Decide if it's SAFE or PHISHING.")

    phishing_messages = [
        ("URGENT! Your bank account is locked. Click here: bank-login-secure.com", "PHISHING"),
        ("Hey! Are you coming to the study group tomorrow at 5pm?", "SAFE"),
        ("Your package delivery failed. Confirm your address now: fedex-delivery-support.net", "PHISHING"),
        ("Reminder: School meeting at 3pm in room 210.", "SAFE"),
        ("Congratulations! You won $1000. Claim now by entering your password.", "PHISHING")
    ]

    if "current_msg" not in st.session_state:
        st.session_state.current_msg = random.choice(phishing_messages)

    msg, correct = st.session_state.current_msg
    st.write(f"📩 **Message:** {msg}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ SAFE"):
            if correct == "SAFE":
                st.success("Correct! This message is safe.")
                st.session_state.score += 15
            else:
                st.error("Wrong! That was phishing.")
                st.session_state.score -= 5

            st.session_state.level = 3
            st.rerun()

    with col2:
        if st.button("🚨 PHISHING"):
            if correct == "PHISHING":
                st.success("Correct! You avoided a phishing attack.")
                st.session_state.score += 15
            else:
                st.error("Wrong! That message was safe.")
                st.session_state.score -= 5

            st.session_state.level = 3
            st.rerun()

    if st.button("🤖 Ask AURA for help"):
        aura_hint("Look for urgency, weird links, spelling mistakes, or requests for passwords/personal info.")


# -------------------------------
# LEVEL 3: DEEPFAKE DANGER
# -------------------------------
elif st.session_state.level == 3:
    st.subheader("🎭 Level 3: Deepfake Danger")
    st.write("Someone uploaded a video of YOU saying something harmful. Is it real or fake?")

    st.write("""
    **Video Clues:**
    - The voice sounds slightly robotic  
    - Lips do not match perfectly  
    - Lighting flickers unnaturally  
    """)

    choice = st.radio("Is the video real or a deepfake?", ["REAL", "DEEPFAKE"])

    if st.button("Submit Answer"):
        if choice == "DEEPFAKE":
            st.success("✅ Correct! It was a deepfake.")
            st.session_state.score += 20
            st.session_state.level = 4
            st.rerun()
        else:
            st.error("❌ Wrong! It was a deepfake. You got tricked.")
            st.session_state.score -= 10

    if st.button("🤖 Ask AURA for help"):
        aura_hint("Deepfakes often have lip-sync errors, weird blinking, robotic voice tones, or unnatural shadows.")


# -------------------------------
# LEVEL 4: PRIVACY SETTINGS MAZE
# -------------------------------
elif st.session_state.level == 4:
    st.subheader("👁️ Level 4: Privacy Settings Maze")
    st.write("Your profile is leaking personal data. Choose the BEST privacy setting.")

    option = st.radio("Which setting is most important to protect your identity?",
                      ["Keep location tagging ON", "Enable Two-Factor Authentication (2FA)", "Make profile public"])

    if st.button("Lock In Choice"):
        if option == "Enable Two-Factor Authentication (2FA)":
            st.success("✅ Correct! 2FA is one of the strongest protections.")
            st.session_state.score += 25
            st.session_state.level = 5
            st.rerun()
        else:
            st.error("❌ Not the best choice. That increases risk.")
            st.session_state.score -= 5

    if st.button("🤖 Ask AURA for help"):
        aura_hint("2FA stops hackers even if they steal your password.")


# -------------------------------
# LEVEL 5: FINAL BOSS
# -------------------------------
elif st.session_state.level == 5:
    st.subheader("💀 Level 5: Boss Battle — PHANTOM AI")
    st.write("PHANTOM AI attacks your account with AI-powered hacking tools. Choose your defense move!")

    boss_choice = st.radio("Choose your defense:", [
        "Share your password with a friend",
        "Enable encryption + 2FA + strong passwords",
        "Click random links to confuse the hacker",
        "Turn off security updates"
    ])

    if st.button("⚔️ Fight!"):
        if boss_choice == "Enable encryption + 2FA + strong passwords":
            st.success("🏆 You defeated PHANTOM AI!")
            st.session_state.score += 40
            st.session_state.level = 6
            st.rerun()
        else:
            st.error("💥 PHANTOM AI hacked you. Bad move.")
            st.session_state.score -= 15

    if st.button("🤖 Ask AURA for help"):
        aura_hint("Best defense is layered security: strong passwords, 2FA, encryption, and updates.")


# -------------------------------
# WIN SCREEN
# -------------------------------
elif st.session_state.level == 6:
    st.subheader("🎉 Mission Complete!")
    st.write("You escaped the Digital World and protected your identity!")

    final_score = st.session_state.score
    hints = st.session_state.hints_used

    st.write(f"### ⭐ Final Score: {final_score}")
    st.write(f"### 🤖 Total Hints Used: {hints}")

    if final_score >= 90:
        st.success("🥇 Rank: Digital Guardian")
    elif final_score >= 60:
        st.warning("🥈 Rank: Firewall Fighter")
    else:
        st.error("🥉 Rank: Cyber Rookie")

    st.write("### 🧠 Cyber Tip:")
    st.info("Always use strong passwords + 2FA. Never click suspicious links. Protect your digital identity!")

    if st.button("🔄 Play Again"):
        restart_game()
        st.rerun()
