@echo off
title Order Dragon - Iniciar Backend y Frontend

echo ============================
echo   INICIANDO ORDER DRAGON
echo ============================

echo.
echo [1/2] Iniciando BACKEND...
start cmd /k "cd /d C:\Users\migui\Desktop\tfg_gestor_tareas\backend && venv\Scripts\activate && python app.py"

echo.
echo [2/2] Iniciando FRONTEND...
start cmd /k "cd /d C:\Users\migui\Desktop\tfg_gestor_tareas\frontend\frontend && npm run dev"

echo.
echo Todo iniciado correctamente.
echo Cierra esta ventana cuando quieras.
pause
