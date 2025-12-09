@echo off
echo =============================================
echo INSTALADOR AUTOMATICO BACKEND + PYTHON 3.12
echo =============================================
echo.

REM --- 1. DESCARGAR PYTHON 3.12 ---
echo Descargando Python 3.12...
curl -L -o python312.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

echo Instalando Python 3.12...
start /wait python312.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo Python 3.12 instalado.
echo.

REM --- 2. IR A LA CARPETA BACKEND ---
echo Moviendose al directorio backend...
cd /d C:\Users\migui\Desktop\tfg_gestor_tareas\backend

REM --- 3. CREAR ENTORNO VIRTUAL CON PYTHON 3.12 ---
echo Creando entorno virtual con Python 3.12...
py -3.12 -m venv venv

REM --- 4. ACTIVAR EL ENTORNO ---
echo Activando entorno...
call venv\Scripts\activate

REM --- 5. INSTALAR DEPENDENCIAS ---
echo Instalando dependencias...
pip install --upgrade pip
pip install supabase flask flask-cors flask-bcrypt flask-jwt-extended python-dotenv

REM --- 6. EJECUTAR BACKEND ---
echo Lanzando backend...
python app.py

pause
