import os
import configparser

path = os.path.split(os.path.realpath(__file__))[0]
ui_config_path = os.path.join(path, '../Conf/UI_config.ini')
ui_config = configparser.ConfigParser()  # 调用外部的读取配置文件的方法
ui_config.read(ui_config_path, encoding='utf-8')

class ReadConfig():

    def get_mspaint_App(self, name):
        value = ui_config.get('mspaint_App', name)
        return value

    def get_Wechat_App(self, name):
        value = ui_config.get('Wechat_App', name)
        return value

    def get_common_config(self, name):
        value = ui_config.get('common_config', name)
        return value

if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
        ...
