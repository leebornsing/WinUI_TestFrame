import datetime
import os
import time
import pytest
import patoolib

def file_is_existed(file_path, is_exp_succ=True):
    """
    检查基础文件是否存在
    :param
    file_path:（str）：传文件路径
    :return:
    None
    """
    is_exists_config = os.path.exists(file_path)
    assert is_exists_config == is_exp_succ, "{}，这个文件不存在".format(file_path)

def get_newest_file(path, pre_fileName='sprint9_'):
    files = [f for f in os.listdir(path) if f.startswith(pre_fileName)]
    if not files:
        return None
    newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
    return os.path.join(path, newest_file)

def replace_str_in_filePath(file_path, old_string, new_string):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 将指定字符串a替换为指定字符串b
    new_content = content.replace(old_string, new_string)

    # 将替换后的内容写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def get_value_in_file(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    try:
        return eval(content).get(key)
    except:
        return

def check_int(value):
    if value is None:
        pytest.exit("SysErr")
    else:
        try:
            int(value)
        except:
            pytest.exit("SysErr")

def try_to_delete_files_and_dirs(path_list, is_delete_path: bool = True):
    for path in path_list:
        try:
            if os.listdir(path):
                try:
                    delete_files_and_dirs(path, is_delete_path=is_delete_path)
                except:
                    pass
            else:
                try:
                    os.remove(path)
                except:
                    pass
        except:
            pass

def delete_files_and_dirs(path, is_delete_path=False):
    if os.path.exists(path):
        for file_or_dir in os.listdir(path):
            full_path = os.path.join(path, file_or_dir)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                delete_files_and_dirs(full_path)
                os.rmdir(full_path)
        if is_delete_path:
            os.rmdir(path)

def _delete_files(path):
    for file_name in os.listdir(os.path.abspath(path)):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def clean_cache_png():
    """
    清理cache目录内的cache内容
    :return:
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    _delete_files(path)

def try_to_mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass

def find_string_directories(path, string="log"):
    if os.path.exists(path):
        directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
        log_directories = [name for name in directories if name.startswith(string)]
        if log_directories:
            return log_directories
    return None

def extract_zip_file(zip_file_path, extract_folder):
    patoolib.extract_archive(archive=zip_file_path, outdir=extract_folder)

def get_last_dir_path(directory):
    max_dir = None
    max_num = float('-inf')
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            try:
                num = int(item)
                if num > max_num:
                    max_num = num
                    max_dir = item_path
            except ValueError:
                pass
    return max_dir

def get_mtime_form_file_path(file_path):
    return time.ctime(os.path.getmtime(file_path))

def get_log_times(report_log_path):
    log_list = find_string_directories(path=report_log_path, string='log')
    if log_list is None:
        return os.path.join(report_log_path, "log2")
    elif "log2" in log_list:
        return os.path.join(report_log_path, "log2")
    elif "log1" in log_list:
        return os.path.join(report_log_path, "log1")
    elif "log0" in log_list:
        return os.path.join(report_log_path, "log0")
    else:
        return os.path.join(report_log_path, "log2")

def get_file_size(file_path):
    return os.stat(file_path).st_size

def compare_mtime(file1, file2):
    mtime1 = os.path.getmtime(file1)
    mtime2 = os.path.getmtime(file2)
    dt1 = datetime.datetime.fromtimestamp(mtime1)
    dt2 = datetime.datetime.fromtimestamp(mtime2)
    time_diff = abs(dt1 - dt2)
    if time_diff <= datetime.timedelta(days=1):
        return True
    else:
        return False

if __name__ == "__main__":
    # get_newest_file(path=, pre_fileName='sprint9_')
    # ...
    os.rmdir(r'D:\WRP-Simconductor4.0\t1')