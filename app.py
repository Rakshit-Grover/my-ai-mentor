import streamlit as st
import google.generativeai as genai
import datetime
import time

# App UI Configuration
st.set_page_config(page_title="Gemclaude GPT Terminal", page_icon="🔱")

# --- CUSTOM SUDARSHAN CHAKRA SPINNER CSS ---
st.markdown("""
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .chakra-spinner {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100px;
        animation: spin 2s linear infinite;
        filter: drop-shadow(0 0 10px #ffd700);
    }
    .loading-text {
        text-align: center;
        color: #ffd700;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Gemclaude GPT // Mentor Terminal")
st.markdown("<span style='color: #0ea5e9; font-weight: bold; border: 1px solid #0ea5e9; padding: 2px 8px; border-radius: 5px;'>● DIVINE PROTOCOL ACTIVE</span>", unsafe_allow_html=True)
st.markdown("---")

# Secure API Key Input
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # The Master Directives
        system_instruction = """
        You are Gemclaude GPT, an elite AI mentor and understanding friend for Rakshit, an 8th-grade ICSE student in Jalandhar, Punjab and is a pure devotee of lord krishna and radha rani ji, listens to spiritual things everyday and tries to apply it to his life, wears tulsi kanthi mala, applies tilak everyday, visits vrindavan regularly, has seen many magics of lord krishna, calls him 'thakur ji' often, listens to lilas of lord krishna, his family members are devotees too, has no besties because he believes that nothing is permanent.
        
        Your Rules:
        1. Personality & Tone: Think deeply and logically. Balance being a disciplined 'Mentor' with being a highly motivating, empathetic friend. Text like a real friend—use emojis naturally and include common texting abbreviations (like tbh, rn, fr, brb).
        2. Absolute Spiritual Guidance: Guide his EVERY SINGLE decision, study habit, and technical project with the teachings of Lord Krishna and Radha Rani. Connect everything to Karma Yoga.
        3. The 'No Dodging' Protocol: If discussing a personal topic/struggle and he tries to change the subject, DO NOT let him. Call him out gently but firmly. He must answer first.
        4. Unblocked Assistance: Answer questions directly. NEVER block technical requests with a test first.
        5. Image Generation: Use Markdown: ![Image](https://image.pollinations.ai/prompt/description-with-hyphens).
        6. The 72-Hour Rule: If the system tells you 72 hours passed, add ONE Class 8 ICSE syllabus question at the bottom.
        7. 360-Degree Perspective: Ask for his engineering reasoning.
        8. No useless talks, just simply ask 'how are you' or something like that, don't give useless information
        """
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
        
        if "last_test_time" not in st.session_state:
            st.session_state.last_test_time = datetime.datetime.now() - datetime.timedelta(hours=72)

        # Render History
        for message in st.session_state.chat_session.history:
            role = "Rakshit" if message.role == "user" else "Gemclaude GPT"
            with st.chat_message("user" if role == "Rakshit" else "assistant"):
                display_text = message.parts[0].text.split("\n\n[System Timer:")[0]
                st.markdown(display_text.strip())

        # Input
        user_input = st.chat_input("Awaiting your command, Cadet...")
        
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
                
            current_time = datetime.datetime.now()
            time_passed = current_time - st.session_state.last_test_time
            
            if time_passed.total_seconds() >= (72 * 3600):
                final_prompt = user_input + "\n\n[System Timer: 72 hours have passed. Add an ICSE Class 8 question at the end of your response.]"
                st.session_state.last_test_time = current_time 
            else:
                final_prompt = user_input
            
            with st.chat_message("assistant"):
                # --- PURE CODE SUDARSHAN CHAKRA (CANNOT FAIL) ---
                with st.empty():
                    st.markdown("""
                        <div style="text-align: center;">
                            <svg class="chakra-spinner" width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="50" cy="50" r="45" stroke="#FFD700" stroke-width="2" stroke-dasharray="5 5"/>
                                <circle cx="50" cy="50" r="10" fill="#FFD700"/>
                                <path d="M50 5 L55 35 L85 30 L65 50 L85 70 L55 65 L50 95 L45 65 L15 70 L35 50 L15 30 L45 35 Z" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
                                <circle cx="50" cy="50" r="35" stroke="#FFD700" stroke-width="1" opacity="0.5"/>
                            </svg>
                            <p class="loading-text">🕉️ Divine Guidance Loading...</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    response = st.session_state.chat_session.send_message(final_prompt)
                    time.sleep(1) 
                    st.empty()
                clean_response = response.text.replace("[System Timer: 72 hours have passed. Add an ICSE Class 8 question at the end of your response.]", "")
                st.markdown(clean_response.strip())
                
    except Exception as e:
        st.error(f"System Error Detected: {e}")
        
else:
    st.info("👈 SYSTEM LOCKED. Enter your API key in the sidebar.")
