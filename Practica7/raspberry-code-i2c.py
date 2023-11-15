''' 
Interactúa con un Arduino a través de I2C para calcula variaciones de fase y escriber valores de potencia.

@Author: Mauricio Matamoros
@License: MIT

@Modify by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.11.14
'''

import smbus2
import struct
import time
import math

# Variables globales
d={}
timeEnable=1000

# Dirección I2C del dispositivo Arduino
SLAVE_ADDR = 0x0A

# Inicializa el bus I2C
# RPI version 1 requiere smbus.SMBus(0)
i2c = smbus2.SMBus(1)

# === Obtener la lectura de potencia desde el esclavo ===
def readPower():
	try:
		# Leer 4 bytes de datos del dispositivo esclavo
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)
		data = list(msg)
		# Convertir los bytes en un valor de temperatura (float)
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		pwr = struct.unpack('<f', ba)
		# print('Received temp: {} = {}'.format(data, pwr))
		return pwr
	except:
		return None

# === Escribe el valor del potencia al Arduino === 
def writePower(pwr):
	try:
		data = struct.pack('<f', pwr) # Empaqueta como float
		# Crea el mensaje de 4 bytes
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)  # Realiza la escritura
	except:
		pass

# === Calcula la potencia basanda en el ángulo alpha ===
def power_factor(alpha):
	result = math.sin(2.0 * alpha)/2.0
	result+= math.pi - alpha
	result/= math.pi
	return math.sqrt(result)

# === Convierte el ángulo a tiempo ===
def a2t(alpha, freq = 60):
	return alpha / (2 * math.pi * freq)

# === Calcula e imprime las variaciones de fase [0, pi] ===
def phase_calc():
	global d
	N = 1000
	d = {}
	# Calcula n variaciones de fase
	for i in range(0, N):
		alpha = i * math.pi / N
		#pf = "{0:.2f}".format(100 * power_factor(alpha))
		pf = 100 * power_factor(alpha)
		pf=round(pf,2)
		#t = "{0:.3f}ms".format(1000 * a2t(alpha))
		t =1000 * a2t(alpha)
		t=round(t,4)
		if pf not in d:
			d[pf] = t
			print("{}: {}".format(pf, t))

# === Interpola el tiempo por el factor de potencia ===
def interpolate_time(val):
	global d
	j=0
	k=0

	for i in d:
		if i<=val:
			j=i
			break
		k=i
	if k==val:
		y=d[k]    # Limite superior
	elif j==val:
		y=d[j]    # Limite inferior
	else:
		y=d[j]+((val-j)/(k-j))*(d[k]-d[j])
		y=round(y, 4)
	print("Valor estimado: "+str(y))
	yu=(int)(y*1000)
	print("t(us): "+str(yu))
	return yu


def main():
	global timeEnable
	phase_calc()
	while True:
		try:
			power = input("Power? ")
			power = float(power)
			if power >= 0 and power <= 100:
				timeEnable=interpolate_time(power)
				writePower(timeEnable)
				#print("\tPower set to {}".format(readPower()))
			else:
				print("\tInvalid!")
		except:
			print("\tInvalid!")

if __name__ == '__main__':
	main()
