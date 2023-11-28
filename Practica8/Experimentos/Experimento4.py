''' 
Imprime en la primera línea del display LCD el apellido paterno de algun integrante del equipo y en la segunda la lectura de la temperatura en C° y F°

@Author by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.11.28
'''

import smbus
import time
import socket
from datetime import timedelta

# Parametros del sensor de temperatura
model_temp = "28-d37beb086461"

# Parametros del dispositivo LCD
I2C_ADDR  = 0x27 # Direccion I2C
LCD_WIDTH = 16   # Max. caracter por línea
bus = smbus.SMBus(1) # Versiones anteriores usan 0

# === BANDERAS ===
# Modo
LCD_CHR = 1 # Modo - Envio commando
LCD_CMD = 0 # Modo - Envio data

# Luz del display
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

# Direccion
LCD_1LINE = 0x80
LCD_2LINE = 0xC0

# Modo bit
ENABLE = 0b00000100

# Tiempo
E_PULSE = 0.0001
E_DELAY = 0.0001

# === COMANDOS ===
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02


# === Cambio entre modos ===
def lcd_toggle(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)


# === Envia comando o caracter ===
def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High&Low bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle(bits_high)
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle(bits_low)


# === Inicialización del display ===
def lcd_init():
  lcd_byte(0x33,LCD_CMD) # Inicializar
  lcd_byte(0x32,LCD_CMD) # Inicializar
  lcd_byte(0x28,LCD_CMD) # Data length, number of lines, font size

  lcd_byte(0x06,LCD_CMD) # Dirección de movimiento del cursor
  lcd_byte(0x0C,LCD_CMD) # Display On, Cursor Off, Parpadeo Off

  lcd_byte(LCD_CLEARDISPLAY,LCD_CMD) # Limpia Display
  time.sleep(E_DELAY)


# === Envia un string al LCD ===
def lcd_msj(message,line):
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

# === Envia un string al LCD y espera 1 segundo para actualizarla ===
def lcd_msj_refresh_1s(message,line):
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
  time.sleep(1)

# === Lee la temperatura en C° desde el archivo "w1_slave" ===
def temp_Celcius():
  with open('/sys/bus/w1/devices/'+ model_temp + "/w1_slave", 'r') as f:
    contenido = f.read()
    temp = contenido.split('=')

    tempCelcius = "C: "+ str(int(int(temp[len(temp)-1])/1000))+ "   "
  return tempCelcius

# === Lee la temperatura en F° desde el archivo "w1_slave" ===
def temp_Fahrenheit():
  with open('/sys/bus/w1/devices/'+ model_temp + "/w1_slave", 'r') as f:
    contenido = f.read()
    temp = contenido.split('=')

    tempFahrenheit = "F: " + str(int((int(temp[len(temp)-1])/1000)*(9/5)+32))
  return tempFahrenheit

def main():
  lcd_init()

  while True:
    lcd_msj("Castillo Montes",LCD_1LINE)
    lcd_msj_refresh_1s(temp_Celcius()+temp_Fahrenheit(),LCD_2LINE)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(LCD_CLEARDISPLAY, LCD_CMD)
    lcd_byte(LCD_RETURNHOME, LCD_CMD)
