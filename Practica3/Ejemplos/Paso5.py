#########################################################
# Display 7 segmentos
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

# Configurar pines 36, 38, 40 y 37 como salida y habilitar en bajo
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

# Mapea bits a los pines de la GPIO
def bcd7(num):
  GPIO.output(32, GPIO.HIGH if num & 0x00000008 else GPIO.LOW )
  GPIO.output(38, GPIO.HIGH if num & 0x00000004 else GPIO.LOW )
  GPIO.output(40, GPIO.HIGH if num & 0x00000002 else GPIO.LOW )
  GPIO.output(37, GPIO.HIGH if num & 0x00000001 else GPIO.LOW )

# === Funcionamiento muestra número a display ===
flag = True
while flag:
  try:
    num = int(input("Ingrese número entero: "))
    bcd7(num)
  except:
    flag = False

# Reinicia los puertos GPIO (cambian de salida a entrada)
GPIO.cleanup()