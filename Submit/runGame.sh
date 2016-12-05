#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "50 50" "python MyBot.py" "python PracticeBot.py"
else
    ./halite -d "50 50" "python MyBot.py" "python PracticeBot.py"
fi
