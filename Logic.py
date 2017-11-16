# -*- coding: UTF-8 -*-
#宏定义
LightNumMax = 9
LightShowMax = 2
LightShowTh = 1
SensorNumMax =  11
#宏定义结束

#灯具-传感器 对应表
#灯Id 传感器id1、2、3 传感器点1、2、3 权值百分比1、2、3
LightSensorTable = [
#顶灯
    [1,1,2,3,4,5,24,24,24,24,24,18,55,18,18,0],
    [2,2,3,4,5,6,24,24,24,24,24,18,18,55,18,18],
    [3,4,5,6,7,8,24,24,24,24,24,18,18,55,18,18],
    [4,6,7,8,9,10,24,24,24,24,24,18,18,55,18,18],
    [5,7,8,9,10,11,24,24,24,24,24,0,18,18,55,18],
#射灯
    [6,1,2,3,4,5,24,24,24,24,24,30,60,30,0,0],
    [7,4,5,6,7,8,24,24,24,24,24,30,60,30,0,0],
    [8,7,8,9,10,11,24,24,24,24,24,30,60,30,0,0],
    [9,9,10,11,7,8,24,24,24,24,24,30,60,30,0,0]]

#顶灯-射灯/台灯 对应表
LightLightTable = [
    [1,6,0],
    [2,6,7],
    [3,7,8],
    [4,8,0],
    [5,9,0]]

#灯具输出 对应表
LightOutputTable = [ 0x41,0x54,0x2B,0x4E,0x4F,0x54,0x49,0x46,0x59,0x3D,0x01,0x50,0x50,0x50,0x50,0x50,0x00,0x00,0x00,0x00 ]

#extern bool SensorData[SensorNumMax][64];

#灯具控制函数
#HumanCalcula start
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




def main():
    i = j = 0
  #HAL_Init();
#  Configure the system clock
  #SystemClock_Config();
#  Initialize all configured peripherals
  #MX_GPIO_Init();
  #MX_DMA_Init();
  #MX_USART1_UART_Init();
  #MX_USART2_UART_Init();
  # __HAL_UART_ENABLE_IT( &huart2, UART_IT_IDLE);    //使能串口2空闲中断
  # HAL_UART_Receive_IT(&huart2,RX_BUFFER,UART2_RECV_LEN);
    var = 1
    while var == 1 :
        for i  in range(0,LightNumMax) :
            LightCalOLD[i+11] = LightOutputTable[i+11]
            LightCalTemp[i] = ( HumanCalcula(LightSensorTable[i][1],LightSensorTable[i][6]) * LightSensorTable[i][11]
                                                        + HumanCalcula(LightSensorTable[i][2],LightSensorTable[i][7]) * LightSensorTable[i][12]
                                                        + HumanCalcula(LightSensorTable[i][3],LightSensorTable[i][8]) * LightSensorTable[i][13]
                                                        + HumanCalcula(LightSensorTable[i][4],LightSensorTable[i][9]) * LightSensorTable[i][14]
                                                        + HumanCalcula(LightSensorTable[i][5],LightSensorTable[i][10]) * LightSensorTable[i][15] )
            if i < 5 :
                LightCalTemp[i] += 40
            if LightCalTemp[i] > 255 :
                LightOutputTable[i+11] = 255
            else:
                LightOutputTable[i+11] = LightCalTemp[i]

            if LightOutputTable[i+11] < LightCalOLD[i+11] :
                LightOutputTable[i+11] = LightCalOLD[i+11] - 3
            if LightOutputTable[i+11] < 0 :
                LightOutputTable[i+11] = 0
#      for(i = 0;i < LightShowMax;i++)
#      {
#          j = LightLightTable[i][0];
#          LightOutputTable[j+2] =  LightOutputTable[j+2] - LightShowTh * LightOutputTable[LightLightTable[i][1]+2]
#              LightOutputTable[j+2] = 0;
#          }
#      }
#      LightOutputTable[3] =  HumanCalcula(LightSensorTable[0][1],LightSensorTable[0][4]) * LightSensorTable[0][7] ;
#  LightOutputTable[5] = 0x30;
#      HAL_UART_Transmit_DMA(&huart1,LightOutputTable,sizeof(LightOutputTable));//uart1_send_str(LightOutputTable);
#       /* 数据输入处理和输出 */
#        HAL_Delay(100);
#        HAL_UART_DMAStop(&huart1);
#        /* 数据输入处理和输出结束 */
#  }
#  /* USER CODE END 3 */


