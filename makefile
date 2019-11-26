#!/bin/bash

build:
	mkdir -p package && \
	pip3 install -t ./package requests && \
	cd package && \
	zip -r9 main.zip . && \
	mv main.zip .. && \
	cd .. && \
	zip -g main.zip main.py

deploy: build
	aws lambda update-function-code --function-name chronogg-auto-spin --zip-file fileb://main.zip
