# Epic to Story Generator

## Overview

This service converts high-level epics into detailed user stories using LangGraph and LLMs (OpenAI or Ollama).

## Features

- Decompose epics into user stories
- Generate detailed descriptions and acceptance criteria
- Verify story completeness with API, error, and validation details
- FastAPI-based REST service with interactive API docs (Swagger UI and ReDoc)

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd epic_to_story
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root with your OpenAI API key:
```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o  # or your preferred model
```

### 4. Start the server
```bash
uvicorn main:app --reload
```

## API Usage

### Base URL
```
http://127.0.0.1:8000
```

### Interactive API Documentation
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can use these interfaces to explore and test the API endpoints interactively.

### Example Request

#### Generate Stories from an Epic
- **Endpoint:** `POST /stories/`
- **Request Body:**
```json
{
  "epic": "As a user, I want to manage my profile so that I can keep my information up to date."
}
```
- **Response:**
```json
{
  "stories": [
    {
      "story_title": "User can update personal information in their profile",
      "story_description": "...",
      "story_acceptance_criteria": "..."
    },
    ...
  ]
}
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required if using OpenAI as the model provider)
- `MODEL_NAME`: The model to use (e.g., `gpt-4o`, `gpt-4o-mini`, `llama3.2:1b`, etc.)
- `MODEL_PROVIDER`: The model provider to use (`openai` or `ollama`)

## Troubleshooting
- If you get a 500 Internal Server Error, check the server logs for details.
- Ensure your `.env` file is present and contains a valid API key.
- Make sure your Python version is compatible (3.10+ recommended).

