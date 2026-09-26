# 📚 Handbook Copilot RAG

An AI-powered Retrieval-Augmented Generation (RAG) assistant for exploring the Harvard Law School Handbook of Academic Policies.

Handbook Copilot allows users to ask natural-language questions about the handbook and receive grounded answers with relevant source passages and direct links to the corresponding pages of the official handbook PDF.

---

## 🎯 Problem Statement

Academic handbooks contain a large amount of important information, but finding a specific policy or requirement can be time-consuming.

Users often need to:

- Search through lengthy PDF documents
- Find the exact section containing an answer
- Understand policy information quickly
- Verify where an answer came from

Handbook Copilot solves this problem by providing a conversational AI interface for querying the handbook.

---

## 💡 Solution

Handbook Copilot uses Retrieval-Augmented Generation (RAG).

Instead of relying only on the language model's existing knowledge, the system:

1. Processes the handbook PDF.
2. Splits the document into searchable text chunks.
3. Converts the chunks into vector embeddings.
4. Stores the embeddings in a vector database.
5. Retrieves the most relevant sections for a user's question.
6. Sends the retrieved context to an AI language model.
7. Generates an answer grounded in the retrieved handbook content.
8. Displays the relevant source passages and handbook page links.

This helps users get answers while still being able to verify the original source.

---

## ✨ Features

- 🤖 AI-powered handbook question answering
- 🔎 Semantic document search
- 📚 Retrieval-Augmented Generation (RAG)
- 📄 Source passages for generated answers
- 🔗 Direct links to relevant handbook pages
- 💬 Conversational chat interface
- 🕘 Recent conversation history
- 🗑️ Conversation management
- 🎨 Dark, modern AI-assistant interface
- 🏛️ Harvard Law School inspired branding
- ⚡ Streamlit-based interactive web application

---

## 🧠 How the RAG Pipeline Works

```text
                Handbook PDF
                     │
                     ▼
              Document Ingestion
                     │
                     ▼
              Text Extraction
                     │
                     ▼
                Text Chunks
                     │
                     ▼
              Embeddings Model
                     │
                     ▼
              Chroma Vector DB
                     │
                     │
User Question ───────┘
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Handbook Context
      │
      ▼
Groq Language Model
      │
      ▼
Grounded AI Answer
      │
      ▼
Answer + Sources + Page Links 

---

## ✨ Features

- 🤖 AI-powered handbook question answering
- 🔎 Semantic document search
- 📚 Retrieval-Augmented Generation (RAG)
- 📄 Source passages for generated answers
- 🔗 Direct links to relevant handbook pages
- 💬 Conversational chat interface
- 🕘 Recent conversation history
- 🗑️ Conversation management
- 🎨 Dark, modern AI-assistant interface
- 🏛️ Harvard Law School inspired branding
- ⚡ Streamlit-based interactive web application

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### AI / LLM
- Groq
- `openai/gpt-oss-120b`

### RAG
- LangChain
- ChromaDB
- Sentence Transformers
- PyPDF

### Programming Language
- Python

### Database
- SQLite

### Development
- Visual Studio Code
- Git
- GitHub


---

## 📂 Project Structure

```text
Handbook-Copilot-RAG/
│
├── app.py
├── ingest.py
├── rag.py
├── database.py
├── README.md
├── .gitignore
│
└── data/
    └── harvard hb.pdf



---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shreyajayaraman26-alt/Handbook-Copilot-RAG.git


### 2. Open the project

```bash
cd Handbook-Copilot-RAG

### 3. Create a virtual environment

```bash
python -m venv venv

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1

### 5. Install dependencies

```bash
pip install -r requirements.txt

### 6. Configure the Groq API key

Create a file named `.env` in the project root folder.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here

### 7. Run the application

Start the Streamlit application using:

```bash
python -m streamlit run app.py

### 8. How to use

1. Open the Handbook Copilot application.
2. Enter a question about the handbook.
3. The system searches the handbook for relevant information.
4. The AI generates an answer using the retrieved content.
5. Relevant source passages are displayed below the answer.
6. Click the handbook page link to verify the information in the official PDF

---

## 🔐 Security

- API keys are stored in a `.env` file.
- `.env` is excluded from GitHub using `.gitignore`.
- Users should create their own Groq API key when running the project.
- Never commit or share your API key publicly.

---

## 🔄 Project Workflow

```text
User Question
      ↓
Streamlit Chat Interface
      ↓
Question Processing
      ↓
ChromaDB Semantic Search
      ↓
Relevant Handbook Content
      ↓
Groq LLM
      ↓
AI Generated Answer
      ↓
Source Passages + PDF Page Links

---

## 🎯 Use Case

Handbook Copilot is designed to help students and users quickly find and understand information from a lengthy academic handbook.

Instead of manually searching through pages of a PDF, users can ask questions in natural language and receive relevant answers along with source passages and links to the corresponding handbook pages.

---

## ⚠️ Limitations

- The current version is designed for the Harvard Law School Handbook of Academic Policies.
- Answers depend on the information available in the indexed handbook.
- The AI may occasionally require users to verify information using the provided source passages.
- The local conversation database is intended for the project demonstration environment.

---

## 🌐 Project Repository

The complete source code for Handbook Copilot RAG is available on GitHub.

The repository contains the application code, RAG pipeline, database configuration, project documentation, and setup instructions.

---

## 🚀 Future Improvements

- Support for multiple handbooks and documents
- PDF upload functionality
- Improved document search and filtering
- More advanced citation and source tracking
- User authentication
- Cloud-based vector database
- Deployment as a publicly accessible web application

---

## 👩‍💻 Author

**Shreya Jayaraman**

B.Tech Artificial Intelligence & Machine Learning

---

## 📄 License

This project is created for educational and demonstration purposes.