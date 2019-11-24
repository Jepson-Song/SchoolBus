import os
import sys
import time
from PIL import Image

def pull_screenshot():
    ret = os.system('adb shell screencap -p /sdcard/sb.png') #截图
    #print("ret = ", ret)
    if ret!=0:
        print("设备未连接！！！")
        sys.exit(0)
    os.system('adb pull /sdcard/sb.png .') #从手机拉取截图

def find_lineup_button():
    im = Image.open('./sb.png')
    global picture_x, picture_y
    picture_x, picture_y = im.size

    global button_x, button_y
    button_x = 0
    button_y = 0

    pixel = im.load()
    button_r, button_g, button_b, _ =pixel[picture_x/2, picture_y/10] #获取排队按钮颜色
    print("排队按钮的颜色是：",end="")
    print((button_r, button_g, button_b))

    button_x = picture_x/2
    step = 1
    global button_top #找到排队按钮上界
    button_top = 0
    for j in range(int(picture_y/2), picture_y, step):
        r, g, b, _ = pixel[button_x, j]
        #print((r, g, b))
        if r==button_r and g==button_g and b==button_b:
            button_top = j
            break
    print("button_top = ",button_top)
    
    button_bot = 0 #找到排队按钮下界
    for j in range(picture_y-10, button_top, -step):
        r, g, b, _ = pixel[button_x, j]
        #print((r, g, b))
        if r==button_r and g==button_g and b==button_b:
            button_bot = j
            break
    print("button_bot = ",button_bot)
    
    button_y = (button_top+button_bot)/2

def click(click_x, click_y):
    os.system('adb shell input tap {x} {y}'.format(x=click_x, y=click_y)) #点击
    print("click：",end="")
    print((click_x, click_y))

def run():
    pull_screenshot()
    find_lineup_button()
    while True:
        click(button_x, button_y)
        time.sleep(1)
        click(picture_x/2, picture_y/2)

def main():
    s = input("输入开始时间(格式为HH:MM:SS，若立即开始则直接回车)：")
    if len(s)>0:
        timelist = s.split(":")
        timelist = [int(x) for x in timelist]
        h = timelist[0]
        m = timelist[1]
        s = timelist[2]
        print("设置的开始时间为：",(h, m, s))
        while True:
            localtime = time.localtime(time.time())
            print("当前时间：",localtime)
            if (localtime.tm_hour==h and localtime.tm_min==m and localtime.tm_sec>=s
            or localtime.tm_hour==h and localtime.tm_min>m
            or localtime.tm_hour>h):
                run()
                break
    else:
        run()

if __name__ == "__main__":
    main()
