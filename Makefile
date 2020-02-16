all: init

init:
	pip install -r requirements.txt

help:
	python seimei/seimei.py -h
	
.PHONY:	init
