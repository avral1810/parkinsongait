from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math 
import datetime
import os
import time





# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
ap.add_argument("-s", "--save", help = "Record data", required = False)

args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
current_millis = lambda: int((time.time()) * 1000)

name = input('Enter name of the subject : ')
height = input('Enter height (cm) of the subject : ')
today = datetime.date.today()
today = str(today)
startTime = datetime.datetime.now()
startTime = str(startTime)

"""Aditya
greenLower = (27, 117, 14)
greenUpper = (154, 169, 172)

blueLower = (96, 117, 23)
blueUpper = (145, 255, 184)

redLower = (135, 125, 82)
redUpper = (216, 255, 255)

ARU
greenLower = (39, 102, 146)
greenUpper = (87, 169, 255)

blueLower = (18, 201, 106)
blueUpper = (255, 255, 255)

redLower = (116, 129, 198)
redUpper = (223, 229, 255)
"""
#LARI
greenLower = (36, 105, 155)
greenUpper = (92, 219, 255)

blueLower = (15, 201, 187)
blueUpper = (255, 255, 255)

redLower = (144, 66, 170)
redUpper = (200, 217, 255)



pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

print('Working on video')
old_timer = current_millis()
# keep looping
timeIter = int(0)
while True:
	if current_millis() - old_timer >= 1000:
		timeIter += 1
		print(str(timeIter) + "s")
		old_timer = current_millis()
	# grab the current frame
	(grabbed, frame) = camera.read()
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=800)
	frame = frame[100:][20:]
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	maskGreen = cv2.inRange(hsv, greenLower, greenUpper)
	maskGreen = cv2.erode(maskGreen, None, iterations=2)
	maskGreen = cv2.dilate(maskGreen, None, iterations=2)

	maskRed = cv2.inRange(hsv, redLower, redUpper)
	maskRed = cv2.erode(maskRed, None, iterations=2)
	maskRed = cv2.dilate(maskRed, None, iterations=2)

	maskBlue = cv2.inRange(hsv, blueLower, blueUpper)
	maskBlue = cv2.erode(maskBlue, None, iterations=2)
	maskBlue = cv2.dilate(maskBlue, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cntsGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	cntsRed = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	cntsBlue = cv2.findContours(maskBlue.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	
	centerGreen = None
	centerBlue = None
	centerRed = None
 
	if len(cntsGreen) > 0:
		cnts = cntsGreen
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		centerGreen = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
			cv2.circle(frame, centerGreen, 5, (0, 255, 0), -1)

	if len(cntsRed) > 0:
		cnts = cntsRed
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		centerRed = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
			cv2.circle(frame, centerRed, 5, (0, 0, 255), -1)

	if len(cntsBlue) > 0:
		cnts = cntsBlue
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		centerBlue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x), int(y)), int(radius),(255, 0, 0), 2)
			cv2.circle(frame, centerBlue, 5, (255, 0, 0), -1)


	
	cv2.line(frame, centerGreen, centerBlue, (255,255,0),1)
	cv2.line(frame, centerGreen, centerRed, (0,255,255),1)

	if centerBlue and centerGreen and centerRed:
		printTime = str(current_millis())
		printStr = name + ":" + str(height) + ":" + str(centerBlue) + ":" + str(centerGreen) + ":" + str(centerRed) + ":" + printTime +"\n"
		if args.get("save"):
			what = args["save"]
			if what == "train":
				try:
					try:
						os.mkdir('dataFiles/' + name)
					except:
						pass
					try:
						os.mkdir('dataFiles/' + name + '/' + today)
					except:
						pass
					file = open('datafiles/' + name + '/' + today + '/' + startTime + '.txt','a')
					print('Test File Created')
					file.write(printStr)
					file.close()
				except:
					print("Error")
					camera.release()
					cv2.destroyAllWindows()
			elif what == "run":
				try:
					try: 
						os.mkdir('datafiles/test1/' + today)
					except:
						pass
					file = open('datafiles/test1/' + today + '/' + startTime + '.txt','a')
					print('Test File Created')
					file.write(printStr2)
					file.close()
				except:
					print("Error")
					camera.release()
					cv2.destroyAllWindows()	

		else:
			print(printStr)


	ok = int(0)

	if centerGreen:
		centerGreen = list(centerGreen)
		ok += 1

	if centerRed:
		centerRed = list(centerRed)
		ok += 1
	if centerBlue:
		centerBlue = list(centerBlue)
		ok +=1

	if ok == 3: 
		pass

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

if args.get("save"):
	try:
		i = int(0)
		what = args["save"]
		if what == "train":
			file = open('datafiles/' + name + '/' + today + '/' + startTime + '.txt','r')
			print('File Written')
			for e_line in file:
				i = i + 1
			file.close()
			exit('datafiles/' + name + '/' + today + '/' + startTime + '.txt')
		elif what == "run":
			file = open('datafiles/test1/' + today + '/' + startTime + '.txt')
			print('File Written')
			for e_line in file:
				i = i + 1
			file.close()
			exit('datafiles/test1/' + today + '/' + startTime + '.txt')
	except:
		print("Error in writing file")
		exit("ERROR")

else:
	print("Done")
	exit("NOT")