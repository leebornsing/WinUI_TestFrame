import os
import time
import traceback
import pyautogui
from config_lib import images_on_screen
from config_lib.Draw_Relationship_Base_Tree import Draw_Relationship_Base_Tree

class Various_Base_Methods(Draw_Relationship_Base_Tree):
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

class MainMenu_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

class MenuTools_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

class MenuTools_Shape_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

    def _Base_Elements(self, Element_tree, x: int, y: int, Shape_width=50, Shape_height=50, element_name=None):
        Shape = self.create_img_object(self.Shape_Shape, parent_region=self.Top_region)
        Shape_region = (Shape.left-100, Shape.top-90, 250, 140)
        _Base_Elements = self.create_img_object(Element_tree, parent_region=Shape_region)
        _Base_Elements.dragTo(x=x+Shape_width, y=y+Shape_height, focus_x=x, focus_y=y)
        Shape_width = Shape_width if Shape_width != 0 else 1
        Shape_height = Shape_height if Shape_height != 0 else 1
        updatae_region = (x, y, Shape_width, Shape_height)
        _Base_Elements.update_object(updatae_region)
        _Base_Elements.element_name = element_name
        return _Base_Elements

    def Recovery_Line_Mode(func):
        def inner(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self._click_StraightLine()
            return res
        return inner
    Recovery_Line_Mode = staticmethod(Recovery_Line_Mode)

    def draw_StraightLine(self, x: int, y: int, Shape_width=50, Shape_height=50):
        try:
            Element = self._Base_Elements(Element_tree=self.Shape_StraightLined, x=x, y=y, Shape_width=Shape_width,
                                          Shape_height=Shape_height, element_name="straightLine")
        except:
            Element = self._Base_Elements(Element_tree=self.Shape_StraightLine, x=x, y=y, Shape_width=Shape_width,
                                          Shape_height=Shape_height, element_name="straightLine")
        return Element

    def _click_StraightLine(self):
        Shape = self.create_img_object(self.Shape_Shape, parent_region=self.Top_region)
        Shape_region = (Shape.left-100, Shape.top-90, 250, 140)
        _Base_Elements = self.create_img_object(self.Shape_StraightLine, parent_region=Shape_region)

    @Recovery_Line_Mode
    def draw_Rectangle(self, x: int, y: int, Shape_width=50, Shape_height=50):
        return self._Base_Elements(Element_tree=self.Shape_Rectangle, x=x, y=y, Shape_width=Shape_width,
                            Shape_height=Shape_height, element_name="rectangle")


    @Recovery_Line_Mode
    def draw_Hexagram(self, x: int, y: int, Shape_width=50, Shape_height=50):
        return self._Base_Elements(Element_tree=self.Shape_Hexagram, x=x, y=y, Shape_width=Shape_width,
                            Shape_height=Shape_height, element_name="hexagram")

class MenuTools_Graphics_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

    def Rotate_the_current_Canvas(self, rotate_mode="向左旋转 90 度"):
        Graphics_region = self._get_Graphics_region()
        Rotate = self.create_img_object(self.Graphics_Rotate, parent_region=Graphics_region)
        self._get_img_obj_from_first_position(
            destination_file=rotate_mode, first_ele_position=(Rotate.center_x, Rotate.center_y))

    def _get_Graphics_region(self):
        Graphics = self.create_img_object(self.Graphics_Graphics, parent_region=self.LeftTop_region)
        Graphics_region = (Graphics.left-70, Graphics.top-100, 160, 110)
        return Graphics_region

class Canvas_Operation(Various_Base_Methods):
    def __init__(self):
        super().__init__()

    def copy_canvas_to_clipboard(self):
        self.logger.debug("复制画图到剪切板")
        SelectOperation = self.create_img_object(self.Graphics_SelectOperation, parent_region=self.LeftTop_region)
        SelectOperation.click()
        currentMouseX, currentMouseY = SelectOperation.mouse_position()
        SelectOp_region = (currentMouseX-160, currentMouseY-300, 320, 600)
        try:
            self.create_img_object(self.Graphics_SelectAll, parent_region=SelectOp_region)
        except:
            # 其他程序打开后，这个程序在后台，会有一次click为聚焦锁定。
            # 所以如果第一次没找到select all，就再点一次选择再找找看
            SelectOperation.click()
            self.create_img_object(self.Graphics_SelectAll, parent_region=SelectOp_region)
        self._select_rightClick_menu_region(menu_tree=self.Canvas_Copy)

    def _select_rightClick_menu_region(self, menu_tree, Rclick_x=None, Rclick_y=None ):
        Graphics = self.create_img_object(self.Graphics_Graphics, parent_region=self.LeftTop_region)
        focus_y = Rclick_y if Rclick_y is not None else Graphics.lenth_y+30
        Graphics.rightClick(focus_x=Rclick_x, focus_y=focus_y)
        currentMouseX, currentMouseY = Graphics.mouse_position()
        RCmenu_region = (currentMouseX-160, currentMouseY-300, 320, 600)
        self.create_img_object(menu_tree, parent_region=RCmenu_region)

class Mspaint_Operation(MainMenu_Operation, MenuTools_Operation, MenuTools_Shape_Operation, MenuTools_Graphics_Operation,
                        Canvas_Operation):
    def __init__(self):
        super().__init__()

    def start(self, test_name, is_need_start=True, ):
        self.logger.start(test_name)
        self.Draw_relationship_tree()
        if is_need_start:
            self.appbase.closed_application(self.appbase.mspaint_handlen_name)
            self.appbase.start_application(product=self.appbase.mspaint_handlen_name)


    def save_the_picture(self, save_path=None, file_name=None, is_select_path=True):
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1)
        save_path = save_path if save_path else self.appbase.picture_store
        file_name = file_name if file_name else self.formatting_time(Common_formatting=False)
        file_path = os.path.join(save_path, file_name)
        try:
            self.select_file_or_dir_by_WinSystem(
                windows_tree=self.MainMenu_SaveWindows, file_path=file_path, is_select_file=True, is_save_path=True,
                is_need_switch_InputMethods=True)
        except:
            self.assert_True(is_select_path is False, traceback.format_exc())
