<h1 align="center">🎓 EduGPT — Multi-Agent AI Study Assistant</h1>

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

---

## 📖 About

# EduGPT: Multi-Agent RAG Study Assistant

An AI study assistant I built for myself, mostly because I got tired of copy-pasting notes into ChatGPT one topic at a time. You either upload a PDF (like a chapter or your class notes) or just type a question, and it gives you back three things: clean notes, a proper explanation like a tutor would give, and a 5-question quiz to check if you actually understood it.

It's a Streamlit app under the hood, using LangChain to chain together a few small "agents," Groq for the actual LLM calls (fast + free tier is generous), Gemini for embeddings, and AstraDB as the vector store.

## Why I built it this way

I originally just had one big prompt doing everything, but the output was inconsistent — sometimes it would skip the quiz, sometimes the notes were too long. Splitting it into separate steps (retrieve → summarize → explain → quiz) fixed that and made debugging way easier, since I could test each piece on its own.

## What it does

- Upload a PDF and it gets chunked + stored so you can ask questions against it later
- If you don't upload anything (or the PDF doesn't have what you need), it falls back to Wikipedia + DuckDuckGo search
- Generates:
  - Study notes (bullet points, key terms, formulas if relevant)
  - A tutor-style explanation with analogies — I specifically prompted it to *not* sound like a textbook
  - A 5-question quiz, mixed difficulty, with answers explained
- Everything is downloadable as markdown so you can dump it into Notion/Obsidian/whatever

## Technical Architecture
```
User Query / PDF Ingest
       │
       ▼
[Retriever Agent] ──▶ Queries AstraDB Vector Store & Web (Wikipedia/DDG)
       │
       ├─▶ Context Document
       ▼
[Summarizer Agent] ──▶ Structured Notes & Definitions (LLM Model)
       │
       ├─▶ Summary Notes
       ▼
[Explainer Agent] ──▶ Conversational Explanation, Analogy, Pitfalls
       │
       ├─▶ Explained Concepts
       ▼
[Quiz Master Agent] ──▶ 5 MCQs (Answers + Explanations)
       │
       ▼
Streamlit UI Presentation (Tabbed Interface & Markdown Exports)
```
## Agent Details

| Agent | Role | Temperature | Strategy |
|-------|------|-------------|----------|
|  **Retriever** | Finds relevant context | N/A | Vector search + Web search (always combined) |
|  **Summarizer** | Creates study notes | 0.3 (precise) | Focused on the specific question asked |
|  **Explainer** | Personal tutor explanation | 0.7 (creative) | Conversational with analogies & examples |
|  **Quiz Master** | Generates MCQs | 0.5 (balanced) | 2 Easy + 2 Medium + 1 Hard |


## Technology Stack
- **Orchestration:** LangChain
- **Interface:** Streamlit
- **Vector Database:** AstraDB (DataStax)
- **Embedding Model:** Google Gemini (`gemini-embedding-001`)
- **LLM Provider:** Groq (`llama-3.3-70b-versatile`)
- **Web Scraping / Fallback:** Wikipedia API, DuckDuckGo Search API

---

## Installation & Setup

### Prerequisites
You will need API keys for the following services (all offer free tiers):
1. [Google AI Studio (Gemini Key)](https://aistudio.google.com/)
2. [Groq Console (Groq Key)](https://console.groq.com/)
3. [DataStax AstraDB Connection Credentials](https://astra.datastax.com/) (API Endpoint and Application Token)

### Step 1: Clone the Repo
```bash
git clone https://github.com/yourusername/edugpt.git
cd edugpt
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root folder of your project using the keys from `.env.example`:
```env
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
ASTRA_DB_API_ENDPOINT=https://your-astra-db-endpoint
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token
ASTRA_DB_COLLECTION_NAME=edugpt_docs
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

---

## Code Structure
- `app.py`: Streamlit application interface, session management, and visual progression.
- `config.py`: Service client initializations (LLM & Embeddings) and credential validation.
- `agents/`: Separate modules containing prompt orchestrations and runtime calls for each agent (`retriever`, `summarizer`, `explainer`, `quiz_generator`).
- `prompts/`: Standardized LangChain prompt templates separating prompt engineering rules from implementation code.
- `utils/`: Core processing logic (`pdf_processor` for parsing/splitting, `vector_store` for DB actions, and `web_search` for scraping fallbacks).

---

##  Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [LangChain](https://www.langchain.com/) — Agent orchestration framework
- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [Google Gemini](https://ai.google.dev/) — Embedding model
- [DataStax AstraDB](https://www.datastax.com/) — Vector database
- [Streamlit](https://streamlit.io/) — Web UI framework

---

<p align="center">
  Made with ❤️ for students everywhere
</p>
