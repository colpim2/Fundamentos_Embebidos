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
velocidad=200
# Configurar los pines 32-40 como salida y habilitar en bajo
gpiout=[32,26,24,22,18,16,12]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)


def ingresa_velocidad():
    global velocidad
    while True:
        velocidad = int(input("Ingrese la velocidad (ms):  ")) #entre 100 para que sea un retraso de máximo 1 seg
        while velocidad<0:
            velocidad = int(input("Ingrese la velocidad (ms):  ")) #entre 100 para que sea un retraso de máximo 1 seg
        print("Velocidad seleccionada: "+str(velocidad))

def enciende_leds():
    # El siguiente código hace parpadear el led
    while True: # Bucle infinito
        global velocidad
        for i in gpiout:
            GPIO.output(i, GPIO.HIGH) # Enciende el led
            sleep(velocidad/1000)                 # Espera Xms
            GPIO.output(i, GPIO.LOW)  # Apaga el led

#Inicialización de hilos
hilo1=threading.Thread(target=ingresa_velocidad,args=())
hilo2=threading.Thread(target=enciende_leds,args=())

hilo2.start()
hilo1.start()
#Ejecución de hilos
hilo1.join()
hilo2.join()

print("Fin de programa")




#Revisado 
