#!/bin/bash

if hash python3 2>/dev/null; then
    ..\game_files\halite.exe -d "50 50" "python3 ../PracticeBot.py" "python3 ./debug/pipe_socket_translator.py 2000"
else
    ..\game_files\halite.exe -d "50 50" "python ../PracticeBot.py" "python ./debug/pipe_socket_translator.py 2000"
fi
