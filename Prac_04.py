#!/usr/bin/python
import RPi.GPIO as GPIO
import spidev
import time
import os 
import sys

global FrequencyIndex
FrequencyIndex = 0

global Delay
Delay = 0.5

global Run
Run = 1

global Five_Recent
Five_Recent = ["","","","",""]

global First_5
First_5 = ["","","","",""]

def Reset(channel):
	print("Reset")
	global Start_Time_H
	Start_Time_H = int(time.strftime("%H", time.localtime()))
	global Start_Time_M
	Start_Time_M = int(time.strftime("%M"))
	global Start_Time_S
	Start_Time_S = int(time.strftime("%S"))
	
	clear = lambda: os.system("cls")
	clear()
	
def Frequency(channel):
	
	global Delay
	global FrequencyIndex
	FrequencyIndex += 1
	
	if FrequencyIndex > 2:
		FrequencyIndex = 0
		
	if FrequencyIndex == 0:
		Delay = 0.5
		print("Frequency = 0.5s")
		
	elif FrequencyIndex == 1:
		Delay = 1
		print("Frequency = 1s")
		
	elif FrequencyIndex == 2:
		Delay = 2
		print("Frequency = 2s")
	
	
def Stop(channel):
	#print("Stop/Start")
	global Run
	if Run:
		Run = 0
		print("Stop")	
	else:
		Run = 1
		print("Start")
		First_5[0] = Read_All_Sensors()
		time.sleep(Delay)
		First_5[1] = Read_All_Sensors()
		time.sleep(Delay)
		First_5[2] = Read_All_Sensors()
		time.sleep(Delay)
		First_5[3] = Read_All_Sensors()
		time.sleep(Delay)
		First_5[4] = Read_All_Sensors()
		time.sleep(Delay)

def Display(channel):
	print("Display")
	print("Time     Timer    Pot      Temp      Light")
	print(First_5[0])
	print(First_5[1])
	print(First_5[2])
	print(First_5[3])
	print(First_5[4])

GPIO.setmode(GPIO.BCM) # use GPIO pin numbering

ResetPin = 5 
FrequencyPin = 6 
StopPin = 13
DisplayPin =  19

# Set up buttons
GPIO.setup(ResetPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(FrequencyPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(StopPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(DisplayPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setwarnings(False)

# Add Events 
GPIO.add_event_detect(ResetPin, GPIO.FALLING,bouncetime=400)
GPIO.add_event_callback(ResetPin, Reset)

GPIO.add_event_detect(FrequencyPin, GPIO.FALLING,bouncetime=400)
GPIO.add_event_callback(FrequencyPin, Frequency)

GPIO.add_event_detect(StopPin, GPIO.FALLING,bouncetime=400)
GPIO.add_event_callback(StopPin, Stop)

GPIO.add_event_detect(DisplayPin, GPIO.FALLING,bouncetime=400)
GPIO.add_event_callback(DisplayPin, Display)

# Open SPI bus
spi = spidev.SpiDev() # create spi object 
spi.open(0,0) 
spi.max_speed_hz = 1000000 #adjust max speed of spi interface
# RPI has one bus (#0) and two devices (#0 & #1) 

# function to read ADC data from a channel 
def GetData(channel): # channel must be an integer 0-7 
	adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes 
	data = ((adc[1]&3) << 8) + adc[2] 
	return data 
	
# functions to convert data to respective units 
def ConvertVolts(data): 
	volts = (data * 3.3) / float(1023) 
	volts = round(volts,1) 
	return volts 
	
def ConvertTemp(data): 
	temp = (data * 330) / float(1023) -50
	temp = round(temp,1) 
	return temp
	
def ConvertLight(data): 
	light = (data * 100) / float(1023) 
	light = round(light,0) 
	return light

# def Add_to_5_Recent(data):
	# global Five_Recent
	# Five_Recent[4] = Five_Recent[3]
	# Five_Recent[3] = Five_Recent[2]
	# Five_Recent[2] = Five_Recent[1]
	# Five_Recent[1] = Five_Recent[0]
	# Five_Recent[0] = data
	
# Define sensor channels 
Temp_channel = 0 
Pot_channel = 1
Light_channel = 2

global Start_Time_H
Start_Time_H = int(time.strftime("%H", time.localtime()))
global Start_Time_M
Start_Time_M = int(time.strftime("%M"))
global Start_Time_S
Start_Time_S = int(time.strftime("%S"))

def Stopwatch():
	global Start_Time_H
	global Start_Time_M
	global Start_Time_S
	
	Current_Time_H = int(time.strftime("%H", time.localtime()))
	Current_Time_M = int(time.strftime("%M"))
	Current_Time_S = int(time.strftime("%S"))
	
	Seconds_Elapsed = (Current_Time_H - Start_Time_H)*3600 + (Current_Time_M - Start_Time_M)*60 + (Current_Time_S - Start_Time_S)

	Time_Elapsed_H = Seconds_Elapsed//3600
	Seconds_Elapsed -= Time_Elapsed_H*3600
	
	Time_Elapsed_M = Seconds_Elapsed//60
	Seconds_Elapsed -= Time_Elapsed_M*60
	
	Time_Elapsed_S = Seconds_Elapsed
	Seconds_Elapsed -= Time_Elapsed_S
	
	Time_Elapsed_H = str(Time_Elapsed_H)
	Time_Elapsed_M = str(Time_Elapsed_M)
	Time_Elapsed_S = str(Time_Elapsed_S)
	
	if len(Time_Elapsed_H) < 2:
		Time_Elapsed_H = "0"+Time_Elapsed_H
	if len(Time_Elapsed_M) < 2:
		Time_Elapsed_M = "0"+Time_Elapsed_M
	if len(Time_Elapsed_S) < 2:
		Time_Elapsed_S = "0"+Time_Elapsed_S
		
	return Time_Elapsed_H + ":" + Time_Elapsed_M + ":" + Time_Elapsed_S
	
def Read_All_Sensors():
	Current_Time = time.strftime("%H:%M:%S", time.localtime())
	Timer_Time = Stopwatch()
	
	# Read the data 
	Temp_data = GetData(Temp_channel) 
	Temp_degrees = ConvertTemp(Temp_data)
	
	Pot_data = GetData(Pot_channel)
	Pot_volts = ConvertVolts(Pot_data)
	
	Light_data = GetData(Light_channel)
	Light_percent = ConvertLight(Light_data)
	
	data = Current_Time + " " + Timer_Time + " " + str(Pot_volts) + "V     " + str(Temp_degrees) + "C      " + str(Light_percent) + "%"
	
	# Wait before repeating loop 
	#time.sleep(Delay)
	
	return data
	
	

print("Environment Monitor")
x = 1

try: 
	while True: 
		if x == 1:
			First_5[0] = Read_All_Sensors()
			time.sleep(Delay)
			First_5[1] = Read_All_Sensors()
			time.sleep(Delay)
			First_5[2] = Read_All_Sensors()
			time.sleep(Delay)
			First_5[3] = Read_All_Sensors()
			time.sleep(Delay)
			First_5[4] = Read_All_Sensors()
			time.sleep(Delay)
			
			x=2
		else:
			#Just keep busy - an empty "while True" seems to slow Pi down
			y = Read_All_Sensors()
			
except KeyboardInterrupt: 
	spi.close()
