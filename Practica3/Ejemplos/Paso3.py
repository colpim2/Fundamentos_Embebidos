#########################################################
# 1 Led parpadente en pin 32 GPIO Raspberry Pi
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)

GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.
    # Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom

GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)  # Pin 32 como salida y habilitar en bajo

# El siguiente código hace parpadear el led 7
while True:     # Bucle infinito
    sleep(0.5)     # Espera 500ms
    GPIO.output(32, GPIO.HIGH)     # Enciende el led
    sleep(0.5)     # Espera 500ms
    GPIO.output(32, GPIO.LOW)      # Apaga el led