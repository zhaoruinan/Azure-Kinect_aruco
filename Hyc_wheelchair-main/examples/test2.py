import sys, time
from bledevice import scanble, BLEDevice
Device1 = BLEDevice("DD:43:89:16:43:81")
Device2 = BLEDevice("F4:82:B3:50:ED:55")
def data_ON(Device1,Device2):
	Device1.writereq(0xd,'545457550D0A') #RUN_flag
	Device2.writereq(0xd,'545457550D0A') #RUN_flag
def data_OFF(Device1,Device2):
	Device1.writereq(0xd,'545446660D0A') #RUN_flag
	Device2.writereq(0xd,'545446660D0A') #RUN_flag
def motor_OFF(Device1,Device2):
	Device1.writereq(0xd,'545246680D0A') #RUN_flag
	Device2.writereq(0xd,'545246680D0A') #RUN_flag
def motor_ON(Device1,Device2):
	Device1.writereq(0xd,'54524F5F0D0A') #RUN_flag
	Device2.writereq(0xd,'54524F5F0D0A') #RUN_flag
def M_FWD(Device1,Device2,direciton):
	#motor_ON()
	print("M_FWD")
	
	if direction == -1:
		M_STOP();
		time.sleep(0.2)
		Device1.writereq(0xd,'544443790D0A')#CCW forward
		Device2.writereq(0xd,'544443790D0A')#CCW forward
		direction = 1;
		motor_ON();
		M_IDLE()
	Device1.writereq(0xd,'545750590D0A')#5km/h
	Device2.writereq(0xd,'545750590D0A')#5km/h
def M_IDLE(Device1,Device2):
	#motor_ON()
	#print("MOTOR IDLE\n");
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
def M_BWD(Device1,Device2,direction):
	#motor_ON()
	global direction
	if direction == 1:
		M_STOP();
		time.sleep(0.2)
		Device1.writereq(0xd,'544457650D0A')#CW backward
		Device2.writereq(0xd,'544457650D0A')#CW backward
		direction = -1;
		motor_ON();
		M_IDLE()
	Device1.writereq(0xd,'545708A10D0A')#0.8km/h
	Device2.writereq(0xd,'545708A10D0A')#0.8km/h
def M_RIGHT(Device1,Device2):
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545732770D0A')#5km/h
def M_LEFT(Device1,Device2):
	Device1.writereq(0xd,'545732770D0A')#5km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
def M_STOP(Device1,Device2):
	Device1.writereq(0xd,'545700A90D0A')#0km/h
	Device2.writereq(0xd,'545700A90D0A')#0km/h
def fFASTER(Device1,Device2):
	Device1.writereq(0xd,'547575160D0A')#Spd_Up
	Device2.writereq(0xd,'547575160D0A')#Spd_Up
def fSLOWER(Device1,Device2):
	Device1.writereq(0xd,'546464380D0A')#Spd_Down
	Device2.writereq(0xd,'546464380D0A')#Spd_Down

def M_FWD_RIGHT(Device1,Device2):
	print("\nM_FWD_RIGHT")
def M_FWD_LEFT(Device1,Device2):
	print("\nM_FWD_LEFT")

#vh=Device1.getvaluehandle(b"0000ffe1")
Device1.writereq(0xd,'54524F5F0D0A')
Device2.writereq(0xd,'54524F5F0D0A')
time.sleep(0.5)
sum_time = 0;
mean_time = 0;
count = 0;
while True:
	count = count+1;	
	start = time.time() 
	data = Device1.notify();
	sum_time = sum_time + time.time() - start;
	mean_time = sum_time/count;
	print("time :", time.time() - start,"mean_time : ",mean_time,"\n",);
	print(data)
	print("\n")

'''
while True:
    #vh=hm10.getvaluehandle("ffe1")
    #hm10.writecmd(vh, "hello\r\n".encode('hex'))
    vh=hm10.getvaluehandle(b"0000ffe1")
    hm10.writecmd(vh, bytes("test\r\n".encode('utf-8')).hex())
    data = hm10.notify()
    if data is not None:
        print("Received: ", data)
    time.sleep(1)
'''
