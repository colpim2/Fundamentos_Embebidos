#########################################################
# 7 Leds en marquesina de Derecha a izquierda con PWM
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

gpiout=[32,26,24,22,18,16,12]       # 7 Pines Salida orden inverso a [12,16,18,22,24,26,32]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)      #Habilitación en bajo
    pwm = GPIO.PWM(i, 1)     # Inicializar los pines como PWM a una frecuencia de 2Hz


# === Funcionamiento parpadeo PWM ===
flag = True
while flag:
  try:
    velocidad = int(input("Ingrese la velocidad de parpadeo: "))
    try:
      for i in gpiout:
        pwm.start(50)
        GPIO.output(i, GPIO.HIGH)     # Enciende el led
        sleep(velocidad)        # Pausa según la velocidad
        GPIO.output(i, GPIO.LOW)      # Apaga el led
    except:
      pass
  except:
    flag = False
    pwm.ChangeDutyCycle(0)

pwm.stop()      # Detiene el PWM
GPIO.cleanup()  # Reinicia los puertos GPIO (cambian de salida a entrada)
