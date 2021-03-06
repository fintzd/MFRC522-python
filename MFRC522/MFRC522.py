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


from time import sleep

from datetime import datetime as dt

import RPi.GPIO as GPIO
import spidev


class MFRC522:
    RSTGPIO = 25

    MAX_LEN = 16

    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03

    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SELECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ = 0x30
    PICC_WRITE = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE = 0xC2
    PICC_TRANSFER = 0xB0
    PICC_HALT = 0x50

    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2

    Reserved00 = 0x00
    CommandReg = 0x01
    CommIEnReg = 0x02
    DivlEnReg = 0x03
    CommIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E
    Reserved01 = 0x0F

    Reserved10 = 0x10
    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxAutoReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19
    Reserved11 = 0x1A
    Reserved12 = 0x1B
    MifareReg = 0x1C
    Reserved13 = 0x1D
    Reserved14 = 0x1E
    SerialSpeedReg = 0x1F

    Reserved20 = 0x20
    CRCResultRegM = 0x21
    CRCResultRegL = 0x22
    Reserved21 = 0x23
    ModWidthReg = 0x24
    Reserved22 = 0x25
    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    TCounterValueRegH = 0x2E
    TCounterValueRegL = 0x2F

    Reserved30 = 0x30
    TestSel1Reg = 0x31
    TestSel2Reg = 0x32
    TestPinEnReg = 0x33
    TestPinValueReg = 0x34
    TestBusReg = 0x35
    AutoTestReg = 0x36
    VersionReg = 0x37
    AnalogTestReg = 0x38
    TestDAC1Reg = 0x39
    TestDAC2Reg = 0x3A
    TestADCReg = 0x3B
    Reserved31 = 0x3C
    Reserved32 = 0x3D
    Reserved33 = 0x3E
    Reserved34 = 0x3F

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
        self.Init()

    def Reset_MFRC522(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)

    def Write_MFRC522(self, addr, val):
        val = self.spi.xfer2([(addr << 1) & 0x7E, val])

    def Read_MFRC522(self, addr):
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return val[1]

    def SetBitMask_MFRC522(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp | mask)

    def ClearBitMask_MFRC522(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp & (~mask))

    def AntennaOn_MFRC522(self):
        temp = self.Read_MFRC522(self.TxControlReg)
        if (~(temp & 0x03)):
            self.SetBitMask_MFRC522(self.TxControlReg, 0x03)

    def AntennaOff_MFRC522(self):
        self.ClearBitMask_MFRC522(self.TxControlReg, 0x03)

    def Communicate_MFRC522(self, command, sendData):
        backData = []
        backLen = 0
        status = self.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0

        if command == self.PCD_AUTHENT:
            irqEn = 0x12
            waitIRq = 0x10
        if command == self.PCD_TRANSCEIVE:
            irqEn = 0x77
            waitIRq = 0x30

        self.Write_MFRC522(self.CommIEnReg, irqEn | 0x80)
        self.ClearBitMask_MFRC522(self.CommIrqReg, 0x80)
        self.SetBitMask_MFRC522(self.FIFOLevelReg, 0x80)

        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE)

        for i, item in enumerate(sendData):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])

        self.Write_MFRC522(self.CommandReg, command)

        if command == self.PCD_TRANSCEIVE:
            self.SetBitMask_MFRC522(self.BitFramingReg, 0x80)

        i = 2000
        while True:
            sleep(0.01)
            n = self.Read_MFRC522(self.CommIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x01) and not (n & waitIRq)):
                break

        self.ClearBitMask_MFRC522(self.BitFramingReg, 0x80)

        if i != 0:
            if (self.Read_MFRC522(self.ErrorReg) & 0x1B) == 0x00:
                status = self.MI_OK

                if n & irqEn & 0x01:
                    status = self.MI_NOTAGERR

                if command == self.PCD_TRANSCEIVE:
                    n = self.Read_MFRC522(self.FIFOLevelReg)
                    lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
                    if lastBits != 0:
                        backLen = (n - 1) * 8 + lastBits
                    else:
                        backLen = n * 8

                    if n == 0:
                        n = 1
                    if n > self.MAX_LEN:
                        n = self.MAX_LEN

                    for i in range(n):
                        backData.append(self.Read_MFRC522(self.FIFODataReg))
            else:
                status = self.MI_ERR
        return (status, backData, backLen)

    def Request_MFRC522(self, reqMode):
        status = None
        backBits = None
        TagType = []

        self.Write_MFRC522(self.BitFramingReg, 0x07)
        TagType.append(reqMode)

        (status, backData, backBits) = self.Communicate_MFRC522(
            self.PCD_TRANSCEIVE, TagType)

        if ((status != self.MI_OK) | (backBits != 0x10)):
            status = self.MI_ERR

        return (status, backBits)

    def Anticoll_MFRC522(self):
        backData = []
        serNumCheck = 0
        serNum = []

        self.Write_MFRC522(self.BitFramingReg, 0x00)

        serNum.append(self.PICC_ANTICOLL)
        serNum.append(0x20)

        (status, backData, backBits) = self.Communicate_MFRC522(
            self.PCD_TRANSCEIVE, serNum)

        if (status == self.MI_OK):
            if len(backData) == 5:
                for i in range(4):
                    serNumCheck = serNumCheck ^ backData[i]
                if serNumCheck != backData[4]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR
        return (status, backData)

    def CalulateCRC_MFRC522(self, pIndata):
        self.ClearBitMask_MFRC522(self.DivIrqReg, 0x04)
        self.SetBitMask_MFRC522(self.FIFOLevelReg, 0x80)

        for i, item in enumerate(pIndata):
            self.Write_MFRC522(self.FIFODataReg, pIndata[i])

        self.Write_MFRC522(self.CommandReg, self.PCD_CALCCRC)

        i = 0xFF
        while True:
            n = self.Read_MFRC522(self.DivIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break

        pOutData = []
        pOutData.append(self.Read_MFRC522(self.CRCResultRegL))
        pOutData.append(self.Read_MFRC522(self.CRCResultRegM))
        return pOutData

    def SelectTag_MFRC522(self, serNum):
        backData = []
        buff = []
        buff.append(self.PICC_SELECTTAG)
        buff.append(0x70)

        for i in range(5):
            buff.append(serNum[i])

        pOut = self.CalulateCRC_MFRC522(buff)

        buff.append(pOut[0])
        buff.append(pOut[1])

        (status, backData, backLen) = self.Communicate_MFRC522(
            self.PCD_TRANSCEIVE, buff)

        if (status == self.MI_OK) and (backLen == 0x18):
            return backData[0]
        return 0

    def Auth_MFRC522(self, authMode, BlockAddr, Sectorkey, serNum):
        buff = []
        buff.append(authMode)
        buff.append(BlockAddr)

        for i, item in enumerate(Sectorkey):
            buff.append(Sectorkey[i])

        for i in range(4):
            buff.append(serNum[i])

        (status, backData, backLen) = self.Communicate_MFRC522(
            self.PCD_AUTHENT, buff)
        return status

    def StopCrypto_MFRC522(self):
        self.ClearBitMask_MFRC522(self.Status2Reg, 0x08)

    def Read(self, blockAddr):
        recvData = []
        recvData.append(self.PICC_READ)
        recvData.append(blockAddr)

        pOut = self.CalulateCRC_MFRC522(recvData)

        recvData.append(pOut[0])
        recvData.append(pOut[1])

        (status, backData, backLen) = self.Communicate_MFRC522(
            self.PCD_TRANSCEIVE, recvData)

        if not (status == self.MI_OK):
            now = dt.now().strftime("%Y%m%d-%H:%M:%S")
            print(f"{now} - Reading error")
        return backData

    def Write(self, blockAddr, writeData):
        buff = []
        buff.append(self.PICC_WRITE)
        buff.append(blockAddr)

        crc = self.CalulateCRC_MFRC522(buff)

        buff.append(crc[0])
        buff.append(crc[1])

        (status, backData, backLen) = self.Communicate_MFRC522(
            self.PCD_TRANSCEIVE, buff)

        if not (status == self.MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
            status = self.MI_ERR

        if status == self.MI_OK:
            buff = []

            for i in range(16):
                buff.append(writeData[i])

            crc = self.CalulateCRC_MFRC522(buff)

            buff.append(crc[0])
            buff.append(crc[1])

            (status, backData, backLen) = self.Communicate_MFRC522(
                self.PCD_TRANSCEIVE, buff)

            if not (status == self.MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
                status = self.MI_ERR
                now = dt.now().strftime("%Y%m%d-%H:%M:%S")
                print(f"{now} - Writing error")
        return status

    def DumpClassic1K(self, key, uid):
        for i in range(64):
            status = self.Auth_MFRC522(self.PICC_AUTHENT1A, i, key, uid)
            if status == self.MI_OK:
                self.Read(i)
            else:
                now = dt.now().strftime("%Y%m%d-%H:%M:%S")
                print(f"{now} - Authentication error")

    def Init(self):
        self.Reset_MFRC522()
        self.Write_MFRC522(self.TModeReg, 0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL, 30)
        self.Write_MFRC522(self.TReloadRegH, 0)
        self.Write_MFRC522(self.TxAutoReg, 0x40)
        self.Write_MFRC522(self.ModeReg, 0x3D)
        self.AntennaOn_MFRC522()
