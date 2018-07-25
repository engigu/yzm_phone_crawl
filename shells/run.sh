#!/bin/bash

python_env='/root/.virtualenvs/sp/bin/python'

cd ../spiders/
nohup $python_env main.py heart_beat > /dev/null 2>&1 &