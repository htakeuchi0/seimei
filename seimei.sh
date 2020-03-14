#!/bin/bash

if [ ! -e env ]; then
	source makeenv.sh
	source activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	clear
fi

source activate
python seimei.py -g
deactivate

