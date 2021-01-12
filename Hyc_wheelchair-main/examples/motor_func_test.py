
def data_ON(Device1,Device2):
	print("\nData ON")
	'''
	Device1.writereq(0x12,'545457550D0A') #RUN_flag
	Device2.writereq(0x12,'545457550D0A') #RUN_flag
	'''
def data_OFF(Device1,Device2):
	print("\nData OFF")
	'''
	Device1.writereq(0x12,'545446660D0A') #RUN_flag
	Device2.writereq(0x12,'545446660D0A') #RUN_flag
	'''
def motor_OFF(Device1,Device2):
	print("\nmotor OFF")
	'''
	Device1.writereq(0x12,'545246680D0A') #RUN_flag
	Device2.writereq(0x12,'545246680D0A') #RUN_flag
	'''
def motor_ON(Device1,Device2):
	print("\nmotor ON")
	'''
	Device1.writereq(0x12,'54524E600D0A') #RUN_flag
	Device2.writereq(0x12,'54524E600D0A') #RUN_flag
	'''
def M_FWD(Device1,Device2,direciton):
	global state
	state = 1
	print('state = ',state,'\n')
	print("\nM_FWD")
	'''
	if direction == -1:
		M_STOP();
		time.sleep(0.2)
		Device1.writereq(0x12,'544443790D0A')#CCW forward
		Device2.writereq(0x12,'544443790D0A')#CCW forward
		direction = 1;
		motor_ON();
		M_IDLE()
	Device1.writereq(0x12,'545750590D0A')#5km/h
	Device2.writereq(0x12,'545750590D0A')#5km/h
	'''
def M_FWD_RIGHT(Device1,Device2):
	print("\nM_FWD_RIGHT")
def M_FWD_LEFT(Device1,Device2):
	print("\nM_FWD_LEFT")

def M_IDLE(Device1,Device2):
	print("\nM_IDLE")
	'''
	#motor_ON()
	#print("MOTOR IDLE\n");
	Device1.writereq(0x12,'545714950D0A')#2km/h
	Device2.writereq(0x12,'545714950D0A')#2km/h
	'''
def M_BWD(Device1,Device2,direction):
	print("\nM_BWD")
	'''
	#motor_ON()
	global direction
	if direction == 1:
		M_STOP();
		time.sleep(0.2)
		Device1.writereq(0x12,'544457650D0A')#CW backward
		Device2.writereq(0x12,'544457650D0A')#CW backward
		direction = -1;
		motor_ON();
		M_IDLE()
	Device1.writereq(0x12,'545708A10D0A')#0.8km/h
	Device2.writereq(0x12,'545708A10D0A')#0.8km/h
	'''
def M_RIGHT(Device1,Device2):
	print("\nM_RIGHT")
	'''
	Device1.writereq(0x12,'545714950D0A')#2km/h
	Device2.writereq(0x12,'545732770D0A')#5km/h
	'''
def M_LEFT(Device1,Device2):
	print("\nM_LEFT")
	'''
	Device1.writereq(0x12,'545732770D0A')#5km/h
	Device2.writereq(0x12,'545714950D0A')#2km/h
	'''
def M_STOP(Device1,Device2):
	print("\nM_STOP")
	'''
	Device1.writereq(0x12,'545700A90D0A')#0km/h
	Device2.writereq(0x12,'545700A90D0A')#0km/h
	'''
def fFASTER(Device1,Device2):
	print("\nM_fFASTER")
	'''
	Device1.writereq(0x12,'547575160D0A')#Spd_Up
	Device2.writereq(0x12,'547575160D0A')#Spd_Up
	'''
def fSLOWER(Device1,Device2):
	print("\nM_fSLOWER")
	'''
	Device1.writereq(0x12,'546464380D0A')#Spd_Down
	Device2.writereq(0x12,'546464380D0A')#Spd_Down
	'''

