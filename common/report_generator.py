import json
import os
import shutil
import socket
import zipfile


# 设置保留报告历史数据数量，仅保留基本数据
HISTORY_NUMBER = 30


class AllureReportApi:

    def __init__(self, raw_path, port=63342):
        self.report_server_ip = socket.gethostbyname((socket.gethostname()))   # 获取本地ip地址
        self.report_server_port = port
        self.report_url = 'http://{}:{}/index.html'.format(self.report_server_ip, self.report_server_port)
        self.raw_path = raw_path
        self.report_path = os.path.join(os.path.dirname(self.raw_path), 'allure-reports')

    def generate_report(self, clean=True, copy_log_path=None):
        """
        生成allure测试报告（报告路径存放在与源数据同级下名为allure-reports的文件夹下），并开启本地报告渲染（开启后可通过地址查看报告）
        :param clean: 是否清理历史数据，默认每次清理
        :param copy_log_path: 是否清理历史数据，默认每次清理
        :return:
        """
        # 获取历史数据
        history_path = os.path.join(self.report_path, 'history/history-trend.json')
        history_trend_data = []
        try:
            history_trend_data = self.read_json_data(history_path)
        except Exception as e:
            print(e)
        # 保留最近N次记录
        if len(history_trend_data) > HISTORY_NUMBER:
            index = -HISTORY_NUMBER
            history_trend_data = history_trend_data[index:]
        # 生成allure报告
        command_line = 'allure generate {raw_data_path} -o {report_path}'.format(raw_data_path=self.raw_path,
                                                                                 report_path=self.report_path)
        if clean:
            command_line += ' --clean'
        os.system(command_line)
        if os.path.exists(copy_log_path):
            shutil.move(copy_log_path, self.report_path)
        # 更新历史数据
        if history_trend_data:
            current_data = self.read_json_data(history_path)  # 获取当前数据
            history_trend_data.insert(0, current_data[0])  # 将当前数据添加到历史数据
            with open(history_path, 'a', encoding='utf-8') as sfp:
                # 清空
                sfp.seek(0)
                sfp.truncate()
                # 重新写入历史数据
                sfp.write(json.dumps(history_trend_data))
            sfp.close()


    def open_allure_server(self):
        """开启本地报告渲染，类实例设置本地ip地址以供其他端访问"""
        command_line = 'allure serve {raw_data_path} -o {report_path}'.format(raw_data_path=self.raw_path,
                                                                              report_path=self.report_path)
        command_line += ' -h {} -p {}'.format(self.report_server_ip, self.report_server_port)
        os.system(command_line)

    @staticmethod
    def read_json_data(json_path):
        """读取allure报告summary文件，返回报告字典"""
        summary_file_path = os.path.join(json_path)
        with open(summary_file_path, 'r', encoding='utf-8') as sfp:
            data = json.load(sfp)
        sfp.close()
        return data


    def get_fail_testcase_log(self):
        json_path = os.path.join(self.report_path, 'widgets/severity.json')
        test_cases_dir_path = os.path.join(self.report_path, 'data/test-cases')
        os.path.join(self.report_path, 'widgets/summary.json')
        summary_file_path = os.path.join(json_path)
        with open(summary_file_path, 'r', encoding='utf-8') as sfp:
            datas = json.load(sfp)
        sfp.close()
        testcasedir_path_list = []
        for data in datas:
            if data["status"] != "passed":
                testcase_js_path = os.path.join(test_cases_dir_path, data["uid"] + ".json")
                with open(testcase_js_path, 'r', encoding='utf-8') as sfp:
                    testcase_js = json.load(sfp)
                sfp.close()
                if testcase_js["links"] == []:
                    pass
                else:
                    teast_case_path = testcase_js["links"][0]["url"].split("..")[-1]
                    testcasedir_path = ".." + teast_case_path.split(teast_case_path.split("/")[-1])[0]
                    testcasedir_path = os.path.join(os.path.dirname(__file__), testcasedir_path)
                    testcasedir_path_list.append(testcasedir_path)

        return testcasedir_path_list

    def _zip_test_case_dirs(self, test_case_dir_path_list):
        zip_list = []
        for test_case_dir_path in test_case_dir_path_list:
            zip_path = self._zip_test_case_dir(test_case_dir_path)
            zip_list.append(zip_path)
        return zip_list

    def _zip_test_case_dir(self, test_case_dir_path):
        path = test_case_dir_path.replace("\\", "/")
        path = path.split("/")[-2] if path.split("/")[-1] == "" else path.split("/")[-1]
        test_case_dir_path = "../test_pytest/allure-reports/log/"+path
        # 判断path是文件还是目录
        if os.path.isfile(test_case_dir_path):
            # 如果是文件，则获取文件所在目录路径
            dir_path = os.path.dirname(test_case_dir_path)
            # 获取文件名和后缀名
            file_name, file_ext = os.path.splitext(os.path.basename(test_case_dir_path))
            # 创建压缩文件路径
            zip_path = os.path.join(dir_path, file_name + '.zip')
            # 创建压缩文件对象
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # 将文件添加到压缩文件中
                zip_file.write(test_case_dir_path, file_name + file_ext)
            # 返回压缩文件路径
            return zip_path
        elif os.path.isdir(test_case_dir_path):
            # 如果是目录，则获取目录路径
            dir_path = test_case_dir_path
            # 创建压缩文件路径
            zip_path = os.path.join(dir_path, os.path.basename(dir_path) + '.zip')
            # 创建压缩文件对象
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # 遍历目录下的所有文件和子目录
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        # 获取文件相对路径
                        rel_path = os.path.relpath(os.path.join(root, file), dir_path)
                        # 将文件添加到压缩文件中
                        zip_file.write(os.path.join(root, file), rel_path)
                        # 返回压缩文件路径
            return zip_path
        else:
            # 如果path既不是文件也不是目录，则抛出异常
            raise ValueError('Invalid path')

        # todo 备注是可单独运行的,只是解压目录很奇怪,但压缩率高
        # if os.path.isfile(test_case_dir_path):
        #     with open(test_case_dir_path, "rb") as input_file:
        #         output_file_path = test_case_dir_path + ".gz"
        #         with gzip.open(output_file_path, "wb") as output_file:
        #             output_file.writelines(input_file)
        # else:
        #     path = test_case_dir_path.replace("\\", "/")
        #     path = path.split("/")[-2] if path.split("/")[-1] == "" else path.split("/")[-1]
        #     output_file_path = test_case_dir_path + ".targz"
        #     with tarfile.open(output_file_path, "w:gz") as output_file:
        #         output_file.add("../test_pytest/allure-reports/log/" + path)
        # return output_file_path


if __name__ == '__main__':
    ...

