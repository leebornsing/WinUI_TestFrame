import os.path
import pytest
from common.report_generator import AllureReportApi
from config_lib import Operation_Files_Base
from config_lib.Config_Base import App_Base_Config

allure_data_path = os.path.join(os.path.dirname(__file__), 'allure-results')


if __name__ == '__main__':
    appbase = App_Base_Config()
    appbase.set_config_parm()
    hour = int(appbase.wait_time.split(":")[0])
    minute = int(appbase.wait_time.split(":")[1])
    appbase.wait_to_time(hour, minute)
    # appbase.wait_until_time(hour, minute)
    print('等待完毕，开始执行测试！')
    # 运行测试
    log_path = "../log/log"
    try:
        Operation_Files_Base.delete_files_and_dirs(log_path)
    except:
        pass
    pytest_cmd = [
        "-sv",
    ]
    # test_cases = appbase.running_test_case.replace("\r", "").replace("\n", "").replace(" ", "").replace('"', "").split(",")
    test_case = [
        '../test_case/',
    ]
    pytest_cmd += test_case
    pytest_cmd += ['--alluredir', './allure-results', '--clean-alluredir']
    pytest.main(pytest_cmd)
    # 生成allure测试报告
    report = AllureReportApi(raw_path=allure_data_path)
    report.generate_report(copy_log_path=log_path)

    # # 启动allure报告服务c
    # report.open_allure_server()

    # os.system("shutdown -s -t 60")
