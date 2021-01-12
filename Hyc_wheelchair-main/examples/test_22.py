import sys, time
import threading
import keyboard
import numpy as np

from bledevice import scanble, BLEDevice
Device1 = BLEDevice("DD:43:89:16:43:81")
Device2 = BLEDevice("F4:82:B3:50:ED:55")

Device1.writereq(0xd,'545246680D0A') #STOP_flag
Device2.writereq(0xd,'545246680D0A') #STOP_flag
Device1.writereq(0xd,'54524F5F0D0A') #RUN_flag
Device2.writereq(0xd,'54524F5F0D0A') #RUN_flag
Device1.writereq(0xd,'544443790D0A')#CW forward
Device2.writereq(0xd,'544443790D0A')#CW forward
Device1.writereq(0xd,'54571E8B0D0A')#5km/h
Device2.writereq(0xd,'54571E8B0D0A')#5km/h
t = 0;
toggle = 1;
while 1:

	if t>1:

		if toggle == 1:

			Device1.writereq(0xd,'544457650D0A')#CCW backward
			Device2.writereq(0xd,'544457650D0A')#CCW backward
			time.sleep(2);
			
		else :
			Device1.writereq(0xd,'544443790D0A')#CCW forward
			Device2.writereq(0xd,'544443790D0A')#CCW forward
			time.sleep(2);
		toggle = toggle*-1		
	print(t)
	t = t+0.01

	time.sleep(0.01)
