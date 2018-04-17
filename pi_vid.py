from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
import serial
import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


def loop():
	
	# xs = []
	# ys = []

	#Camera Variables 

	camera = PiCamera()
	camera.resolution = (320, 240)
	camera.vflip = True 
	camera.framerate = 32

	# Wait for the automatic gain control to settle
	time.sleep(2)

	# Now fix the values
	camera.shutter_speed = camera.exposure_speed
	camera.exposure_mode = 'off'
	g = camera.awb_gains
	camera.awb_mode = 'off'
	camera.awb_gains = g

	rawCapture = PiRGBArray(camera, size=(320, 240))

	font = cv2.FONT_HERSHEY_SIMPLEX

	scen_x = 320/2
	scen_y = 240/2

	ser = serial.Serial(

	  port='/dev/ttyACM0',
	  baudrate = 115200,
	  stopbits=serial.STOPBITS_ONE,
	  bytesize=serial.EIGHTBITS,
	  timeout=1,
	  write_timeout=0 )

	i_time = 0 
	f_time = 0 
	t_time = 0 
	velocity = 0 
	p_velocity = 0
	accel = 0
	vel = 0
	i_d = 0
	dis = 0 

	vel_x = 0
	vel_y = 0 

	i_x = 0
	i_y = 0


	for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
		i_time = time.time()

		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
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
			# area = cv2.contourArea(c)
			# print(area)
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
		# pos = str(offset_x)+','+str(offset_y)+'\n'
		pos = str(offset_x)+','+str(offset_y)+','+str(vel_x)+','+str(vel_y)+'\n'


		#ser.write(str('100').encode('utf-8'))
		
		ser.write(str(pos).encode('utf-8'))
		ser.flushInput()
		ser.flushOutput()


		f_time = time.time()

		t_time = f_time - i_time

		#distance = math.sqrt((f_time)**2 + (i_time)**2)
		#print(distance)

		#print(t_time)

		if ((offset_y < 10 and offset_y > -10) and (offset_x < 10 and offset_x > -10)):
			velocity = '0'+' '+'px/s'
			accel = '0'+' '+'px/s^2'
			vel_x = '0'
			vel_y = '0'
		else:
			dis = int((math.sqrt((offset_y)**2 + (offset_x)**2)))
			vel = int ((dis - i_d)/t_time)

			vel_x = str((i_x - offset_x)/t_time)
			vel_y = str((i_y - offset_y)/t_time)

			velocity = str(vel)+' '+'px/s'
			accel = str(int((vel- p_velocity)/t_time))+' '+'px/s^2'


		#print(x)

		cv2.circle(frame, center, 10, (0, 255, 0), -1)
		cv2.putText(frame, offset ,center, font, 1,(255,255,255),2,cv2.LINE_AA)
		cv2.line(frame, (int(scen_x),int(scen_y)), center, (0, 255, 0),5)
		cv2.putText(frame, velocity ,(20,40), font, 1,(0,0,255),2,cv2.LINE_AA)
		cv2.putText(frame, accel ,(20,85), font, 1,(0,0,255),2,cv2.LINE_AA)
		

		#cv2.imshow('thresh', result)
		cv2.imshow('frame', frame)
		cv2.imshow('mask', mask)
		
		key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# data = ser.readline()
		# print(data)

		i_x = offset_x
		i_y = offset_y

		i_d = dis
		p_velocity = vel 

		
		# xs.append(i_time)
		# ys.append(vel)

		# ax1.clear()
		# ax1.plot(xs, ys)


		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break


if __name__ == '__main__':
	
	loop()
	cv2.destroyAllWindows()

