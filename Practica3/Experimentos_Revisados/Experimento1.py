#########################################################
# 7 Leds parpadentes usando la GPIO de la Raspberry Pi

# @Author:
#   -Castillo Montes Pamela
#   -Cruz Cedillo Daniel Alejandro
#   -Hernández Jaimes Rogelio Yael

# @Date: 12/09/2023
#########################################################

# === Librerias ===
    # Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

gpiout=[12,16,18,22,24,26,32]       # 7 Pines Salida
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)      #Habilitación en bajo

# === Funcionamiento  ===
while True:     # Bucle infinito
    sleep(0.5)     # Espera 500ms
    for i in gpiout:
        GPIO.output(i, GPIO.HIGH)     # Enciende el led
    sleep(0.5)
    for i in gpiout:
        GPIO.output(i, GPIO.LOW)      # Apaga el led