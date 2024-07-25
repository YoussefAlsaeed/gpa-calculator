@echo off
REM Install the required Python packages
pip install -r requirements.txt

REM Run the fetch.py script
python fetch.py

REM Run the calculate.py script
python calculate.py

pause
