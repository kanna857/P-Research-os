@echo off
echo ===================================================
echo     Launching ResearchOS Full-Stack Platform
echo ===================================================
echo.

echo Starting ResearchOS FastAPI Backend on http://localhost:8000 ...
start "ResearchOS Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting ResearchOS Next.js Frontend on http://localhost:3000 ...
start "ResearchOS Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===================================================
echo   ResearchOS is running!
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000/docs
echo ===================================================
pause

