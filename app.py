import streamlit as st
import google.generativeai as genai

# App UI Configuration
st.set_page_config(page_title="Rakshit's AI Mentor", page_icon="🚀")
st.title("My Personal AI Mentor (Diagnostic Mode)")
st.markdown("---")

# Secure API Key Input via Sidebar
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- SMART AUTO-DETECT ---
        # This asks Google: "What models is this API key allowed to use?"
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Clean up the name
                clean_name = m.name.replace('models/', '')
                available_models.append(clean_name)
        
        if not available_models:
            st.error("Error: Your API key is valid, but your Google account doesn't have access to any text models right now.")
        else:
            # Tell the user what models were found
            st.success(f"Connection successful! Found these brains: {', '.join(available_models)}")
            
            # Pick the best available model automatically
            working_model = available_models[0] # Default to the first one it finds
            for name in available_models:
                if "1.5-flash" in name:
                    working_model = name
                    break
            
            st.info(f"Auto-selected model: **{working_model}**")
            
            # Connect to the chosen model (Personality temporarily removed for safety)
            model = genai.GenerativeModel(model_name=working_model)

            # Initialize Memory
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = model.start_chat(history=[])

            # Render Previous Transmissions
            for message in st.session_state.chat_session.history:
                role = "Rakshit" if message.role == "user" else "AI"
                with st.chat_message("user" if role == "Rakshit" else "assistant"):
                    st.markdown(message.parts[0].text)

            # Command Input
            user_input = st.chat_input("Say hi to test the connection...")
            
            if user_input:
                with st.chat_message("user"):
                    st.markdown(user_input)
                    
                with st.chat_message("assistant"):
                    response = st.session_state.chat_session.send_message(user_input)
                    st.markdown(response.text)
                
    except Exception as e:
        st.error(f"System Error Detected: {e}")
        
else:
    st.info("👈 Please enter your API key in the sidebar.")
