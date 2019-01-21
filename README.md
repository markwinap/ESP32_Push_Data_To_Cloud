# ESP32_SigFox_Sonar_Sensor

### I2CXL-MaxSonar - MB7040 PinOut

| PIN | DESCRIPTION | NOTES |
| ------ | ------ | ------ |
| 1 | Temporary Default | This pin is internally pulled high. On power up, the state of this pin is checked; if left high or
disconnected, the sensor will use the address stored memory for I2C communications. If pulled low, the sensor will use its
default address for the current power cycle. |
| 2 | Address Announce / Status | While the sensor is performing a range reading, this pin is set high and I2C
communications are ignored. |
| 3 | Not Used | NA |
| 4 | SDA (I2C Data) | This is the data line for I2C communications. |
| 5 | SCL (I2C Clock) | This is the clock line for I2C communications. |
| 6 | V+ |  2.7V - 5.5V DC. |
| 7 | GND  |  2.7V - 5.5V DC. |


###  SIPY PinOut

| PIN | DESCRIPTION | NOTES |
| ------ | ------ | ------ |
| 18 | GPIO12 SDA (I2C Data) | This is the data line for I2C communications. |
| 20 | GPIO13 SCL (I2C Clock) | This is the clock line for I2C communications. |
| 6 | V+ |  2.7V - 5.5V DC. |
| 7 | GND  |  2.7V - 5.5V DC. |