#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import MFRC522,SimpleMFRC522
import subprocess
import csv

ledPin = 16

simpleReader = SimpleMFRC522()
process = None
detected = False

GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)

fileMap = {}

with open('dict.csv','r') as dictionnary:
	reader = csv.reader(dictionnary)
	for row in reader:
		fileMap[row[0]] = row[1]
	

try:
	while True:
		id = simpleReader.read_id_no_block()
		if id == None:
			id = simpleReader.read_id_no_block()

		if id == None and process != None:
			process.terminate()
			process = None

		if id != None and process == None:
			print(id)
			file = fileMap[str(id)]
			print(file)
			if file != None:
				process = subprocess.Popen(["cvlc", file])
finally:
	GPIO.cleanup()
