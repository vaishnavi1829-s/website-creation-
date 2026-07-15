@echo off
echo ========================================
echo   CineBook - Starting All Servers
echo ========================================
echo.

echo [1/2] Starting Backend (FastAPI on :8000)...
start "CineBook Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Frontend (Vite on :5173)...
start "CineBook Frontend" cmd /k "cd /d %~dp0frontend && npx vite --host 0.0.0.0 --port 5173"

echo.
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   Docs:     http://localhost:8000/docs
echo ========================================
pause
