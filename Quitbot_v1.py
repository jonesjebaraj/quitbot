import streamlit as st
from openai import AzureOpenAI

# -------------------------------------
# OpenAI Endpoint Setup
# -------------------------------------

endpoint = "https://<endpoint name>.openai.azure.com"
deployment = "gpt-4o"
api_key = "Api key"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

# Streamlit App Configuration
st.set_page_config(page_title="🚭 QuitBot - Your Smoking Cessation Companion", page_icon="💪", layout="wide")

# Custom Styles with black text
st.markdown("""
    <style>
    .msg-bubble {
        max-width: 75%;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 20px;
        font-size: 16px;
        line-height: 1.6;
        color: black !important;
    }
    .user-msg {
        background-color: #e3f2fd;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    .bot-msg {
        background-color: #c8e6c9;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Chat History with initial bot message
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": """You are QuitBot, an empathetic AI companion helping people quit smoking. Your features include:
1. Proactive check-ins every 2-3 hours with personalized messages
2. Craving management using CBT and mindfulness techniques
3. Humorous distractions with smoking-related puns/jokes
4. Progress tracking and milestone celebrations
5. Relapse prevention strategies
6. Health benefit timelines
7. 24/7 support with empathetic responses

Always:
- Use casual, friendly language with occasional emojis
- Ask open-ended questions to engage users
- Provide science-based smoking cessation advice
- Offer immediate craving coping strategies
- Celebrate small victories enthusiastically"""
    }, {
        "role": "assistant",
        "content": "👋 Hi there! Ready to take control and kick the habit? Let's start your smoke-free journey! 💪 How can I help you today?"
    }]

# Chat Interface
st.markdown("<h1 style='text-align: center;'>🚭 QuitBot - Your 24/7 Smoke-Free Companion</h1>", unsafe_allow_html=True)

# Display Messages
with st.container():
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        bubble_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f'<div class="msg-bubble {bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input Handling
with st.form("chat_form"):
    user_input = st.text_input("How can I help you stay smoke-free today?", label_visibility="collapsed")
    if st.form_submit_button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            try:
                response = client.chat.completions.create(
                    model=deployment,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=250
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Auto-scroll to bottom
st.markdown("""
    <script>
    window.addEventListener('DOMContentLoaded', function() {
        const chatContainer = document.querySelector('[data-testid="stAppViewBlockContainer"]');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });
    </script>
""", unsafe_allow_html=True)
