#!/usr/bin/env python3

#    -*- coding: utf8 -*-
#
#    Copyright 2021
#
#    This file is part of MFRC522-Python.
# 
#    MFRC522-Python is a simple Python implementation for the MFRC522 NFC Card Reader
#    for the Raspberry Pi.
#
#    This is a free software: 
#    You can redistribute it and/or modify it under the terms of the GNU Lesser General 
#    Public License as published by the Free Software Foundation, either version 3 of 
#    the License, or (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#    See the GNU Lesser General Public License for more details.


import RPi.GPIO as GPIO
import spidev
import signal
from time import sleep
import logging


class MFRC522:
    RSTGPIO             = 25
    
    MAX_LEN             = 16
    
    PCD_IDLE            = 0x00
    PCD_AUTHENT         = 0x0E
    PCD_RECEIVE         = 0x08
    PCD_TRANSMIT        = 0x04
    PCD_TRANSCEIVE      = 0x0C
    PCD_RESETPHASE      = 0x0F
    PCD_CALCCRC         = 0x03
    
    PICC_REQIDL         = 0x26
    PICC_REQALL         = 0x52
    PICC_ANTICOLL       = 0x93
    PICC_SELECTTAG      = 0x93
    PICC_AUTHENT1A      = 0x60
    PICC_AUTHENT1B      = 0x61
    PICC_READ           = 0x30
    PICC_WRITE          = 0xA0
    PICC_DECREMENT      = 0xC0
    PICC_INCREMENT      = 0xC1
    PICC_RESTORE        = 0xC2
    PICC_TRANSFER       = 0xB0
    PICC_HALT           = 0x50
    
    MI_OK               = 0
    MI_NOTAGERR         = 1
    MI_ERR              = 2
    
    Reserved00          = 0x00
    CommandReg          = 0x01
    CommIEnReg          = 0x02
    DivlEnReg           = 0x03
    CommIrqReg          = 0x04
    DivIrqReg           = 0x05
    ErrorReg            = 0x06
    Status1Reg          = 0x07
    Status2Reg          = 0x08
    FIFODataReg         = 0x09
    FIFOLevelReg        = 0x0A
    WaterLevelReg       = 0x0B
    ControlReg          = 0x0C
    BitFramingReg       = 0x0D
    CollReg             = 0x0E
    Reserved01          = 0x0F
    
    Reserved10          = 0x10
    ModeReg             = 0x11
    TxModeReg           = 0x12
    RxModeReg           = 0x13
    TxControlReg        = 0x14
    TxAutoReg           = 0x15
    TxSelReg            = 0x16
    RxSelReg            = 0x17
    RxThresholdReg      = 0x18
    DemodReg            = 0x19
    Reserved11          = 0x1A
    Reserved12          = 0x1B
    MifareReg           = 0x1C
    Reserved13          = 0x1D
    Reserved14          = 0x1E
    SerialSpeedReg      = 0x1F
    
    Reserved20          = 0x20
    CRCResultRegM       = 0x21
    CRCResultRegL       = 0x22
    Reserved21          = 0x23
    ModWidthReg         = 0x24
    Reserved22          = 0x25
    RFCfgReg            = 0x26
    GsNReg              = 0x27
    CWGsPReg            = 0x28
    ModGsPReg           = 0x29
    TModeReg            = 0x2A
    TPrescalerReg       = 0x2B
    TReloadRegH         = 0x2C
    TReloadRegL         = 0x2D
    TCounterValueRegH   = 0x2E
    TCounterValueRegL   = 0x2F
    
    Reserved30          = 0x30
    TestSel1Reg         = 0x31
    TestSel2Reg         = 0x32
    TestPinEnReg        = 0x33
    TestPinValueReg     = 0x34
    TestBusReg          = 0x35
    AutoTestReg         = 0x36
    VersionReg          = 0x37
    AnalogTestReg       = 0x38
    TestDAC1Reg         = 0x39
    TestDAC2Reg         = 0x3A
    TestADCReg          = 0x3B
    Reserved31          = 0x3C
    Reserved32          = 0x3D
    Reserved33          = 0x3E
    Reserved34          = 0x3F
        
    serNum = []
    

    def __init__(self, bus=0, device=0, spd=1000000):
        # setup spi
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = spd
        # setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RSTGPIO, GPIO.OUT)
        GPIO.output(self.RSTGPIO, 1)
        # initialise
        self.MFRC522_Init()

        
