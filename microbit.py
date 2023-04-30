from microbit import *
import random

speed='Medium'
def sleptime(speed):
    if speed=='Fast':
        return 250
    elif speed=='Medium':
        return 500
    else:
        return 750

#*****************************WIFI模块内部代码***************************************************
class Obloq(object):
    def connectWifi(self,SSID,PASSWORD,TIME):
        uart.write('AT+CWJAP="%s","%s"\r\n' %(SSID, PASSWORD))      # 设置wifi模块连接无线网络
        display.scroll("wait...");display.show(Image.HAPPY)
        uart.write('AT+CIPMUX=0\r\n');sleep(500)                   # 设置WIFI模块单路链接模式
        uart.write('AT+CIPSTART="TCP","0",0\r\n');sleep(TIME)   
        if uart.any():                                              #第二次读，返回服务器IP设置消息
            data = str(uart.readall(), "UTF-8");sleep(1000)    
        uart.write('AT+CIFSR\r\n');sleep(200);data=0               # 设置这个后 读串口返回绑定ip 
        if uart.any():
            data = str(uart.readall(), "UTF-8")
            temp = data.split("\"",5)
            self.ip_address = temp[1]
            if self.ip_address[0]=='1' and len(self.ip_address)>10: 
                return True
            else:
                display.show(".");sleep(300)
                return False     
        else:
            display.show(".");sleep(300)
            return False
                        
    def ifconfig(self):
        return self.ip_address
               
    def httpSet(self,IP,PORT):
        uart.write('AT+CIPSTART="TCP","%s",%s\r\n' %(IP, PORT))  
        sleep(6000)
        uart.write('AT+CIPMODE=1\r\n')  # 设置WIFI模块为透穿模式
        sleep(500)
        uart.write('AT+CIPSEND\r\n')  # 在透穿模式下开始发送数据
        sleep(2000)
        if uart.any():  # 如果串口有值
            self.res = str(uart.readall(), "UTF-8")
            self.res = 0
      
    def get(self,url,time):
        uart.write('GET /'+ url + '\r\n\r\n')  
        sleep(1000)
        if uart.any():  # 如果串口有值
            res = str(uart.readall(), "UTF-8")  
            return (200,res)
        return (404,"NOT FOUND")
  
Obloq = Obloq()
#***********************************************************************************************
# 串口初始化
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin12, rx=pin8)    
IP="10.0.0.23"
PORT="7999"
SSID="ORBI37"
PASSWORD="yellobug535"

while Obloq.connectWifi(SSID,PASSWORD,10000) != True:
    display.show(".")
Obloq.httpSet(IP,PORT)

#判定是否进入/game
while True:
    status,resp=Obloq.get('ifgame',2000)
    if status==200:
        if resp[0]=='1':
            speed=resp[1]
            break
        else:
            sleep(2000)

# 初始化贪吃蛇
snake = [[2, 2]]
dir = [1, 0]

# 生成食物
food = [random.randint(0, 4), random.randint(0, 4)]

# 显示初始状态
display.set_pixel(snake[0][0], snake[0][1], 9)
display.set_pixel(food[0], food[1], 5)

while True:
    score=0
    # 判断按键
    if button_a.was_pressed():
        dir = [dir[1], -dir[0]]  # 左转
    elif button_b.was_pressed():
        dir = [-dir[1], dir[0]]  # 右转

    # 移动贪吃蛇
    new_head = [snake[0][0] + dir[0], snake[0][1] + dir[1]]
    if new_head == food:
        food = [random.randint(0, 4), random.randint(0, 4)]
        display.set_pixel(food[0], food[1], 5)
        score+=1
    else:
        tail = snake.pop()
        display.set_pixel(tail[0], tail[1], 0)
    snake.insert(0, new_head)

    # 判断游戏结束
    if new_head[0] < 0 or new_head[0] > 4 or new_head[1] < 0 or new_head[1] > 4:
        display.show(Image.SKULL)
        Obloq.get("input?score="+str(score),2000)
        break
    elif new_head in snake[1:]:
        display.show(Image.SKULL)
        Obloq.get("input?score="+str(score),2000)
        break

    # 显示贪吃蛇
    display.set_pixel(new_head[0], new_head[1], 9)
    sleep(sleptime(speed))
