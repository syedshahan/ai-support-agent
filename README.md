# AI Support Agent

An AI-powered customer support backend built with FastAPI, LangGraph, Gemini, PostgreSQL, and pgvector.

The project combines traditional backend engineering with an LLM-powered support agent capable of using tools, retrieving information from a knowledge base, maintaining conversational context, and interacting with a persistent database.

## Features

- FastAPI backend
- AI support agent powered by Gemini
- LangGraph agent workflow
- LLM tool calling
- Customer/user management
- Support conversation handling
- PostgreSQL database
- SQLAlchemy ORM
- pgvector for vector storage
- Document ingestion and embeddings
- Semantic retrieval
- RAG-based knowledge retrieval
- Conversational memory
- Dockerized application
- Docker Compose development environment
- Automated tests with pytest
- Environment-based configuration

## Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         │  API / Frontend  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │      API         │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌──────────────┐           ┌──────────────┐
             │ User Routes  │           │  AI Routes   │
             └──────┬───────┘           └──────┬───────┘
                    │                          │
                    ▼                          ▼
             ┌──────────────┐           ┌──────────────┐
             │ PostgreSQL  │           │   LangGraph  │
             │ / SQLAlchemy│           │    Agent     │
             └──────────────┘           └──────┬───────┘
                                               │
                                  ┌────────────┼────────────┐
                                  │            │            │
                                  ▼            ▼            ▼
                              ┌────────┐  ┌─────────┐  ┌──────────┐
                              │  LLM   │  │  Tools  │  │ Memory   │
                              │ Gemini │  │         │  │          │
                              └────────┘  └─────────┘  └──────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ RAG / Search │
                                        └──────┬───────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ PostgreSQL +    │
                                      │    pgvector     │
                                      └─────────────────┘
````

## AI Agent Flow

```text
User Message
     │
     ▼
FastAPI AI Endpoint
     │
     ▼
LangGraph Agent
     │
     ├──► Understand request
     │
     ├──► Decide whether a tool is required
     │
     ├──► Retrieve relevant knowledge
     │
     ├──► Use available tools
     │
     └──► Generate response
              │
              ▼
        Support Response
```

## RAG Pipeline

```text
Documents
   │
   ▼
Document Loader
   │
   ▼
Text Splitting
   │
   ▼
Embeddings
   │
   ▼
PostgreSQL + pgvector
   │
   ▼
Semantic Retrieval
   │
   ▼
Relevant Context
   │
   ▼
LLM
```

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI / Agent

* Google Gemini
* LangGraph
* LLM tool calling

### Database

* PostgreSQL
* SQLAlchemy
* Psycopg
* pgvector

### RAG

* Embeddings
* Document loading
* Text splitting
* Vector similarity search

### Testing

* pytest

### Infrastructure

* Docker
* Docker Compose

## Project Structure

```text
ai-support-agent/
│
├── app/
│   ├── main.py
│   │
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── tools.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── ai.py
│   │       └── users.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   └── splitter.py
│   │
│   └── services/
│       ├── memory.py
│       ├── rag.py
│       └── retrieval.py
│
├── documents/
│
├── tests/
│   └── test_tools.py
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/syedshahan/ai-support-agent.git
cd ai-support-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/ai_support
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Running with Docker

The application and PostgreSQL database can be run together using Docker Compose.

```bash
docker compose up --build
```

This starts:

```text
FastAPI     → localhost:8000
PostgreSQL  → localhost:5432
```

To stop the services:

```bash
docker compose down
```

To view application logs:

```bash
docker compose logs app
```

To view running containers:

```bash
docker compose ps
```

## Database

The application uses PostgreSQL with SQLAlchemy.

Docker Compose uses:

```text
pgvector/pgvector:pg16
```

The database stores application data and vector embeddings.

When running locally, the application connects to:

```text
localhost:5432
```

When running with Docker Compose, the application connects to:

```text
db:5432
```

`db` is the Docker Compose service name.

## API

### User Endpoints

| Method | Endpoint           | Purpose       |
| ------ | ------------------ | ------------- |
| POST   | `/users/`          | Create a user |
| GET    | `/users/`          | Get users     |
| GET    | `/users/{user_id}` | Get a user    |
| PUT    | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |

### AI Endpoint

| Method | Endpoint   | Purpose                                |
| ------ | ---------- | -------------------------------------- |
| POST   | `/ai/chat` | Send a message to the AI support agent |

Example request:

```json
{
  "user_id": 1,
  "conversation_id": 1,
  "message": "What is your refund policy?"
}
```

Example response:

```json
{
  "response": "..."
}
```

The AI endpoint:

1. Validates the conversation.
2. Saves the user's message.
3. Loads conversation memory.
4. Runs the LangGraph agent.
5. Uses tools or retrieval when required.
6. Saves the assistant response.
7. Returns the response.

## Testing

Tests are written using pytest.

Run the tests with:

```bash
python -m pytest tests/test_tools.py -v
```

Example:

```text
1 passed
```

## Environment Variables

The application uses:

```text
DATABASE_URL
GEMINI_API_KEY
```

A template is provided in:

```text
.env.example
```

Never commit real API keys or passwords to Git.

## Docker Architecture

```text
┌─────────────────────┐
│      FastAPI        │
│      app service    │
│                     │
│      Port 8000      │
└──────────┬──────────┘
           │
           │ Docker Network
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│       pgvector      │
│                     │
│      Port 5432      │
└─────────────────────┘
```

Docker Compose includes a database healthcheck so the application waits for PostgreSQL to be ready before starting.

## What This Project Demonstrates

This project demonstrates practical AI engineering by combining:

* FastAPI backend development
* PostgreSQL and SQLAlchemy
* LangGraph agent workflows
* Gemini LLM integration
* Tool calling
* RAG and vector search
* Conversational memory
* Docker and Docker Compose
* Automated testing
* Environment-based configuration

## Future Improvements

* Authentication and authorization
* Streaming AI responses
* More comprehensive testing
* Alembic database migrations
* Observability and tracing
* Rate limiting
* Background jobs
* CI/CD
* Production deployment
* Agent evaluation
* Human-in-the-loop support

## License

This project is intended as a portfolio Project.
