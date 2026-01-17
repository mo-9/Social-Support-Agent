# 🏛️ Social Support AI Workflow Automation

## 📋 Overview
An intelligent, agentic AI solution designed to automate the social support application process for government entities. This system reduces processing time from days to minutes by leveraging **Multimodal GenAI (Llama3)**, **Machine Learning (Scikit-learn)**, and **RAG (Retrieval-Augmented Generation)** to analyze documents, assess risk, and ensure legal compliance.

---

## 🏗️ Architecture & Tech Stack

The solution follows a **Microservices-based Architecture**:

* **Orchestration:** LangGraph (Stateful Multi-Agent Workflow)
* **LLM Serving:** Ollama (Llama3 - Local Privacy Focused)
* **ML Engine:** Scikit-learn (Random Forest for Risk Scoring)
* **Vector Database:** Qdrant (Legal Knowledge Base)
* **OCR & Multimodal:** Tesseract & Pandas (PDF, Images, Excel, CSV)
* **Backend API:** FastAPI
* **Async Workers:** Celery + Redis
* **Frontend:** Streamlit

### 🔄 System Data Flow
```mermaid
graph TD
    User([User]) -->|Uploads Docs| UI[Streamlit UI]
    UI -->|POST /submit| API[FastAPI Backend]
    API -->|Push Task| Redis[(Redis Queue)]
    Redis -->|Pull Task| Worker[Celery Worker]
    
    subgraph "AI Logic Layer (LangGraph)"
        Worker --> OCR[OCR Engine]
        OCR --> LLM[Llama3 Extraction]
        LLM --> ML[Scikit-Learn Risk Model]
        ML --> RAG[Qdrant Legal Search]
        RAG --> Decision[Final Decision Agent]
    end
    
    Decision -->|Save Result| DB[(PostgreSQL)]
    UI -->|Poll Result| API
    API -->|Fetch Status| DB




🚀 Key Features
Multimodal Ingestion: Processes Images, PDFs, and Excel/CSV financial sheets.

Hybrid AI Reasoning: Combines GenAI (extraction/reasoning) with Traditional ML (probabilistic risk scoring).

Legal Compliance (RAG): Cross-references applicant data against a vectorized legal knowledge base (Qdrant) to prevent fraud.

Economic Enablement: Suggests upskilling and job roles for rejected or low-income applicants.

Interactive UI: Real-time tracking of the application status via Streamlit.

🛠️ Installation & Setup
Prerequisites
Python 3.10+

Docker Desktop (Running)

Tesseract OCR (Installed on system)

1. Clone & Setup Environment
Bash

git clone <your-repo-link>
cd social-support-ai
python -m venv venv

# Activate venv:
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
2. Infrastructure Setup (Docker)
Start PostgreSQL, Redis, and Qdrant services:

Bash

docker-compose up -d
3. Initialize Models
Train the Risk Assessment Model and Seed the Legal Knowledge Base:

Bash

python train_risk_model.py
python seed_laws.py
4. Run the System
To run the full system, open 3 separate terminals and run the following commands in order (ensure venv is activated in all):

Terminal 1: Backend API

Bash

uvicorn app.main:app --reload
Terminal 2: AI Worker

Bash

celery -A app.core.celery_app worker --loglevel=info --pool=solo
Terminal 3: Frontend UI

Bash

streamlit run ui.py
🧠 AI Agent Workflow (LangGraph)
The system uses a graph-based orchestration pattern:

Node	Description
OCR Node	Extracts raw text from uploaded files (Tesseract/Pandas).
Extraction Node	Llama3 converts unstructured text into structured JSON.
Risk Node	Random Forest model predicts fraud risk based on income & family size.
RAG Node	Retrieves relevant legal articles from Qdrant based on applicant profile.
Enablement Node	Generates career advice using GenAI.
Decision Node	Final orchestrator synthesizes all data to output APPROVED, REJECTED, or SOFT_DECLINE.

التصدير إلى "جداول بيانات Google"

📂 Project Structure
Plaintext

social-support-ai/
├── app/
│   ├── agents/workflow.py    # Master Agent (LangGraph)
│   ├── core/                 # Config, DB, Celery
│   ├── services/             # ML Models, Vector Store
│   ├── utils/ocr.py          # Multimodal Readers
│   └── main.py               # API Endpoints
├── data/uploads/             # Temp Storage
├── seed_laws.py              # RAG Seeder
├── train_risk_model.py       # ML Trainer
├── ui.py                     # Streamlit App
└── docker-compose.yml        # Infrastructure
