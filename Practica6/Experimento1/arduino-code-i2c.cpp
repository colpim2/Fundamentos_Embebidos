''' 
Lectura de temperatura mediante los pines A0(Vout+) y A1(Vout-).

@Author: Mauricio Matamoros
@License: MIT

@Modify by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.10.17
'''

#include <Wire.h>

// Constantes
#define VAREF 2.7273
#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13

// Variables globales
float temperature = 0;

// Prototipos de funciones
void i2c_received_handler(int count);
void i2c_request_handler(int count);
float read_temp(void);

// ==== Configura el Arduino ===
void setup(void){
	// Configura el ADC para usar la referencia de voltaje desde el pin AREF (externo)
	analogReference(EXTERNAL);
	// Establece la resolución del ADC a 10 bits
	// analogReadResolution(10)

	// Configura el I2C para funcionar en modo esclavo con la dirección definida
	Wire.begin(I2C_SLAVE_ADDR);
	// Configura el manejador para los datos I2C recibidos
	Wire.onReceive(i2c_received_handler);
	// Configura el manejador para solicitudes de datos a través de I2C
	Wire.onRequest(i2c_request_handler);

	// Configura el puerto serial para operar a 56.6kbps
	Serial.begin(56600);

	// Configura el LED de la placa
	pinMode(BOARD_LED, OUTPUT);
}

/* ==== Maneja las solicitudes de datos recibidas a través del bus I2C
*				Enviar inmediatamente la temperatura leída como un valor float === */
void i2c_request_handler(){
	Wire.write((byte*) &temperature, sizeof(float));
}

/* ==== Maneja los datos recibidos a través del bus I2C.
*				Los datos se reenvían al puerto serial y hacen parpadear el LED de la placa === */
void i2c_received_handler(int count){
	char received = 0;
	while (Wire.available()){
		received = (char)Wire.read();
		digitalWrite(BOARD_LED, received ? HIGH : LOW);
		Serial.println(received);
	}
}

/* ==== Lee la temperatura en grados Celsius desde el ADC === */
float read_temp(void){
	// La temperatura real
	int vplus  = analogRead(0);
	// El valor de temperatura de referencia, es decir, 0°C
	int vminus = analogRead(1);
	// Calcula la diferencia. cuando V+ es menor que V- tenemos una temperatura negativa
	int vdiff = vplus - vminus;
	// Temp = vdiff * VAREF / (1024 * 0.01)
	return vdiff * VAREF / 10.24f;
}

void loop(){
	temperature = read_temp();
	delay(100);
}
