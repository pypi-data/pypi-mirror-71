# Turta Sensor uHAT for Raspberry Pi Zero
Sensor uHAT is a sensor and IR control board for Raspberry Pi Zero.

This repository includes libraries, samples, and component datasheets of Sensor uHAT.

## Features
- Measures temperature, relative humidity, air pressure, and calculates altitude via Bosch Sensortec BME280 environmental sensor.
- Detects movement and theft attempts via accelerometer and tilt sensor NXP MMA8491Q.
- Senses ambient light and UV Index via Silicon Labs SI1133 sensor.
- Controls home electronics via IR remote transmitter.
- Sensor uHAT has Grove System compatible I2C, UART, and digital ports.
- Carries ID EEPROM for Raspberry Pi HAT specification compliance.

## Raspberry Pi Configuration
- You should enable I2C from the Raspberry Pi's configuration. To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable the I2C.

## Documentation
Visit [docs.turta.io](https://docs.turta.io) for documentation.