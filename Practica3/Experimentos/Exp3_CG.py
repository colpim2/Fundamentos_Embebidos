import RPi.GPIO as GPIO
from time import sleep

# Configuración GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pines de salida para los 7 LEDs (en orden inverso)
gpiout = [12, 16, 18, 22, 24, 26, 32]

# Inicializar los pines como salidas
for pin in gpiout:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Inicializar los pines como PWM
pwm_objects = [GPIO.PWM(pin, 100) for pin in gpiout]

# Funcionamiento de la marquesina PWM
try:
    velocidad = float(input("Ingrese la velocidad de la marquesina (en segundos): "))
    while True:
        for i, pin in enumerate(gpiout):
            # Encender el LED actual con PWM
            pwm_objects[i].start(50)
            sleep(velocidad)

            # Apagar el LED actual con PWM
            pwm_objects[i].ChangeDutyCycle(0)
        
except KeyboardInterrupt:
    pass

# Detener y limpiar los objetos PWM y los pines GPIO
for pwm in pwm_objects:
    pwm.stop()

GPIO.cleanup()
