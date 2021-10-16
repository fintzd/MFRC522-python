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
from MFRC522 import MFRC522


class Read_KEY:
    
    def __init__(self):
        self.READER = MFRC522()
        self.KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.DATALOCATION = [8, 9, 10]

    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n

    def read_info(self):
        (status, TagType) = self.READER.Request_MFRC522(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        
        (status, uid) = self.READER.Anticoll_MFRC522()
        if status != self.READER.MI_OK:
            return None, None

        id = self.uid_to_num(uid)
        
        self.READER.SelectTag_MFRC522(uid)
        status = self.READER.Auth_MFRC522(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        
        buff = []
        if status == self.READER.MI_OK:
            for block_num in self.DATALOCATION:
                block = self.READER.Read(block_num) 
                if block:
            		buff += block
            if buff:
                 data = ''.join(chr(i) for i in buff)
        
        self.READER.StopCrypto1_MFRC522()
        return id, data
