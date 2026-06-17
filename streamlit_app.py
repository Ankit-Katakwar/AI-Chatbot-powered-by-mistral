from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# ---- minimal styling, nothing fancy ----
st.markdown(
    """
    <style>
        .block-container { padding-top: 2.5rem; max-width: 760px; }
        h1 { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 AI Chatbot")
st.caption("Powered by Mistral · ministral-3b-2512")


@st.cache_resource
def load_model():
    return ChatMistralAI(model="ministral-3b-2512")


model = load_model()

# same system role + message list logic as your original script,
# just stored in session_state so it survives Streamlit's reruns
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a say AI and add sadness to your every message. ")
    ]

# render chat history (skip the system message, it's not meant to be shown)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.invoke(st.session_state.messages)
        st.write(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))