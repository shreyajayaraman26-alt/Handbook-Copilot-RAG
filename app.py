
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from database import (
    create_conversation,
    get_conversations,
    get_conversation,
    save_user_message,
    save_assistant_message,
    delete_conversation
)


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Handbook Copilot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY was not found in your .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)


# ============================================================
# HANDBOOK SETTINGS
# ============================================================

HARVARD_PDF_URL = (
    "https://hls.harvard.edu/wp-content/uploads/academics-file/HAP.pdf"
)

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_value(item, key, default=None):

    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

@st.cache_resource
def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vectorstore


vectorstore = load_vectorstore()


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN APP
       ========================= */

    .stApp {
        background-color: #111318;
        color: #f4f0e9;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #181b21;
        border-right: 1px solid #2c3038;
    }


    section[data-testid="stSidebar"] .stMarkdown {
        color: #f4f0e9;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {

        width: 100%;

        background-color: #20232a;

        color: #e8e8e8;

        border: 1px solid #343842;

        border-radius: 10px;

        padding: 10px 12px;

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        background-color: #a41034;

        border-color: #a41034;

        color: white;
    }


    /* =========================
       LINK BUTTON
       ========================= */

    .stLinkButton > a {

        border-radius: 10px;
    }


    /* =========================
       CHAT MESSAGES
       ========================= */

    [data-testid="stChatMessage"] {

        background-color: #181b21;

        border: 1px solid #2c3038;

        border-radius: 14px;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {

        border-color: #363a43;
    }


    /* =========================
       SIDEBAR DIVIDERS
       ========================= */

    section[data-testid="stSidebar"] hr {

        border-color: #30343c;
    }


    /* =========================
       SIDEBAR HEADINGS
       ========================= */

    section[data-testid="stSidebar"] h3 {

        color: #a41034;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = None


if "pending_prompt" not in st.session_state:

    st.session_state.pending_prompt = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # HARVARD LAW SCHOOL BRANDING
    # --------------------------------------------------------

    st.markdown(
        "<div style='font-family: Georgia, Times New Roman, serif; "
        "font-size: 1.75rem; "
        "font-weight: 600; "
        "letter-spacing: 0.01em; "
        "line-height: 1.1; "
        "margin-bottom: 6px;'>"
        "HARVARD LAW SCHOOL"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size: 0.85rem; "
        "font-weight: 600; "
        "letter-spacing: 0.08em; "
        "color: #b9b9bd;'>"
        "VERITAS · LEX ET IUSTITIA"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size: 0.95rem; "
        "font-weight: 700; "
        "color: #a41034; "
        "margin-top: 8px;'>"
        "HANDBOOK COPILOT"
        "</div>",
        unsafe_allow_html=True
    )

    st.divider()


    # --------------------------------------------------------
    # NEW CONVERSATION
    # --------------------------------------------------------

    if st.button(
        "＋  New conversation",
        use_container_width=True
    ):

        st.session_state.conversation_id = None

        st.session_state.pending_prompt = None

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # RECENT CONVERSATIONS
    # --------------------------------------------------------

    st.caption("RECENT CONVERSATIONS")

    conversations = get_conversations()


    if conversations:

        for conversation in conversations:

            conversation_id = get_value(
                conversation,
                "id"
            )

            conversation_title = get_value(
                conversation,
                "title",
                "New conversation"
            )


            if conversation_id is None:

                continue


            if st.button(
                "💬  " + str(conversation_title),
                key=f"conversation_{conversation_id}",
                use_container_width=True
            ):

                st.session_state.conversation_id = (
                    conversation_id
                )

                st.rerun()


            if st.button(
                "🗑 Delete",
                key=f"delete_{conversation_id}",
                use_container_width=True
            ):

                delete_conversation(
                    conversation_id
                )


                if (
                    st.session_state.conversation_id
                    == conversation_id
                ):

                    st.session_state.conversation_id = None


                st.rerun()


    else:

        st.caption("No conversations yet.")


    st.divider()


    # --------------------------------------------------------
    # DOCUMENTATION
    # --------------------------------------------------------

    st.caption("DOCUMENTATION")

    st.write(
        "📕 **Harvard Law School Handbook**"
    )

    st.caption(
        "Official Handbook of Academic Policies"
    )

    st.caption("134 pages")


    st.link_button(
        "↗ Open official handbook",
        HARVARD_PDF_URL,
        use_container_width=True
    )


    st.divider()


    # --------------------------------------------------------
    # AI SYSTEM
    # --------------------------------------------------------

    st.caption("AI SYSTEM")

    st.write(
        "✦ **RAG Assistant**"
    )

    st.caption(
        "Retrieval-Augmented Generation"
    )

    st.caption(
        "Chroma · Sentence Transformers · Groq"
    )


    st.divider()


    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.caption("SYSTEM STATUS")

    st.success(
        "Knowledge base online"
    )

    st.caption(
        "Handbook indexed and ready"
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.markdown(
    "### ◈ HANDBOOK COPILOT"
)


st.markdown(
    "# Ask the "
    "<span style='color:#A41034'>Handbook.</span>",
    unsafe_allow_html=True
)


st.write(
    "Search, understand and explore academic policies "
    "using an AI-powered handbook assistant."
)


st.markdown(
    "**VERITAS · LEX ET IUSTITIA**"
)


# ============================================================
# SHOW EXISTING CONVERSATION
# ============================================================

if st.session_state.conversation_id is not None:

    conversation = get_conversation(
        st.session_state.conversation_id
    )


    if conversation:

        messages = get_value(
            conversation,
            "messages",
            []
        )


        for message in messages:

            role = get_value(
                message,
                "role",
                "assistant"
            )

            content = get_value(
                message,
                "content",
                ""
            )


            if role not in [
                "user",
                "assistant"
            ]:

                continue


            with st.chat_message(role):

                st.write(content)


                # --------------------------------------------
                # SOURCES
                # --------------------------------------------

                if role == "assistant":

                    sources = get_value(
                        message,
                        "sources",
                        []
                    )


                    if sources:

                        st.markdown(
                            "### 📚 Sources Used"
                        )


                        for source in sources:

                            page_number = get_value(
                                source,
                                "page",
                                get_value(
                                    source,
                                    "page_number",
                                    0
                                )
                            )


                            passage = get_value(
                                source,
                                "content",
                                get_value(
                                    source,
                                    "text",
                                    ""
                                )
                            )


                            try:

                                pdf_page = (
                                    int(page_number) + 1
                                )

                            except:

                                pdf_page = 1


                            with st.container(
                                border=True
                            ):

                                st.write(
                                    f"📄 **Handbook Page {pdf_page}**"
                                )


                                if passage:

                                    st.caption(
                                        passage
                                    )


                                st.link_button(
                                    f"↗ Open Official Harvard PDF at Page {pdf_page}",
                                    f"{HARVARD_PDF_URL}#page={pdf_page}"
                                )


# ============================================================
# NEW CONVERSATION SCREEN
# ============================================================

if st.session_state.conversation_id is None:

    st.subheader(
        "What would you like to know?"
    )


    st.write(
        "Ask a question about the Harvard Law School "
        "Handbook of Academic Policies."
    )


    st.write("")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "What are the requirements for graduation?",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "What are the requirements for graduation?"
            )

            st.rerun()


    with col2:

        if st.button(
            "How does the grading system work?",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "How does the grading system work?"
            )

            st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask something about the handbook..."
)


# ============================================================
# QUICK QUESTION HANDLING
# ============================================================

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None


# ============================================================
# PROCESS QUESTION
# ============================================================

if prompt:

    # --------------------------------------------------------
    # CREATE CONVERSATION
    # --------------------------------------------------------

    if st.session_state.conversation_id is None:

      conversation_id = create_conversation(
        title=prompt[:60]
    )

    st.session_state.conversation_id = conversation_id

    conversation_id = (
        st.session_state.conversation_id
    )


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    save_user_message(
        conversation_id,
        prompt
    )


    with st.chat_message("user"):

        st.write(prompt)


    # --------------------------------------------------------
    # RETRIEVE HANDBOOK CONTENT
    # --------------------------------------------------------

    with st.spinner(
        "Searching the handbook..."
    ):

        documents = vectorstore.similarity_search(
            prompt,
            k=3
        )


    context_parts = []


    for document in documents:

        context_parts.append(
            document.page_content
        )


    context = "\n\n---\n\n".join(
        context_parts
    )


    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = """
You are Handbook Copilot, an AI assistant for the
Harvard Law School Handbook of Academic Policies.

Answer questions using ONLY the handbook context provided.

Rules:

1. Give a clear and accurate answer.
2. Do not invent policies.
3. If the answer cannot be found in the retrieved context,
   clearly say that the information was not found.
4. Keep answers easy to understand.
5. Use short sections or bullets when useful.
"""


    user_prompt = f"""
HANDBOOK CONTEXT:

{context}


QUESTION:

{prompt}
"""


    # --------------------------------------------------------
    # GROQ RESPONSE
    # --------------------------------------------------------

    with st.spinner(
        "Preparing your answer..."
    ):

        response = client.chat.completions.create(

            model=MODEL_NAME,

            temperature=0.2,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )


    answer = (
        response
        .choices[0]
        .message
        .content
    )


    # --------------------------------------------------------
    # PREPARE SOURCES
    # --------------------------------------------------------

    sources = []


    for document in documents:

        metadata = document.metadata


        page_number = metadata.get(
            "page",
            0
        )


        sources.append(
            {
                "page": page_number,
                "content": document.page_content
            }
        )


    # --------------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # --------------------------------------------------------

    save_assistant_message(
        conversation_id,
        answer,
        sources
    )


    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        st.write(answer)


        if sources:

            st.markdown(
                "### 📚 Sources Used"
            )


            for source in sources:

                page_number = source["page"]

                passage = source["content"]


                try:

                    pdf_page = (
                        int(page_number) + 1
                    )

                except:

                    pdf_page = 1


                with st.container(
                    border=True
                ):

                    st.write(
                        f"📄 **Handbook Page {pdf_page}**"
                    )


                    st.caption(
                        passage
                    )


                    st.link_button(
                        f"↗ Open Official Harvard PDF at Page {pdf_page}",
                        f"{HARVARD_PDF_URL}#page={pdf_page}"
                    )


    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    st.rerun()
