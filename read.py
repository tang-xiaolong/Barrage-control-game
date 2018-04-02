# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:38:35 2017

@author: 唐小龙
"""

import socket
import time
import ctypes
import requests
from bs4 import BeautifulSoup
import multiprocessing
import re,threading
timeValue = 1
countValue = 5
count = 1
zhiling = ['#上','#上3','#下','#下3','#左','#左3','#右','#右3','#确认','#返回','#保存游戏','#查看背包','#查看技能','#跳过']
SendInput = ctypes.windll.user32.SendInput
keyCodeDec = {'backspace':0x08,
'tab':0x09,
'enter':0x0D,
'esc':0x1B,
'left_arrow':0x25,
'up_arrow':0x26,
'right_arrow':0x27,
'down_arrow':0x28,
'0':0x30,
'1':0x31,
'2':0x32,
'3':0x33,
'4':0x34,
'5':0x35,
'6':0x36,
'7':0x37,
'8':0x38,
'9':0x39,
'a':0x41,
'b':0x42,
'c':0x43,
'd':0x44,
'e':0x45,
'f':0x46,
'g':0x47,
'h':0x48,
'i':0x49,
'j':0x4A,
'k':0x4B,
'l':0x4C,
'm':0x4D,
'n':0x4E,
'o':0x4F,
'p':0x50,
'q':0x51,
'r':0x52,
's':0x53,
't':0x54,
'u':0x55,
'v':0x56,
'w':0x57,
'x':0x58,
'y':0x59,
'z':0x5A
}
keyCodeHex = {
0x08:0x0E,
0x09:0x0F,
0x0D:0x1C,
0x1B:0x01,
0x25:0x4B,
0x26:0x48,
0x27:0x4D,
0x28:0x50,
0x30:0x0B,
0x31:0x02,
0x32:0x03,
0x33:0x04,
0x34:0x05,
0x35:0x06,
0x36:0x07,
0x37:0x08,
0x38:0x09,
0x39:0x0A,
0x41:0x1E,
0x42:0x30,
0x43:0x2E,
0x44:0x20,
0x45:0x12,
0x46:0x21,
0x47:0x22,
0x48:0x23,
0x49:0x17,
0x4A:0x24,
0x4B:0x25,
0x4C:0x26,
0x4D:0x32,
0x4E:0x31,
0x4F:0x18,
0x50:0x19,
0x51:0x10,
0x52:0x13,
0x53:0x1F,
0x54:0x14,
0x55:0x16,
0x56:0x2F,
0x57:0x11,
0x58:0x2D,
0x59:0x15,
0x5A:0x2C
        }
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, keyCodeHex[hexKeyCode], 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, keyCodeHex[hexKeyCode], 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def sendInput(s_input):
    if(s_input in keyCodeDec.keys()):
##        if(keyCodeDec[s_input] == 'enter' or keyCodeDec[s_input] == 'esc'):
##            k = 0.1
##        else:
        k = 0.1
        PressKey(keyCodeDec[s_input])
        time.sleep(k)
        ReleaseKey(keyCodeDec[s_input])
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
def LookMyStatus():#查看自己的状态
    sendInput('s')
def UseSkill():#使用技能
    sendInput('esc')
    time.sleep(0.05)
    sendInput('down_arrow')
    time.sleep(0.05)
    sendInput('enter')
def LookBag():#查看我的背包
    sendInput('esc')
    time.sleep(0.05)
    sendInput('down_arrow')
    time.sleep(0.05)
    sendInput('down_arrow')
    time.sleep(0.05)
    sendInput('enter')
def SaveGame():#保存游戏
    sendInput('esc')
    time.sleep(0.05)
    sendInput('up_arrow')
    time.sleep(0.05)
    sendInput('enter')
    time.sleep(0.05)
    sendInput('enter')
    time.sleep(0.05)
    sendInput('enter')
def Enter():
    sendInput('enter')
def Up():
    sendInput('up_arrow')
def Down():
    sendInput('down_arrow')
def Right():
    sendInput('right_arrow')
def Left():
    sendInput('left_arrow')
def average(what):
    if(what  == 'saveGame'):
        SaveGame()
    elif(what == 'lookBag'):
        LookBag()
    elif(what == 'useSkill'):
        UseSkill()
    elif(what == 'tiaoGuo'):
        for i in range(8):
            sendInput('r')
    else:
        sendInput(what)
def Move(i):
    if(i == '#w'):
        Up()
    elif(i == '#s'):
        Down()
    elif(i == '#a'):
        Left()
    elif(i == '#d'):
        Right()
def chuli_1():
    global dic
    move = re.compile(r'#[wasd]([1-9][0-9]?)?')
    while(True):
        if(dic!={}):
            print('dic = ',dic)
            #time.sleep(2)
        for i in list(dic.values()):
            pp = move.match(i)
            if(pp == None):#不是方向键
                #处理其他指令和错误指令
                if(i == '#c'):#保存游戏
                    SaveGame()
                elif(i == '#b'):#查看背包
                    LookBag()
                elif(i == '#k'):#使用技能
                    UseSkill()
                elif(i == '#t'):#跳过对话
                    average('tiaoGuo')
                elif(i == '#h'):
                    average('enter')
                elif(i == '#e'):
                    average('esc')
                elif(i == '#A'):#战斗状态下，自动普通攻击直至结束
                    average('a')
                elif(i == '#D'):#战斗状态下，防御
                    average('d')
                else:#非法指令
                    continue
            else:
                s = pp.group()
                totalCount = re.sub("\D", "", s)
                if(totalCount == ''):#单纯移动
                    Move(s)
                else:#移动加数字
                    m = re.compile(r'(#[wasd])')
                    m = m.match(s)
                    for j in range(int(totalCount)):
                        Move(m.group())
        dic = {}
        time.sleep(0.5)
def chuli():
    global dic
    global timeValue
    global countValue
    global zhiling
    global count
    while(True):
        up_arrow =0
        down_arrow = 0
        left_arrow = 0
        right_arrow = 0
        enter = 0
        esc = 0
        saveGame = 0
        lookBag = 0
        useSkill = 0
        tiaoGuo = 0
        for i in range(timeValue):#每隔timeValue秒计算一次
            time.sleep(1)
            if(len(dic) >= countValue):#如果此时消息数大于countValue了，跳出去
                break
        #5秒后
        
        d = {}
        #去掉无关指令
        s = [i for i in dic.keys() if(dic[i] not in zhiling)]#找出所有不在指令内的操作
        if(s != []):
            print('无关指令 :',s)
            for i in s:
                dic.pop(i)
        #print('dic为：',dic)
        for i in list(dic.values()):
            if(i == '#上'):
                up_arrow+=1
            elif(i == '#下'):
                down_arrow+=1
            elif(i == '#左'):
                left_arrow+=1
            elif(i == '#右'):
                right_arrow+=1
            elif(i == '#确认'):
                enter+=1
            elif(i == '#返回'):
                esc +=1
            elif(i == '#保存游戏'):
                saveGame+=1
            elif(i == '#查看背包'):
                lookBag+=1
            elif(i == '#查看技能'):
                useSkill+=1
            elif(i == '#跳过'):
                tiaoGuo+=1
                #保存游戏','#查看背包','#查看技能
        if(up_arrow != 0):
            d['up_arrow'] = up_arrow
        if(down_arrow != 0):
            d['down_arrow'] = down_arrow
        if(left_arrow != 0):
            d['left_arrow'] = left_arrow
        if(right_arrow != 0):
            d['right_arrow'] = right_arrow
        if(enter != 0):
            d['enter'] = enter
        if(esc != 0):
            d['esc'] = esc
        if(saveGame != 0):
            d['saveGame'] = saveGame
        if(lookBag != 0):
            d['lookBag'] = lookBag
        if(useSkill != 0):
            d['useSkill'] = useSkill
        if(tiaoGuo != 0):
            d['tiaoGuo'] = tiaoGuo
        if(d != {}):
            print('最终操作为：',max(d))
            average(max(d))
            dic = {}
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostbyname("openbarrage.douyutv.com")
port=8601
client.connect((host,port))
danmu_path=re.compile(b'txt@=(.+?)/cid@')
uid_path=re.compile(b'uid@=(.+?)/nn@')
nickname_path = re.compile(b'nn@=(.+?)/txt@')
level_path=re.compile(b'level@=([1-9][0-9]?)/sahf@')
col_path = re.compile(b'col@=([1-9][0-9]?)/rg')



def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
	          + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn
def login(roomid):
    msg='type@=loginreq/roomid@={}/\0'.format(roomid)
    sendmsg(msg)
    msg_more='type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    sendmsg(msg_more)
    print('连接到{}的直播间'.format(get_name(roomid)))
def start(roomid):
    global dic
    #msg='type@=loginreq/roomid@={}/\0'.format(roomid)
    #msg='type@=loginreq/username@=rieuse/password@=douyu/roomid@={}/\0'.format(roomid)
    #sendmsg(msg)
##    msg_more='type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
##    sendmsg(msg_more)
##    print('连接到{}的直播间'.format(get_name(roomid)))
    while True:
        data=client.recv(1024)
        #print(data)
        uid_more=uid_path.findall(data)
        nickname_more = nickname_path.findall(data)
        level_more = level_path.findall(data)
        danmu_more = danmu_path.findall(data)
        col_more = col_path.findall(data)

        
        if(not level_more):
            level_more = b'0'
        if(not data):
            continue
        else:
            for i in range(0,len(danmu_more)):
                try:
                    product = {
                            'uid':uid_more[0].decode(encoding='utf-8'),
                            'nickname':nickname_more[0].decode(encoding='utf-8'),
                            'level':level_more[0].decode(encoding='utf-8'),
                            'danmu':danmu_more[0].decode(encoding='utf-8')
                            }
                    print(product['danmu'])
                    if(product['nickname'] not in dic.keys() and product['danmu'][0] == '#'):
                        dic[product['nickname']] = product['danmu']
                    f = open('data.txt','a+')
                    f.write(str(product)+'\n')
                    f.close()
                    #time.sleep(3)
                except Exception as e:
                    print(e)
def keeplive():
    while(True):
        msg = 'type@=mrkl/' + '/\0'
        #msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        sendmsg(msg)
        time.sleep(15)
        
def get_name(roomid):
	r = requests.get("http://www.douyu.com/"+roomid)
	soup = BeautifulSoup(r.text, 'lxml')
	return soup.find('a', {'class', 'zb-name'}).string
if __name__ == '__main__':
    dic = {}
    room_id=input("请输入房间号：")
    login(room_id)
    p1 = threading.Thread(target=start,args=(room_id,))
    p2 = threading.Thread(target=keeplive)
#    p1=multiprocessing.Process(target=start,args=(room_id,))
#    p2=multiprocessing.Process(target=keeplive)
    p1.daemon = False
    p2.daemon = False
    
    p1.start()
    p2.start()
    chuli_1()
#    p1.join()
#    p2.join()70231
