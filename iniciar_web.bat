@echo off
title SEPARALAB
cd /d "%~dp0"
echo.
echo ==========================================
echo       SEPARALAB - laboratorio digital
echo ==========================================
echo.
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask no esta instalado. Instalando dependencias...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo No se pudo instalar Flask. Comprueba que Python este instalado.
        pause
        exit /b 1
    )
)
echo Iniciando SEPARALAB...
echo Cuando aparezca la direccion, abre http://127.0.0.1:5000 en tu navegador.
echo Para cerrar, presiona Ctrl+C en esta ventana.
echo.
python app.py
pause
