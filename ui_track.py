from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
import serial
from tkinter import *
from PIL import Image
from PIL import ImageTk



camera = PiCamera()
camera.resolution = (640, 480)
# camera.framerate = 32
camera.vflip = True 
# camera.exposure_mode = 'sports'
# camera.awb_mode = 'auto'

# camera.resolution = (1280, 720)
camera.framerate = 32
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rawCapture = PiRGBArray(camera, size=(640, 480))

font = cv2.FONT_HERSHEY_SIMPLEX

# time.sleep(0.1)

scen_x = 640/2
scen_y = 480/2

ser = serial.Serial(

  port='/dev/ttyACM0',
  baudrate = 115200,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1,
  write_timeout=0


)



def UI():

	panelA = None
	panelB = None
	
	

	for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		root = Tk()

		frame = img.array

		# show the frame
		hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
		#lower = np.array([140,50,100])
		#GREEEN 
		lower = np.array([40,200,40])
		#YELLOW
		#lower = np.array([70,100,65])

		upper = np.array([255,255,255])
		
		mask = cv2.inRange(hsv, lower, upper)
		#mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

		center = None

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	 
		#print(center)

		if center == None:
			x = scen_x
			y = scen_y
			center = (int(scen_x),int(scen_y))

		else:
			x,y = center 

		offset_x = scen_x - x
		offset_y = scen_y - y 
		offset = str(offset_x)+' '+str(offset_y)
		pos = str(offset_x)+','+str(offset_y)+'\n'

		#ser.write(str('100').encode('utf-8'))
		
		ser.write(str(pos).encode('utf-8'))
		ser.flushInput()
		ser.flushOutput()

		#print(x)

		cv2.circle(frame, center, 10, (0, 255, 0), -1)
		cv2.putText(frame, offset ,center, font, 1,(255,255,255),2,cv2.LINE_AA)
		cv2.line(frame, (int(scen_x),int(scen_y)), center, (0, 255, 0),5)

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# cv2.imshow('test', frame)
		# key = cv2.waitKey(1) & 0xFF

		# if key == ord("q"):
		# 	break

		rawCapture.truncate(0)

		frame = Image.fromarray(frame)
		mask = Image.fromarray(mask)

		frame = ImageTk.PhotoImage(frame)
		mask = ImageTk.PhotoImage(mask)

		if panelA is None or panelB is None:

			panelA = Label(root, image=frame)
			panelA.frame = frame
			panelA.pack(side = "left", padx =10, pady =10)

			panelB = Label(root, image=mask)
			panelB.mask = mask
			panelB.pack(side = "right", padx =10, pady =10)

		else: 

			panelA.configure(image= frame)
			panelA.image = frame
			panelB.configure(image = mask)
			panelA.image = mask


		
		# panelA = None
		# panelB = None

		root.mainloop()
		

if __name__ == '__main__':
	UI()


