#! /usr/bin/python

import urllib2
from flask import Flask
import cv2
import numpy as np

fk = Flask("Color Detection Scratch Helper")
fk.logger.removeHandler(fk.logger.handlers[0])

cap = cv2.VideoCapture(0)
print cap
hsv_range = {"Lower" : np.array([0, 0, 0], np.uint8),
             "Upper" : np.array([0, 0, 0], np.uint8)}
hsv_p = {"Hue" : 0, "Saturation" : 1, "Value" : 2}
hrset = {}

min_size = 0

_camset = False
_rangeset = False

def largest_contour(contours):
	max_contour = [0, None]
	if contours:
		for idx, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > max_contour[0]:
				max_contour = [area, contour]
		return max_contour[1]
	return []


@fk.route('/poll')
def poll():
	 detected = False
	 if not (_camset and _rangeset):
	 	return "_problem Set Camera and the HSV range to begin\n"
	 _, img = cap.read()
	 timg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	 timg = cv2.inRange(timg, hsv_range["Lower"], hsv_range["Upper"])
	 timg = cv2.dilate(timg, np.ones((5, 5), "uint8"))
	 _, conts, hier = cv2.findContours(timg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	 dr = largest_contour(conts)
	 if len(dr) != 0 and cv2.contourArea(dr) > min_size:
	 	h, w, _ = img.shape
		(x, y), r = cv2.minEnclosingCircle(dr)
		c = (int(x), int(y))
		r = int(r)
		cv2.circle(img, c, r, (0, 255, 0), 2)
		cv2.imshow("colorDetr", img)
		cv2.waitKey(10)
		detected = True
	 return "isDetected " + str("true" if detected else "false") + "\n"

@fk.route('/setMinSize/<int:siz>')
def setMinSize(siz):
	global min_size
	min_size = np.abs(siz)
	return "OK"

@fk.route('/setCamera/<int:cam>')
def setCamera(cam):
	global cap; global _camset
	if cam != 0:
		cap = cv2.VideoCapture(cam)
	_camset = True
	return "OK"

@fk.route('/setRange/<string:ranget>/<string:hsvp>/<int:rangev>')
def setParam(ranget, hsvp, rangev):
	global hsv_range; global _rangeset; global hrset
	hsv_range[ranget][hsv_p[hsvp]] = rangev
	hrset[ranget+hsvp] = 0
	if len(hrset.keys()) == 6:
		_rangeset = True
	return "OK"

@fk.route('/setColor')
def setColor(st):
    return "OK"

@fk.route('/reset_all')
def reset_all():
    return "OK"

fk.run('0.0.0.0', port=8888)
