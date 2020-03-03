all: init

init:
	pip install -r requirements.txt

help:
	python seimei.py -h

seimei: 
	python seimei.py

gui:
	python seimei.py -g
	
.PHONY:	init help seimei gui
