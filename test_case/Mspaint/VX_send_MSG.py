import time
import pyautogui
from pywinauto import keyboard

def send_msg(msg: str = None, times=100):
    for _ in range(times):
        if msg is not None:
            for c in msg:
                if c == ' ':
                    keyboard.send_keys('{SPACE}')
                elif c == '\n':
                    keyboard.send_keys('{ENTER}')
                else:
                    keyboard.send_keys(c)
        else:
            pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

# 输入框的坐标
x = 1850
y = 1050

# 发送次数
send_times = 3

# 发送内容，None就发送剪切板的东西
send_msgs = None

if __name__ == "__main__":
    # 输入框的坐标
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.click()
    for _ in range(send_times):
        send_msg(msg=send_msgs, times=send_times)
