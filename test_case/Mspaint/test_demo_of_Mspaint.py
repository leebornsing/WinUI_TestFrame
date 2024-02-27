import sys
import time
import traceback

class Test_case_Demo:
    def test_draw(self, msp):
        test_name = f"{sys._getframe().f_code.co_name}_{int(time.time())}"
        try:
            msp.start(test_name)

            msp.logger.step("预存一下图片位置")
            msp.save_the_picture()

            msp.logger.step("画一个矩形和一个六芒星，把他们中心点用直线连接")
            Rectangle = msp.draw_Rectangle(x=100, y=300, Shape_width=100, Shape_height=100)
            Hexagram = msp.draw_Hexagram(x=400, y=300, Shape_width=100, Shape_height=100)
            Shape_width = Hexagram.center_x - Rectangle.center_x
            Shape_height = Hexagram.center_y - Rectangle.center_y
            StraightLine = msp.draw_StraightLine(x=Rectangle.center_x, y=Rectangle.center_y,
                                                 Shape_width=Shape_width, Shape_height=Shape_height)
        except Exception as e:
            msp.raise_err(traceback.format_exc())

    def test_rotate(self, msp):
        test_name = f"{sys._getframe().f_code.co_name}_{int(time.time())}"
        try:
            msp.start(test_name)

            msp.logger.step("预存一下图片位置")
            msp.save_the_picture()

            msp.logger.step("画一个矩形和一个六芒星")
            Rectangle = msp.draw_Rectangle(x=100, y=300, Shape_width=100, Shape_height=100)
            Hexagram = msp.draw_Hexagram(x=400, y=300, Shape_width=100, Shape_height=100)

            msp.logger.step("选择[向左旋转 90 度]旋转方式")
            msp.Rotate_the_current_Canvas(rotate_mode="向左旋转 90 度")

            msp.logger.step("选择[向左旋转 90 度]旋转方式")
            msp.Rotate_the_current_Canvas(rotate_mode="垂直翻转")
        except Exception as e:
            msp.raise_err(traceback.format_exc())

    def test_send_123(self, wx):
        test_name = f"{sys._getframe().f_code.co_name}_{int(time.time())}"
        try:
            wx.start(test_name)

            wx.logger.step("给文件传输助手发送123")
            wx.select_wechat_user("文件传输助手")
            wx.send_something(string="123")

        except Exception as e:
            wx.raise_err(traceback.format_exc())

    def test_send_pic_to_wx_form_msp(self, msp, wx):
        test_name = f"{sys._getframe().f_code.co_name}_{int(time.time())}"
        try:
            msp.start(test_name)
            msp.logger.step("预存一下图片位置")
            msp.save_the_picture()

            msp.logger.step("画一个矩形和一个六芒星，把他们中心点用直线连接")
            Rectangle = msp.draw_Rectangle(x=100, y=300, Shape_width=100, Shape_height=100)
            Hexagram = msp.draw_Hexagram(x=400, y=300, Shape_width=100, Shape_height=100)
            Shape_width = Hexagram.center_x - Rectangle.center_x
            Shape_height = Hexagram.center_y - Rectangle.center_y
            StraightLine = msp.draw_StraightLine(x=Rectangle.center_x, y=Rectangle.center_y,
                                                 Shape_width=Shape_width, Shape_height=Shape_height)
            wx.start("test_rotate")

            wx.logger.step("选择到文件传输助手")
            wx.select_wechat_user("文件传输助手")

            wx.logger.step("复制画布的图像，通过wx发送")
            msp.copy_canvas_to_clipboard()
            wx.appbase.start_application(product=wx.appbase.wx_handlen_name)
            wx.send_something(is_use_clipboard=True)

        except Exception as e:
            wx.raise_err(traceback.format_exc())