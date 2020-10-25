import wx
import socket
from socket import error as SocketError
import errno
import threading
from threading import Lock
from datetime import datetime
import time
#from utils import tf_neck2cam
from ctypes import *
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
HOST = '192.168.0.117'  # The server's hostname or IP address
PORT = 32452        # The port used by the server
SIZE_DATA_ASCII_MAX = 32
SIZE_DATA_TCP_MAX  = 200
class Data(Union):
    _fields_ = [("byte", c_ubyte * SIZE_DATA_TCP_MAX),("double6dArr", c_double * 6),("boolArr", c_bool * 8)]
global send_data,res_data,send_data_dou,send_data_b
send_data = Data()
res_data = Data()
res_data.double6dArr[0] = 0.0
res_data.double6dArr[1] = 0.0

send_data_dou = [0.1,0.1,0.1,0.1,0.1,0.1]
send_data_b = [True,True,True,True,True,True]
lock = Lock()
def socket_tcp():
    global send_data,res_data,send_data_dou,send_data_b,sim_v1,sim_v2 
    if not is_sim:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    while True:
        #lock.acquire()
        send_data.double6dArr[5] = 0.001 +send_data.double6dArr[5]
        send_data.double6dArr[0]= send_data_dou[0]
        send_data.boolArr[0]= send_data_b[0]
        send_data.double6dArr[1]= send_data_dou[1]
        send_data.boolArr[1]= send_data_b[1]
        sim_v1 = send_data_dou[0]
        sim_v2 = send_data_dou[1]
        if not is_sim:
            tcp_client(s)
def tcp_client(s):
    global send_data,res_data,send_data_dou,send_data_b
    lock.acquire()
    write_buffer = (c_char* 1024)()  
    memmove( write_buffer, send_data.byte,1024)
    lock.release()
    s.sendall(write_buffer)
    start = datetime.now()
    #if res_data.double6dArr[0]:
    #    print('neck2cam',tf_neck2cam(res_data.double6dArr[0],res_data.double6dArr[1]))
    end = datetime.now()
    exec_time = end - start
    print(exec_time,exec_time.total_seconds())
    time.sleep(0.2-exec_time.total_seconds())
    read_buffer = s.recv(1024)
    lock.acquire()
    memmove( res_data.byte,read_buffer, 1024)
    print('receive data  ',chr(res_data.byte[0]))
    print("client",datetime.fromtimestamp(time.time()))
    print('send data  ',send_data.double6dArr[5])
    print('speed 1 ',send_data.double6dArr[0])
    print('speed 2 ',send_data.double6dArr[1])
    #print('neck2cam',tf_neck2cam(res_data.double6dArr[0],res_data.double6dArr[1]))
    lock.release()

def motor_set_speed(node,speed,m=1):
    
    if node == 5:
        global send_data,res_data,send_data_dou,send_data_b
        lock.acquire()
        send_data_b[0] = True
        send_data_dou[0] = speed * m
        lock.release()
    if node == 3:
        lock.acquire()
        send_data_b[1] = True
        send_data_dou[1] = speed * m
        lock.release()
def motor_read_pos(node):
    global send_data,res_data
    if node ==5:
        return res_data.double6dArr[0]       
    if node ==3:
        return res_data.double6dArr[1]
    return 55555
  
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
        motor_set_speed(5,self.speed1,-1)

    def OnButton1_1(self, event):
        motor_set_speed(3,0)
        pos = motor_read_pos(3)
        #print(pos)
        self.text4.SetValue(str(pos))
        
    def OnButton2_1(self, event):
        motor_set_speed(3,self.speed3)
    
    def OnButton3_1(self, event):
        motor_set_speed(3,self.speed3,-1)

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
    t_tcp = threading.Thread(target=socket_tcp)
    t_tcp.start()
    t_sim = threading.Thread(target=neck_bullt_sim)
    t_sim.start()
    app = MyApp()
    app.MainLoop()
#if __name__ =='__main__':
main()