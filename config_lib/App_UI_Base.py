import os
import re
import pyautogui
import pyperclip
import win32api
import win32con
import time
from pywinauto import keyboard
from config_lib import images_on_screen
from config_lib import operation_base
from config_lib.Config_Base import App_Base_Config, Config_File_for_ProdictProject
from config_lib.Log_Lib import TestLogger
from config_lib.UIautomation_Base import Handle_Operation


class Test_keyword():
    def __init__(self):
        self.logger = TestLogger()
        self.handle_operation = Handle_Operation()
        self.appbase = App_Base_Config()
        self.appbase.set_config_parm()
        self.ConfigFile = Config_File_for_ProdictProject()
        super().__init__()

    def assert_True(self, expression, err_msg="err", is_mark_region=None):
        try:
            assert expression, err_msg
        except Exception as e:
            self.logger.error(e, is_mark_region=is_mark_region)
            raise Exception(err_msg)

    def raise_err(self, err_msg="err", success=False, is_mark_region=None):
        if is_mark_region is None:
            try:
                is_mark_region = eval(err_msg.split("内找不到")[1].split("在")[-1])
            except:
                pass
            if isinstance(is_mark_region, tuple) and len(is_mark_region) == 4:
                pass
            else:
                is_mark_region = None
        self.logger.error(err_msg, success=success, is_mark_region=is_mark_region)
        raise Exception(err_msg)

class Img_Obejct(Test_keyword):
    def __init__(self, confidence=0.8, duration=0.2, interval=0.3):
        self.name = None
        self.left = None
        self.top = None
        self.width = None
        self.height = None
        self.img_path = None
        self.center_x = None
        self.center_y = None
        self.list = None
        self.is_must = True
        self.default_operation = None
        self.operation = []
        self.confidence = confidence
        self.duration = duration
        self.interval = interval
        self.element_uniqueness = False
        self.object_uniqueness = False
        self.aft_operation_waittime = 0.2
        self.is_click_center = False
        pyautogui.FAILSAFE = False
        self.sefault_resolution = [1920, 1080]
        self.screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        self.screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
        self.region = (0, 0, self.screen_x, self.screen_y)
        self.screen_x_rate = self.screen_x/self.sefault_resolution[0]
        self.screen_y_rate = self.screen_y/self.sefault_resolution[1]
        self.Left_region = (0, 0, self.screen_x//2, self.screen_y)
        self.LeftTop_region = (0, 0, self.screen_x//2, self.screen_y//2)
        self.RightTop_region = (self.screen_x//2, 0, self.screen_x//2, self.screen_y//2)
        self.Right_region = (self.screen_x//2, 0, self.screen_x//2, self.screen_y)
        self.LeftBottom_region = (0, self.screen_y//2, self.screen_x//2, self.screen_y//2)
        self.RightBottom_region = (self.screen_x//2, self.screen_y//2, self.screen_x//2, self.screen_y//2)
        self.Intermediate_region = (self.screen_x//4, self.screen_y//4, self.screen_x//2, self.screen_y//2)
        self.Larger_Central_region = (self.screen_x//5, self.screen_y//5, self.screen_x*3//5, self.screen_y*3//5)
        self.Middle_region = (self.screen_x//5, 0, self.screen_x*3//5, self.screen_y)
        self.Top_region = (0, 0, self.screen_x, self.screen_y//2)
        self.Bottom_region = (0, self.screen_y//2, self.screen_x, self.screen_y//2)
        super().__init__()

    def operation_time_interval(func):
        def inner(self, *args, **kwargs):

            Object_Name = self.name
            Operation_name = func.__name__
            Operation = "Object Name: {}\nOperation: {}".format(Object_Name, Operation_name)
            if Operation_name == operation_base.dragTo or Operation_name == "dragRel":
                currentMouseX, currentMouseY = pyautogui.position()
                before_msg = "The position of the mouse before the operation: {}, {}".format(currentMouseX, currentMouseY)
                self.logger.info(message=before_msg, Operation=Operation, is_mark_region=self.region)

            res = func(self, *args, **kwargs)
            currentMouseX, currentMouseY = pyautogui.position()
            after_msg = "The position of the mouse after the operationn: {}, {}".format(currentMouseX, currentMouseY)
            if Operation_name == operation_base.typewrite:
                if len(args) != 0:
                    exc_str = args[0]
                elif kwargs.get("text") is not None:
                    exc_str = kwargs.get("text")
                else:
                    self.raise_err(f"入参不对：args: {args},kwargs: {kwargs}")
                exc_str = exc_str.replace("\r\n", "\n")
                typewrite_msg = "向输入框写入：【{}】".format(exc_str)
                self.logger.debug(message=typewrite_msg, Operation=Operation)
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(len(exc_str) // 100 + 1)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(len(exc_str) // 100 + 1)
                text = pyperclip.paste()
                text = text.replace("\r\n", "\n")
                if text != exc_str:
                    time.sleep(len(exc_str)//100+1)
                    pyautogui.hotkey('ctrl', 'a')
                    time.sleep(len(exc_str)//100+1)
                    pyautogui.hotkey('ctrl', 'c')
                    text = pyperclip.paste()
                    text = text.replace("\r\n", "\n")
                self.assert_True(text == exc_str,
                                 "输入文字不太对，可能没有输入成功预期为{}，实际为{}".format(exc_str, text))
            elif Operation_name == operation_base.hotkey:
                after_msg += "\r\n hotkey is {}".format([arg for arg in args])
                self.logger.debug(message=after_msg, Operation=Operation, is_mark_region=self.region)
            else:
                self.logger.debug(message=after_msg, Operation=Operation, is_mark_region=self.region)
            time.sleep(self.aft_operation_waittime if self.aft_operation_waittime is not None else 0.5)
            return res
        return inner
    operation_time_interval = staticmethod(operation_time_interval)

    def create_img_obj(self, img_obj_tree, parent_region=None, do_default_operation=False):
        if img_obj_tree.get("is_must"):
            img_obj = self.__create_img_object(img_obj_tree, parent_region=parent_region)
        else:
            try:
                img_obj = self.__create_img_object(img_obj_tree, parent_region=parent_region)
            except:
                self.logger.info("{}该对象不是必须的，可以不查找".format(img_obj_tree.get("name")))
                return None
        if img_obj_tree.get("is_must") is False and not isinstance(img_obj, object):
            self.logger.info("{}该对象不是必须的，可以不查找".format(img_obj_tree.get("name")))
            return None
        else:
            if do_default_operation and img_obj is not None:
                if isinstance(img_obj, list):
                    for obj in img_obj:
                        obj.logger = self.logger
                else:
                    img_obj.logger = self.logger
                    img_obj.operation_param(img_obj.default_operation, param=img_obj.operation_param)
                    time.sleep(img_obj.aft_operation_waittime)
            else:
                if isinstance(img_obj, list):
                    for obj in img_obj:
                        obj.logger = self.logger
                else:
                    img_obj.logger = self.logger
            return img_obj

    def create_relationship_tree(self, img_path, operation=None, default_operation=None, _operation_param=None,
                                  region=None, is_must: bool = True, box_index: int = -1, obj_uniqueness: bool = True,
                                  search_wait_interval: float = 0.2, aft_operation_waittime: float = 0.15):
        if default_operation:
            pass
        elif operation:
            default_operation = [operation, ][0]
        else:
            default_operation = operation_base.focus_object
            operation = [default_operation, ]
        tree = \
            {
                    "name": self.get_img_name(img_path),
                    "img_path": img_path,
                    "operation": operation,
                    "default_operation": default_operation,
                    "_operation_param": _operation_param,
                    "region": region if region else self.region,
                    "is_must": is_must,
                    "box_index": box_index if obj_uniqueness is not True else 0,
                    "obj_uniqueness": obj_uniqueness,
                    "search_wait_interval": search_wait_interval,
                    "aft_operation_waittime": aft_operation_waittime,
            }
        return tree

    def __create_img_object(self, img_obj_tree, parent_region=None):
        search_region = parent_region if parent_region is not None else img_obj_tree.get("region")
        img_box, object_uniqueness, actual_confidence = images_on_screen.find_images_on_screen(
            img_path=img_obj_tree.get("img_path"), search_region=search_region,
            search_wait_interval=img_obj_tree.get("search_wait_interval"))
        obj_list = []
        if img_obj_tree.get("is_must") and img_obj_tree.get("obj_uniqueness") is True:
            if img_obj_tree.get("obj_uniqueness") != object_uniqueness:
                self.logger.warning("{}，这个图片对象实际不唯一,{}".format(
                    img_obj_tree.get("img_path"), [box for box in img_box]))
        if img_obj_tree.get("obj_uniqueness") is True:
            img_box = img_box[img_obj_tree.get("box_index")]
            obj = self.__generate_imgobj(img_box, img_obj_tree, object_uniqueness, actual_confidence, box_index=img_obj_tree.get("box_index"))
            return obj
        else:
            if img_obj_tree.get("box_index") != -1:
                obj = self.__generate_imgobj(img_box[img_obj_tree.get("box_index")], img_obj_tree, object_uniqueness,
                                             actual_confidence, box_index=img_obj_tree.get("box_index"))
                return obj
            else:
                for index in range(len(img_box)):
                    obj = self.__generate_imgobj(img_box[index], img_obj_tree, object_uniqueness, actual_confidence,
                                                 box_index=index)
                    obj_list.append(obj)
                return obj_list

    def __generate_imgobj(self, img_box, img_obj_tree, object_uniqueness, actual_confidence, box_index):
        self.img_obejct = Img_Obejct()
        self.img_obejct.confidence = actual_confidence
        self.img_obejct.object_uniqueness = object_uniqueness
        self.img_obejct.center_x = int(img_box[0] + img_box[2]/2)
        self.img_obejct.center_y = int(img_box[1] + img_box[3]/2)
        self.img_obejct.left = img_box[0]
        self.img_obejct.top = img_box[1]
        self.img_obejct.width = img_box[2]
        self.img_obejct.height = img_box[3]
        self.img_obejct.lenth_x = img_box[0] + img_box[2]
        self.img_obejct.lenth_y = img_box[1] + img_box[3]
        self.img_obejct.box_index = box_index
        self.is_click_center = False
        if img_obj_tree is not None:
            self.img_obejct._operation_param = img_obj_tree.get("_operation_param")
            self.img_obejct.aft_operation_waittime = img_obj_tree.get("aft_operation_waittime")
            obj_name = self.get_img_name(img_obj_tree.get("img_path"))
            self.img_obejct.name = obj_name if obj_name is not None else "empty_obj"
            self.img_obejct.img_path = img_obj_tree.get("img_path")
            self.img_obejct.default_operation = img_obj_tree.get("default_operation")
            self.img_obejct.operation = img_obj_tree.get("operation")
            self.img_obejct.is_must = img_obj_tree.get("is_must")
        else:
            self.img_obejct.aft_operation_waittime = 0.5
            self.img_obejct.default_operation = "focus_object"
            self.img_obejct.operation = "focus_object"
            self.img_obejct.is_must = False
        self.img_obejct.region = self.img_obejct.get_img_obj_region()
        return self.img_obejct

    def get_img_obj_region(self):
        left = self.left
        top = self.top
        width = self.width
        height = self.height
        return left, top, width, height

    def get_img_name(self, img_path=None):
        if img_path is not None:
            img_name = os.path.basename(img_path).split(".")[0]
            return img_name

    def operation_param(self, operation: str, param=None, *args, **kwargs):
        """
        做一些操作，调用例：
        img_obj.operation_param(operation=operation, param=param)

        :param operation:
        :param param:
        :param args:
        :param kwargs:
        :return:
        """
        if operation == operation_base.focus_object:
            self.focus_object()

        elif operation == operation_base.click:
            self.click(**kwargs)

        elif operation == operation_base.doubleClick:
            self.doubleClick(**kwargs)

        elif operation == operation_base.moveRel:
            x = param.get("x")
            y = param.get("y")
            self.moveRel(x=x, y=y, **kwargs)

        elif operation == operation_base.moveTo:
            x = param.get("x")
            y = param.get("y")
            self.moveTo(x=x, y=y, **kwargs)

        elif operation == operation_base.dragTo:
            x = param.get("x")
            y = param.get("y")
            button = param.get("button", "left")
            focus_x = param.get("button", "focus_x")
            focus_y = param.get("button", "focus_y")
            self.dragTo(x=x, y=y, button=button, focus_x=focus_x, focus_y=focus_y, **kwargs)

        elif operation == operation_base.scroll:
            amount_to_scroll = param.get("amount_to_scroll")
            is_click = param.get("is_click", True)
            self.scroll(amount_to_scroll, is_click, **kwargs)

        elif operation == operation_base.hotkey:
            self.hotkey(*args, **kwargs)

        elif operation == operation_base.press:
            key = param.get("key")
            is_click = param.get("is_click", False)
            self.press(key, is_click, **kwargs)

        elif operation == operation_base.rightClick:
            self.rightClick(**kwargs)
        else:
            self.raise_err("{},操作参数不支持，请联系框架作者新增".format(operation))

    @operation_time_interval
    def focus_object(self, focus_x=None, focus_y=None, **kwargs):
        """
        默认聚焦在对象偏左上模块位置
        :param kwargs:
        :return:
        """
        self._focus_object(x=focus_x, y=focus_y, **kwargs)

    def _focus_object(self, x=None, y=None, **kwargs):
        """
        默认聚焦在对象偏左上模块位置
        :param kwargs:
        :return:
        """
        if self.is_click_center is True:
            x = self.center_x
        x = int(x) if x is not None else int((self.width)/3 + self.left)
        y = int(y) if y is not None else int(self.center_y)
        time.sleep(0.1)
        pyautogui.moveTo(x, y, duration=self.duration, **kwargs)
        time.sleep(0.1)

    @operation_time_interval
    def click(self, focus_x=None, focus_y=None, **kwargs):
        self._focus_object(focus_x, focus_y)
        pyautogui.click(duration=self.duration, **kwargs)

    @operation_time_interval
    def rightClick(self, focus_x=None, focus_y=None, **kwargs):
        self._focus_object(x=focus_x, y=focus_y)
        pyautogui.rightClick(duration=self.duration, **kwargs)

    @operation_time_interval
    def doubleClick(self, focus_x=None, focus_y=None, **kwargs):
        self._focus_object(x=focus_x, y=focus_y)
        pyautogui.doubleClick(duration=self.duration, **kwargs)

    @operation_time_interval
    def tripleClick(self, focus_x=None, focus_y=None, **kwargs):
        self._focus_object(x=focus_x, y=focus_y)
        pyautogui.tripleClick(duration=self.duration, **kwargs)

    @operation_time_interval
    def moveRel(self, x: int, y: int, **kwargs):
        """
        移动到元素后,再移动到的元素相对位置
        :param kwargs:
        :return:
        """
        self.focus_object()
        # pyautogui.moveRel(xOffset=x, yOffset=y, duration=duration if duration else self.duration, **kwargs)
        pyautogui.moveRel(xOffset=x, yOffset=y, duration=1.9, **kwargs)

    @operation_time_interval
    def moveTo(self, x: int, y: int, **kwargs):
        pyautogui.moveTo(int(x), int(y), duration=self.duration, **kwargs)

    @operation_time_interval
    def dragTo(self, x: int, y: int, focus_x=None, focus_y=None, **kwargs):
        self.focus_object(focus_x, focus_y)
        # time.sleep(2)
        pyautogui.mouseDown()
        pyautogui.moveTo(int(x), int(y), duration=2.5, **kwargs)
        time.sleep(2)
        pyautogui.mouseUp()
        time.sleep(0.1)

    @operation_time_interval
    def dragRel(self, x: int, y: int, focus_x=None, focus_y=None, **kwargs):
        self._focus_object(focus_x, focus_y)
        time.sleep(2)
        try:
            pyautogui.mouseDown()
            self.moveRel(x, y, **kwargs)
        finally:
            time.sleep(2)
            time.sleep(self.duration)
            pyautogui.mouseUp()
            time.sleep(0.1)

    @operation_time_interval
    def scroll(self, amount_to_scroll, focus_x=None, focus_y=None, is_click=True, is_focus=True, **kwargs):
        """
        :param amount_to_scroll:鼠标中键滚动次数
        :param is_click:
        :param kwargs:
        :return:
        """
        if is_focus:
            self._focus_object(x=focus_x, y=focus_y)
        if is_click:
            self.click()
        pyautogui.scroll(amount_to_scroll, **kwargs)

    @operation_time_interval
    def hotkey(self, *args, **kwargs):
        """
        热键、快捷键，例: self.hotkey('ctrl', 'v')
        pyautogui.KEY_NAMES     可以看到支持的按键名称
        :param args:
        :param kwargs:
        :return:
        """
        self._focus_object()
        pyautogui.hotkey(duration=self.duration, *args, **kwargs)

    @operation_time_interval
    def press(self, key=None, is_focus=False, is_click=False, **kwargs):
        """
        单次按压键盘，例: self.press('4')
        pyautogui.KEY_NAMES     可以看到支持的按键名称
        :return:
        """
        if is_focus:
            self._focus_object()
        if is_click:
            self.click()
        pyautogui.press(key, interval=self.interval, **kwargs)

    @operation_time_interval
    def get_position_RGB(self, x: int = None, y: int = None):
        """
        获取img对象的颜色，默认获取获取元素图片中央，也可以指定坐标点
        :param x:
        :param y:
        :return:
        """
        if x is None:
            x = self.center_x
        if y is None:
            y = self.center_y
        pix = pyautogui.pixel(x, y)
        return pix

    @operation_time_interval
    def compare_RGB_same(self, pix: tuple, x: int = None, y: int = None, tolerance: int = 0):
        if x is None:
            x = self.center_x
        if y is None:
            y = self.center_y
        is_same = pyautogui.pixelMatchesColor(x, y, pix, tolerance=tolerance)
        return is_same

    @operation_time_interval
    def typewrite(self, text=None, is_click=False, **kwargs):
        self._focus_object()
        if is_click:
            self.click()
        if self.contains_chinese_or_fullwidth(text):
            for c in text:
                if c == ' ':
                    keyboard.send_keys('{SPACE}')
                elif c == '\n':
                    pyautogui.press('enter', **kwargs)
                elif c.isascii() and c.isalpha() is False:
                    pyautogui.typewrite(c, **kwargs)
                else:
                    keyboard.send_keys(c)
        elif "(" in text or ")" in text:
            pyautogui.typewrite(text, **kwargs)
        else:
            self.handle_operation.typewrite_by_handle(text=text)

    def contains_chinese_or_fullwidth(self, string):
        """
        判断字符串中是否含有中文或全角符号
        """
        pattern = re.compile(r'[\u4e00-\u9fa5\uff00-\uffff]')  # 匹配中文和全角字符
        return bool(pattern.search(string))

    @operation_time_interval
    def keyDown(self, key=None, is_click=False, **kwargs):
        """
        pyautogui.KEY_NAMES     可以看到支持的按键名称
        :return:
        """
        self._focus_object()
        if is_click:
            self.click()
        pyautogui.keyDown(key, interval=self.interval, **kwargs)

    @operation_time_interval
    def keyUp(self, key=None, is_click=False, **kwargs):
        """
        pyautogui.KEY_NAMES     可以看到支持的按键名称
        :return:
        """
        self._focus_object()
        if is_click:
            self.click()
        pyautogui.keyUp(key, interval=self.interval, **kwargs)

    @operation_time_interval
    def mouseDown(self, focus_x=None, focus_y=None, is_click=False, **kwargs):
        """
        按下鼠标
        """
        self._focus_object(focus_x, focus_y)
        if is_click:
            self.click(focus_x=focus_x, focus_y=focus_y)
        pyautogui.mouseDown(**kwargs)
        time.sleep(self.interval)

    @operation_time_interval
    def mouseUp(self, focus_x=None, focus_y=None, is_click=False, **kwargs):
        """
        释放鼠标
        """
        self._focus_object(focus_x, focus_y)
        if is_click:
            self.click(focus_x=focus_x, focus_y=focus_y)
        pyautogui.mouseUp(**kwargs)
        time.sleep(self.interval)

    def mouse_position(self):
        currentMouseX, currentMouseY = pyautogui.position()
        return currentMouseX, currentMouseY

    def formatting_time(self, Common_formatting=True):
        if Common_formatting:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        else:
            return time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))

    def _update_object(self, region=None):
        cache_name = self.name + "_screenshot_{}".format(self.formatting_time(Common_formatting=False))
        self.img_path = images_on_screen.screenshot_to_cache(region, cache_name)
        region = tuple(region)
        self.left = region[0]
        self.top = region[1]
        self.width = region[2]
        self.height = region[3]
        self.center_x = int(region[0] + region[2]/2)
        self.center_y = int(region[1] + region[3]/2)
        self.lenth_x = region[0] + region[2]
        self.lenth_y = region[1] + region[3]
        self.region = region
        self.logger.info("已更新img对象【{}】的区域，区域：{}".format(self.name, self.region), is_mark_region=region)

    def update_object(self, region=None, left=None, top=None, width=None, height=None):
        if any([left, top, width, height]):
            region = (left if left else self.left, top if top else self.top,
                      width if width else self.width, height if height else self.height)
        else:
            region = region if region else self.get_img_obj_region()
        self._update_object(region=region)

    def create_empty_obj_for_log(self, position=None, region=None):
        if position is not None:
            img_box = (position[0] - 3, position[1] - 3, 6, 6)
        elif region is not None:
            img_box = region
        else:
            currentMouseX, currentMouseY = self.mouse_position()
            img_box = (currentMouseX-3, currentMouseY-3, 6, 6)
        img_obj_tree = {}
        img_obejct = self.__generate_imgobj(img_box=img_box, img_obj_tree=img_obj_tree,
                                            object_uniqueness=True, actual_confidence=1, box_index=0)
        return img_obejct

    def rightRegion(self, allowance=5):
        return (self.left+self.width//2, self.top-allowance, self.width//2+allowance, self.height+2*allowance)

    def leftRegion(self, allowance=5):
        return (self.left-allowance, self.top-allowance, self.width // 2 + allowance, self.height+2*allowance)

    def topRegion(self, allowance=5):
        return (self.left-allowance, self.top-allowance, self.width+allowance*2, self.height//2+allowance)

    def bottomRegion(self, allowance=5):
        return (self.left-allowance, self.top+self.height//2, self.width+allowance*2, self.height+allowance)

class App_UI_Base(Img_Obejct):
    def __init__(self, confidence=0.8, duration=0.2, interval=0.3):
        self.confidence = confidence
        self.duration = duration
        self.interval = interval
        super().__init__()

    def region_scaling(self, region: tuple, x_rate=None, y_rate=None):
        region_list = list(region)
        if x_rate is None:
            x_rate = self.screen_x_rate
        if y_rate is None:
            y_rate = self.screen_y_rate
        region_list[0] = int(region[0] * x_rate)
        region_list[1] = int(region[1] * y_rate)
        region_list[2] = int(region[2] * x_rate)+1
        region_list[3] = int(region[3] * y_rate)+1
        return region_list

    def check_img_in_screen(self, relationship_tree):
        try:
            Existing_ICD = self.create_img_obj(relationship_tree)
            return Existing_ICD
        except:
            return None

    def input_string_by_tree(self, tree, tree_region, string: str=None, offset_x=None, offset_y=None,
                            is_clear_oldstring=True, is_press_enter=False):
        img_obj = self.create_img_object(tree, parent_region=tree_region, do_default_operation=False)
        focus_x = img_obj.center_x if offset_x is None else img_obj.center_x+offset_x
        focus_y = img_obj.center_y if offset_y is None else img_obj.center_y+offset_y
        self.input_string_by_obj(img_obj=img_obj, string=string, focus_x=focus_x, focus_y=focus_y,
                                 is_clear_oldstring=is_clear_oldstring, is_press_enter=is_press_enter)

    def input_string_by_obj(self, img_obj, string: str, focus_x=None, focus_y=None,
                            is_clear_oldstring=True, is_press_enter=False):
        img_obj.click(focus_x=focus_x, focus_y=focus_y)
        if is_clear_oldstring:
            img_obj.hotkey("ctrl", "a")
        img_obj.typewrite(str(string))
        time.sleep(1)
        if is_press_enter:
            img_obj.press("enter")

    def create_img_object(self, tree, parent_region=None, do_default_operation=True):
        if isinstance(tree, dict):
            img_obj = self.create_img_obj(tree, parent_region=parent_region,
                                              do_default_operation=do_default_operation)
            return img_obj
        else:
            return tree

    def _select_options_from_path(
            self, destination_file, first_ele_position=None, is_doubleClick_for_first_operation=False,
            is_doubleClick=True, need_before_num=None, is_need_open_and_closed=False, next_element_operation="down",
            is_adjustment=True):
        self.logger.info(f"将选择{destination_file}选项")
        destination_file = str(destination_file)
        if is_need_open_and_closed:
            self.handle_operation.start_inspect()
        if first_ele_position:
            pyautogui.moveTo(0, 0)
            self.handle_operation.refresh_inspect()
            pyautogui.moveTo(first_ele_position[0], first_ele_position[1])
            time.sleep(0.5)
            if is_doubleClick_for_first_operation:
                pyautogui.doubleClick()
                pyautogui.click()
            else:
                pyautogui.click()
            if is_adjustment:
                time.sleep(0.2)
                pyautogui.press("down")
                time.sleep(0.3)
                pyautogui.press("up")
                time.sleep(0.3)
                self.logger.info("从第一个元素开始查找")

        _destination_file = None
        _destination = 0
        _x, _y = None, None
        if need_before_num is not None:
            for _ in range(need_before_num):
                pyautogui.press("up")
                time.sleep(0.3)
        try:
            for _ in range(1000):
                first_ele_name = self.handle_operation.get_name_from_inspect()
                x, y = self.handle_operation.get_click_position_from_inspect()
                if first_ele_name == destination_file:
                    pyautogui.moveTo(x, y)
                    if is_doubleClick:
                        pyautogui.doubleClick()
                    else:
                        pyautogui.click()
                    select_region = self.handle_operation.get_box_from_inspect()
                    self.logger.info(f"选择{destination_file}选项,{x},{y}", is_mark_region=select_region)
                    _x = x
                    _y = y
                    return _x, _y
                else:
                    if _destination_file != first_ele_name:
                        _destination_file = first_ele_name
                        self.logger.info(f"当前选定文件是{first_ele_name}，目标文件是{destination_file}，不对，选择下一个文件")
                        pyautogui.press(next_element_operation)
                        time.sleep(0.2)
                        _destination = 0
                    else:
                        _destination += 1
                        if _destination >= 5:
                            return _x, _y
                        else:
                            _destination_file = first_ele_name
                            if _destination >= 3:
                                pyautogui.press("down")
                            else:
                                pyautogui.press(next_element_operation)
                            time.sleep(0.2)
        finally:
            if is_need_open_and_closed:
                self.handle_operation.closed_inspect()
            return _x, _y

    def _get_img_obj_from_first_position(self, destination_file, first_ele_position=None,
                                         need_before_num=None, is_need_open_and_closed=True,
                                         next_element_operation="down", is_adjustment=True, is_doubleClick=False):
        x, y = self._select_options_from_path(
            destination_file, first_ele_position=first_ele_position, is_doubleClick=is_doubleClick,
            need_before_num=need_before_num, is_need_open_and_closed=is_need_open_and_closed,
            next_element_operation=next_element_operation, is_adjustment=is_adjustment)
        if x is None or y is None:
            return None
        else:
            with self.handle_operation as ho:
                img_obj = self.create_empty_obj_for_log(position=(x, y))
                img_obj.click()
                img_region = ho.get_box_from_inspect()
                img_obj.update_object(img_region)
            return img_obj

    def _check_ele_in_list(self, first_ele_position=None, destination_list: list = None, is_need_open_and_closed=True,
                           need_before_num=None):
        self.logger.debug("检查需要检索的东西里的东西是不是都包含在list内")
        if is_need_open_and_closed:
            self.handle_operation.start_inspect()
        if first_ele_position:
            pyautogui.moveTo(0, 0)
            self.handle_operation.refresh_inspect()
            pyautogui.moveTo(first_ele_position[0], first_ele_position[1])
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.press("down")
            time.sleep(0.3)
            pyautogui.press("up")
            time.sleep(0.3)
            self.logger.info("从第一个元素开始查找")

        _destination_file = None
        _destination = 0
        _x, _y = None, None
        is_check_succ = False
        if need_before_num is not None:
            for _ in range(need_before_num):
                pyautogui.press("up")
                time.sleep(0.3)
        try:
            for _ in range(1000):
                first_ele_name = self.handle_operation.get_name_from_inspect()
                x, y = self.handle_operation.get_click_position_from_inspect()
                if first_ele_name not in destination_list:
                    pyautogui.moveTo(x, y)
                    pyautogui.click()
                    self.logger.warning(f"{first_ele_name}不在{destination_list}内，检查一下")
                    is_check_succ = False
                    break
                else:
                    if _destination_file != first_ele_name:
                        _destination_file = first_ele_name
                        pyautogui.press("down")
                        time.sleep(0.2)
                        _destination = 0
                    else:
                        _destination += 1
                        if _destination >= 5:
                            is_check_succ = True
                            break
                        else:
                            _destination_file = first_ele_name
                            pyautogui.press("down")
                            time.sleep(0.2)
        finally:
            if is_need_open_and_closed:
                self.handle_operation.closed_inspect()
            return is_check_succ

    def get_string_in_obj(self, obj, focus_x=None, focus_y=None, is_double_click=True, is_get_name_by_tripleClick=False):
        pyperclip.copy('')
        if is_double_click:
            obj.doubleClick(focus_x=focus_x, focus_y=focus_y)
        else:
            obj.click(focus_x=focus_x, focus_y=focus_y)
        if is_get_name_by_tripleClick is True:
            time.sleep(0.5)
            obj.tripleClick(focus_x=focus_x, focus_y=focus_y)
        else:
            obj.hotkey("ctrl", "a")
        obj.hotkey("ctrl", "c")
        text = pyperclip.paste()
        return text

    def get_string_by_tree(self, tree, tree_region=None, offset_x=None, offset_y=None, is_double_click=True,
                           is_get_name_by_tripleClick=False):
        obj = self.create_img_object(tree, parent_region=tree_region)
        focus_x = obj.center_x+offset_x if offset_x is not None else None
        focus_y = obj.center_y+offset_y if offset_y is not None else None
        text = self.get_string_in_obj(obj, focus_x=focus_x, focus_y=focus_y, is_double_click=is_double_click,
                                      is_get_name_by_tripleClick=is_get_name_by_tripleClick)
        return text

    def _try_to_select_box(self, is_select=True, location_element=None, location_element_sreach_region=None,
                           location_offset_x=0, location_offset_y=0, location_focus_x=None, location_focus_y=None,
                           location_region_width=None, location_region_height=None, Box_tree=None, element_is_obj=False,
                           is_check_succ=True, is_try_again=True):
        if element_is_obj is True:
            location_obj = location_element
        else:
            location_obj = self.create_img_object(location_element, parent_region=location_element_sreach_region)
        region_x = location_focus_x if location_focus_x else location_obj.left+location_offset_x
        region_y = location_focus_y if location_focus_y else location_obj.top+location_offset_y
        location_region = (region_x, region_y, location_region_width, location_region_height)
        selectBox = self.create_img_object(Box_tree, parent_region=location_region)
        if selectBox.confidence < 0.8:
            if is_select is True:
                selectBox.click()
        elif selectBox is not None:
            if is_select is False:
                selectBox.click()
        if is_check_succ is True:
            time.sleep(0.5)
            selectBox = self.create_img_object(Box_tree, parent_region=location_region)
            if is_select is True:
                if is_try_again is True and selectBox.confidence < 0.8:
                    self._try_to_select_box(
                        is_select=is_select, location_element=location_element,
                        location_element_sreach_region=location_element_sreach_region,
                        location_offset_x=location_offset_x, location_offset_y=location_offset_y,
                        location_focus_x=location_focus_x, location_focus_y=location_focus_y,
                        location_region_width=location_region_width, location_region_height=location_region_height,
                        Box_tree=Box_tree, element_is_obj=element_is_obj, is_check_succ=is_check_succ,
                        is_try_again=False)
                else:
                    self.assert_True(selectBox.confidence > 0.8, "看样子没有勾选上")
            else:
                if is_try_again is True and selectBox.confidence > 0.8:
                    self._try_to_select_box(
                        is_select=is_select, location_element=location_element,
                        location_element_sreach_region=location_element_sreach_region,
                        location_offset_x=location_offset_x, location_offset_y=location_offset_y,
                        location_focus_x=location_focus_x, location_focus_y=location_focus_y,
                        location_region_width=location_region_width, location_region_height=location_region_height,
                        Box_tree=Box_tree, element_is_obj=element_is_obj, is_check_succ=is_check_succ,
                        is_try_again=False)
                else:
                    self.assert_True(selectBox.confidence < 0.8, "看样子没有取消勾选")

    def _get_position_by_whole_inspect(self, target_name, first_position=None, pre_methods=None, is_assert_got_it=True):
        self.logger.info(f"将选择{target_name}选项")
        target_name = str(target_name)
        with self.handle_operation as ho:
            pyautogui.moveTo(0, 0)
            time.sleep(1)
            pyautogui.moveTo(first_position[0], first_position[1])
            pyautogui.click()
            time.sleep(1)
            if pre_methods is None:
                pyautogui.press("down")
                time.sleep(0.3)
                pyautogui.press("up")
                time.sleep(0.3)
                self.logger.info("从第一个元素开始查找")
            else:
                for pre_method in pre_methods:
                    pre_method()
            _act_get_name = None
            num_of_repeats = 0
            for _ in range(300):
                act_get_name = ho.get_name_from_inspect()
                self.logger.info(f"当前为：{act_get_name}，目标为：{target_name}")
                if act_get_name == target_name:
                    self.logger.info(f"点击{target_name}选项", is_mark_region=ho.get_box_from_inspect())
                    x, y = ho.get_click_position_from_inspect()
                    pyautogui.moveTo(first_position[0], first_position[1])
                    pyautogui.click()
                    break
                else:
                    if act_get_name == _act_get_name:
                        num_of_repeats += 1
                        ho.next_sibling()
                        if num_of_repeats >= 5:
                            x, y = None, None
                            break
                    else:
                        _act_get_name = act_get_name
                        ho.next_sibling()
                        num_of_repeats = 0
            if is_assert_got_it:
                self.assert_True(x is not None and y is not None,
                                 f"期望找的{target_name}，没有找到")

    def input_string_by_cp_to_tree(self, tree, tree_region, string: str=None, offset_x=None, offset_y=None,
                            is_clear_oldstring=True, is_press_enter=False):
        img_obj = self.create_img_object(tree, parent_region=tree_region, do_default_operation=False)
        focus_x = img_obj.center_x if offset_x is None else img_obj.center_x+offset_x
        focus_y = img_obj.center_y if offset_y is None else img_obj.center_y+offset_y
        self.input_string_by_cp_to_obj(obj=img_obj, string=string, focus_x=focus_x, focus_y=focus_y,
                                 is_clear_oldstring=is_clear_oldstring, is_press_enter=is_press_enter)

    def input_string_by_cp_to_obj(self, obj, string,  focus_x=None, focus_y=None, is_clear_oldstring=True,
                                  is_press_enter=False):
        pyperclip.copy(string)
        obj.click(focus_x, focus_y)
        if is_clear_oldstring:
            obj.hotkey("ctrl", "a")
        obj.hotkey("ctrl", "v")
        if is_press_enter:
            obj.press("enter")

    def _assert_input_string_is_same_as_exp_string(self, exp_string: str=None, input_string: str = None, is_exp_succ=True):
        exp_string = exp_string.replace("\r\n", "\n")
        input_string = input_string.replace("\r\n", "\n")
        if is_exp_succ:
            self.assert_True(exp_string == input_string,
                             f"输入文字与预期不符，预期是：{exp_string}, 实际是：{input_string}")
        else:
            self.assert_True(exp_string != input_string,
                             f"输入文字与预期不符，预期是：{exp_string}, 实际是：{input_string}")

    def _add_ImgObj_set(self, *args: list):
        _box_list = []
        for obj_list in args:
            if isinstance(obj_list, list) is False:
                self.raise_err(f"入参错误：【{args}】:【{obj_list}】")
            for img_obj in obj_list:
                _box_list.append(img_obj.region)
        box_list = images_on_screen._find_special_boxs(_box_list)
        ImgObj_list = []
        for obj_list in args:
            for img_obj in obj_list:
                if img_obj.region in box_list and img_obj.region not in ImgObj_list:
                    ImgObj_list.append(img_obj)
        return sorted(ImgObj_list, key=lambda x: (x.top, x.left))

if __name__ == '__main__':
    pyperclip.copy('')
    initial_text = pyperclip.paste()
    print(initial_text)