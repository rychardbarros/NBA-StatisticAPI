@echo off

start "Streamlit Server" streamlit run main.py
timeout /t 5
cd src\api
python routes.py