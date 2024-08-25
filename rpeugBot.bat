@echo off
REM Install dependencies
python -m pip install --upgrade pip
pip install discord.py

REM Run the bot
python bot.py

REM Keep the console open until the user closes it
pause