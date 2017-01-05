#!/bin/bash

if hash python3 2>/dev/null; then
    ..\game_files\halite.exe -d "50 50" "python3 ../HaliteBotV1.py" "python3 ../PracticeBot.py"
else
    ..\game_files\halite.exe -d "50 50" "python ../HaliteBotV1.py" "python ../PracticeBot.py"
fi
