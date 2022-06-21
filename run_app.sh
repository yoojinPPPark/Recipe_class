#!/bin/bash

#1. Elasticsearch에 대조군 단어들이 있으면 실행하지 않고, 없으면 실행한다.
echo "Checking Elasticsearch..."
isControl=$(python get_index.py)
#echo $isControl

if [ "$isControl" = "yes" ]; then
    echo "There's a control group"
else
    echo "There's no a control group"
    python control.py
fi

#2. flask 실행
flask run