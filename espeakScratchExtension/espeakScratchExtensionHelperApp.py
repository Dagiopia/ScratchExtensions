#! /usr/bin/python

import urllib2
from flask import Flask
import os
import sys
from os import path
from espeak import espeak

app = Flask("scratch_helper")
app.logger.removeHandler(app.logger.handlers[0])
varval = ""

@app.route('/poll')
def poll():
    print espeak.is_playing()
    return "isPlaying " + str(1 if espeak.is_playing() else 0) + "\n"

@app.route('/setGender/<string:gen>')
def setGender(gen):
	g = espeak.Gnder.Male
	if gen == "Female":
		g = espeak.Gender.Female
	espeak.set_voice("en", gender=g)
	return "OK"

@app.route('/setParam/<string:param>/<int:val>')
def setParam(param, val):
	if param == "Pitch":
		espeak.set_parameter(espeak.Parameter.Pitch, val)
	elif param == "Volume":
		espeak.set_parameter(espeak.Parameter.Volume, val)
	elif param == "Rate":
		espeak.set_parameter(espeal.Parameter.Rate, val)
	else:
		return "_problem Unknown Parameter"
	return "OK"

@app.route('/say/<string:st>')
def say(st):
    espeak.synth(urllib2.unquote(st))
    return "OK"

@app.route('/reset_all')
def reset_all():
    reset()
    return "OK"

app.run('0.0.0.0', port=9999)
