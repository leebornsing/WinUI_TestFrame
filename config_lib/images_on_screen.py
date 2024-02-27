import time, os
import cv2
import numpy as np
import pyautogui
import pyperclip
import pytesseract
from PIL import ImageGrab, ImageDraw, Image, ImageEnhance, ImageFilter

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def find_images_on_screen(img_path, search_region=None, confidence: float = 0.8, search_wait_interval: float = 0.1):
    box = []
    object_uniqueness = None
    img_path = img_path.replace('/', '\\')
    confidence = 0.9
    _confidence = confidence
    if search_region is not None:
        search_region = list(search_region)
        _search_region = []
        for search_value in search_region:
            search_value = 0 if search_value < 0 else search_value
            _search_region.append(search_value)
        search_region = tuple(_search_region)
    for cycle_num in range(10):
        confidence = _confidence
        if box == [] or object_uniqueness is None:
            box, object_uniqueness = _pyautogui_default_algorithm(
                image_path=img_path, search_region=search_region, confidence=confidence)
            if box == [] or object_uniqueness is None:
                # box, object_uniqueness = __gray_binarization_algorithm(
                #     image_path=img_path, search_region=search_region, confidence=confidence)
                time.sleep(search_wait_interval*(cycle_num+1))
            _confidence = (10-cycle_num)*0.1
        elif (box != [] or object_uniqueness is not None) and confidence >= 0.6:
            return box, object_uniqueness, confidence
        elif confidence >= 0.6 and len(box) == 1 and object_uniqueness is True:
            return box[0], object_uniqueness, confidence
        if confidence < 0.6:
            raise Exception("confidence太低了,在{}内找不到{}".format(search_region, os.path.split(img_path)[-1]))
        time.sleep(search_wait_interval)
    raise Exception("查询{}时，出现意外错误： \nbox:{}; \nobject_uniqueness:{}; \nconfidence:{}".format(img_path, box, object_uniqueness, confidence))

def __gray_binarization_algorithm(image_path, search_region=None, confidence=0.8):
    # 读取图像并将其转化为OpenCV可以处理的格式
    image_cv = cv2.imread(image_path)

    # 将图片转换为灰度图并进行二值化
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # 在屏幕截图中找到图片
    screen = pyautogui.screenshot()
    # 裁剪对应大小
    if search_region is not None:
        # 转换区域值
        real_region = (search_region[0], search_region[1],
                       search_region[2]+search_region[0], search_region[3]+search_region[1],)
        screen = screen.crop(real_region)
    screen_cv = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen_cv_gary = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
    _, screen_cv = cv2.threshold(screen_cv_gary, 127, 255, cv2.THRESH_BINARY)

    # 同一图片类型
    threshold_image = threshold_image.astype('float32')
    screen_cv = screen_cv.astype('float32')

    # 进行模板匹配
    result = cv2.matchTemplate(screen_cv, threshold_image, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= confidence)
    locations = list(zip(*locations[::-1]))
    if not locations:
        return [], None

    # 返回目标位置和数量
    boxes = []
    for loc in locations:
        boxes.append([loc[0], loc[1], image_cv.shape[1], image_cv.shape[0]])
    object_uniqueness = True if len(boxes) == 1 else False

    return boxes, object_uniqueness

def _pyautogui_default_algorithm(image_path, search_region, confidence, grayscale=True):
    search_region = tuple(search_region)
    img_box_list = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence,
                                                    grayscale=grayscale, region=search_region))
    if len(img_box_list) == 0:
        return [], None
    else:
        really_box_list = _find_special_boxs(img_box_list)
        if len(really_box_list) == 1:
            object_uniqueness = True
        elif len(really_box_list) == 0:
            raise Exception("一个都没返回？不可能")
        else:
            object_uniqueness = False
        return img_box_list, object_uniqueness

# def _find_special_box(box_list):
#     box_list = _find_special_boxs(box_list)
#     box_num = len(box_list)
#     for _ in range(10):
#         box_list = _find_special_boxs(box_list)
#         if box_num == len(box_list):
#             return box_list
#         box_num = len(box_list)
#     return []
#
# def _find_special_boxs(box_list):
#     for box1 in box_list:
#         for box2 in box_list:
#             if _is_box_similar(box1, box2) and box1 != box2:
#                 box_list.pop(box_list.index(box2))
#     return box_list

def _find_special_boxs(box_list):
    l = len(box_list)
    for i in range(l):
        for n in range(i + 1, l):
            if _is_box_similar(box_list[n], box_list[i]) and box_list[n] != box_list[i]:
                box_list.pop(n)
                return _find_special_boxs(box_list)
    return box_list

def _is_box_similar(box1, box2):
    if abs(box1[0] - box2[0]) <= 10 and abs(box1[1] - box2[1]) <= 10:
        return True
    else:
        return False

def screenshot_to_cache(region, cache_file_name=None):
    cache_file_name = cache_file_name if cache_file_name else "screenshot_{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    screenshot = pyautogui.screenshot(region=region)
    # 将截图保存到本地
    screenshot_path = os.path.join(ROOT_PATH, 'cache/{}.png'.format(cache_file_name))
    screenshot.save(screenshot_path)
    return screenshot_path

def get_str_in_img(file_path, is_use_opencv=False, contrast_ratio=False):
    # 读取图像并将其转化为OpenCV可以处理的格式
    if is_use_opencv:
        file_path = cv2.imread(file_path)

    # 增加对比度算法
    if contrast_ratio:
        image = Image.open(file_path)
        # 图片预处理
        image = image.convert('L')
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.filter(ImageFilter.MedianFilter())
        # 多次识别
        for i in range(3):
            text = pytesseract.image_to_string(image, lang='chi_sim')
            if len(text) != 0:
                return text
            image = image.filter(ImageFilter.SHARPEN)

    text = pytesseract.image_to_string(file_path, lang='chi_sim')
    return text

def assert_str_in_img(string, file_path, str_not_in_img=True):
    r"""
    断言str是否在img中，此方法断言无法严谨对待Cc\Pp等大小写类似字符串，也需要尽可能减少特殊字符串的存在
    :param string:
    :param file_path:
    :param err_msg:
    :param str_not_in_img: 默认True，如果False则断言str不在IMG内
    :return:
    """
    text1 = get_str_in_img(file_path=file_path)
    text2 = get_str_in_img(file_path=file_path, is_use_opencv=True)
    text3 = get_str_in_img(file_path=file_path, contrast_ratio=True)
    if str_not_in_img is True:
        assert string in text1 or string in text2 or string in text3, "图片识别不到该字符串"
    elif str_not_in_img is False:
        assert string not in text1 and string not in text2 and string in text3, "图片中有该字符串"
    else:
        raise Exception("未知错误，str_not_in_img可能传入了非BOOL")

def log_screen_and_mark(save_path=None, is_mark_region=None):
    file_name = "screenshot_{}.png".format(int(time.time()))
    file_path = os.path.join(save_path, file_name)
    if is_mark_region is None or isinstance(is_mark_region, tuple):
        capture_and_mark_region(save_path=file_path, is_mark_region=is_mark_region)
    else:
        capture_and_mark_regions(save_path=file_path, regions=is_mark_region)
    return file_path

def capture_and_mark_region(save_path=None, is_mark_region=None):
    """
    标记屏幕上的鼠标位置及指定区域,并保存至指定目录下
    :param save_path: 图片存储路径:目录路径
    :param is_mark_region: 不传则不框出区域, 传元组(left, top, width, height)
    :return:
    """
    # 检查is_mark_region是否为None或元组格式
    if is_mark_region is not None and not isinstance(is_mark_region, tuple):
        raise TypeError("is_mark_region must be None or a tuple (left, top, width, height)")

    # 截取屏幕并将其转换为Pillow Image对象
    screenshot = ImageGrab.grab()

    # 获取鼠标位置
    mouse_x, mouse_y = pyautogui.position()

    # 在屏幕上标记鼠标位置
    draw = ImageDraw.Draw(screenshot)
    draw.ellipse((mouse_x - 2, mouse_y - 2, mouse_x + 2, mouse_y + 2), fill=(255, 0, 0))

    # 如果is_mark_region不为None，则在截图上框出指定区域
    if is_mark_region is not None:
        left, top, width, height = is_mark_region
        draw.rectangle((left, top, left + width, top + height), outline=(255, 0, 0))

    # 保存标记后的屏幕截图
    screenshot.save(save_path)

def capture_and_mark_regions(save_path, regions):
    # 截取当前屏幕截图
    screenshot = pyautogui.screenshot()

    # 创建一个可编辑的图像对象
    image = Image.new('RGB', screenshot.size)
    image.paste(screenshot)

    # 创建一个可绘制的对象
    draw = ImageDraw.Draw(image)

    # 标记传入的每个区域
    for region in regions:
        left, top, width, height = region
        right = left + width
        bottom = top + height
        # 绘制红色边框
        draw.rectangle([(left, top), (right, bottom)], outline='red')
    # 保存图像到指定路径
    image.save(save_path)

def get_text_position(text, region):
    """
    在指定区域内查找字符串的位置。
    :param text: 要查找的字符串。
    :param region: 指定的区域，格式为(left, top, width, height)。
    :return: 如果找到了字符串，返回字符串中心的坐标位置；否则返回None。
    """
    x, y, w, h = region
    screenshot = ImageGrab.grab(bbox=region)
    texts = pytesseract.image_to_string(screenshot,  lang='chi_sim')
    print(texts)
    if text in texts:
        center_x = texts.index(text) + len(text) // 2
        center_y = int(texts.count('\n', 0, texts.index(text)) + 0.5)
        return (x + center_x, y + center_y)
    else:
        return None

def search_blank_piont(x, y, width, height, blank_region_w=225, blank_region_h=125, offset_x=20, offset_y=20):
    """
    寻找A区域内是否有一个空白区域B，返回B区域的left+20, top+20
    :param x: A区域的left坐标
    :param y: A区域的top坐标
    :param width: A区域的宽度
    :param height: A区域的高度
    :param blank_region_w: 需要空白区域的宽
    :param blank_region_h:  需要空白区域的高
    :return:
    """
    screenshot = np.array(pyautogui.screenshot())
    region = screenshot[y:y + height, x:x + width, :]
    white_pixels = np.where(np.all(region == [255, 255, 255], axis=-1))
    for i, j in zip(white_pixels[1], white_pixels[0]):
        if i + blank_region_w < width and j + blank_region_h < height and np.all(region[j:j + blank_region_h, i:i + blank_region_w, :] == [255, 255, 255]):
            return (i + x + offset_x, j + y + offset_y)
    return None

def is_overlap(region1, region2):
    """
    判断两个region是否有重叠的部分
    :param region1: tuple, (left, top, width, height)
    :param region2: tuple, (left, top, width, height)
    :return: bool
    """
    x1, y1, w1, h1 = region1
    x2, y2, w2, h2 = region2
    if x1 + w1 >= x2 and y1 + h1 >= y2 and x1 <= x2 and y1 <= y2:
        return True
    elif x1 + w1 >= x2 + w2 and y1 + h1 >= y2 and x1 <= x2 + w2 and y1 <= y2:
        return True
    elif x1 + w1 >= x2 and y1 + h1 >= y2 + h2 and x1 <= x2 and y1 <= y2 + h2:
        return True
    elif x1 + w1 >= x2 + w2 and y1 + h1 >= y2 + h2 and x1 <= x2 + w2 and y1 <= y2 + h2:
        return True
    else:
        return False

def white_percentage(region):
    """
    判断给定区域纯白色的百分比
    :param region:
    :return:
    """
    # 获取屏幕截图
    screen = ImageGrab.grab()

    # 获取指定区域的截图
    left, top, width, height = region
    box = (left, top, left+width, top+height)
    img = screen.crop(box)

    # 将截图转为灰度图
    gray_img = img.convert('L')

    # 统计白色像素点数量
    white_pixels = 0
    for pixel in gray_img.getdata():
        if pixel == 255:
            white_pixels += 1

    # 计算白色像素点所占比例
    total_pixels = width * height
    white_percentage = white_pixels / total_pixels

    return white_percentage

def get_input_language(input_str):
    # 获取当前窗口句柄
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(input_str)
    pyautogui.click()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    text = pyperclip.paste()
    if input_str == text:
        return "eng"
    elif input_str.upper() == text:
        return "ENG"
    else:
        return "CN"

def config_input_methods(now_input_method="eng", exp_input_method="eng"):
    # 定义输入法状态之间的转换关系
    mappings = {
        "eng": {"eng": [], "CN": ["shift"], "ENG": ["capslock"]},
        "CN": {"eng": ["shift"], "CN": [], "ENG": ["capslock", "shift"]},
        "ENG": {"eng": ["capslock"], "CN": ["shift", "capslock"], "ENG": []}
    }
    # 根据输入法状态之间的转换关系，按下对应的按键
    for key in mappings[now_input_method][exp_input_method]:
        pyautogui.press(key)
    lang = get_input_language("asd13456")
    if lang == exp_input_method:
        return True
    elif lang != exp_input_method and (lang != "ENG" or exp_input_method != "ENG"):
        return False
    else:
        config_input_methods(now_input_method=lang, exp_input_method=exp_input_method)

def detect_lines_on_region(region):
    # 获取屏幕截图
    screen_image = ImageGrab.grab()
    # 转为OpenCV格式
    screen_image = np.array(screen_image)
    screen_image = screen_image[:, :, ::-1].copy()
    # 获取区域
    left, top, width, height = region
    region_image = screen_image[top:top+height, left:left+width]
    # 转为灰度图
    gray = cv2.cvtColor(region_image, cv2.COLOR_BGR2GRAY)
    # 边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # 检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is None:
        return []
    # 计算直线的起始坐标、中点坐标、终点坐标
    result = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        start_point = (left+x1, top+y1)
        end_point = (left+x2, top+y2)
        mid_point = ((start_point[0]+end_point[0])//2, (start_point[1]+end_point[1])//2)
        if is_point_in_region(region, start_point) and is_point_in_region(region, end_point) and is_point_in_region(region, mid_point):
            result.append((start_point, mid_point, end_point))
    return result

def is_point_in_region(region, point):
    """
    判断一个点坐标是否在屏幕上的一个区域内
    :param region:
    :param point:
    :return:
    """
    left, top, width, height = region
    x, y = point
    if left <= x <= left+width and top <= y <= top+height:
        return True
    else:
        return False

def is_right_pixel(x, y, exp_pixel):
    # 获取指定坐标点的像素颜色
    pixel = get_pixel(x, y)
    # 判断是否为期望颜色
    if pixel == exp_pixel:
        return True
    else:
        return False

def get_pixel(x, y):
    """
    获取一个点坐标的像素颜色（返回RGB值）
    :param x:
    :param y:
    :return:
    """
    # 打开当前屏幕截图
    screen_image = ImageGrab.grab()
    # 获取指定坐标点的像素颜色
    pixel = screen_image.getpixel((x, y))
    return pixel

def is_similar_pixel(pixel1, pixel2, similarity=0.95):
    deviation_value = int((1-float(similarity))*255)
    if abs(pixel1[0]-pixel2[0]) < deviation_value:
        if abs(pixel1[1] - pixel2[1]) < deviation_value:
            if abs(pixel1[2] - pixel2[2]) < deviation_value:
                return True
    return False

def get_line_between_Two_regions(region1, region2):
    """
    获取两个区域间所夹的所有线
    :param region1:
    :param region2:
    :return:
    """
    # region1 = (region1[0]-10, region1[1]-10, region1[2]+20, region1[3]+20)
    # region2 = (region2[0]-20, region2[1]-20, region2[2]+40, region2[3]+40)
    # region_all_x = min(region1[0], region2[0])
    # region_all_y = min(region1[1], region2[1])
    # region_all_width = max(region1[0]+region1[2], region2[0]+region2[2])
    # region_all_height = max(region1[1]+region1[3], region2[1]+region2[3])
    # region_all = (region_all_x, region_all_y, region_all_width, region_all_height)
    region_all = get_region_between_Two_regions(region1, region2)
    lines_list = detect_lines_on_region(region_all)
    get_line_list = []
    for line in lines_list:
        if is_point_in_region(region1, line[0]):
            if is_point_in_region(region2, line[2]):
                get_line_list.append(line)
        if is_point_in_region(region1, line[2]):
            if is_point_in_region(region2, line[0]):
                get_line_list.append(line)
    return get_line_list

def get_region_between_Two_regions(region1, region2):
    _x = min(region1[0], region2[0])
    if _x == region1[0]:
        x = min(region1[0]+region1[2], region2[0])
        x_width = abs(region1[0] + region1[2] - region2[0])
    else:
        x = min(region1[0], region2[0]+region2[2])
        x_width = abs(region2[0] + region2[2] - region1[0])

    _y = min(region1[1], region2[1])
    if _y == region1[1]:
        y = min(region1[1]+region1[3], region2[1])
        y_height = abs(region1[1] + region1[3] - region2[1])
    else:
        y = min(region1[1], region2[1]+region2[3])
        y_height = abs(region2[1] + region2[3] - region1[1])
    return (x, y, x_width, y_height)

def get_color_lines_on_region(region, exp_pixel):
    lines_list = detect_lines_on_region(region)
    color_lines_list = []
    for line in lines_list:
        if is_right_pixel(line[0][0], line[0][1], exp_pixel) or is_right_pixel(line[1][0], line[1][1], exp_pixel) or is_right_pixel(line[2][0], line[2][1], exp_pixel):
            color_lines_list.append(line)
    return color_lines_list

def is_rgb_similar(a, b):
    """
    判断RGB颜色a是否与颜色b相似，如果相似度在10%内则返回True，否则返回False。
    """
    # 计算RGB颜色a和b的三个通道的差值
    diff_r = abs(a[0] - b[0])
    diff_g = abs(a[1] - b[1])
    diff_b = abs(a[2] - b[2])

    # 计算RGB颜色a和b的三个通道的平均值
    avg_r = (a[0] + b[0]) / 2
    avg_g = (a[1] + b[1]) / 2
    avg_b = (a[2] + b[2]) / 2

    # 计算RGB颜色a和b的三个通道的相对差值
    rel_diff_r = _get_relative_difference(a[0], diff_r, avg_r)
    rel_diff_g = _get_relative_difference(a[1], diff_g, avg_g)
    rel_diff_b = _get_relative_difference(a[2], diff_b, avg_b)

    # 判断RGB颜色a和b的相似度是否在10%内
    if rel_diff_r <= 0.1 and rel_diff_g <= 0.1 and rel_diff_b <= 0.1:
        return True
    else:
        return False

def _get_relative_difference(rgb, diff, avg):
    if avg == 0:
        if rgb-avg <= 25:
            rel_diff = 0.1
        else:
            rel_diff = 2
    else:
        rel_diff = diff / avg
    return rel_diff

def get_color_in_region(region):
    left, top, width, height = region
    color_list = []
    for increase_x in range(width):
        for increase_y in range(height):
            pixel = get_pixel(left+increase_x, top+increase_y)
            color_list.append(pixel)
    color_set = set(color_list)
    return list(color_set)

def is_the_color_in_color_list(color, color_list):
    for colour in color_list:
        if colour == color or is_rgb_similar(colour, color):
            return True
    return False

def is_pixel_in_region(pixel, region, step_length=1):
    left, top, width, height = region
    for w in range(width//step_length):
        for h in range(height//step_length):
            color = get_pixel(left + w*step_length, top + h*step_length)
            is_similar = is_rgb_similar(color, pixel)
            if is_similar:
                return True
    return False

def get_first_color_in_region(color, region):
    left, top, width, height = region
    for increase_x in range(width):
        for increase_y in range(height):
            pixel = get_pixel(left+increase_x, top+increase_y)
            if color == pixel:
                return increase_x, increase_y
    return None, None

def get_last_color_in_region(color, region):
    left, top, width, height = region
    # 获取屏幕截图
    screen = ImageGrab.grab()
    pixels = list(screen.crop((left, top, left + width, top + height)).getdata())
    if color in pixels:
        for i, p in enumerate(pixels):
            if p == color:
                x = i % width
                y = i // width
                return left + x, top + y
    else:
        return None, None

def judge_area_bearing(start_region, end_region):
    if start_region[0] < end_region[0] and start_region[0]+start_region[2] < end_region[0]:
        x_opsition = "right" # 在右边
    elif end_region[0] < start_region[0] and end_region[0]+end_region[2] < start_region[0]:
        x_opsition = "left"
    else:
        x_opsition = "mid"

    if start_region[1] < end_region[1] and start_region[1]+start_region[3] < end_region[1]:
        y_opsition = "bottom"
    elif end_region[1] < start_region[1] and end_region[1]+end_region[3] < start_region[1]:
        y_opsition = "top"
    else:
        y_opsition = "mid"
    return x_opsition, y_opsition



if __name__ == '__main__':

    a = get_pixel(1204,289)
    b = get_pixel(1033,384)
    c = get_pixel(1043,387)
    print(a ,b, c)
