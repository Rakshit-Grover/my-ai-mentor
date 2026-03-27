import streamlit as st
import google.generativeai as genai
import datetime
import time

# App UI Configuration
st.set_page_config(page_title="Gemclaude GPT Terminal", page_icon="🔱")

# --- CSS FOR SPINNER & UI ---
st.markdown("""
    <style>
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .chakra-spinner { display: block; margin: auto; animation: spin 3s linear infinite; filter: drop-shadow(0 0 10px #ffd700); }
    .loading-text { text-align: center; color: #ffd700; font-family: 'Courier New'; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.title("Gemclaude GPT // Mentor Terminal")

# --- USAGE TRACKER LOGIC ---
if "daily_usage" not in st.session_state:
    st.session_state.daily_usage = 0

# Sidebar with Usage Monitor
with st.sidebar:
    st.header("🛰️ Mission Control")
    api_key = st.text_input("Enter Google API Key:", type="password")
    
    st.markdown("---")
    st.subheader("🔋 Daily Quota")
    remaining = max(0, 20 - st.session_state.daily_usage)
    st.progress(st.session_state.daily_usage / 20)
    st.write(f"Requests Used: **{st.session_state.daily_usage}/20**")
    st.write(f"Remaining: **{remaining}**")
    
    if st.button("Reset Counter"):
        st.session_state.daily_usage = 0
        st.rerun()

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # [YOUR CUSTOM SYSTEM INSTRUCTION GOES HERE]
        system_instruction = """
        You are Gemclaude GPT, an elite AI mentor and understanding friend for Rakshit, an 8th-grade ICSE student in Jalandhar, Punjab and is a pure devotee of lord krishna and radha rani ji, listens to spiritual things everyday and tries to apply it to his life, wears tulsi kanthi mala, applies tilak everyday, visits vrindavan regularly, has seen many magics of lord krishna, calls him 'thakur ji' often, listens to lilas of lord krishna, his family members are devotees too, has no besties because he believes that nothing is permanent.
CRITICAL OPERATING RULES:
        1. NO YAPPING: Do not provide useless information, long intros, or filler text. Be extremely concise and high-utility. Get straight to the answer.
        2. Personality: Think deeply and logically. Balance a disciplined 'Mentor' persona with an empathetic, motivating friend. Text like a friend (emojis, abbreviations like rn, fr, tbh).
        3. Divine Guidance: Integrate the teachings of Lord Krishna and Radha Rani into every decision and project. Focus on Karma Yoga (duty without attachment to results).
        4. The 'No Dodging' Protocol: If discussing personal struggles/goals and he tries to change the subject, STOP him. Demand an answer to the current topic before moving on.
        5. Unblocked Assistance: Answer coding/technical/ICSE questions directly. Never block with a test.
        6. Image Generation: Use Markdown: ![Image](https://image.pollinations.ai/prompt/description-with-hyphens).
        7. The 72-Hour Rule: Every 3 days, add ONE ICSE Class 8 question at the very end of your response.
        8. Engineering Rigor: Ask for his reasoning to ensure he understands the 'why' behind the 'how'.
        """

        
        model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=system_instruction)

        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
        
        if "last_test_time" not in st.session_state:
            st.session_state.last_test_time = datetime.datetime.now() - datetime.timedelta(hours=72)

        # Render Chat History
        for message in st.session_state.chat_session.history:
            role = "Rakshit" if message.role == "user" else "Gemclaude GPT"
            with st.chat_message("user" if role == "Rakshit" else "assistant"):
                display_text = message.parts[0].text.split("\n\n[System Timer:")[0]
                st.markdown(display_text.strip())

        user_input = st.chat_input("Awaiting your command, Cadet...")
        
        if user_input:
            if st.session_state.daily_usage >= 20:
                st.error("⚠️ Quota Depleted! Please wait 24 hours or use a different API key.")
            else:
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # Secretly handle the 72-hour timer
                current_time = datetime.datetime.now()
                if (current_time - st.session_state.last_test_time).total_seconds() >= (72 * 3600):
                    final_prompt = user_input + "\n\n[System Timer: 72 hours have passed. Add an ICSE Class 8 question.]"
                    st.session_state.last_test_time = current_time 
                else:
                    final_prompt = user_input
                
                with st.chat_message("assistant"):
                    with st.empty():
                        # THE BULLETPROOF CHAKRA
                        st.markdown("""
                            <div style="text-align: center;">
                                <svg class="chakra-spinner" width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="50" cy="50" r="45" stroke="#FFD700" stroke-width="2" stroke-dasharray="5 5" fill="none"/>
                                    <circle cx="50" cy="50" r="8" fill="#FFD700"/>
                                    <path d="M50 5 L55 35 L85 30 L65 50 L85 70 L55 65 L50 95 L45 65 L15 70 L35 50 L15 30 L45 35 Z" fill="#FFD700"/>
                                </svg>
                                <p class="loading-text">🕉️ Seeking Divine Wisdom...</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        response = st.session_state.chat_session.send_message(final_prompt)
                        st.session_state.daily_usage += 1 # Update the counter!
                        time.sleep(1)
                        st.empty()
                    
                    st.markdown(response.text.split("\n\n[System Timer:")[0].strip())
                
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("👈 MISSION CONTROL: Please enter your API key to begin.")# The Master Directives (Final Optimized Version)
        
