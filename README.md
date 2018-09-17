# EEE3096S_Prac04
The objective of practical 4 is to develop code for a simple environment monitor system.
The system includes a temperature sensor (MCP9700A), a LDR (1K), a pot (1K), a
MCP3008 IC and three switches.

The monitor works as follow:

  • By default, the system continuously monitors the sensors every 500ms using this
    format:
    
    Time:     Timer:    Pot:  Temp:   Light:
    10:17:15  00:00:00  0.5V  25C     10%
    10:17:20  00:00:05  1.5V  30C     68%
    
  • The reset switch resets the timer and clean the console
  
  • The frequency switch changes the frequency of the monitoring. The possible
    frequencies are 500ms, 1s, 2s. The frequency must loop between those values per
    event occurrence.
    
  • The stop switch stops or starts the monitoring of the sensors. The timer is not
    affected by this functionality.
    
  • The display switch displays the first five reading since the stop switch was
    pressed.
    
