''' 
Lectura de temperatura desde un sensor conectado a través de I2C en Raspberry Pi
y graficación de los valores leidos.

@Author: Mauricio Matamoros
@License: MIT

@Modify by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.10.17
'''

import smbus2
import struct
import time
import traceback
import matplotlib.pyplot as plt
import numpy as np

# Dirección I2C del dispositivo Arduino
SLAVE_ADDR = 0x0A

# Nombre del archivo en el que se guarda el registro de temperatura
LOG_FILE = './temp.log'

# Inicializar el bus I2C;
i2c = smbus2.SMBus(1)		# RPI versión 1 requiere smbus.SMBus(0)

# Historiales
temp_register = []
tiempo = []
cont = 0

# === Obtener la lectura de temperatura desde el esclavo ===
def readTemperature():
	try:
		# Leer 4 bytes de datos del dispositivo esclavo
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)
		data = list(msg)
		# Convertir los bytes en un valor de temperatura (float)
		ba = bytearray(data[0:4])
		temp = struct.unpack('<f', ba)
		print('Temperatura recibida: {} = {}°C'.format(data, temp))
		return temp
	except:
		traceback.print_exc()
		return None

# === Bitácora de temperaturas recibidas y graficación  ===
def log_temp(temperature):
	global cont
	global temp_register
	global tiempo
	tiem = time.ctime(time.time())
	try:
	# Registrar la temperatura en un archivo LOG
		with open(LOG_FILE, 'w+') as fp:
			fp.write('{} {}°C\n'.format(tiem,temperature))
			print('Hora: {}  Temperatura: {}'.format(tiem, temperature))
	except:
		return
	if cont < 10:
		temp_register.append(temperature)
		tiempo.append(tiem)
		cont = cont + 1
		print("Añadiendo elemento")
	else:
		print("Dibujando")
		plt.plot(tiempo, temp_register, label='Temperatura-Tiempo')
		plt.xlabel('Tiempo')
		plt.ylabel('Temperatura [°C]')
		plt.title('Registro de Temperatura')
		plt.legend()
		plt.show()
		cont = 0
		temp_register = []
		tiempo = []


def main():
	while True:
		try:
			cTemp = readTemperature()
			log_temp(cTemp)
			time.sleep(1)
		except KeyboardInterrupt:
			return

if __name__ == '__main__':
    main()
