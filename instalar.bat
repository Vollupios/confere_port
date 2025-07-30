@echo off
echo ================================================
echo     INSTALADOR - SISTEMA CONSULTA CNPJA
echo ================================================
echo.
echo Instalando dependencias Python...
echo.

pip install -r requirements.txt

echo.
echo ================================================
echo Instalacao concluida!
echo.
echo Para executar o sistema, use:
echo   python main.py
echo.
echo Ou para consulta individual:
echo   python consultor_simples.py
echo ================================================
pause
