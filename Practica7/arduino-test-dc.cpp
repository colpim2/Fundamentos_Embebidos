/*
Controla la salida de energía de una carga resistiva utilizando la detección de cruce por cero y un TRIAC.
Código para Arduino UNO.

@Author: Mauricio Matamoros
@License: MIT

@Modify by:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.11.14
*/

#include <Wire.h>

// Constantes
#define ZXPIN 2   // Digital 2 is Pin 2 in UNO
#define TRIAC 3   // Digital 3 is Pin 3 in UNO
#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13

// Prototipos de funciones
void i2c_received_handler(int count);
void i2c_request_handler(int count);
void turnLampOn(void);

// Variables globales
volatile bool flag = false;
int pdelay = 0;
int inc = 1;


// ==== Configura el Arduino ===
void setup(void){
	// Configura el I2C para funcionar en modo esclavo con la dirección definida
	Wire.begin(I2C_SLAVE_ADDR);
	// Configura el manejador para los datos I2C recibidos
	Wire.onReceive(i2c_received_handler);
	// Configura el manejador para solicitudes de datos a través de I2C
	Wire.onRequest(i2c_request_handler);
	// Configura el pin como interrupción INPUT
	pinMode(ZXPIN, INPUT);
	// digitalPinToInterrupt may not work, so we choose directly the
	// interrupt number. It is Zero for pin 2 on Arduino UNO
	// attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
	attachInterrupt(0, zxhandle, RISING);
	// Configura el TRIAC como salida
	pinMode(TRIAC, OUTPUT);
	// Configura el LED
	pinMode(13, OUTPUT);
	Serial.begin(9600);
}

/* ==== Maneja las solicitudes de datos recibidas a través del bus I2C
*				Enviar inmediatamente la temperatura leída como un valor float === */
void i2c_request_handler(){
	Wire.write((byte*) &pdelay, sizeof(float));
}

/* ==== Maneja los datos recibidos a través del bus I2C.
*				Los datos se reenvían al puerto serial y hacen parpadear el LED de la placa === */
void i2c_received_handler(int count){
	float f;
	byte *fp;
	if(count != 4) return;
	byte bytes[4]; // Arreglo para almacenar los bytes
	for (byte i = 0; i < count; ++i)
      bytes[i] = Wire.read();
	memcpy(&f, bytes, sizeof(float));
	pdelay = f;
}

void loop(){
	char buffer[20];
	//sprintf(buffer, "Power = %.2f\n", pdelay);
	//Serial.write(buffer);
	delay(1000);
}

void turnLampOn(){
	// Enciende el LED o foco
	digitalWrite(13, HIGH);
	// Envia un pulso de 10us al TRIAC
	digitalWrite(TRIAC, HIGH);
	delayMicroseconds(20);
	digitalWrite(TRIAC, LOW);
}

void zxhandle(){
	flag = true;
	// Apaga el TRIAC automaticamente en ZX
	digitalWrite(TRIAC, LOW);
	digitalWrite(2, LOW);

	delayMicroseconds(pdelay);

	if(pdelay > 0) turnLampOn();
}