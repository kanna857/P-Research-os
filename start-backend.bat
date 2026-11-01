@echo off
cd /d %~dp0backend
echo Starting ResearchOS FastAPI Backend on port 8000...
python -m uvicorn app.main:app --reload --port 8000
pause

