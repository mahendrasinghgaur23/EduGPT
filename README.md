<h1 align="center">🎓 EduGPT — AI Study Assistant</h1>

<p align="center">
  <em>A Multi-Agent RAG-Powered Study Assistant that transforms any topic into a complete learning package — Notes, Explanations & Quizzes.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/AstraDB-0769AD?style=for-the-badge&logo=datastax&logoColor=white" alt="AstraDB"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 📖 About

**EduGPT** is a sophisticated multi-agent AI study assistant that revolutionizes how students learn from educational content. Unlike conventional AI systems that provide single, monolithic responses, EduGPT employs a team of **four specialized AI agents** working in orchestrated harmony to transform raw study materials into comprehensive learning experiences.

Upload any PDF or ask any question — EduGPT will generate a complete **Learning Package** including crisp study notes, personal tutor-style explanations, and interactive quizzes.

> 💡 Built using **Retrieval-Augmented Generation (RAG)** and **Agentic AI** principles for contextually accurate, pedagogically structured learning support.

---

## ✨ Features

- 📄 **Smart PDF Processing** — Upload any study material (PDF), automatically chunked and stored for intelligent retrieval
- 🔍 **Hybrid Retrieval** — Combines your uploaded documents with web search (Wikipedia + DuckDuckGo) for comprehensive context
- 📝 **Study Notes** — Crisp, exam-ready notes with bullet points, key formulas, and important terms
- 🧑‍🏫 **Personal Tutor Explanations** — Warm, conversational explanations with real-life analogies (not textbook-style!)
- ❓ **Auto-Generated Quizzes** — 5 MCQs with mixed difficulty, correct answers, and explanations
- 🌍 **Real-World Applications** — See how concepts apply in everyday life
- ⚠️ **Common Mistakes** — Learn what pitfalls to avoid
- 📥 **Downloadable** — Export your entire learning package as markdown
- 🎨 **Premium UI** — Dark glassmorphism design with smooth animations

---

## 🏗️ Architecture

EduGPT uses a **multi-agent pipeline** where each agent specializes in one task:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                  │
│                  (Upload PDF / Ask Question)                        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 1: KNOWLEDGE BASE                                            │
│  ┌──────────┐    ┌───────────┐    ┌────────────┐    ┌────────────┐  │
│  │ PDF Load │ ──▶│ Chunking  │ ──▶│ Embeddings │ ──▶│  AstraDB   │  │
│  │(PyPDFLoader)  │(1000/200) │    │ (Gemini)   │    │(Vector DB) │  │
│  └──────────┘    └───────────┘    └────────────┘    └────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 2: RETRIEVAL                                                  │
│  ┌──────────────────┐         ┌─────────────────────┐               │
│  │  Vector Search   │────┐    │   Web Search         │               │
│  │  (AstraDB)       │    ├──▶ │ (Wikipedia+DuckDuckGo)│              │
│  └──────────────────┘    │    └─────────────────────┘               │
│                          ▼                                           │
│              Combined Rich Context                                   │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 3: CONTENT GENERATION (Multi-Agent Pipeline)                  │
│                                                                      │
│  🔍 Retriever ──▶ 📄 Summarizer ──▶ 🧑‍🏫 Explainer ──▶ ❓ Quiz Master │
│  (finds context)  (study notes)    (tutor explanation) (5 MCQs)     │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 4: LEARNING PACKAGE                                           │
│  ┌──────────┐ ┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │  Notes   │ │ Explanation │ │Key Terms │ │Real-World│ │  Quiz  │ │
│  │          │ │(Tutor Style)│ │Dictionary│ │   Apps   │ │(5 MCQs)│ │
│  └──────────┘ └─────────────┘ └──────────┘ └──────────┘ └────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Streamlit   │
                    │  Dashboard   │
                    └──────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.10+ | Core development |
| **Frontend** | Streamlit | Interactive web dashboard |
| **Agent Orchestration** | LangChain | Multi-agent chaining & RAG pipeline |
| **LLM** | Groq (Llama 3.3 70B) | Powers Summarizer, Explainer & Quiz agents |
| **Embeddings** | Google Gemini (`gemini-embedding-001`) | Converts text to vector embeddings |
| **Vector Database** | AstraDB (DataStax) | Stores & retrieves document embeddings |
| **PDF Processing** | PyPDFLoader + RecursiveCharacterTextSplit | Document parsing & chunking |
| **Web Search** | Wikipedia + DuckDuckGo | Fallback retrieval for broader context |

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- A [Groq API Key](https://console.groq.com/) (free)
- A [Google Gemini API Key](https://aistudio.google.com/) (free)
- [AstraDB](https://astra.datastax.com/) account with a Serverless Vector Database (free tier)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/EduGPT.git
cd EduGPT
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
ASTRA_DB_API_ENDPOINT=your_astra_endpoint_here
ASTRA_DB_APPLICATION_TOKEN=your_astra_token_here
ASTRA_DB_COLLECTION_NAME=edugpt_docs
```

<details>
<summary>📋 Where to get each key</summary>

| Key | Where to Get | Cost |
|-----|-------------|------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com/) → API Keys | Free |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com/) → Get API Key | Free |
| `ASTRA_DB_API_ENDPOINT` | [astra.datastax.com](https://astra.datastax.com/) → Your DB → Connect | Free (75GB) |
| `ASTRA_DB_APPLICATION_TOKEN` | Same as above → Generate Token | Free |

</details>

### Step 4: Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🚀

---

## 📖 Usage

### Option 1: Upload a PDF

1. Click **"📁 Upload Study Material"** in the sidebar
2. Upload any educational PDF (textbook chapter, notes, etc.)
3. Click **"⚡ Process PDF"** to chunk and store it
4. Type your question in the search bar
5. Click **"🚀 Generate Learning Package"**

### Option 2: Ask a Question Directly

1. Simply type any educational question in the search bar
2. Click **"🚀 Generate Learning Package"**
3. EduGPT will search the web and generate your learning package

### Output: Complete Learning Package

| Tab | What You Get |
|-----|-------------|
| 📄 **Study Notes** | Crisp, exam-ready notes with bullet points and key terms |
| 🧑‍🏫 **Explanation** | Personal tutor-style explanation with analogies and examples |
| ❓ **Quiz** | 5 MCQs (Easy → Hard) with answers and explanations |

All outputs can be **downloaded as markdown** files for offline study.

---

## 📁 Project Structure

```
EduGPT/
├── 📄 app.py                        # Main Streamlit app & UI orchestrator
├── ⚙️ config.py                     # Configuration, API keys, model init
├── 📋 requirements.txt              # Python dependencies
├── 🔒 .env.example                  # Environment variables template
├── 📜 .gitignore                    # Git ignore rules
├── 📄 LICENSE                       # MIT License
│
├── 🤖 agents/                       # AI Agent modules
│   ├── __init__.py
│   ├── retriever.py                 # Hybrid search (DB + Web)
│   ├── summarizer.py                # Study notes generation
│   ├── explainer.py                 # Personal tutor explanations
│   └── quiz_generator.py            # MCQ quiz creation
│
├── 💬 prompts/                      # LLM prompt templates
│   ├── __init__.py
│   ├── summarizer_prompt.py         # Notes generation prompt
│   ├── explainer_prompt.py          # Tutor explanation prompt
│   └── quiz_prompt.py               # Quiz generation prompt
│
└── 🔧 utils/                        # Utility modules
    ├── __init__.py
    ├── pdf_processor.py             # PDF loading & text chunking
    ├── vector_store.py              # AstraDB vector operations
    └── web_search.py                # Wikipedia & DuckDuckGo search
```

---

## 🤖 Agent Details

| Agent | Role | Temperature | Strategy |
|-------|------|-------------|----------|
| 🔍 **Retriever** | Finds relevant context | N/A | Vector search + Web search (always combined) |
| 📄 **Summarizer** | Creates study notes | 0.3 (precise) | Focused on the specific question asked |
| 🧑‍🏫 **Explainer** | Personal tutor explanation | 0.7 (creative) | Conversational with analogies & examples |
| ❓ **Quiz Master** | Generates MCQs | 0.5 (balanced) | 2 Easy + 2 Medium + 1 Hard |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/) — Agent orchestration framework
- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [Google Gemini](https://ai.google.dev/) — Embedding model
- [DataStax AstraDB](https://www.datastax.com/) — Vector database
- [Streamlit](https://streamlit.io/) — Web UI framework

---

<p align="center">
  Made with ❤️ for students everywhere
</p>
