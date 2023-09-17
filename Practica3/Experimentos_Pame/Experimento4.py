#########################################################
# 7 Leds en marquesina de Derecha a izquierda con PWM
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

gpiout=[12,16,18,22,24,26,32]      # 7 Pines Salida
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)      #Habilitación en bajo

# Inicializar los pines como PWM
pwm_objects = [GPIO.PWM(pin, 100) for pin in gpiout]


# === Funcionamiento marquesina ping pong ===
try:
  velocidad = float(input("Ingrese la velocidad de la marquesina (en segundos): "))
  while True:
    # Recorrido Izquierda a derecha
    for i in range(len(gpiout)):
      pwm_objects[i].start(50)    # Encender el LED actual con PWM
      sleep(velocidad)
      pwm_objects[i].ChangeDutyCycle(0)   # Apagar el LED actual con PWM

    # Recorrido Derecha a izquierda
    for i in range(len(gpiout) - 2, 0, -1):
      pwm_objects[i].start(50)    # Encender el LED actual con PWM
      sleep(velocidad)
      pwm_objects[i].ChangeDutyCycle(0)   # Apagar el LED actual con PWM

except KeyboardInterrupt:
  pass

for pwm in pwm_objects:
  pwm.stop()    # Detiene PWM
GPIO.cleanup()  # Reinicia los puertos GPIO (cambian de salida a entrada)