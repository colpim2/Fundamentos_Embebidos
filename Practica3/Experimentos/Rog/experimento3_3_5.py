#!/usr/bin/env python3
# ## ###############################################
#
# pwm.py
# Controls a 7-segments display using Raspberry Pi
# and a 74LS47 driver
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Importa la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importa la función sleep del módulo time
from time import sleep

# Desactivar advertencias (warnings)
# GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
GPIO.setmode(GPIO.BOARD)
# Configurar pines 36, 38, 40 y 37 como salida y habilitar en bajo
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

# Mapea bits a los pines de la GPIO
def bcd7(num):
	GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW )
def marquesina(num):
    GPIO.output(num, GPIO.HIGH)
	

flag = True
numeros=[36,38,40,37]
while flag:
	velocidad = int(input("Ingrese la velocidad (0-100): "))
	while velocidad<0 or velocidad>100:
		velocidad = int(input("Ingrese la velocidad (0-100): "))
	try:
		for i in numeros:
			GPIO.output(i, GPIO.HIGH)
			sleep(velocidad)
			GPIO.output(i, GPIO.LOW)
	except:
		flag = False

# Reinicia los puertos GPIO (cambian de salida a entrada)
GPIO.cleanup()