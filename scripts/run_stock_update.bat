@echo off
cd /d "%~dp0.."

call venv\Scripts\activate.bat

python scripts\update_all_stocks.py