#!/usr/bin/env python3
# ## ###############################################
#
# pwm.py
# Blinks a led on pin 32 using Raspberry Pi
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
#Importa la clase Threading
import threading
# Desactivar advertencias (warnings)
# GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
# Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom
GPIO.setmode(GPIO.BOARD)

# Configurar los pines 32-40 como salida y habilitar en bajo
gpiout=[32,26,24,22,18,16,12]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)

velocidad=-1 #variable "global" velocidad, indica la velocidad con la que se hace el cambio de 

def ingresa_velocidad():
    while True:
        while velocidad<0 or velocidad>100:
            velocidad = int(input("Ingrese la velocidad (0-100):  "))/100 #entre 100 para que sea un retraso de máximo 1 seg

def enciende_leds():
    # El siguiente código hace parpadear el led
    while True: # Bucle infinito
        for i in gpiout:
            GPIO.output(i, GPIO.HIGH) # Enciende el led
            sleep(velocidad)                 # Espera 500ms
            GPIO.output(i, GPIO.LOW)  # Apaga el led

#Inicialización de hilos
hilo1=threading.Thread(target=ingresa_velocidad)
hilo2=threading.Thread(target=enciende_leds)

#Ejecución de hilos
hilo1.start()
hilo2.start()

print("Fin de programa")
