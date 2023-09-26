''' 
Integración, para un servidor web, de funciones:
1. Encendido del del 1-7 al presionar el boton adecuado
2. Desplegado de la marquesina izquierda al presionar el boton adecuado
3. Desplegado de la marquesina derecha al presionar el boton adecuado
4. Desplegado de la marquesina tipo ping-pong al presionar el boton adecuado
5. Desplegado del dígito correcto en el display de 7 segmentos al presionar el boton correspondiente

@Author:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.09.23
'''

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Librería de control del GPIO de la Raspberry Pi y tiempo
import RPi.GPIO as GPIO
from time import sleep

# Clase Threading
import threading

# Definiciones de GPIO
GPIO.setmode(GPIO.BOARD)
velocidad=200

# Configurar los pines 32-40 como salida y habilitar en bajo
gpiout=[32,26,24,22,18,16,12]
gpiout_inv=[12,16,18,22,24,26,32]
for i in gpiout:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)

# Se establece los pines  36, 38, 40 y 37 como salida y se habilitan en bajo. Pines para el Display
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

# Creamos evento de parada
wait_event=threading.Event()

# Hilo global, este contendrá todas las posibles funciones
thread=threading.Thread()

## === FUNCIONES AUXILIARES ===
# Finaliza el funcionamiento de los hilos
def thread_finalize():
    global wait_event
    global thread
    wait_event.clear()
    if thread.is_alive():
        thread.join()
    wait_event.set()

# Apaga todos los leds y el display de 7 segmentos
def leds_off():
    for i in gpiout:
        GPIO.output(i, GPIO.LOW)      # Apaga todos los leds

    #Apaga display de 7 segmentos:
    GPIO.output(37, GPIO.LOW )
    GPIO.output(40, GPIO.LOW )
    GPIO.output(38, GPIO.LOW )
    GPIO.output(36, GPIO.LOW )


## === FUNCIONES PRINIPALES ===

# === Enciende el leds especificados en num, apagando los demás ===
    # num: numero de led a encender, el valor num va de 1-7, por lo que debe restarse 1 para acceder al led real
def leds(num):
    thread_finalize()       #Termina la ejecución de cualquier hilo (marquesina) en ejecucion
    leds_off()              #Apaga todos los leds
    GPIO.output(gpiout[num-1], GPIO.HIGH)     # Enciende el led "num", menos uno para acceder en rango 0-6


# === Activa el modo marquesina ===
    # type toma tres valores: left, right y pingpong
def marquee(type='pingpong'):
    global wait_event
    global thread

    #Bloquea todos los hilos (eventos bloqueados)
    switcher = {
        'left'     : _marquee_left,
        'right'    : _marquee_right,
        'pingpong' : _marquee_pingpong
    }

    thread_finalize()
    leds_off()          #Apaga todos los leds
    func = switcher.get(type, None)
    if func:
        thread=threading.Thread(target=func,args=())
        thread.start()


# === Despliega en número proporcionado en el display de siete segmentos ===
def bcd(num):
    thread_finalize()       #Finaliza cualquier hilo (marquesina) en ejecución
    leds_off()              #Apaga todos los leds

    # Mapea bits a los pines de la GPIO
    GPIO.output(37, GPIO.HIGH if num & 0x00000008 else GPIO.LOW ) 
    GPIO.output(40, GPIO.HIGH if num & 0x00000004 else GPIO.LOW ) 
    GPIO.output(38, GPIO.HIGH if num & 0x00000002 else GPIO.LOW ) 
    GPIO.output(36, GPIO.HIGH if num & 0x00000001 else GPIO.LOW ) 


# === Activa el modo marquesina continua a la izquierda ===
def _marquee_left():
    global wait_event
    global velocidad
    while wait_event.is_set():  # Bucle infinito
        # Secuencia de encendido derecha a izquierda
        for i in gpiout:            
            GPIO.output(i, GPIO.HIGH)       # Enciende el led
            sleep(velocidad/1000)           # Espera Xms,  entre 1000 para el valor ingresado sea en milisegundos
            GPIO.output(i, GPIO.LOW)        # Apaga el led


# === Activa el modo marquesina continua a la derecha ===
def _marquee_right():
    global wait_event
    global velocidad
    while wait_event.is_set():  # Bucle infinito
        # Secuencia de encendido de izquierda a derecha
        for i in gpiout_inv:    
            GPIO.output(i, GPIO.HIGH)   # Enciende el led
            sleep(velocidad/1000)       # Espera Xms,  entre 1000 para el valor ingresado sea en milisegundos
            GPIO.output(i, GPIO.LOW)    # Apaga el led

# === Activa el modo marquesina ping-pong ===
def _marquee_pingpong():
    global wait_event
    global velocidad
    while wait_event.is_set():  # Bucle infinito
        #Secuencia de encendido derecha a izquierda
        for i in gpiout:         
            GPIO.output(i, GPIO.HIGH)   # Enciende el led
            sleep(velocidad/1000)       # Espera Xms,  entre 1000 para el valor ingresado sea en milisegundos
            GPIO.output(i, GPIO.LOW)    # Apaga el led
        #Secuencia de encendido izquierda a derecha
        for i in gpiout_inv:    
            GPIO.output(i, GPIO.HIGH)   # Enciende el led
            sleep(velocidad/1000)       # Espera Xms,  entre 1000 para el valor ingresado sea en milisegundos
            GPIO.output(i, GPIO.LOW)    # Apaga el led
