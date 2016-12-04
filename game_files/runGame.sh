#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "50 50" "python3 ../HaliteBotV1.py" "python3 ../PracticeBot.py"
else
    ./halite -d "50 50" "python ../HaliteBotV1.py" "python ../PracticeBot.py"
fi
