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

