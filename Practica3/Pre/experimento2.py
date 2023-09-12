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

# Desactivar advertencias (warnings)
# GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
# Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom
GPIO.setmode(GPIO.BOARD)

# Configurar los pines 32-40 como salida y habilitar en bajo
gpiout=[12,16,18,22,24,26,32]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)


# El siguiente código hace parpadear el led
while True: # Bucle infinito
    for i in gpiout:
        GPIO.output(i, GPIO.HIGH) # Enciende el led
        sleep(0.5)                 # Espera 500ms
        GPIO.output(i, GPIO.LOW)  # Apaga el led




