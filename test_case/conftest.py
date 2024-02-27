import allure
import pytest
import pyautogui
import shutil
import os
# from common.Logs import Log
from config_lib.Draw_Operation import Mspaint_Operation
from config_lib.UIautomation_Base import Handle_Operation
from config_lib import images_on_screen, Operation_Files_Base
from config_lib.Wechat_Operation import Wechat_Operation

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
# logger = Log(__name__).logger
LOG_PATH = os.path.dirname(os.path.dirname(__file__)).replace("/", "\\")
compini = True

def pre_for_test():
    global compini
    if compini:
        Operation_Files_Base.clean_cache_png()
        log_path = os.path.join(ROOT_PATH, "/log")
        logger_path = os.path.join(log_path, "/log")
        cache_path = os.path.join(ROOT_PATH, "/cache")
        Operation_Files_Base.try_to_mkdir(log_path)
        Operation_Files_Base.try_to_mkdir(logger_path)
        Operation_Files_Base.try_to_mkdir(cache_path)
        compini = False

def aft_for_test():
    pass

@pytest.fixture(scope="session", autouse=True)
def msp():
    # 配置Artstudio基础界面
    msp = Mspaint_Operation()
    pre_for_test()
    yield msp
    aft_for_test()

@pytest.fixture(scope="session", autouse=True)
def wx():
    # 配置Artstudio基础界面
    wx = Wechat_Operation()
    pre_for_test()
    yield wx
    aft_for_test()

def pre_for_funtest():
    pass

def aft_for_funtest(app, is_close_inspect=False):
    if is_close_inspect is False:
        try:
            handle_operation = Handle_Operation()
            handle_operation.closed_inspect()
        except:
            pass
    try:
        app.logger.end()
        test_case_path = app.logger.log_dir_path
        path = app.logger.log_file_path

        allure.dynamic.link(f"http://localhost:63342/{os.path.basename(ROOT_PATH)}/test_pytest/allure-reports" + path.split(LOG_PATH)[-1],
                            app.logger.testcase_name)
        shutil.copytree(test_case_path, f"{LOG_PATH}/log/log/" + app.logger.log_dir_name)
    except:
        # debug时候这里会失败，此仅在正式使用时调用
        pass

@pytest.fixture(scope="function", autouse=True)
def init_base_env(msp):
    pre_for_funtest()
    yield
    aft_for_funtest(msp)





if __name__ == '__main__':
    print(os.path.basename(ROOT_PATH))
