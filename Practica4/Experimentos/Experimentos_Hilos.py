# !/usr/bin/env python3
# ## ###############################################
#
# led_manager.py
# Controls leds in the GPIO
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

#LEDS
gpiout=[12,16,18,22,24,26,32]       # 7 Pines Salida
gpiout_inv=[32,26,24,22,18,16,12]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)      #Habilitación en bajo

#7Seg
gpiout_seg=[38,40,37]		#Se omite 32 porque ya se habilito en bajo
for i in gpiout_seg:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)      #Habilitación en bajo


""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
def leds(num):
	for i in gpiout:
		GPIO.output(i, GPIO.LOW)      # Apaga todos los leds

	GPIO.output(gpiout[num-1], GPIO.HIGH)     # Enciende el led "num"

""" Activa el modo marquesina
	type toma tres valores: left, right y pingpong
	(To be developed by the student)
"""
def marquee(type='pingpong'):
	switcher = {
		'left'     : _marquee_left,
		'right'    : _marquee_right,
		'pingpong' : _marquee_pingpong
	}
	func = switcher.get(type, None)
	if func:
		func()


"""	Despliega en número proporcionado en el display de siete segmentos.
	(To be developed by the student)
"""
def bcd(num):
	# Mapea bits a los pines de la GPIO
	GPIO.output(37, GPIO.HIGH if num & 0x00000008 else GPIO.LOW ) #Si
	GPIO.output(40, GPIO.HIGH if num & 0x00000004 else GPIO.LOW ) #Si
	GPIO.output(38, GPIO.HIGH if num & 0x00000002 else GPIO.LOW ) #Si
	GPIO.output(36, GPIO.HIGH if num & 0x00000001 else GPIO.LOW ) #Si

	pass

""" Activa el modo marquesina continua a la izquierda"""
def _marquee_left():
	while True:     # Bucle infinito
		for i in gpiout:
			sleep(0.5)     # Espera 500ms
			GPIO.output(i, GPIO.HIGH)     # Enciende el led
			sleep(0.5)
			GPIO.output(i, GPIO.LOW)      # Apaga el led
	pass

""" Activa el modo marquesina continua a la derecha"""
def _marquee_right():
	while True:     # Bucle infinito
		for i in gpiout_inv:
			sleep(0.5)     # Espera 500ms
			GPIO.output(i, GPIO.HIGH)     # Enciende el led
			sleep(0.5)
			GPIO.output(i, GPIO.LOW)      # Apaga el led
	pass

""" Activa el modo marquesina ping-pong"""
def _marquee_pingpong():
	while True: # Bucle infinito
		for i in gpiout:
				GPIO.output(i, GPIO.HIGH) # Enciende el led
				sleep(0.5)                 # Espera 500ms
				GPIO.output(i, GPIO.LOW)  # Apaga el led
		for i in gpiout_inv:
				GPIO.output(i, GPIO.HIGH) # Enciende el led
				sleep(0.5)                 # Espera 500ms
				GPIO.output(i, GPIO.LOW)  # Apaga el led
	pass
