# MFRC522-python

Python library to read/write RFID tags via the budget MFRC522 RFID module.

<br>

## First Steps

<br>

### Enable SPI

Open the raspberry pi configuration with: `sudo raspi-config`.<br>
In the menu that pops up select `5 Interfacing options`.<br>
And finally enable SPI by selecting `P4 SPI`.<br>
For the changes to take effect, reboot the raspberry pi with? `sudo reboot`.<br>

<br>

### Wiring the Pins

Connect the RC522's Pins to the RaspberryPi's GPIO pins. *No need to connect the IRQ pin.*

RC522 | GPIO pin
----- | ----------:
SDA   | 8
SCK   | 11
MOSI  | 10
MISO  | 9
IRQ   | -
GND   | GND
RST   | 25
3.3V  | 3.3V

