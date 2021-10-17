# MFRC522-python

Python library to read and write RFID tags via the MFRC522 RFID module.

<br>

## First Things First


### Enable SPI

Open the raspberry pi configuration with: `sudo raspi-config`.<br>
In the menu that pops up select `5 Interfacing options`.<br>
And finally enable SPI by selecting `P4 SPI`.<br>
For the changes to take effect, reboot the raspberry pi with? `sudo reboot`.<br>


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

<br>

Pin numbers in the table above are based on the GPIO numbering, **not the pin numbering**. You can check out the following image for more information about how to wire the reader.

![GPIO-Pinout-Diagram-2](https://user-images.githubusercontent.com/35842457/137625592-c4a3e099-f2b6-406f-b158-6eb90a4393b3.jpg)
*image source: [https://www.raspberrypi.com/](https://www.raspberrypi.com/documentation/computers/os.html)*

<br>

## Installation and Setup

You can either simple clone this repository to where you want to use it and import the scripts into your code from there, or install this as a module.


### Setup - Clone and Edit

First install the dependencies required to run this code, which are git, python-dev, and spidev. You can do this with the following bash commands.

```bash
sudo apt install git python-dev -y
python3 -m pip install spidev
```


Simply use the following bash commands to clone the repo. Once executed, you're in and ready to go.

```bash
cd ~
git clone https://github.com/fintzd/MFRC522-python.git
cd MFRC522-python/
```


### Setup - With `setup.py`

First install the dependencies required to run this code, which are git & python-dev. You can do this with the following bash commands.

```bash
sudo apt install git python-dev -y
```

Then you can use the `setup.py` file to set this script up. To do this, use the following commands in the top level directory (or wherever you want to use it). *Mind you, that we are using python3 in this repository.*

```bash
cd ~
git clone https://github.com/fintzd/MFRC522-python.git
cd MFRC522-python/
sudo python3 setup.py install
```


### Setup - As a Python Module

***TODO***


<br>

## Just a Simple Use Case

***TODO***
