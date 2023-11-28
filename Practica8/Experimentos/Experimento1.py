''' 
Despliega en consola la temperatura sensada por el DS18B20 cada segundo.

@Author by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.11.28
'''

import time

# Serie del sensor
model_temp = "28-d37beb086461"

def main():
  while True:  
    # Leer la información desde el archivo "w1_slave"
    with open('/sys/bus/w1/devices/'+ model_temp + "/w1_slave", 'r') as f:
      contenido = f.read()
      temp = contenido.split('=')

      # Conversiones
      print("Celcius = "+ str(int(temp[len(temp)-1])/1000))
      print("Fahreheit = " + str((int(temp[len(temp)-1])/1000)*(9/5)+32))

    time.sleep(1)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
