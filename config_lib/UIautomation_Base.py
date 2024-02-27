import os
import re
import time
import pyautogui
import pygetwindow
import pyperclip
import win32com.client
import win32gui
from config_lib.Config_Base import App_Base_Config

class Handle_Operation():
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self.start_inspect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed_inspect()

    def is_WindowText(self):
        # 获取当前活动窗口的句柄
        hwnd = win32gui.GetForegroundWindow()
        return hwnd
        # # 判断窗口是否是输入框

    def typewrite_by_handle(self, text):
        # 创建SendKeys对象
        shell = win32com.client.Dispatch("WScript.Shell")
        send_keys = shell.SendKeys
        # 将指定字符串发送到窗口
        send_keys(text)

    def start_inspect(self):
        self.closed_inspect()
        parent_dir = os.path.dirname(__file__)
        parent_dir = parent_dir.replace("/", "\\")
        start_succ = os.system(r'start "" /d {} {}'.format(parent_dir, "inspect.exe"))
        if start_succ == "1":
            raise Exception("启动失败，请检查配置")
        App_Base = App_Base_Config()
        app_started = App_Base.search_windows_handel(app_name="Inspect", name_is_end=False)
        if app_started is False:
            assert Exception("窗口没有找到，请检查是否启动成功")
        self.set_window_size_and_position(window_title="Inspect", width=305, height=35, x=1525, y=5)

    def set_window_size_and_position(self, window_title, width, height, x, y):
        # 设置窗口大小和位置
        window = pygetwindow.getWindowsWithTitle(window_title)[0]
        window.resizeTo(width, height)
        window.moveTo(x, y)

    def closed_inspect(self):
        try:
            os.system(' @taskkill /f /im {}'.format("inspect.exe"))
        except:
            pass

    def refresh_inspect(self):
        currentMouseX, currentMouseY = pyautogui.position()
        pyautogui.hotkey("ctrl", "shift", "5")
        time.sleep(1)
        pyautogui.moveTo(currentMouseX, currentMouseY)

    def get_box_from_inspect(self):
        information = self.get_element_information()
        region_text = information['BoundingRectangle:']
        numbers = re.findall(r'\d+', region_text)
        if len(numbers) == 4:
            region = (int(numbers[0]), int(numbers[1]),
                      int(numbers[2]) - int(numbers[0]), int(numbers[3]) - int(numbers[1]))
            return region

    def get_click_position_from_inspect(self):
        box = self.get_box_from_inspect()
        x = int(box[0] + box[2]/2)
        y = int(box[1] + box[3]/2)
        return x, y

    def get_name_from_inspect(self):
        information = self.get_element_information()
        name = information.get('LegacyIAccessible.Name:')
        if name is None:
            name = information.get('Name:')
        if name is not None:
            name = name.replace("'", '').replace('"', '')
        return name

    def get_LocalizedControlType(self):
        information = self.get_element_information()
        name = information.get('LocalizedControlType:')
        return name

    def get_element_information(self):
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "shift", "4")
        time.sleep(0.5)
        text = pyperclip.paste()
        messages = text.split("\r\n")
        information_dict = {}
        for message in messages:
            msg = message.split("\t")
            if len(msg) > 1:
                information_dict[msg[0]] = msg[1]
        return information_dict

    def parent_element(self):
        pyautogui.hotkey("ctrl", "shift", "F6")
        time.sleep(1)

    def first_child(self):
        pyautogui.hotkey("ctrl", "shift", "F7")
        time.sleep(1)

    def last_child(self):
        pyautogui.hotkey("ctrl", "shift", "F9")
        time.sleep(1)

    def next_sibling(self):
        pyautogui.hotkey("ctrl", "shift", "F8")
        time.sleep(1)

    def previos_sibling(self):
        pyautogui.hotkey("ctrl", "shift", "F5")
        time.sleep(1)

if __name__ == '__main__':
    ...


