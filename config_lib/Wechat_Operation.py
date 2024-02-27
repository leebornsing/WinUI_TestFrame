import os
import time
import traceback

import pyautogui
import pyperclip

from config_lib import images_on_screen
from config_lib.Wechat_Relationship_Base_Tree import Wechat_Relationship_Base_Tree

class Various_Base_Methods(Wechat_Relationship_Base_Tree):
    def __init__(self, confidence=0.8, duration=0.2, interval=0.2):
        super().__init__(confidence=confidence, duration=duration, interval=interval)

    def _switch_InputMethods(self):
        self.logger.info("尝试切换输入法")
        pyautogui.hotkey("ctrl", "a")
        now_input_method = images_on_screen.get_input_language("abc" + str(time.time()))
        images_on_screen.config_input_methods(now_input_method)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.5)

    def select_file_or_dir_by_WinSystem(self, windows_tree, file_path, region_width=950, region_height=550,
                                        is_select_file=True, is_save_path=False, is_need_switch_InputMethods=False):
        """
        在windows弹窗界面选择文件或目录
        :param windows_tree: 弹窗窗口tree/obj
        :param file_path: 文件/目录路径
        :param region_width: 窗口宽度
        :param region_height: 窗口高度
        :param is_select_file: 是否是文件【如果是目录请传False】
        :return:
        """
        windows = self.create_img_object(windows_tree)
        win_region = (windows.left, windows.top, region_width, region_height)
        if is_select_file:
            file_path, file_name = os.path.split(file_path)
        InputAndRefush = self.create_img_object(self.Windows_InputButtons, parent_region=win_region)
        if is_need_switch_InputMethods is True:
            InputAndRefush.click(focus_x=InputAndRefush.left - 50)
            self._switch_InputMethods()
        self.input_string_by_obj(img_obj=InputAndRefush, string=file_path, focus_x=InputAndRefush.left - 50,
                                 is_press_enter=True)
        if is_select_file:
            FileName = self.create_img_object(self.Windows_FileNameN, parent_region=win_region)
            self.input_string_by_obj(img_obj=FileName, string=file_name, focus_x=FileName.left + FileName.width + 30)
            if is_save_path:
                self.create_img_object(self.Windows_SaveS, parent_region=win_region)
            else:
                self.create_img_object(self.Windows_OpenO, parent_region=win_region)
        else:
            if is_save_path:
                self.create_img_object(self.Windows_SaveS, parent_region=win_region)
            else:
                self.create_img_object(self.Windows_SelectFile, parent_region=win_region)

class Chat_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

    def select_wechat_user(self, user_name=None):
        Chat_SearchUserBox = self.create_img_object(self.Chat_SearchUserBox)
        self.input_string_by_obj(img_obj=Chat_SearchUserBox, string=user_name, focus_x=Chat_SearchUserBox.lenth_x)
        first_ele_position = (Chat_SearchUserBox.center_x, Chat_SearchUserBox.lenth_y+30)
        x, y = self._select_options_from_path(destination_file=user_name, first_ele_position=first_ele_position,
                                              is_need_open_and_closed=True, is_doubleClick=False)
        self.assert_True(x is not None and y is not None, f"{user_name}这个可能没有找到，你check下日志")

    def send_something(self, string: str = None, is_use_clipboard=False, is_clear_entered_information=True):
        SendButton = self.create_img_object(self.Chat_SendButton)
        if is_clear_entered_information is True:
            SendButton.click(focus_y=SendButton.top - 30)
            SendButton.hotkey("ctrl", "a")
            SendButton.press("backspace")
        if string is not None:
            self.input_string_by_obj(img_obj=SendButton, string=string, focus_y=SendButton.top-30,
                                     is_clear_oldstring=False)
        if is_use_clipboard is True:
            SendButton.click(focus_y=SendButton.top - 30)
            SendButton.hotkey("ctrl", "v")
        SendButton.click()

class Wechat_Operation(Chat_Operation):
    def __init__(self):
        super().__init__()

    def start(self, test_name, is_need_start=True, ):
        self.logger.start(test_name)
        self.Wechat_relationship_tree()
        if is_need_start:
            self.appbase.start_application(product=self.appbase.wx_handlen_name)
