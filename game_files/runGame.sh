#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "30 30" "python3 ../HaliteBotV1.py" "python3 ../PracticeBot.py"
else
    ./halite -d "30 30" "python ../HaliteBotV1.py" "python ../PracticeBot.py"
fi
