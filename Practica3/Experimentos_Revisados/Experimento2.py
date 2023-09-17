#########################################################
# 7 Leds en marquesina de Izquierda a derecha
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

# === Funcionamiento marquesina ===
while True:     # Bucle infinito
    for i in gpiout:
        sleep(0.5)     # Espera 500ms
        GPIO.output(i, GPIO.HIGH)     # Enciende el led
        sleep(0.5)
        GPIO.output(i, GPIO.LOW)      # Apaga el led
        


#Revisado 
