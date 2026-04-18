# MedConnect AI CRM – HCP Interaction Module

## Project Overview
MedConnect AI CRM is an AI-first Customer Relationship Management system designed for Healthcare Professional (HCP) engagement in the life sciences domain.

This solution helps pharmaceutical field representatives log doctor interactions using an intelligent conversational interface powered by LangGraph and Groq LLM.

---

## Business Purpose
The system is designed to streamline HCP visit logging, doctor follow-up planning, and interaction analytics.

It reduces manual CRM form filling by converting free-text conversational notes into structured interaction records.

---

## Tech Stack
- Frontend: React + Redux
- Backend: FastAPI (Python)
- AI Framework: LangGraph
- LLM: Groq (Gemma 2 9B)
- Database: PostgreSQL
- Styling: Inter Font + Professional Dashboard UI

---

## Key Features
- AI chat-style interaction logging
- Doctor interaction history
- Search interactions
- Edit interaction
- Delete interaction
- Analytics dashboard
- Doctor engagement view
- PostgreSQL persistence

---

## LangGraph AI Tools
The system uses 5 AI tools:

1. Log Interaction Tool
2. Sentiment Analysis Tool
3. Follow-up Recommendation Tool
4. Doctor Profile Lookup Tool
5. Meeting Scheduler Tool

---

## Architecture Flow
React UI
→ FastAPI APIs
→ LangGraph Workflow
→ Groq LLM
→ PostgreSQL

---

## API Endpoints
- POST /interaction/ai-log
- GET /interaction/history
- GET /interaction/search
- PUT /interaction/edit/{id}
- DELETE /interaction/delete/{id}

---

## How to Run

### Backend
```bash
python -m uvicorn app.main:app --reload