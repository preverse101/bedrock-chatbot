from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from portkey_ai import Portkey

st.set_page_config(
    page_title="Bedrock Chat",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    .chat-container {
        max-width: 720px;
        margin: 0 auto;
    }

    .message-user {
        background: #1e3a5f;
        border-radius: 12px 12px 2px 12px;
        padding: 12px 16px;
        margin: 8px 0 8px 60px;
        color: #e0eaff;
        font-size: 15px;
        line-height: 1.5;
    }

    .message-assistant {
        background: #1a1d26;
        border: 1px solid #2a2d3a;
        border-radius: 12px 12px 12px 2px;
        padding: 12px 16px;
        margin: 8px 60px 8px 0;
        color: #d4d8e8;
        font-size: 15px;
        line-height: 1.5;
    }

    .role-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }

    .label-user { color: #6ea8fe; text-align: right; margin-right: 4px; }
    .label-assistant { color: #9ca3af; }

    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stHorizontalBlock"]) {
        position: sticky;
        bottom: 0;
        background: #0f1117;
        padding-top: 8px;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)


MODEL_OPTIONS = {
    "Claude Opus 5": "us.anthropic.claude-opus-5",
    "Claude Sonnet 5": "us.anthropic.claude-sonnet-5",
    "Claude Fable 5.1": "us.anthropic.claude-fable-5-1",
    "Claude Opus 4.8": "us.anthropic.claude-opus-4-8",
    "Claude Haiku 4.5": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
}

DEFAULT_SYSTEM = (
    "You are a helpful, concise, and knowledgeable assistant. "
    "Respond clearly and directly."
)


def get_client() -> Portkey:
    return Portkey(
        api_key=os.environ.get("PORTKEY_API_KEY"),
        provider="@bedrock-dev-integration",
    )


def stream_response(messages: list, model: str, system: str) -> str:
    client = get_client()
    full_text = ""
    placeholder = st.empty()

    all_messages = [{"role": "system", "content": system}] + messages

    stream = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=all_messages,
        stream=True,
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        full_text += text
        placeholder.markdown(
            f'<div class="message-assistant">{full_text}▌</div>',
            unsafe_allow_html=True,
        )
    placeholder.markdown(
        f'<div class="message-assistant">{full_text}</div>',
        unsafe_allow_html=True,
    )
    return full_text


# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "aws_region" not in st.session_state:
    st.session_state.aws_region = "us-east-1"



# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")

    selected_model_label = st.selectbox(
        "Model",
        list(MODEL_OPTIONS.keys()),
        index=0,
    )
    model_id = MODEL_OPTIONS[selected_model_label]

    st.session_state.aws_region = st.text_input(
        "AWS Region",
        value=st.session_state.aws_region,
    )

    system_prompt = st.text_area(
        "System Prompt",
        value=DEFAULT_SYSTEM,
        height=120,
    )

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption(f"Model ID: `{model_id}`")


# --- Header ---
st.markdown("## 🤖 Bedrock Chat")
st.markdown("---")

# --- Chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="label-user role-label">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="label-assistant role-label">Assistant</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-assistant">{msg["content"]}</div>', unsafe_allow_html=True)

# --- Input ---
user_input = st.chat_input("Message Claude…")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    st.markdown(f'<div class="label-user role-label">You</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-user">{user_input.strip()}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="label-assistant role-label">Assistant</div>', unsafe_allow_html=True)

    response_text = stream_response(
        messages=st.session_state.messages,
        model=model_id,
        system=system_prompt,
    )

    st.session_state.messages.append({"role": "assistant", "content": response_text})
