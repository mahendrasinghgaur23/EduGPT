import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import validate_config
from utils.pdf_processor import process_pdf
from utils.vector_store import get_vector_store, add_documents
from agents.retriever import retrieve
from agents.summarizer import summarize
from agents.explainer import explain
from agents.quiz_generator import generate_quiz

# Page Configuration
st.set_page_config(
    page_title="EduGPT — AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown(
    """
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e3f 0%, #15152d 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0ff;
    }

    /* ── Hero title area ── */
    .hero-title {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .hero-title h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .hero-title p {
        color: #a8a8d0;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* ── Glass card ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.08);
    }

    /* ── Agent status cards ── */
    .agent-pipeline {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .agent-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50px;
        padding: 0.4rem 1rem;
        font-size: 0.82rem;
        color: #c0c0e0;
        transition: all 0.3s ease;
    }
    .agent-badge.active {
        background: rgba(102,126,234,0.2);
        border-color: rgba(102,126,234,0.5);
        color: #a0b4ff;
        box-shadow: 0 0 15px rgba(102,126,234,0.15);
    }
    .agent-badge.done {
        background: rgba(46,204,113,0.15);
        border-color: rgba(46,204,113,0.4);
        color: #6ee7a0;
    }

    /* ── Source badge ── */
    .source-badge {
        display: inline-block;
        background: rgba(102,126,234,0.15);
        border: 1px solid rgba(102,126,234,0.3);
        border-radius: 50px;
        padding: 0.3rem 0.9rem;
        font-size: 0.8rem;
        color: #a0b4ff;
        margin-bottom: 1rem;
    }
    .source-badge.web {
        background: rgba(243,156,18,0.15);
        border-color: rgba(243,156,18,0.3);
        color: #f5c96a;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 0.4rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        color: #a0a0c8;
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(102,126,234,0.2) !important;
        color: #c8d4ff !important;
        border: 1px solid rgba(102,126,234,0.3) !important;
    }

    /* ── Button styling ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(102,126,234,0.5);
        transform: translateY(-1px);
    }

    /* ── Text input ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        color: #e0e0ff;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(102,126,234,0.5);
        box-shadow: 0 0 20px rgba(102,126,234,0.1);
    }
    .stTextInput > div > div > input::placeholder {
        color: #6a6a9a;
    }

    /* ── File uploader ── */
    .stFileUploader > div {
        background: rgba(255,255,255,0.04);
        border: 2px dashed rgba(255,255,255,0.12);
        border-radius: 12px;
        transition: border-color 0.3s ease;
    }
    .stFileUploader > div:hover {
        border-color: rgba(102,126,234,0.4);
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.06);
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04);
        border-radius: 8px;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(102,126,234,0.3);
        border-radius: 3px;
    }

    /* ── Success/Info/Warning boxes ── */
    .stAlert {
        border-radius: 12px;
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# Session State Initialization

if "learning_package" not in st.session_state:
    st.session_state.learning_package = None
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chunks_count" not in st.session_state:
    st.session_state.chunks_count = 0
if "processing" not in st.session_state:
    st.session_state.processing = False



# Config Validation

missing_keys = validate_config()
if missing_keys:
    st.error(
        f"⚠️ Missing environment variables: **{', '.join(missing_keys)}**\n\n"
        "Please create a `.env` file in the project root with the required keys. "
        "See `.env.example` for reference."
    )
    st.stop()



# Sidebar

with st.sidebar:
    # App branding
    st.markdown(
        """
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.3rem;">🎓</div>
        <h1 style="font-size: 1.8rem; font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0;">EduGPT</h1>
        <p style="color: #8888b0; font-size: 0.85rem; margin-top: 0.3rem;">
            Your AI Study Assistant</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── PDF Upload Section ──
    st.markdown(
        "### 📁 Upload Study Material",
    )
    st.caption("Upload a PDF to build your knowledge base")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed",
        key="pdf_uploader",
    )

    if uploaded_file is not None:
        if st.button(" Process PDF", use_container_width=True):
            with st.spinner(" Reading and processing your PDF..."):
                try:
                    # Initialize vector store if needed
                    if st.session_state.vector_store is None:
                        st.session_state.vector_store = get_vector_store()

                    # Process PDF
                    chunks = process_pdf(uploaded_file)
                    add_documents(st.session_state.vector_store, chunks)

                    st.session_state.pdf_processed = True
                    st.session_state.chunks_count = len(chunks)
                    st.success(
                        f" Processed **{len(chunks)}** chunks from your PDF!"
                    )
                except Exception as e:
                    st.error(f" Error processing PDF: {str(e)}")

    # ── Knowledge Base Status ──
    st.divider()
    st.markdown("### Knowledge Base")

    if st.session_state.pdf_processed:
        st.markdown(
            f"""
        <div style="background: rgba(46,204,113,0.1); border: 1px solid rgba(46,204,113,0.3);
                    border-radius: 10px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 1.5rem;"></div>
            <div style="color: #6ee7a0; font-weight: 600; font-size: 0.9rem;">
                Documents Loaded</div>
            <div style="color: #4ade80; font-size: 1.4rem; font-weight: 700;">
                {st.session_state.chunks_count} chunks</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 10px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 1.5rem;"></div>
            <div style="color: #8888b0; font-size: 0.85rem;">
                No documents loaded yet.<br/>
                Upload a PDF or ask any question!</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── How it Works ──
    st.divider()
    with st.expander(" How EduGPT Works", expanded=False):
        st.markdown(
            """
        **4 AI Agents work together:**

        1.  **Retriever** — Finds relevant info
        2.  **Summarizer** — Creates study notes
        3.  **Explainer** — Personal tutor explanation
        4.  **Quiz Master** — Tests your understanding

        *Upload a PDF or just ask a question!*
        """
        )


# ─────────────────────────────────────────────
# Main Content Area
# ─────────────────────────────────────────────

# Hero Title
st.markdown(
    """
<div class="hero-title">
    <h1>EduGPT</h1>
    <p>Transform any topic into a complete learning experience — notes, explanations, and quizzes.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Agent Pipeline Visual ──
st.markdown(
    """
<div class="agent-pipeline" style="justify-content: center; margin-bottom: 1.5rem;">
    <div class="agent-badge"> Retriever</div>
    <div style="color: #555; display: flex; align-items: center;">→</div>
    <div class="agent-badge"> Summarizer</div>
    <div style="color: #555; display: flex; align-items: center;">→</div>
    <div class="agent-badge"> Explainer</div>
    <div style="color: #555; display: flex; align-items: center;">→</div>
    <div class="agent-badge"> Quiz Master</div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Question Input ──
st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True,
)
question = st.text_input(
    "What would you like to learn about?",
    placeholder="Specify only the topic or question",
    key="question_input",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button(
        " Generate Learning Package",
        type="primary",
        use_container_width=True,
        key="generate_btn",
    )
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Generation Pipeline
# ─────────────────────────────────────────────
if generate_btn:
    if not question.strip():
        st.warning(" Please enter a topic or question to get started!")
    else:
        # Initialize vector store if needed
        if st.session_state.vector_store is None:
            try:
                st.session_state.vector_store = get_vector_store()
            except Exception as e:
                st.error(f" Failed to connect to AstraDB: {str(e)}")
                st.stop()

        # ── Run the Agent Pipeline ──
        with st.status(" AI Agents are working on your learning package...", expanded=True) as status:

            # Step 1: Retriever Agent
            st.write(" **Retriever Agent** — Searching for relevant information...")
            try:
                context, source = retrieve(question, st.session_state.vector_store)
                if source == "database":
                    st.write("Found relevant content from your uploaded documents")
                elif source == "database + web":
                    st.write("Found content from your documents + web search")
                else:
                    st.write(" Found relevant content from web sources")
            except Exception as e:
                st.error(f"Retriever Agent failed: {str(e)}")
                st.stop()

            # Step 2: Summarizer Agent
            st.write(" **Summarizer Agent** — Creating concise study notes...")
            try:
                notes = summarize(context, question)
                st.write(" Study notes ready")
            except Exception as e:
                st.error(f" Summarizer Agent failed: {str(e)}")
                st.stop()

            # Step 3: Explainer Agent
            st.write(" **Explainer Agent** — Preparing personal explanation...")
            try:
                explanation = explain(notes, question)
                st.write(" Explanation ready")
            except Exception as e:
                st.error(f"Explainer Agent failed: {str(e)}")
                st.stop()

            # Step 4: Quiz Generator Agent
            st.write("❓ **Quiz Master** — Generating quiz questions...")
            try:
                quiz = generate_quiz(notes, question)
                st.write(" Quiz ready")
            except Exception as e:
                st.error(f" Quiz Generator failed: {str(e)}")
                st.stop()

            status.update(
                label=" Learning package is ready!", state="complete", expanded=False
            )

        # Store results
        st.session_state.learning_package = {
            "notes": notes,
            "explanation": explanation,
            "quiz": quiz,
            "source": source,
            "topic": question,
        }


# ─────────────────────────────────────────────
# Display Learning Package
# ─────────────────────────────────────────────
if st.session_state.learning_package:
    pkg = st.session_state.learning_package

    st.divider()

    # ── Package Header ──
    st.markdown(
        f"""
    <div style="text-align: center; margin: 1rem 0;">
        <h2 style="color: #e0e0ff; font-weight: 700; margin-bottom: 0.3rem;">
            Your Learning Package</h2>
        <p style="color: #8888b0; font-size: 1rem; margin-bottom: 0.8rem;">
            <em>{pkg['topic']}</em></p>
        <div class="source-badge {'web' if pkg['source'] == 'web' else ''}">
            {'Source: Web Search' if pkg['source'] == 'web' else ' Source: Your Documents'}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Tabbed Content ──
    tab_notes, tab_explain, tab_quiz = st.tabs(
        [" Study Notes", " Explanation", " Quiz"]
    )

    with tab_notes:
        st.markdown(
            '<div class="glass-card">', unsafe_allow_html=True
        )
        st.markdown(pkg["notes"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Download notes button
        st.download_button(
            label=" Download Notes",
            data=pkg["notes"],
            file_name=f"edugpt_notes_{pkg['topic'][:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    with tab_explain:
        st.markdown(
            '<div class="glass-card">', unsafe_allow_html=True
        )
        st.markdown(pkg["explanation"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Download explanation button
        st.download_button(
            label=" Download Explanation",
            data=pkg["explanation"],
            file_name=f"edugpt_explanation_{pkg['topic'][:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    with tab_quiz:
        st.markdown(
            '<div class="glass-card">', unsafe_allow_html=True
        )
        st.markdown(pkg["quiz"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Download quiz button
        st.download_button(
            label=" Download Quiz",
            data=pkg["quiz"],
            file_name=f"edugpt_quiz_{pkg['topic'][:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    # ── Full Download ──
    st.divider()
    full_package = f"""# EduGPT Learning Package
## Topic: {pkg['topic']}
## Source: {'Your Documents' if pkg['source'] == 'database' else 'Web Search'}

---

{pkg['notes']}

---

{pkg['explanation']}

---

{pkg['quiz']}
"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label=" Download Complete Learning Package",
            data=full_package,
            file_name=f"edugpt_complete_{pkg['topic'][:30].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
