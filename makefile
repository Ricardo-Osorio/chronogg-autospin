#!/bin/bash

build:
	mkdir -p package && \
	virtualenv chronogg && \
	source chronogg/bin/activate && \
	pip3 install -t ./package requests && \
	deactivate && \
	cd package && \
	zip -r main.zip . && \
	mv main.zip .. && \
	cd .. && \
	zip -g main.zip main.py

deploy: build
	aws lambda update-function-code --function-name chronogg-auto-spin --zip-file fileb://main.zip
