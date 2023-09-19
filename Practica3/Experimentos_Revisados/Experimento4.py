#########################################################
# 7 Leds en marquesina Ping-Pong

# @Author:
#   -Castillo Montes Pamela
#   -Cruz Cedillo Daniel Alejandro
#   -Hernández Jaimes Rogelio Yael

# @Date: 12/09/2023
#########################################################

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
gpiout_inv=[12,16,18,22,24,26,32]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)


def ingresa_velocidad():
    global velocidad
    while True:
        velocidad = int(input("Ingrese la velocidad (ms):  ")) #entre 100 para que sea un retraso de máximo 1 seg
        while velocidad<0 :
                velocidad = int(input("Ingrese la velocidad (ms):  ")) #entre 100 para que sea un retraso de máximo 1 seg
        print("Velocidad seleccionada: "+str(velocidad))

def enciende_leds():
    # El siguiente código hace parpadear el led
    while True: # Bucle infinito
        global velocidad
        for i in gpiout:
            GPIO.output(i, GPIO.HIGH) # Enciende el led
            sleep(velocidad/1000)                 # Espera 500ms
            GPIO.output(i, GPIO.LOW)  # Apaga el led
        for i in gpiout_inv:
            GPIO.output(i, GPIO.HIGH) # Enciende el led
            sleep(velocidad/1000)                 # Espera 500ms
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