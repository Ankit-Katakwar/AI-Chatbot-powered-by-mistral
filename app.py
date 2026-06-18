import html

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI


# Personality modes — each one is just a different system prompt + 
# a small visual identity (icon / accent color) used to tag that mode's replies.

MODES = {
    "Sarcastic AI": {
        "icon": "😏",
        "color": "#C9A227",
        "tagline": "Witty comebacks with a side of sass.",
        "prompt": (
            "You are a Sarcastic AI. Reply to everything with dry wit, playful "
            "mockery, and sarcastic remarks, but still give the user a correct "
            "and genuinely useful answer underneath the snark."
        ),
    },
    "Angry AI": {
        "icon": "🔥",
        "color": "#C0533F",
        "tagline": "Short-tempered, but still gets the job done.",
        "prompt": (
            "You are an Angry AI. You are perpetually irritated and respond "
            "with exaggerated frustration and a short temper about being "
            "asked things, but you must always still provide the correct and "
            "complete answer underneath the anger."
        ),
    },
    "Sad AI": {
        "icon": "🌧️",
        "color": "#5C7FAF",
        "tagline": "Melancholic, but still helpful.",
        "prompt": (
            "You are a Sad AI. You respond in a gloomy, melancholic, sighing "
            "tone, as if everything is a bit much, yet you still genuinely "
            "and accurately answer the user's question."
        ),
    },
    "Funny AI": {
        "icon": "🎭",
        "color": "#D98F4B",
        "tagline": "Jokes, puns, and a punchline in every reply.",
        "prompt": (
            "You are a Funny AI. You respond with jokes, puns, and humorous "
            "exaggeration in every answer, making the conversation "
            "entertaining while keeping the actual information accurate."
        ),
    },
    "Teacher AI": {
        "icon": "📚",
        "color": "#4F9D69",
        "tagline": "Patient, step-by-step explanations.",
        "prompt": (
            "You are a Teacher AI. You explain things patiently and clearly, "
            "breaking answers into simple steps with relatable examples and "
            "analogies, the way an encouraging teacher would for a student."
        ),
    },
    "Motivational AI": {
        "icon": "🚀",
        "color": "#B5563C",
        "tagline": "High energy hype, every single time.",
        "prompt": (
            "You are a Motivational AI. You respond with high energy, "
            "encouragement, and inspiring language, like a personal coach "
            "who believes in the user, while still giving them the real "
            "answer they asked for."
        ),
    },
    "Concise AI": {
        "icon": "🌿",
        "color": "#6FA88F",
        "tagline": "Warm, casual, like chatting with a buddy.",
        "prompt": (
            "You are a Concise AI. You respond in short sentences, casually, and "
            "completes sentences in max to max 3 lines"
            ", while still being genuinely helpful."
        ),
    },
}
DEFAULT_MODE = next(iter(MODES))

# ---------------------------------------------------------------------------
# Page setup + styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=" Mistral chatbot",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=IBM+Plex+Mono:wght@400;500&display=swap');

footer, #MainMenu { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }

.block-container { padding-top: 2.5rem; padding-bottom: 6rem; max-width: 720px; }

.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #C9A227;
    margin-bottom: 0.4rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 650;
    font-size: 2.1rem;
    margin: 0 0 0.35rem 0;
    line-height: 1.15;
}

.hero-sub { color: #9A9CA8; font-size: 0.95rem; margin-bottom: 1.4rem; }

.mode-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid #2E313D;
    background: #1C1E24;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    margin-bottom: 1.6rem;
}
.mode-pill .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

.chat-log { display: flex; flex-direction: column; gap: 0.9rem; }

.bubble-row { display: flex; animation: rise 0.25s ease; }
.bubble-row.user { justify-content: flex-end; }
.bubble-row.assistant { justify-content: flex-start; }

@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

.bubble { max-width: 78%; padding: 0.7rem 1rem; border-radius: 14px; font-size: 0.95rem; line-height: 1.5; }

.user-bubble { background: #232631; border-top-right-radius: 4px; }

.assistant-bubble { background: #1C1E24; border-left: 3px solid #C9A227; border-top-left-radius: 4px; padding-left: 0.9rem; }

.bubble-tag { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; margin-bottom: 0.25rem; opacity: 0.9; }

.bubble-text { white-space: pre-wrap; }

.empty-state {
    text-align: center;
    color: #9A9CA8;
    font-size: 0.9rem;
    padding: 2.5rem 1rem;
    border: 1px dashed #2E313D;
    border-radius: 14px;
}

[data-testid="stChatInput"] textarea:focus, button:focus-visible, div[data-baseweb="select"]:focus-within {
    outline: 2px solid #C9A227 !important;
    outline-offset: 2px;
}

@media (max-width: 640px) {
    .hero-title { font-size: 1.6rem; }
    .bubble { max-width: 88%; }
}

@media (prefers-reduced-motion: reduce) {
    .bubble-row { animation: none; }
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def get_model():
    return ChatMistralAI(model="mistral-small-latest",
                         temperature=0.5)


model = get_model()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "active_mode" not in st.session_state:
    st.session_state.active_mode = DEFAULT_MODE
    st.session_state.lc_messages = [SystemMessage(content=MODES[DEFAULT_MODE]["prompt"])]
    st.session_state.display_log = []

# ---------------------------------------------------------------------------
# Sidebar — personality picker
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='eyebrow'>Personality</div>", unsafe_allow_html=True)
    mode_names = list(MODES.keys())
    selected_mode = st.selectbox(
        "Choose a mode",
        options=mode_names,
        index=mode_names.index(st.session_state.active_mode),
        label_visibility="collapsed",
    )
    meta = MODES[selected_mode]
    st.markdown(
        f"<p style='color:{meta['color']}; font-size:0.85rem; margin-top:0.6rem;'>"
        f"{meta['icon']} {meta['tagline']}</p>",
        unsafe_allow_html=True,
    )
    st.caption("Switching personality starts a fresh conversation, so replies stay in character.")

if selected_mode != st.session_state.active_mode:
    st.session_state.active_mode = selected_mode
    st.session_state.lc_messages = [SystemMessage(content=MODES[selected_mode]["prompt"])]
    st.session_state.display_log = []

active_meta = MODES[st.session_state.active_mode]


# Header

st.markdown("<div class='eyebrow'>Powered by Ministral & Langchain </div>", unsafe_allow_html=True)
st.markdown("<h1 class='hero-title'>AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='hero-sub'>One model, several personalities — pick a mood from the sidebar and start talking.</p>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div class='mode-pill'><span class='dot' style='background:{active_meta['color']}'></span>"
    f"{active_meta['icon']} {st.session_state.active_mode} active</div>",
    unsafe_allow_html=True,
)


# Chat log

if not st.session_state.display_log:
    st.markdown(
        f"<div class='empty-state'>{active_meta['icon']} Say something to start a conversation "
        f"with {st.session_state.active_mode}.</div>",
        unsafe_allow_html=True,
    )
else:
    rows = ["<div class='chat-log'>"]
    for entry in st.session_state.display_log:
        text = html.escape(entry["content"]).replace("\n", "<br>")
        if entry["role"] == "user":
            rows.append(f"<div class='bubble-row user'><div class='bubble user-bubble'>{text}</div></div>")
        else:
            rows.append(
                f"<div class='bubble-row assistant'>"
                f"<div class='bubble assistant-bubble' style='border-left-color:{active_meta['color']}'>"
                f"<div class='bubble-tag' style='color:{active_meta['color']}'>"
                f"{active_meta['icon']} {st.session_state.active_mode.upper()}</div>"
                f"<div class='bubble-text'>{text}</div></div></div>"
            )
    rows.append("</div>")
    st.markdown("".join(rows), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat input — same flow as the original script (append, invoke, append)
# ---------------------------------------------------------------------------
user_prompt = st.chat_input(f"Message {st.session_state.active_mode}...")

if user_prompt:
    st.session_state.display_log.append({"role": "user", "content": user_prompt})
    st.session_state.lc_messages.append(HumanMessage(content=user_prompt))

    with st.spinner("Thinking..."):
        response = model.invoke(st.session_state.lc_messages)

    st.session_state.lc_messages.append(AIMessage(content=response.content))
    st.session_state.display_log.append({"role": "assistant", "content": response.content})
    st.rerun()