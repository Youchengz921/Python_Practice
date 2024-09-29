import pyautogui
import time
import keyboard

num = int(input("模式(1:買，2:開):"))

def mouse(step): 
    for i in range(step):
        try:
            if keyboard.is_pressed('i'):
                print("偵測到 'i' 鍵，停止點擊")
                break 
        except Exception as e:
            print(f"檢測鍵盤事件時發生錯誤: {e}")
        
        pyautogui.mouseDown()  
        time.sleep(0.5)          
        pyautogui.mouseUp()    
        time.sleep(0.5)        
        print(f"第{i+1}次")
    
def keyboard_action(step):  
    pyautogui.mouseDown()  
    pyautogui.mouseUp() 
    for i in range(step):
        try:
            if keyboard.is_pressed('i'):
                print("偵測到 'i' 鍵，停止點擊")
                break 
        except Exception as e:
            print(f"檢測鍵盤事件時發生錯誤: {e}")
        pyautogui.mouseDown()  
        pyautogui.mouseUp()    
        time.sleep(0.5)        
        pyautogui.keyDown('r')  
        time.sleep(0.2)         
        pyautogui.keyUp('r')    
        print(f"第{i+1}次")
    
def delet(step):
    for i in range(step):
        pyautogui.mouseDown()
        time.sleep(1)
        pyautogui.mouseUp()
        print(f"第{i+1}次")

step = int(input("次數:"))

if num == 1:
    mouse(step)
elif num == 2:
    keyboard_action(step)  
elif num == 3:
    delet(step)