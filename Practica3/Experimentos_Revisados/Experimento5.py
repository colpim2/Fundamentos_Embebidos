#########################################################
# Parpadeo gradual
#########################################################

import RPi.GPIO as GPIO     # Librería de control GPIO de Raspberry Pi
from time import sleep      # Función sleep del módulo time

#=== Configuración GPIO ===
GPIO.setwarnings(False)     # Desactivar advertencias (warnings)
GPIO.setmode(GPIO.BOARD)    # Configurar el número de pin.

led_pin = 32    # Pin para el LED que se atenuará gradualmente
GPIO.setup(led_pin, GPIO.OUT)     # Configurar el pin como salida

gpiout=[12,16,18,22,24,26]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)


# === Función atenuar el LED gradualmente ===
pwm = GPIO.PWM(led_pin, 100)  # Crear objeto PWM con una frecuencia de 100 Hz
pwm.start(0)    # Iniciar con ciclo de trabajo del 0% (LED apagado)

flag = True
while flag:
  try:
    # Encender gradualmente el LED
    for duty_cycle in range(0, 101):
      pwm.ChangeDutyCycle(duty_cycle)   # Cambiar el ciclo de trabajo
      sleep(0.01)    # Pausa para transición gradual

    sleep(0.5)    # Mantener encendido el LED durante medio segundo

    # Apagar gradualmente el LED
    for duty_cycle in range(100, -1, -1):
      pwm.ChangeDutyCycle(duty_cycle)
      sleep(0.01)

  except:
    flag = False
    pwm.stop()  # Detener el PWM al salir
    GPIO.cleanup()    # Reiniciar los puertos GPIO (cambian de salida a entrada)




#Revisado 
