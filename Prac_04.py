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

def Reset(channel):
	print("Reset")
	
def Frequency(channel):
	print("Frequency")
	
	global Delay
	global FrequencyIndex
	FrequencyIndex += 1
	
	if FrequencyIndex > 2:
		FrequencyIndex = 0
		
	if FrequencyIndex == 0:
		Delay = 0.5
		
	elif FrequencyIndex == 1:
		Delay = 1
		
	elif FrequencyIndex == 2:
		Delay = 2
	
	
def Stop(channel):
	print("Stop")
	
	global Run
	if Run:
		Run = 0
	else:
		Run = 1

def Display(channel):
	print("Display")
	print(Five_Recent[4])
	print(Five_Recent[3])
	print(Five_Recent[2])
	print(Five_Recent[1])
	print(Five_Recent[0])

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
GPIO.add_event_detect(ResetPin, GPIO.FALLING,bouncetime=300)
GPIO.add_event_callback(ResetPin, Reset)

GPIO.add_event_detect(FrequencyPin, GPIO.FALLING,bouncetime=300)
GPIO.add_event_callback(FrequencyPin, Frequency)

GPIO.add_event_detect(StopPin, GPIO.FALLING,bouncetime=300)
GPIO.add_event_callback(StopPin, Stop)

GPIO.add_event_detect(DisplayPin, GPIO.FALLING,bouncetime=300)
GPIO.add_event_callback(DisplayPin, Display)

# Open SPI bus
spi = spidev.SpiDev() # create spi object 
spi.open(0,0) 
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
	temp = (data * 3.3) / float(1023) 
	temp = round(temp,0) 
	return temp
	
def ConvertLight(data): 
	light = (data * 100) / float(1023) 
	light = round(light,0) 
	return light

def Add_to_5_Recent(data):
	global Five_Recent
	Five_Recent[4] = Five_Recent[3]
	Five_Recent[3] = Five_Recent[2]
	Five_Recent[2] = Five_Recent[1]
	Five_Recent[1] = Five_Recent[0]
	Five_Recent[0] = data
	
# Define sensor channels 
Temp_channel = 0 
Pot_channel = 1
Light_channel = 2

Start_Time_H = time.strftime("%H")
Start_Time_M = time.strftime("%M")
Start_Time_S = time.strftime("%S")

print("Time     Timer    Pot      Temp      Light"
	
try: 
	while True: 
		if Run:
			Current_Time = time.strftime("%H:%M:%S")
			Timer_Time = "00:00:00"
			
			# Read the data 
			Temp_data = GetData(Temp_channel) 
			Temp_degrees = ConvertTemp(Temp_data)
			
			Pot_data = GetData(Pot_channel)
			Pot_volts = ConvertVolts(Pot_data)
			
			Light_data = GetData(Light_channel)
			Light_percent = ConvertLight(Light_data)
			
			data = Current_Time + " " + Timer_Time + " " + str(Pot_volts) + "V     " + str(Temp_degrees) + "C      " + str(Light_percent) + "%"
			Add_to_5_Recent(data)
			
			# Wait before repeating loop 
			time.sleep(Delay) 
	
except KeyboardInterrupt: 
	spi.close()