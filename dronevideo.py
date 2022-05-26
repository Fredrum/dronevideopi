#!/usr/bin/python3

import time
import subprocess
import ctypes
from sdl2 import *
#import sdl2.ext
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
#import libcamera   NEWER OFFICIAL?

def apply_timestamp(request):
    timestamp = time.strftime("%Y-%m-%d %X")

# Needed for PyBluez bluetooth
#sudo apt-get install libbluetooth-dev
#sudo apt-get install python-dev
#pip3 install PyBluez
#import bluetooth
# '84:17:66:D6:66:8D' - Wireless Controller (not green sticker)

####  Bluetooth Connection using command line
# Gamepad must have been set to Trusted
while True:
	time.sleep(1)
	print("bluetooth searching for controller 84:17:66:D6:66:8D")
	btcmd = "bluetoothctl info 84:17:66:D6:66:8D"
	process = subprocess.Popen(btcmd.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	btFound = output.decode('UTF-8')
	print("output: " + btFound )
	#print("error: " + str(error))
	if(btFound.find("Connected: yes") > -1):
		print("Bluetooth found connected controller")
		break



#####  Camera + Video setup
is_recording = False
picam2 = Picamera2()

video_config_720 = picam2.video_configuration({"size": (1280, 720)},
											raw={"size": (1640, 1232)},
											controls={"FrameDurationLimits": (16666, 16666)})

video_config_1080 = picam2.video_configuration({"size": (1920, 1080)},
											raw={"size": (1640, 1232)},
											controls={"FrameDurationLimits": (33333, 33333)})

#picam2.set_controls({"AwbEnable": 0, "AeEnable": 0}) #works
#picam2.start_preview(Preview.QTGL)

encoder = H264Encoder(20000000, False, 10)	# bitrate, repeat, iperiod
picam2.pre_callback = apply_timestamp






#### SDL and main loop
SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_GAMECONTROLLER | SDL_INIT_EVENTS)
#sdl2.ext.init()
controller = SDL_GameController()

numjoy = SDL_NumJoysticks()
print("SDL detected Gamepads:  "  + str(numjoy))
if(numjoy > 0):
	controller = SDL_GameControllerOpen(0)
	SDL_JoystickEventState(SDL_ENABLE);
	SDL_GameControllerRumble(controller, 30000, 30000, 1000)


print("\nstarting main loop\n")
event = SDL_Event()
while True:
	while SDL_PollEvent(ctypes.byref(event)) != 0:
		if event.type == SDL_QUIT:
			running = False
			break
		elif event.type == SDL_JOYBUTTONDOWN:
						
			if(event.jbutton.button == 0):		# X
				SDL_GameControllerRumble(controller, 30000, 30000, 1000)
				if (is_recording):
					picam2.stop_recording()
					is_recording = False
					print("Stopped Recording")
				else:
					picam2.configure(video_config_1080)
					picam2.start_recording(encoder, 'test.h264')
					is_recording = True
					print("Started Recording")
					
			if(event.jbutton.button == 1):		# O
				SDL_GameControllerRumble(controller, 40000, 40000, 250)
				if (is_recording):
					picam2.stop_recording()
					is_recording = False
					print("Stopped Recording")
			
			if(event.jbutton.button == 2):		# ^
				SDL_GameControllerRumble(controller, 30000, 30000, 1000)
				if (is_recording):
					picam2.stop_recording()
					is_recording = False
					print("Stopped Recording")
				else:
					picam2.configure(video_config_720)
					picam2.start_recording(encoder, 'test.h264')
					is_recording = True
					print("Started Recording")






print("quitting")
quit(1)
