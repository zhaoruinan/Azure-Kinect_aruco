import wx
import can
import time
import math
from datetime import datetime
import threading
from neck_sim import neck_sim
global sim_v1,sim_v2,is_sim 
sim_v1,sim_v2= 0.0,0.0
is_sim = True
def neck_bullt_sim():
    sim = neck_sim()
    while True:
        global sim_v1,sim_v2,is_sim
        if is_sim:
            sim.motor_set_speed(3,sim_v1)
            sim.motor_set_speed(5,sim_v2)
        sim.step()
    sim.stop()
bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=1000000)
def int_to_char(n):
    b = [0x00, 0x00, 0x00, 0x00]
    b[0] =b[0]+ ((n & 0xff000000) >> 24)
    b[1] =b[1]+ ((n & 0xff0000) >> 16)
    b[2] =b[2]+ ((n & 0xff00) >> 8)
    b[3] =b[3]+ (n & 0xff)
    return b
class motor:
    def __init__(self,node,angle,min,max):
        self.node = node
        self.angle_value = angle
        self.speed = 10
        self.angle_max = max
        self.angle_min = min
    def angle_set(self,angle):
        self.angle_value = angle
    def angle_go(self):
        value = self.pos_r_one()
        print(self.angle_value,self.angle_max)
        if self.angle_value > self.angle_max:
            self.angle_set(self.angle_max)
        if self.angle_value < self.angle_min:
            self.angle_set(self.angle_min)

        if self.angle_value > value+50:
            print(self.angle_value,value,"go +")
            self.motor_set_speed(self.speed)
        elif self.angle_value < value-50:
            print(self.angle_value,value,"go -")
            self.motor_set_speed(-1*self.speed)
        else:
            print(self.angle_value,value,"stop")
            self.motor_set_speed(0)
            value = self.pos_r_one()
            self.angle_set(value)


    def motor_set_speed(self,speed):
        n = speed*100
        b = int_to_char(n)
        #print(b)
        msg = can.Message(arbitration_id=0x140+self.node, data=[0xA2, 0x00, 0x00, 0x00, 0x00+b[3], 0x00+b[2], 0x00+b[1], 0x00+b[0]], is_extended_id=False)
        bus.send(msg)
        recv = bus.recv()
    def motor_muti_angle_set(self,pos,orr):
        pos = int(pos)
        #print(pos)
        char_pos = int_to_char(pos)
        #print(b)
        print(self.node,orr,pos,char_pos)
        msg = can.Message(arbitration_id=0x140+self.node, data=[0xA4, 0x00, 0x05, 0x00, 0x00+char_pos[3], 0x00+char_pos[2], 0x00, 0x00], is_extended_id=False)
        bus.send(msg)
        recv = bus.recv()
        #print("recv",recv.data[1])
    def motor_one_angle_set(self,pos,orr):
        pos = int(pos)
        #print(pos)
        char_pos = int_to_char(pos)
        #print(b)
        print(self.node,orr,pos,char_pos)
        msg = can.Message(arbitration_id=0x140+self.node, data=[0xA6, 0x00+orr, 0x05, 0x00, 0x00+char_pos[3], 0x00+char_pos[2], 0x00, 0x00], is_extended_id=False)
        bus.send(msg)
        recv = bus.recv()
        #print("recv",recv.data[1])
    def pos_r_muti(self):
        msg = can.Message(arbitration_id=0x140+self.node, data=[0x92, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)  #duoquan
        bus.send(msg)
        recv = bus.recv()
        #print(recv)
        try:
            return((recv.data[7]<<48)+(recv.data[6]<<40)+(recv.data[5]<<32)+(recv.data[4]<<24)+(recv.data[3]<<16)+(recv.data[2]<<8)+recv.data[1])
        except:
            print("please make sure CAN cable is working")
    def pos_r_one(self):
        msg = can.Message(arbitration_id=0x140+self.node, data=[0x94, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)  #duoquan
        bus.send(msg)
        recv = bus.recv()
        #print(recv)
        try:
            return((recv.data[7]<<8)+(recv.data[6]))
        except:
            print("please make sure CAN cable is working")

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent = None,title = 'wxPython',size = (280,560))
        panel = wx.Panel(frame, -1)
        self.speed1, self.speed3, self.pos1, self.pos2 = 0,0,0,0
        self.button1 = wx.Button(panel,-1,'Stop1',pos = (30,80))
        self.button2 = wx.Button(panel,-1,'move1',pos = (30,120))
        self.button3 = wx.Button(panel,-1,'move1-',pos = (30,40))
        self.Bind(wx.EVT_BUTTON, self.OnButton1,self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButton2,self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButton3,self.button3)
        
        self.button1_1 = wx.Button(panel,-1,'Stop2',pos = (150,80))
        self.button2_1 = wx.Button(panel,-1,'move2+',pos = (150,120))
        self.button3_1 = wx.Button(panel,-1,'move2-',pos = (150,40))
        self.Bind(wx.EVT_BUTTON, self.OnButton1_1,self.button1_1)
        self.Bind(wx.EVT_BUTTON, self.OnButton2_1,self.button2_1)
        self.Bind(wx.EVT_BUTTON, self.OnButton3_1,self.button3_1)

        self.label1 = wx.StaticText(panel,-1, "speed(0.01rad)",pos = (30,160))
        self.text1 = wx.TextCtrl(panel, -1,pos = (30,180),size = (80,-1))
        self.Bind(wx.EVT_TEXT, self.OnText1, self.text1)  
        self.label2 = wx.StaticText(panel,-1, "speed(0.01rad)",pos = (150,160))
        self.text2 = wx.TextCtrl(panel, -1,pos = (150,180),size = (80,-1))
        self.Bind(wx.EVT_TEXT, self.OnText2, self.text2)  

        self.label3 = wx.StaticText(panel,-1, "Pos(0.01rad)",pos = (30,210))
        self.text3 = wx.TextCtrl(panel, -1,pos = (30,230),size = (80,-1),style = wx.TE_READONLY)
        self.label4 = wx.StaticText(panel,-1, "Pos(0.01rad)",pos = (150,210))
        self.text4 = wx.TextCtrl(panel, -1,pos = (150,230),size = (80,-1),style = wx.TE_READONLY)

        self.update_button = wx.Button(panel,-1,'update',pos = (30,270))
        self.Bind(wx.EVT_BUTTON, self.OnUpdate,self.update_button)
        self.text1.SetValue('0')
        self.text2.SetValue('0')

        self.label5 = wx.StaticText(panel,-1, "pos_set(0.01rad)",pos = (30,310))
        self.text5 = wx.TextCtrl(panel, -1,pos = (30,330),size = (80,-1))
        self.Bind(wx.EVT_TEXT, self.OnText5, self.text5)  
        self.label6 = wx.StaticText(panel,-1, "pos_set(0.01rad)",pos = (150,310))
        self.text6 = wx.TextCtrl(panel, -1,pos = (150,330),size = (80,-1))
        self.Bind(wx.EVT_TEXT, self.OnText6, self.text6)
        self.button4 = wx.Button(panel,-1,'go',pos = (150,380))
        self.Bind(wx.EVT_BUTTON, self.OnButton4,self.button4)

        frame.Show()
        return True
    def OnButton1(self, event):
        value = motor1.pos_r_one()
        print("motor1",value)
        motor1.angle_set(value)
        motor1.motor_set_speed(0)
        pos = motor1.pos_r_one()
        #print(pos)
        self.text3.SetValue(str(pos))
        
    def OnButton2(self, event):
        motor1.motor_set_speed(self.speed1)  
    def OnButton3(self, event):
        motor1.motor_set_speed(-1*self.speed1)
    def OnButton1_1(self, event):
        value = motor2.pos_r_one()
        motor2.angle_set(value)
        motor2.motor_set_speed(0)
        pos = motor2.pos_r_one()
        #print(pos)
        self.text4.SetValue(str(pos))        
    def OnButton2_1(self, event):
        motor2.motor_set_speed(self.speed2) 
    
    def OnButton3_1(self, event):
        motor2.motor_set_speed(-1*self.speed2) 
    def OnButton4(self, event):
        pos_m1 = self.pos1
        motor1.angle_set(pos_m1)
        pos_m2 = self.pos2
        motor2.angle_set(pos_m2)

    def OnUpdate(self, event):
        pos1 = motor1.pos_r_one()
        pos2 = motor2.pos_r_one()
        ##print(pos1,pos2)
        self.text3.SetValue(str(pos1))
        self.text4.SetValue(str(pos2))
    def OnText1(self, event):
        text = self.text1.GetValue()
        try:
            #print(int(text))
            self.speed1 = int(text)
        except:
            self.text1.SetValue('0')
    def OnText2(self, event):
        text = self.text2.GetValue()
        try:
            #print(int(text))
            self.speed2 = int(text)
        except:
            self.text2.SetValue('0')

    def OnText5(self, event):
        text = self.text5.GetValue()
        try:
            #print(int(text))
            self.pos1 = int(text)
        except:
            self.text5.SetValue('0')
    def OnText6(self, event):
        text = self.text6.GetValue()
        try:
            #print(int(text))
            self.pos2 = int(text)
        except:
            self.text6.SetValue('0')
def angle_control():
    while True:
        start = datetime.now()
        motor1.angle_go()
        motor2.angle_go()
        global sim_v1,sim_v2
        sim_v1 = (motor1.pos_r_one()-15000)/1000/3.14/2
        sim_v2 = (motor2.pos_r_one()-26000)/1000/3.14/2
        end = datetime.now()
        exec_time = end - start
        print(exec_time,exec_time.total_seconds())
        if 0.2-exec_time.total_seconds() > 0:
            time.sleep(0.2-exec_time.total_seconds())


    pass


def search():
    time.sleep(5)
    pos_list = [[0,0],[0,4000],[7500,4000],[6000,0]]
    for pos in pos_list:
        motor1.angle_set(pos[0]+15000)
        motor2.angle_set(pos[1]+26000)
        print(pos[0],pos[1])
        time.sleep(5)
def main():
    t_sim = threading.Thread(target=neck_bullt_sim)
    t_sim.start()
    p_control = threading.Thread(target=angle_control)
    p_control.start()
    p_search = threading.Thread(target=search)
    p_search.start()
    app = MyApp()
    app.MainLoop()

    
#if __name__ =='__main__':

motor1 = motor(node =5, angle =18700, min =12627, max =22530)#12627 ~ 22530  #21000
motor2 = motor(node =3, angle =28000, min =25523, max =30157)#30157 ~ 25523

main()
