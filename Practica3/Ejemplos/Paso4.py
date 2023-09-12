#########################################################
# 1 Led parpadente con PWM
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)  # Pin 32 como salida y habilitar en bajo

pwm = GPIO.PWM(32, 1)     # Inicializar el pin 32 como PWM a una frecuencia de 2Hz


# === Funcionamiento parpadeo PWM ===
pwm.start(50)

flag = True
while flag:
  try:
    dutyCycle = int(input("Ingrese ciclo de trabajo: "))
    pwm.ChangeDutyCycle(dutyCycle)
  except:
    flag = False
    pwm.ChangeDutyCycle(0)

pwm.stop()      # Detiene el PWM
GPIO.cleanup()  # Reinicia los puertos GPIO (cambian de salida a entrada)
