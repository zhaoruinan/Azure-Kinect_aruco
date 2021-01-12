#!/usr/bin/env python3
"""PyBluez example read_name.py
Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
This software is under the terms of GPLv3 or later.
"""

import sys

from bluetooth.ble import GATTRequester


class Reader:

    def __init__(self, address):
        self.requester1 = GATTRequester("40:06:A0:97:74:A9", False)
        self.requester2 = GATTRequester("40:06:A0:94:FE:F7", False)

        self.connect()
        self.send_data()
        #self.request_data()

    def connect(self):
        print("Connecting...", end=" ")
        sys.stdout.flush()

        self.requester1.connect(True)
        self.requester2.connect(True)

        print("OK.")

    def request_data(self):
        data1 = self.requester1.read_by_uuid(
            "00001800-0000-1000-8000-00805f9b34fb")[0]
        data2 = self.requester2.read_by_uuid(
            "00001800-0000-1000-8000-00805f9b34fb")[0]

        try:
            print("Device name:", data1.decode("utf-8"))
        except AttributeError:
            print("Device name:", data1)

    def send_data(self):
        #data = str(bytearray("TTWU"))
        #print("Send Ok ,"+data)
        print("sidong off")
        self.requester1.write_by_handle(0x12, b'\x54\x52\x46\x68\x0D\x0A')
        self.requester2.write_by_handle(0x12, b'\x54\x52\x46\x68\x0D\x0A')
        #print("brake")
        #self.requester1.write_by_handle(0x12, b'\x54\x53\x53\x5A\x0D\x0A')
        #self.requester2.write_by_handle(0x12, b'\x54\x53\x53\x5A\x0D\x0A')
        print("Sidong ON")
        #self.requester1.write_by_handle(0x12, b'\x54\x52\x4E\x60\x0D\x0A')        
        #self.requester2.write_by_handle(0x12, b'\x54\x52\x4E\x60\x0D\x0A')        
        print("SPEED SLOW")
        #self.requester1.write_by_handle(0x12, b'\x54\x57\x32\x77\x0D\x0A')        
        #self.requester2.write_by_handle(0x12, b'\x54\x57\x32\x77\x0D\x0A')
        print("SPEED FULL")
        #self.requester1.write_by_handle(0x12, b'\x54\x57\x82\x27\x0D\x0A')        
        #self.requester2.write_by_handle(0x12, b'\x54\x57\x82\x27\x0D\x0A')        


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    Reader("40:06:A0:97:74:A9")
   
    print("Done.")
