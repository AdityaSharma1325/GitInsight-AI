import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="GitInsight AI",
    page_icon="🤖",
    layout="wide",
)


def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()

from src.github.clone_repo import clone_repository
from src.analysis.repo_summary import analyze_repository
from src.analysis.ai_repository import analyze_repository_ai
from src.review.code_review import review_repository
from src.parser.file_loader import load_repository_files
from src.parser.repository_files import get_all_files
from src.parser.chunker import chunk_documents
from src.vectorstore.faiss_store import create_faiss_index, save_faiss_index
from src.llm.rag_chat import ask_repository
from src.memory.conversation import add_message
from src.explainer.file_explainer import explain_file
from src.detector.dependency_detector import detect_dependencies
from src.graph.dependency_graph import (
    build_dependency_graph,
    visualize_graph
)

if "repo_ready" not in st.session_state:
    st.session_state.repo_ready = False

if "repo_path" not in st.session_state:
    st.session_state.repo_path = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# Explain File
if "file_explanation" not in st.session_state:
    st.session_state.file_explanation = None

# Repository Chat
if "chat_answer" not in st.session_state:
    st.session_state.chat_answer = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retrieved_docs" not in st.session_state:
    st.session_state.retrieved_docs = []

# Repository Analyzer
if "repository_analysis" not in st.session_state:
    st.session_state.repository_analysis = None

# Code Review
if "code_review" not in st.session_state:
    st.session_state.code_review = None

# Technology Detector
if "tech_stack" not in st.session_state:
    st.session_state.tech_stack = None

with st.sidebar:
    try:
        st.image("assets/logo.png", width=120)
    except FileNotFoundError:
        pass

    page = st.radio(
        "Navigation",
        [
            "📂 Repository",
            "💬 Chat",
            "📄 Explain File",
            "📊 Repository Analyzer",
            "🔍 Code Reviewer",
            "🛠 Technology Detector",
            "📈 Dependency Graph"
        ]
    )

    st.divider()

    if st.session_state.repo_ready:
        st.success("Repository Loaded")
    else:
        st.warning("No Repository Loaded")

    if st.session_state.index_ready:
        st.info("FAISS Ready")
    else:
        st.warning("FAISS Not Ready")

    st.success("Groq Connected")


# ------------------------------------------------------------------
# 📂 Repository Page
# ------------------------------------------------------------------
if page == "📂 Repository":
    st.title("🤖 GitInsight AI")
    st.write("Clone any public GitHub repository.")

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
    )

    if st.button("Clone Repository"):
        if not repo_url.strip():
            st.warning("Please enter a GitHub repository URL.")
        else:
            progress = st.progress(0)

            success, result = clone_repository(repo_url)
            progress.progress(20)

            if success:
                st.session_state.repo_ready = True
                st.session_state.repo_path = result
                st.session_state.summary = analyze_repository(result)
                st.session_state.index_ready = False
                st.session_state.file_explanation = None
                st.session_state.chat_answer = None
                st.session_state.retrieved_docs = []
                st.session_state.chat_history = []
                st.session_state.repository_analysis = None
                st.session_state.code_review = None
                st.session_state.tech_stack = None

                documents = load_repository_files(result)
                progress.progress(40)

                chunks = chunk_documents(documents)
                progress.progress(60)
                st.session_state.chunk_count = len(chunks)

                vectorstore = create_faiss_index(chunks)
                save_faiss_index(vectorstore)
                progress.progress(80)

                st.session_state.index_ready = True
                progress.progress(100)
                progress.empty()

                st.success("Repository ready! FAISS index created successfully!")
            else:
                progress.empty()
                st.error(result)

    if st.session_state.repo_ready:
        summary = st.session_state.summary

        python_files = summary["languages"].get("Python", 0)
        languages_list = ", ".join(summary["languages"].keys())
        vector_status = "Ready" if st.session_state.index_ready else "Pending"

        overview_html = f"""
        <div class="metric-card">
            <h3 style="margin-top:0; color:#F8FAFC;">📦 Repository Overview</h3>
            <table>
                <tr><td>Repository</td><td>{summary['repository_name']}</td></tr>
                <tr><td>Python Files</td><td>{python_files}</td></tr>
                <tr><td>Languages</td><td>{languages_list}</td></tr>
                <tr><td>Vector Index</td><td>{vector_status}</td></tr>
                <tr><td>Repository Size</td><td>{summary['repository_size_kb']} KB</td></tr>
            </table>
        </div>
        """
        st.markdown(overview_html, unsafe_allow_html=True)

        st.subheader("Programming Languages")
        language_df = pd.DataFrame(
            summary["languages"].items(),
            columns=["Language", "Files"],
        )
        st.table(language_df)

        st.subheader("Largest Files")
        largest_files_df = pd.DataFrame(summary["largest_files"])
        st.table(largest_files_df)


# ------------------------------------------------------------------
# 💬 Chat Page
# ------------------------------------------------------------------
elif page == "💬 Chat":
    st.header("💬 Ask About the Repository")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask a question about the codebase")

        if question:
            with st.chat_message("user"):
                st.markdown(question)

            with st.spinner("Thinking..."):
                answer, docs = ask_repository(question, st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.chat_answer = answer
            st.session_state.retrieved_docs = docs
            st.session_state.chat_history = add_message(
                st.session_state.chat_history,
                "user",
                question
            )
            st.session_state.chat_history = add_message(
                st.session_state.chat_history,
                "assistant",
                answer
            )

        if st.button("Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()

        if st.session_state.retrieved_docs:
            with st.expander("📄 Retrieved Context"):
                for i, doc in enumerate(st.session_state.retrieved_docs, start=1):
                    with st.expander(f"Chunk {i} - {doc.metadata['source']}"):
                        st.code(doc.page_content)


# ------------------------------------------------------------------
# 📄 Explain File Page
# ------------------------------------------------------------------
elif page == "📄 Explain File":
    st.header("📄 Explain Any File")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        files = get_all_files(st.session_state.repo_path)

        selected = st.selectbox(
            "Choose a file",
            files,
            format_func=lambda x: x.name,
        )

        if st.button("Explain File"):
            with st.spinner("Analyzing..."):
                st.session_state.file_explanation = explain_file(selected)

        if st.session_state.file_explanation:
            st.markdown(st.session_state.file_explanation)


# ------------------------------------------------------------------
# 📊 Repository Analyzer Page
# ------------------------------------------------------------------
elif page == "📊 Repository Analyzer":
    st.header("📊 AI Repository Analyzer")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        if st.button("Analyze Repository"):
            with st.spinner("Analyzing repository..."):
                st.session_state.repository_analysis = analyze_repository_ai()

        if st.session_state.repository_analysis:
            st.markdown(st.session_state.repository_analysis)


# ------------------------------------------------------------------
# 🔍 Code Reviewer Page
# ------------------------------------------------------------------
elif page == "🔍 Code Reviewer":
    st.header("🔍 AI Code Reviewer")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        if st.button("Review Repository"):
            with st.spinner("Reviewing repository..."):
                st.session_state.code_review = review_repository()

        if st.session_state.code_review:
            st.markdown(st.session_state.code_review)


# ------------------------------------------------------------------
# 🛠 Technology Detector Page
# ------------------------------------------------------------------
elif page == "🛠 Technology Detector":
    st.header("🛠️ AI Technology Detector")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        if st.button("Detect Technology Stack"):
            with st.spinner("Analyzing technologies..."):
                st.session_state.tech_stack = detect_dependencies(
                    st.session_state.repo_path
                )

        if "tech_stack" in st.session_state:
            if st.session_state.tech_stack:
                st.markdown(st.session_state.tech_stack)


# ------------------------------------------------------------------
# 📈 Dependency Graph Page
# ------------------------------------------------------------------
elif page == "📈 Dependency Graph":
    st.header("📈 Repository Dependency Graph")

    if not st.session_state.repo_ready:
        st.info("Clone a repository first on the 📂 Repository page.")
    else:
        if st.button("Generate Dependency Graph"):
            graph = build_dependency_graph(
                st.session_state.repo_path
            )

            html_file = visualize_graph(graph)

            with open(html_file, "r", encoding="utf-8") as f:
                st.components.v1.html(
                    f.read(),
                    height=700,
                    scrolling=True
                )


st.divider()

st.caption(
    "GitInsight AI • Built with Streamlit, LangChain, FAISS, Groq"
)
