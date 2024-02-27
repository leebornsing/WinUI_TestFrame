
import re
import shutil

import pyautogui
import win32con
import time
import requests
import datetime
import os
import zipfile
import win32gui
from common.readConfig import ReadConfig
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

class App_Base_Config():

    def start_application(self, product="画图", wait_time=120, app_path=None):
        self.set_config_parm()
        app_parent_dir, app_exe_name, app_WindowsName = self._set_application_param(product)
        if app_path is not None:
            app_parent_dir = app_path
        self._start_application(app_parent_dir=app_parent_dir, app_exe_name=app_exe_name,
                                app_WindowsName=app_WindowsName, wait_time=wait_time)

    def _set_application_param(self, product="画图"):
        app_parent_dir = None
        app_exe_name = None
        app_WindowsName = None
        self.set_config_parm()
        if product == "画图":
            app_parent_dir = self.mspaint_parent_dir
            app_exe_name = self.mspaint_exe_name
            app_WindowsName = self.mspaint_handlen_name
        elif product == "微信":
            app_parent_dir = self.wx_parent_dir
            app_exe_name = self.wx_exe_name
            app_WindowsName = self.wx_handlen_name

        return app_parent_dir, app_exe_name, app_WindowsName

    def _start_application(self, app_parent_dir=None, app_exe_name=None, app_WindowsName=None, wait_time=120):
        self.set_config_parm()
        start_succ = os.system(r'start "" /d "{}" {}'.format(app_parent_dir, app_exe_name))
        if start_succ == "1":
            raise Exception("启动失败，请检查配置")

        app_started = self.search_windows_handel(app_name=app_WindowsName, wait_time=wait_time)
        print('app process status：{}'.format(app_started))
        app = self.search_windows_handel(app_name=app_WindowsName)
        win32gui.GetWindowText(app)


    def closed_application(self, product="画图",
                           wait_time: int = 6, search_interval_time: int = 1, by_kill_exe=True):
        app_parent_dir, app_exe_name, app_WindowsName = self._set_application_param(product)
        if by_kill_exe:
            os.system(' @taskkill /f /im {}'.format(app_exe_name))
        else:
            self.maximize_and_focus_window_by_title_suffix(app_WindowsName)
            pyautogui.moveTo(1900, 15)
            time.sleep(1)
            pyautogui.click()
        app_closed = self.search_windows_handel(app_name=app_WindowsName, wait_time=wait_time,
                                                search_interval_time=search_interval_time)
        if app_closed is True:
            assert Exception("窗口没有关闭，结束进程失败")

    def is_aliving_process(self, app_exe_name):
        is_aliving = os.system(f'tasklist |findstr "{app_exe_name}"')
        if is_aliving == 0:
            return True
        else:
            return False

    def search_windows_handel(self, app_name=None, wait_time: int = 60, search_interval_time: int = 1, name_is_end=True):
        search_times = int(wait_time/search_interval_time)
        for _ in range(search_times):
            # 找到所有窗口的句柄
            hwnds = []
            win32gui.EnumWindows(lambda hwnd, arg: arg.append(hwnd), hwnds)
            # 遍历所有窗口，找到标题结尾为指定字符串的窗口句柄
            for hwnd in hwnds:
                if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if name_is_end:
                        if title.endswith(app_name):
                            return True
                    else:
                        if title.startswith(app_name):
                            return True
            time.sleep(search_interval_time)
        return False

    def set_mspaint_parm(self):
        self.mspaint_parent_dir = ReadConfig().get_mspaint_App('mspaint_parent_dir')
        self.mspaint_exe_name = ReadConfig().get_mspaint_App('mspaint_exe_name')
        self.mspaint_handlen_name = ReadConfig().get_mspaint_App('mspaint_handlen_name')
        self.picture_store = ReadConfig().get_mspaint_App('picture_store')

    def set_wechat_parm(self):
        self.wx_parent_dir = ReadConfig().get_Wechat_App('wx_parent_dir')
        self.wx_exe_name = ReadConfig().get_Wechat_App('wx_exe_name')
        self.wx_handlen_name = ReadConfig().get_Wechat_App('wx_handlen_name')

    def set_common_config_parm(self):
        is_debug = ReadConfig().get_common_config('is_debug')
        self.is_debug = True if is_debug.lower() == "true" else False
        self.running_test_case = ReadConfig().get_common_config('running_test_case')
        self.wait_time = ReadConfig().get_common_config('wait_until_time')

    def set_config_parm(self):
        self.set_common_config_parm()
        self.set_mspaint_parm()
        self.set_wechat_parm()

    def wait_until_time(self, hour, minute=1):
        if int(hour) >= 25:
            return True
        while True:
            now = datetime.datetime.now()
            if now.hour == hour and now.minute == minute:
                return True
            elif now.hour < hour:
                # 计算还有多少小时和分钟
                remaining_hours = hour - now.hour - 1
                remaining_minutes = 60 - now.minute
                print("先等待{}小时{}分钟".format(remaining_hours, remaining_minutes))
                # 先等待remaining_hours小时
                time.sleep(remaining_hours * 3600)
                # 再等待remaining_minutes分钟
                time.sleep(remaining_minutes * 60)
            elif now.hour > hour:
                remaining_hours = 24 + hour - now.hour - 1
                remaining_minutes = 60 - now.minute
                print("可能需要跨越一天时间, 先等待{}小时{}分钟".format(remaining_hours, remaining_minutes))
                time.sleep(remaining_hours * 3600)
                time.sleep(remaining_minutes * 60)
            elif now.hour == hour and now.minute < minute and minute - now.minute - 1 != 0:
                # 计算还有多少分钟
                remaining_minutes = minute - now.minute - 1
                print("再等待{}分钟".format(remaining_minutes))
                # 先等待remaining_minutes分钟
                time.sleep(remaining_minutes * 60)
            else:
                now = datetime.datetime.now()
                if now.hour == hour and now.minute == minute:
                    return True
                else:
                    print("快到点了，每次等待10s")
                    time.sleep(10)

    @staticmethod
    def wait_to_time(hour: int, minute: int):
        if hour > 24 or hour < 0 or minute > 60 or minute < 0:
            print('时间格式不正确! 跳过等待!')
            return
        current_time_stamp = datetime.datetime.now()
        current_date = current_time_stamp.strftime('%Y-%m-%d')
        waite_time_stamp = time.mktime(time.strptime(current_date, '%Y-%m-%d')) + 3600*hour + 60*minute
        wait_time = waite_time_stamp - time.time()
        if wait_time > 0:
            print('开始等待，时长：{}时{}分{}秒.'.format(int(wait_time//3600), int(wait_time % 3600//60), int(wait_time % 3600 % 60)))
            time.sleep(wait_time)
        elif wait_time + 24*3600 > 0:
            wait_time += 24*3600
            print('跨天等待，时长：{}时{}分{}秒.'.format(int(wait_time//3600), int(wait_time % 3600//60), int(wait_time % 3600 % 60)))
            time.sleep(wait_time)
        else:
            print('设置时间不满足等待要求，跳过等待！')

    def file_is_existed(self, file_path):
        """
        检查基础文件是否存在
        :param
        file_path:（str）：传文件路径
        :return:
        None
        """
        is_exists_config = os.path.exists(file_path)
        if is_exists_config:
            assert Exception("{}，这个配置文件不存在".format(file_path))

    def maximize_and_focus_window_by_title_suffix(self, title_suffix):
        """
        找到窗口标题结尾为指定字符串的窗口并最大化，同时将它置于最前。
        :param title_suffix: 窗口标题的后缀字符串
        """
        # 找到所有窗口的句柄
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, arg: arg.append(hwnd), hwnds)

        # 遍历所有窗口，找到标题结尾为指定字符串的窗口句柄
        for hwnd in hwnds:
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title.endswith(title_suffix):
                    # 最大化窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    # 将窗口置于最前
                    win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)

    def minimize_window(self, window_name):
        # 获取所有顶层窗口句柄
        windows = []

        def callback(hwnd, windows):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(callback, windows)

        # 遍历窗口，找到匹配的窗口并最小化
        for hwnd, title in windows:
            if window_name in title:
                # set_window_style(hwnd, win32con.WS_OVERLAPPEDWINDOW)
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def set_window_style(self, hwnd, style):
        if hwnd != 0:
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
            win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)

    def delete_files_with_string(self, path, strings):
        # 获取path下的所有文件和文件夹
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if strings in file:
                    os.remove(file_path)
            else:
                if strings in file:
                    shutil.rmtree(file_path)

class Config_File_for_ProdictProject():
    def __indent(self, elem, level=0):
        """
        xml格式化缩进
        :param elem: xml元素对象
        :param level: 所属层级（root级别为0）
        :return: 无
        """
        i = "\n" + level * "\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

if __name__ == '__main__':
    ...
