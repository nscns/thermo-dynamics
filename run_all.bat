@echo off
setlocal
echo Installing requirements...
py -3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt
echo Running auto runner (no input)...
py -3 auto_run.py || python auto_run.py
echo Done. Plots are in .\plots
pause
