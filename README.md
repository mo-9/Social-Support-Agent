# 🏛️ Social Support Agent

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-green.svg)](https://langchain-ai.github.io/langgraph/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-purple.svg)](https://ollama.ai/)

> **AI-Powered Social Support Application Workflow Automation**

An intelligent multi-agent system designed to automate government social security department workflows, reducing application processing time from 5-20 working days to just minutes through GenAI-powered automation.

**Author:** Mohamed Hammad

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution Architecture](#-solution-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The Social Support Agent is an end-to-end AI solution that automates the assessment and approval process for social support applications. It leverages:

- **Multimodal AI Processing** - Handles text, images, and tabular data
- **Agentic AI Orchestration** - Multiple specialized agents working together
- **Local LLM Hosting** - Privacy-focused with locally hosted models
- **Interactive Chat Interface** - User-friendly Streamlit-based UI

---

## 🔍 Problem Statement

### Current Pain Points

| Pain Point | Description | Impact |
|------------|-------------|--------|
| **Manual Data Gathering** | Manual entry from scanned documents, physical collection from offices | Data entry errors, delays |
| **Semi-Automated Validations** | Basic form validation with manual inconsistency checks | Significant manual effort |
| **Inconsistent Information** | Discrepancies in addresses, income, family details | Verification bottlenecks |
| **Time-Consuming Reviews** | Multiple review rounds across departments | 5-20 working days processing |
| **Subjective Decision-Making** | Human bias in assessments | Inconsistent, unfair decisions |

### Solution Goals

- ✅ **99% Automation** - Automated decision-making within minutes
- ✅ **Multi-source Data Ingestion** - Bank statements, Emirates ID, resumes, assets/liabilities
- ✅ **Eligibility Assessment** - Based on income, employment, family size, wealth
- ✅ **Support Recommendations** - Financial support approval or soft decline
- ✅ **Economic Enablement** - Upskilling, job matching, career counseling suggestions

---

## 🏗️ Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                         (Streamlit Web Application)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MASTER ORCHESTRATOR                                │
│                    (LangGraph Agentic Orchestration)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   ReAct     │  │  Reflexion  │  │    PaS      │  │   Custom    │        │
│  │  Reasoning  │  │  Framework  │  │  Framework  │  │   Agents    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    Data      │  │    Data      │  │  Eligibility │  │   Decision   │
│  Extraction  │  │  Validation  │  │    Check     │  │Recommendation│
│    Agent     │  │    Agent     │  │    Agent     │  │    Agent     │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA PIPELINE LAYER                               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │  PostgreSQL   │  │   MongoDB     │  │    Qdrant     │  │   Neo4j     │  │
│  │  (Relational) │  │   (NoSQL)     │  │   (Vector)    │  │   (Graph)   │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI/ML MODEL LAYER                                   │
│  ┌───────────────────────────┐    ┌───────────────────────────────────┐    │
│  │   Scikit-learn Models     │    │      Local LLM (Ollama)           │    │
│  │   - Classification        │    │   - Text Generation               │    │
│  │   - Eligibility Scoring   │    │   - Document Understanding        │    │
│  └───────────────────────────┘    └───────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          OBSERVABILITY LAYER                                 │
│                              (Langfuse)                                      │
│         Tracing │ Metrics │ Logging │ Performance Monitoring                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction** → Applicant submits documents via Streamlit UI
2. **Data Extraction** → Agent extracts information from all document types
3. **Data Validation** → Agent validates and cross-references data
4. **Eligibility Check** → ML models assess eligibility criteria
5. **Decision Recommendation** → Final recommendation generated
6. **Response** → User receives decision with explanations

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| 📄 **Document Processing** | Extract data from bank statements, IDs, resumes, Excel files |
| 🔍 **Multi-source Validation** | Cross-reference information across multiple documents |
| 📊 **ML-based Assessment** | Scikit-learn models for eligibility scoring |
| 🤖 **Conversational Interface** | Interactive chat with GenAI chatbot |
| 📈 **Real-time Tracking** | Application status and processing visibility |

### AI Agents

| Agent | Responsibility |
|-------|---------------|
| **Master Orchestrator** | Coordinates all agents and manages workflow |
| **Data Extraction Agent** | Extracts structured data from multimodal inputs |
| **Data Validation Agent** | Validates data consistency and accuracy |
| **Eligibility Check Agent** | Assesses eligibility based on defined criteria |
| **Decision Recommendation Agent** | Generates final recommendations |

---

## 🛠️ Technology Stack

### Programming & Framework

| Category | Technology | Justification |
|----------|------------|---------------|
| **Language** | Python 3.10+ | Industry standard for AI/ML, extensive library ecosystem |
| **Web Framework** | Streamlit | Rapid prototyping, built-in components for data apps |
| **API Framework** | FastAPI | High-performance, async support, auto-documentation |

### Data Pipeline

| Database | Type | Use Case |
|----------|------|----------|
| **PostgreSQL** | Relational | Structured applicant data, transactions |
| **MongoDB** | NoSQL | Unstructured documents, application forms |
| **Qdrant** | Vector | Semantic search, document embeddings |
| **Neo4j** | Graph | Relationship mapping, family connections |

### AI/ML Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **ML Models** | Scikit-learn | Classification, eligibility scoring |
| **LLM Hosting** | Ollama + OpenWebUI | Local model inference |
| **Agent Orchestration** | LangGraph | Multi-agent workflow management |
| **Reasoning Framework** | ReAct, Reflexion | Structured agent reasoning |
| **Observability** | Langfuse | Tracing, monitoring, debugging |

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Docker & Docker Compose
- Git
- 16GB+ RAM recommended

### Step 1: Clone Repository

```bash
git clone https://github.com/mo-9/Social-Support-Agent.git
cd Social-Support-Agent
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Databases (Docker)

```bash
docker-compose up -d
```

### Step 5: Install Ollama & Download Models

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Download required models
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Step 6: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your configurations
```

### Step 7: Initialize Databases

```bash
python scripts/init_databases.py
```

### Step 8: Run the Application

```bash
streamlit run app/main.py
```

---

## 🚀 Usage

### Starting the Application

```bash
# Start all services
docker-compose up -d

# Run Streamlit app
streamlit run app/main.py
```

### Application Workflow

1. **Upload Documents**
   - Bank Statement (PDF)
   - Emirates ID (Image)
   - Resume/CV (PDF)
   - Assets/Liabilities (Excel)
   - Credit Report (PDF)

2. **Interactive Chat**
   - Answer clarifying questions
   - Provide additional information
   - Track application progress

3. **Receive Decision**
   - Eligibility status
   - Support recommendations
   - Economic enablement suggestions

### API Endpoints

```bash
# Health Check
GET /api/health

# Submit Application
POST /api/applications

# Get Application Status
GET /api/applications/{application_id}

# Chat Interaction
POST /api/chat
```

---

## 📁 Project Structure

```
Social-Support-Agent/
├── app/
│   ├── main.py                 # Streamlit application entry
│   ├── pages/
│   │   ├── home.py             # Home page
│   │   ├── application.py      # Application submission
│   │   └── status.py           # Status tracking
│   └── components/
│       ├── chat.py             # Chat interface
│       ├── upload.py           # Document upload
│       └── dashboard.py        # Admin dashboard
│
├── agents/
│   ├── orchestrator.py         # Master orchestrator agent
│   ├── extraction_agent.py     # Data extraction agent
│   ├── validation_agent.py     # Data validation agent
│   ├── eligibility_agent.py    # Eligibility check agent
│   └── decision_agent.py       # Decision recommendation agent
│
├── models/
│   ├── ml/
│   │   ├── classifier.py       # Eligibility classifier
│   │   └── scorer.py           # Support scoring model
│   └── schemas/
│       ├── applicant.py        # Applicant data schema
│       └── application.py      # Application schema
│
├── services/
│   ├── document_processor.py   # Document processing service
│   ├── database_service.py     # Database operations
│   └── llm_service.py          # LLM interaction service
│
├── data/
│   ├── raw/                    # Raw uploaded documents
│   ├── processed/              # Processed data
│   └── synthetic/              # Synthetic test data
│
├── config/
│   ├── settings.py             # Application settings
│   └── prompts/                # Agent prompts
│
├── scripts/
│   ├── init_databases.py       # Database initialization
│   └── generate_synthetic.py   # Synthetic data generation
│
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
│
├── docs/
│   ├── architecture.md         # Architecture documentation
│   ├── api.md                  # API documentation
│   └── deployment.md           # Deployment guide
│
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Application Dockerfile
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

---

## 📚 API Documentation

### Authentication

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

### Submit Application

```http
POST /api/applications
Content-Type: multipart/form-data

{
  "applicant_name": "string",
  "emirates_id": "file",
  "bank_statement": "file",
  "resume": "file",
  "assets_liabilities": "file",
  "credit_report": "file"
}
```

### Response Schema

```json
{
  "application_id": "uuid",
  "status": "processing | approved | declined | pending_review",
  "eligibility_score": 0.85,
  "recommendations": {
    "financial_support": {
      "eligible": true,
      "amount": 5000,
      "duration": "6 months"
    },
    "economic_enablement": [
      {
        "type": "upskilling",
        "program": "Digital Skills Training",
        "provider": "Government Training Center"
      }
    ]
  },
  "reasoning": "string",
  "created_at": "timestamp",
  "processed_at": "timestamp"
}
```

---

## 🔮 Future Improvements

### Short-term Enhancements

- [ ] Multi-language support (Arabic, English)
- [ ] SMS/Email notifications
- [ ] Mobile-responsive UI
- [ ] Batch application processing

### Medium-term Enhancements

- [ ] Integration with government e-services
- [ ] Biometric verification
- [ ] Appeal workflow automation
- [ ] Advanced analytics dashboard

### Long-term Vision

- [ ] Federated learning for privacy-preserving model updates
- [ ] Cross-department data sharing protocols
- [ ] Predictive analytics for resource allocation
- [ ] Citizen feedback integration

### Integration Considerations

```yaml
# API Integration Points
External Systems:
  - Government ID Verification API
  - Credit Bureau API
  - Employment Records API
  - Property Registry API

Data Pipeline:
  - ETL Jobs: Apache Airflow
  - Real-time Streaming: Apache Kafka
  - Data Lake: MinIO/S3

Security:
  - OAuth 2.0 / OpenID Connect
  - End-to-end Encryption
  - Audit Logging
  - GDPR Compliance
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Write docstrings for all functions
- Include unit tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mohamed Hammad**

- GitHub: [@mo-9](https://github.com/mo-9)

---

## 🙏 Acknowledgments

- LangChain/LangGraph for the agentic AI framework
- Ollama for local LLM hosting
- Streamlit for the rapid UI development
- The open-source AI/ML community

---

<p align="center">
  Made with ❤️ for Government Digital Transformation
</p>
