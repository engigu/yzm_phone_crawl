#!/bin/bash

python_env='/home/tk/.virtualenvs/sp/bin/python'

cd ../spiders/
nohup $python_env main.py heart_beat > /dev/null 2>&1 &