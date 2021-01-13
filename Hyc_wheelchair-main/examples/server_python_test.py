import wx
import socket
import threading
from datetime import datetime
import time
from ctypes import *
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9911        # Port to listen on (non-privileged ports are > 1023)
SIZE_DATA_ASCII_MAX = 32
SIZE_DATA_TCP_MAX  = 200
class Data(Union):
    _fields_ = [("byte", c_ubyte * SIZE_DATA_TCP_MAX),("double6dArr", c_double * 6),("bool", c_bool * 8)]
#from motor_can import motor_set_speed,motor_set_speed_m,motor_read_pos
def server():
    write_buffer = (c_char* 1024)()
    read_buffer = (c_char* 1024)()
    res_data = Data()    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            send_data = Data()
            while True:
                read_buffer = conn.recv(1024)
                #if not read_buffer:
                #    break
                print('send data  ',send_data.double6dArr[5])
                memmove(res_data.byte, read_buffer, 1024)
                print('receive data  ',res_data.double6dArr[5])
                print('speed1  ',res_data.double6dArr[0])
                print('speed2 ',res_data.double6dArr[1])                
                print("server",datetime.fromtimestamp(time.time()))                                
                #motor_set_speed,motor_set_speed_m
                #motor_read_pos
                send_data.double6dArr[5] =0.002 +send_data.double6dArr[5]
                memmove( write_buffer,send_data.byte ,1024)
                print('send data  ',send_data.double6dArr[5])
                conn.sendall(write_buffer)
                time.sleep(0.2)      

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

    def motor_muti_angle_set(self,pos,orr):
        pos = int(pos)
        #print(pos)
        char_pos = int_to_char(pos)
        #print(b)
        print(self.node,orr,pos,char_pos)

        #print("recv",recv.data[1])
    def motor_one_angle_set(self,pos,orr):
        pos = int(pos)
        #print(pos)
        char_pos = int_to_char(pos)
        #print(b)
        print(self.node,orr,pos,char_pos)

        #print("recv",recv.data[1])
        
class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent = None,title = 'wxPython',size = (280,360))
        panel = wx.Panel(frame, -1)
        self.speed1, speed3 = 0,0
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
        frame.Show()
        return True
    def OnButton1(self, event):
        motor_set_speed(5,0)
        pos = motor_read_pos(5)
        #print(pos)
        self.text3.SetValue(str(pos))
        
    def OnButton2(self, event):
        motor_set_speed(5,self.speed1)
    
    def OnButton3(self, event):
        motor_set_speed_m(5,self.speed1)

    def OnButton1_1(self, event):
        motor_set_speed(3,0)
        pos = motor_read_pos(3)
        #print(pos)
        self.text4.SetValue(str(pos))
        
    def OnButton2_1(self, event):
        motor_set_speed(3,self.speed3)
    
    def OnButton3_1(self, event):
        motor_set_speed_m(3,self.speed3)

    def OnUpdate(self, event):
        pos1 = motor_read_pos(5)
        pos2 = motor_read_pos(3)
        #print(pos1,pos2)
        self.text3.SetValue(str(pos1))
        self.text4.SetValue(str(pos2))
    def OnText1(self, event):
        text = self.text1.GetValue()
        try:
            print(int(text))
            self.speed1 = int(text)
        except:
            self.text1.SetValue('0')
    def OnText2(self, event):
        text = self.text2.GetValue()
        try:
            print(int(text))
            self.speed3 = int(text)
        except:
            self.text2.SetValue('0')



def main():
    p_server = threading.Thread(target=server)
    p_server.start()
    app = MyApp()
    app.MainLoop()
#if __name__ =='__main__':
main()