# Epic to Story Generator

## Overview

This service converts high-level epics into detailed user stories using LangGraph and LLMs (OpenAI or Ollama).

## Features

- Decompose epics into user stories
- Generate detailed descriptions and acceptance criteria
- Verify story completeness with API, error, and validation details
- FastAPI-based REST service with Swagger and ReDoc

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload