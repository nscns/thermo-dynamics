@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

echo Using: %PY%
echo Installing requirements...
%PY% -m pip install -r requirements.txt

echo Launching simple plotter (only initial/final P,V,T asked)...
%PY% thermo_plot_simple.py

echo.
pause
