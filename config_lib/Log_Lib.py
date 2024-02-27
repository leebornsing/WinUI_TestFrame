import logging
import time
import os
import pytest

from config_lib import images_on_screen

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class TestLogger:
    def __init__(self):
        self.is_start = False
        super().__init__()

    def start(self, testcase_name="test"):
        self.testcase_name = testcase_name
        self.step_count = 0
        self.logger = logging.getLogger(testcase_name)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        self.log_dir_name = f"{time.strftime('%Y%m%d%H%M%S')}_{testcase_name}"
        self.log_dir_path = os.path.join(ROOT_PATH, f"log/{self.log_dir_name}")
        self.log_file_name = f"{testcase_name}_{time.strftime('%Y%m%d%H%M%S')}.html"
        self.log_file_path = os.path.join(self.log_dir_path, self.log_file_name)
        os.mkdir(self.log_dir_path)
        self.handler = logging.FileHandler(f"{self.log_file_path}", mode="w", encoding="utf-8")
        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        self.handler.stream.write("<meta charset='utf-8'><html><head><title>Test Results</title></head><body><table border='1'><tr><th>Step</th><th>Step_Name</th><th>Success</th></tr>")
        self.is_start = True

    def _write_step(self, content, success=True):
        self.step_count += 1
        self.step_name = "Step_" + str(self.step_count)
        self.step_content = content
        _is_success = "</a></td><td style='color:green;'>PASS</td></tr>" if success else "</a></td><td style='color:red;'>FAIL</td></tr>"
        step_file_name = f"{self.testcase_name}_step{self.step_count}.html"
        self.steplog_file_path = os.path.join(ROOT_PATH, "log", self.log_dir_name, step_file_name)

        self.handler.stream.write(f"<tr><td>{self.step_name}</td><td><a href='{step_file_name}'>{self.step_content}{_is_success}")
        self.handler.flush()

        self.step_file_path = os.path.join(self.log_dir_path, step_file_name)
        self.step_handler = logging.FileHandler(self.step_file_path, mode="w", encoding="utf-8")
        self.step_handler.setLevel(logging.INFO)

        self.logger.addHandler(self.step_handler)
        log_file_path = self.testcase_name
        parent_page = f"<br><a href='{self.log_file_name}'>用例步骤</a>"
        if int(self.step_count - 1) > 0:
            last_page_path = f"{self.testcase_name}_step{self.step_count-1}.html"
            last_page = f"<br><a href='{last_page_path}'>上一步骤</a>"
        else:
            last_page = "<br>"
        next_page_path = f"{self.testcase_name}_step{self.step_count + 1}.html"
        next_page = f"<br><a href='{next_page_path}'>下一步骤</a>"
        step_page_name = f"<br><a style='text-align:center;font-size:20px;font-weight:bold;'>{content}</a>"
        self.step_handler.stream.write(
            f"<meta charset='utf-8'><html><head><title>Step Results</title></head><body>{parent_page}{last_page}{next_page}{step_page_name}<br><table border='1'><tr><th>Time</th><th>Level</th><th>Operation</th><th>messege</th><th>Result</th><th>Log</th></tr>")

        self.step_handler.stream.write("</table></body></html>")
        self.step_handler.flush()
        self.logger.removeHandler(self.step_handler)

    def _write_step_log(self, level, message, success=True, Operation=None, image_path=None):
        string_to_remove = "</table></body></html>"
        # 打开文件，读取内容
        with open(self.step_file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
        # 删除指定字符串
        content = [line.replace(string_to_remove, "") for line in content]
        # 写入文件
        with open(self.step_file_path, "w", encoding="utf-8") as file:
            file.writelines(content)
        image_name = os.path.basename(image_path)
        image_table = f"<td><a href='{image_name}' target='_blank'>Img Log</a></td>" if image_name else "<td><a>None log Img</a></td>"
        execution_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        font_color = 'blue' if level == 'info' else 'green' if level == 'debug' else 'red'
        is_success = "<td style=\"color:green;\">PASS</td>" if success else "<td style=\"color:red;\">FAIL</td>"
        self.step_handler.stream.write(f"<tr><td>{execution_time}</td><td style=\"color:{font_color};\">{level.upper()}</td><td>{Operation}</td><td>{message}{is_success}{image_table}</tr>")
        self.step_handler.stream.write("</table></body></html>")
        self.step_handler.flush()
        self.logger.removeHandler(self.step_handler)

    def generate_html(self, dir_path):

        # 获取文件夹中的所有图片路径
        img_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.jpg') or f.endswith('.png')]

        # 对图片路径进行排序
        img_paths.sort()

        # 生成图片链接列表
        img_links = []
        for img_path in img_paths:
            img_name = os.path.basename(img_path)
            img_link = f'<a href="{img_name}.html">{img_name}</a>'
            img_links.append(img_link)

            # 生成图片对应的HTML文件
            with open(f'{img_name}.html', 'w') as f:
                f.write(f'<img src="{img_path}" style="width: 90%;" /><br>')
                f.write('<button onclick="window.location.href=\'{}\';">Previous</button>'.format(img_links[-2] + '.html') if len(
                    img_links) > 1 else '')
                f.write('<button onclick="window.location.href=\'{}\';">Next</button>'.format(img_links[0] + '.html') if len(
                    img_links) > 1 else '')
                f.write('<button onclick="window.location.href=\'index.html\';">Back to Index</button>')

        # 生成索引HTML文件
        with open('index.html', 'w') as f:
            f.write('<br>'.join(img_links))

    def info(self, message, success=True, Operation='None Operation', is_mark_region=None):
        if self.is_start is False:
            self.start()
            self.step()
        image_path = images_on_screen.log_screen_and_mark(self.log_dir_path, is_mark_region=is_mark_region).split(os.path.join(ROOT_PATH, 'log'))[-1]
        self._write_step_log("info", message, success, Operation=Operation, image_path=image_path)

    def debug(self, message, success=True, Operation='None Operation', is_mark_region=None):
        if self.is_start is False:
            self.start()
            self.step()
        image_path = images_on_screen.log_screen_and_mark(self.log_dir_path, is_mark_region=is_mark_region).split(os.path.join(ROOT_PATH, 'log'))[-1]
        self._write_step_log("debug", message, success, Operation=Operation, image_path=image_path)

    def warning(self, message, success=True, Operation='None Operation', is_mark_region=None):
        if self.is_start is False:
            self.start()
            self.step()
        image_path = images_on_screen.log_screen_and_mark(self.log_dir_path, is_mark_region=is_mark_region).split(os.path.join(ROOT_PATH, 'log'))[-1]
        self._write_step_log("warning", message, success, Operation=Operation, image_path=image_path)
        if success == False:
            self.set_step_fail()

    def error(self, message, success=False, Operation='None Operation', is_mark_region=None):
        if self.is_start is False:
            self.start()
            self.step()
        image_path = images_on_screen.log_screen_and_mark(self.log_dir_path, is_mark_region=is_mark_region).split(os.path.join(ROOT_PATH, 'log'))[-1]
        self._write_step_log("error", message, success, Operation=Operation, image_path=image_path)
        if success == False:
            self.set_step_fail()

    def step(self, content="test", success=True):
        self._write_step(content, success)

    def end(self):
        self.handler.stream.write("</table></body></html>")
        self.handler.flush()
        self.handler.close()

    def set_step_fail(self):
        filepath = self.log_file_path
        set_fail_str = f"<td style='color:red;'>FAIL</td></tr>"
        step_file_name = f"{self.testcase_name}_step{self.step_count}.html"
        begin_str = f"<tr><td>{self.step_name}</td><td><a href='{step_file_name}'>{self.step_content}</a></td>"
        end_str = "<td style='color:green;'>PASS</td></tr>"
        with open(filepath, 'r', encoding="utf-8") as file:
            file_content = file.read()
        old_str = begin_str + end_str
        new_str = begin_str + set_fail_str
        file_content = file_content.replace(old_str, new_str)
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(file_content)


if __name__ == '__main__':
    logger = TestLogger()
    # logger.start("testcase1")
    # logger.step("Step a")
    logger.info("Info message0")
    logger.info("Info message1")

    logger.step("Step b")
    logger.warning("warning message")
    for i in range(5):
        logger.info("Info message{}".format(str(i)))

    logger.step("as撒旦hdsdffdsasfdafdasgadsfa")
    logger.error("Error message")

    logger.step("as撒旦hdsfa")
    logger.warning("warning message")
    logger.end()
    # logger.generate_html("D:\\PythonProject\\Artsudio\\UI_auto\\log\\20230605165420_test_VerificationPlan")


