#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author   : Colson Yang
#Date     : 2017.11.9
#Platform : Raspberry_Pi_3_B
#Version. : 2.0

# 开始

"""
<>  Step1 初始化
      1.1 模块、参数、元组
      1.2 类定义、函数定义
      1.3 TCP初始化
      1.4 打印log
"""

# <-- step1.1 begin -->

#   模块引入
import SocketServer
from time import ctime
import time
import logging
import socket
import thread
import struct
from Tkinter import *           # 导入 Tkinter 库 GUI
#   模块引入结束

#   宏定义
LightNumMax = 9
LightShowMax = 2
LightShowTh = 1
SensorNumMax =  11
HOST = '192.168.2.64'   #ip地址
PORT = 4568              #监听端口
ADDR = (HOST, PORT)
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='log.txt',
        filemode='a+')

root = Tk()                     # 创建窗口对象的背景色
S =Scrollbar(root)
T = Text(root,width=200,height=40)
S.pack(side=RIGHT,fill=Y)
T.pack(side=LEFT,fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """
测 试 D E M O
"""
#   宏定义结束

#   元组定义
'''
    灯具-传感器 对应表
    灯Id 传感器id1、2、3 传感器点1、2、3 权值百分比1、2、3
'''
LightSensorTable = [
#   顶灯
   [1,1,2,3,4,5,24,24,24,24,24,18,55,18,18,0],
    [2,2,3,4,5,6,24,24,24,24,24,18,18,55,18,18],
    [3,4,5,6,7,8,24,24,24,24,24,18,18,55,18,18],
    [4,6,7,8,9,10,24,24,24,24,24,18,18,55,18,18],
    [5,7,8,9,10,11,24,24,24,24,24,0,18,18,55,18],
#   射灯
    [6,1,2,3,4,5,24,24,24,24,24,30,60,30,0,0],
    [7,4,5,6,7,8,24,24,24,24,24,30,60,30,0,0],
    [8,7,8,9,10,11,24,24,24,24,24,30,60,30,0,0],
    [9,9,10,11,7,8,24,24,24,24,24,30,60,30,0,0]]

#   顶灯-射灯/台灯 对应表
LightLightTable = [
    [1,6,0],
    [2,6,7],
    [3,7,8],
    [4,8,0],
    [5,9,0]]

#   灯具输出 对应表
LightOutputTable = [ 0x50,0x50,0x50,0x50,0x50,0x00,0x00,0x00,0x00]
LightCalOLD      = [ 0x50,0x50,0x50,0x50,0x50,0x00,0x00,0x00,0x00]
LightCalTemp     = [ 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
#   sensor data table
SensorData = [[0 for i in range(64)] for i in range(11)]
TempData = [[0 for i in range(64)] for i in range(11)]
#   light data message transfer
a = [0x02,0x01,0x06,0x3f,0x5a,0xa5]
data_light = struct.pack("%dB"%(len(a)),*a)

#   extern bool SensorData[SensorNumMax][64];
#   元组定义结束
# <-- step1.1 over -->

# <-- step1.2 begin -->
#    请求类定义
#light_dev = 0
class MyRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        light_dev = 0
        print '...connected from:', self.client_address
        iii = 0
        while True:
            try:
                if light_dev == 0:
                        data = self.request.recv(1024)
                        iii = 1 + iii
                #light_dev = 0
                if(not data):
                    break
#    TCP报文解析：1.灯具报文发送 2.传感器报文解析
#    1.灯具报文发送 开始
                if data[0] == 'c' and data[1] == '7':
                    light_dev = 1
                    print "%s\n"%(data)
                if light_dev == 1:
                    #time.sleep(0.99) #休眠0.99秒 保障1秒发送一次
                    self.request.sendall(data_light)
                    #iii = 0
#    1.灯具报文发送 结束
                #self.request.sendall('[%s] %s' % (ctime(),data[0]))
                elif iii == 7:
                    iii = 0
                    #self.request.sendall('OK')
#    2.传感器报文解析 开始

                if light_dev == 0:
                    SensorID = int(data[0],16)*10 + int(data[1],16)
                    print "Sensor_ID = ",SensorID
                    print "%d, %d, %d "%(ord(data[2]),ord(data[139]),ord(data[140]))
                    #print "\n"
                    if (ord(data[2])==141 and ord(data[140])==165 and ord(data[139])==90):
                        print "传感器报文格式正确"
                        #print "%d,%d,%d,%d,%d,%d,%d,%d "%(ord(data[3]),ord(data[4]),ord(data[5]),ord(data[6]),ord(data[7]),ord(data[8]),ord(data[9]),ord(dat$
                        for k in range(8):
                            SensorData[SensorID-1][k*8]   = ord(data[k+3])/128#(ord(data[k+3]) & 0x80)>>8
                            SensorData[SensorID-1][k*8+1] = ord(data[k+3])/64%2#(ord(data[k+3]) & 0x40)>>7
                            SensorData[SensorID-1][k*8+2] = ord(data[k+3])/32%2#(ord(data[k+3]) & 0x20)>>6
                            SensorData[SensorID-1][k*8+3] = ord(data[k+3])/16%2#(ord(data[k+3]) & 0x10)>>5
                            SensorData[SensorID-1][k*8+4] = ord(data[k+3])/8%2#(ord(data[k+3]) & 0x08)>>4
                            SensorData[SensorID-1][k*8+5] = ord(data[k+3])/4%2#(ord(data[k+3]) & 0x04)>>3
                            SensorData[SensorID-1][k*8+6] = ord(data[k+3])/2%2#(ord(data[k+3]) & 0x02)>>2
                            SensorData[SensorID-1][k*8+7] = ord(data[k+3])%2#(ord(data[k+3]) & 0x01)>>1
                        for k in range(64):
                            TempData[SensorID-1][k] = ord(data[2*k+11])*256+ord(data[2*k+11+1])
                print "%s\n"%(SensorData[SensorID-1])#打印二值化数据
                #print "%s\n"%(TempData[SensorID-1])#打印温度数据

#    2.传感器报文解析 结束
                #print data[0],data[1]
            except socket.timeout:
                print "caught socket.timeout exception"
    def LogTemplate(self, s):
        return '[id.' + str(id(self.request)) + ']:  ' + str(s)
    def Log(self, s):
        ss =  self.LogTemplate(s)
        print ss
        logging.info(ss)
    def LogErr(self, s):
        ss =  self.LogTemplate(s)
        print ss
        logging.error(ss)

    def setup(self):
        self.Log('进入处理线程')
        self.request.settimeout(60)
    def finish(self):
        self.request.close()
        self.Log("退出处理线程")
#    类定义结束

#    灯具控制函数
def HumanCalcula(ID,SpecialPoint):
    i = 0
    RowI = 0
    RowX = 0
    ColI = 0
    ColX = 0

    Gear4 = 0
    Gear3 = 0
    Gear2 = 0
    Gear1 = 0
    Gear = 0

    RowX = SpecialPoint / 16
    ColX = SpecialPoint % 16

    for i in range(0,64):
        RowI = i / 16
        ColI = i % 16
#        print "i =  ",i,"\n"
        if RowI - RowX < 2 and RowI - RowX > -2 and ColI - ColX < 2 and ColI - ColX > -2 :
#    if( ((RowI - RowX) < 2) && ((RowI - RowX) > -2) && ((ColI - ColX) < 2) && ((ColI - ColX) > -2))
            if SensorData[ID-1][i] == 1 :
                Gear4 = 1
            #goto CaL;
        elif RowI - RowX < 3 and RowI - RowX > -3 and ColI - ColX < 3 and ColI - ColX > -3 :
            if SensorData[ID-1][i] == 1 :
                Gear3 = 1
#       else if( ((ColI - ColX) < 7) || ((ColI - ColX) > -7))
        elif RowI - RowX < 4 and RowI - RowX > -4 and ColI - ColX < 4 and ColI - ColX > -4 :
            if SensorData[ID-1][i] == 1 :
                Gear2 = 1
        else:
            if SensorData[ID-1][i] == 1 :
                Gear1 = 1

#      CaL:
    if Gear4 == 1 :
        Gear = 4
    elif Gear3 == 1 :
        Gear = 3
    elif Gear2 == 1 :
        Gear = 2
    elif Gear1 == 1 :
        Gear = 1

    return Gear
#HumanCalcula finish
# <-- step1.2 over -->

# <-- step1.3 start -->
#   线程定义函数1:TCP connection & decode
def tcp_thread(threadName):
     print "Enter tcp_thread\n"
     print '[%s] %s \n' % (ctime(),threadName)
     tcpServ = SocketServer.ThreadingTCPServer(ADDR, MyRequestHandler)
     print 'waiting for connection...\n'
     tcpServ.serve_forever()
#   主计算逻辑流程main
def main():
    i = j = 0
#  Configure the system clock
#  Initialize all configured peripherals
    var = 1
#    T.pack()
#    T.insert(INSERT,'Program Start\n')
#    T.insert(INSERT,'Program End\n')
#    T.insert(END,quote)
    print "---> Program Start! <--- \n"
    while var == 1 :
#        print "=== Into While === \n"
        for j in range(0,LightNumMax) :
#            print "+++ Into For i in range(0,LightNumMax) +++ \n"
            LightCalOLD[j] = LightOutputTable[j]
#            print " run>>> LightCalOLD[i+11] = LightOutputTable[i+11] \n"
            LightCalTemp[j] = ( HumanCalcula(LightSensorTable[j][1],LightSensorTable[j][6]) * LightSensorTable[j][11]\
                                                        + HumanCalcula(LightSensorTable[j][2],LightSensorTable[j][7]) * LightSensorTable[j][12]\
                                                        + HumanCalcula(LightSensorTable[j][3],LightSensorTable[j][8]) * LightSensorTable[j][13]\
                                                        + HumanCalcula(LightSensorTable[j][4],LightSensorTable[j][9]) * LightSensorTable[j][14]\
                                                        + HumanCalcula(LightSensorTable[j][5],LightSensorTable[j][10]) * LightSensorTable[j][15] )
#            print " run>>> calculate LightCalTemp \n"
            #if j < 5 :
            #    LightCalTemp[j] += 40
#                print " RUN 1\n"
            if LightCalTemp[j] > 255 :
                LightOutputTable[j] = 255
#                print " RUN 2\n"
            else:
                LightOutputTable[j] = LightCalTemp[j]
#                print " RUN 3\n"

            if LightOutputTable[j] < LightCalOLD[j] :
                LightOutputTable[j] = LightCalOLD[j] - 3
#                print " RUN 4\n"
            if LightOutputTable[j] < 0 :
                LightOutputTable[j] = 0
            data_light_new = struct.pack("%dB"%(len(LightOutputTable)),*LightOutputTable)
            print "LIHGT____===>  "
            for k in range(LightNumMax):
                print "%d"%(ord(data_light_new[k]))#打印输出数据
            print "\n"
#                print " RUN 5\n"
#      for(i = 0;i < LightShowMax;i++)
#      {
#          j = LightLightTable[i][0];
#          LightOutputTable[j+2] =  LightOutputTable[j+2] - LightShowTh * LightOutputTable[LightLightTable[i][1]+2]
#                                                                                               - LightShowTh * LightOutputTable[LightLightTable[i][2]+2];
#          if(LightOutputTable[j+2] < 0)
#          {
#              LightOutputTable[j+2] = 0;
#          }
#      }
#      LightOutputTable[3] =  HumanCalcula(LightSensorTable[0][1],LightSensorTable[0][4]) * LightSensorTable[0][7] ;
#  LightOutputTable[5] = 0x30;
#      HAL_UART_Transmit_DMA(&huart1,LightOutputTable,sizeof(LightOutputTable));//uart1_send_str(LightOutputTable);
#       /* 数据输入处理和输出 */
#        HAL_UART_DMAStop(&huart1);
#  }

#   线程定义函数2: 主逻辑计算流程
def cal_light(threadName):
    print "Enter Cal_light\n"
    print '[%s] %s \n' % (ctime(),threadName)
    main()
# <-- step1.3 over -->

"""
<>  Step2 程序顺序执行
      2.1 打开线程一：主计算逻辑
      2.2 打开线程二：TCP连接及解码
      2.3 如有异常  ：打印错误9527
      2.4 进入主循环
"""

try:
    thread.start_new_thread(cal_light,("Thread-1",))
    thread.start_new_thread(tcp_thread,("Thread-2",))
except:
    print "Error<9527> :unable to start thread\n"

while 1:
    pass
#程序结束
