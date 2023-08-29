# -*- coding: utf-8 -*-

"""
Copyright 2023 by RicardoJackMC
Teaching Material Download Manager 使用 GPLv3 许可证
本文件是 Teaching Material Download Manager 的一部分
请自行前往
https://github.com/RicardoJackMC/Teaching-Material-Download-Manager
或
https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager
根据版本号校验本文件MD5
"""

import json
import os
import subprocess
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests


class Downloader():
    def __init__(self):
        self.RUN = True
        self.URL = None  # @
        self.chunk_size = None  # !
        self.file_size = None
        self.url_A = None  # !
        self.ID_A = None
        self.url_json = None
        self.title = None
        self.ID_B = None
        self.url_B = None
        self.url_PDF = None
        self.save_path = None  # !
        self.save_mode = None  # ! 0 为覆盖 1 为加数字后缀 2 为加时间后缀
        self.IDM_path = None  # !
        self.Aria2_url = None  # !
        self.path_PDF = None
        self.download_mode = None  # ! 0 内置下载 1 IDM 2 Aria2 3 复制链接
        self.download_data = {}  # @
        self.url_PDF_current_Left = None  # @ 通用的网址
        self.url_PDF_A_Left = None  # @ 仅使用ID_A的网址
        self.url_json_Left = None  # @
        self.url_PDF_B_Left = None  # @ 仅使用ID_B的网址
        self.warning = False
        self.queue = None  # @
        self.queue_admin = None  # @
        self.queue_command = None  # @
        self.KEY = []  # @
        self.KEY_admin = []  # @

        if os.path.isfile('.\\URL.json'):
            with open('.\\URL.json', 'r') as f:
                self.URL = json.load(f)

        self.url_PDF_current_Left = self.URL['url_PDF_current_Left']
        self.url_PDF_A_Left = self.URL['url_PDF_A_Left']
        self.url_json_Left = self.URL['url_json_Left']
        self.url_PDF_B_Left = self.URL['url_PDF_B_Left']

    def run(self):  # 入口
        pre_key = None
        while self.RUN:
            print('getting command')
            try:
                print('running d')
                command = self.queue_command.get()
                if command == 'CLOSE':
                    self.RUN = False
                if 'command' in command and command['command']['key'] != pre_key:
                    pre_key = command['command']['key']
                    self.url_A = command['command']['url_A']
                    self.save_mode = command['command']['save_mode']
                    self.save_path = command['command']['save_path']
                    if not self.save_path.endswith('\\'):
                        self.save_path = self.save_path + '\\'
                    self.IDM_path = command['command']['IDM_path']
                    self.Aria2_url = command['command']['Aria2_url']
                    self.download_mode = command['command']['download_mode']
                    self.chunk_size = command['command']['chunk_size']

                    self.warning = False
                    self.ID_B = None
                    self.title = None
                    self.file_size = None

                    result = self.get_ID_A()
                    if result:
                        self.verify_url_json()
                        result = self.verify_url_PDF()
                        print('va', result)
                        if result:
                            # 扫了一圈, 在这里设置保存路径最好
                            if self.title is None:
                                self.title = 'pdf'
                            self.path_PDF = self.save_path + self.title + '.pdf'
                            if not self.save_mode == 0:
                                n = 0
                                while os.path.exists(self.path_PDF):
                                    if self.save_mode == 1:
                                        n += 1
                                        self.path_PDF = self.save_path + self.title + ' ' + '(' + str(n) + ')' + '.pdf'
                                    elif self.save_mode == 2:
                                        self.path_PDF = self.save_path + self.title + ' ' + str(datetime.now()).replace(
                                            ':',
                                            '-') + '.pdf'
                            if self.download_mode == 0:
                                result = self.download_PDF()
                            elif self.download_mode == 1:
                                result = self.IDM_download()
                            elif self.download_mode == 2:
                                result = self.Aria2_download()
                            elif self.download_mode == 3:
                                download_url = {'title': self.title, 'download_url': self.url_PDF}
                                self.admin_producer('download_url', download_url)
                                self.download_data_update('FINISH', FINISH_STATE=self.warning)
                                result = True
                            print('result', result)
                            if result:
                                if self.warning:
                                    self.admin_producer('result', 'warning')
                                else:
                                    self.admin_producer('result', 'normal')
                            else:
                                self.admin_producer('result', 'error')
                        else:
                            self.admin_producer('result', 'error')
                    else:
                        self.admin_producer('result', 'ID_A error')
            except:
                pass

    def return_basic_info(self, type_info, info):
        data_info = {type_info: info}
        self.producer('basic_info', data_info)

    def admin_producer(self, type_info, info):
        KEY_admin = time.time()
        while KEY_admin in self.KEY_admin:
            KEY_admin += 0.000001
        data_info = {type_info: info, 'KEY': KEY_admin}
        self.queue_admin.put(data_info)
        self.KEY_admin.append(KEY_admin)

    def producer(self, type_info, info):
        KEY = time.time()
        while KEY in self.KEY:
            KEY += 0.000001
        data_info = {type_info: info, 'KEY': KEY}
        self.queue.put(data_info)
        self.KEY.append(KEY)

    def download_data_update(self, info, FINISH_STATE=None):
        if FINISH_STATE is not None:
            if FINISH_STATE:
                info = 'FINISH WARNING'
            elif not FINISH_STATE:
                info = 'FINISH NORMAL'
        key = time.time()
        while key in self.download_data:
            key += 0.000001
        self.download_data[key] = info
        self.producer('download_data', self.download_data)

    def get_ID_A(self):
        self.producer('state', 'getting ID_A...')
        time.sleep(0.5)
        self.download_data_update('trying to get ID_A from: ' + self.url_A)
        if 'tchMaterial' in self.url_A and 'contentId=' in self.url_A:
            try:
                ID_A_query_params = parse_qs(urlparse(self.url_A).query)
                self.ID_A = ID_A_query_params['contentId'][0]
                self.download_data_update('successfully getting ID_A: ' + self.ID_A + ' from: ' + self.url_A)
                self.return_basic_info('ID_A', self.ID_A)
                time.sleep(0.5)
                return True
            except:
                self.download_data_update('failed to get ID_A from: ' + self.url_A)
                self.download_data_update('FINISH ERROR')
                return False
        else:
            self.download_data_update('failed to get ID_A from: ' + self.url_A)
            self.download_data_update('FINISH ERROR')
            return False

    def verify_url_json(self):
        self.producer('state', 'getting json file...')
        time.sleep(0.5)
        for i in self.url_json_Left:
            self.url_json = i + self.ID_A + '.json'
            self.download_data_update('trying to get json file from: ' + self.url_json)
            try:
                if requests.head(self.url_json).status_code == 200:
                    self.download_data_update('successfully getting json file from: ' + self.url_json)
                    self.download_data_update('trying to getting title or ID_B from:' + self.url_json)
                    get_title_result = self.get_title()
                    get_ID_B_result = self.get_ID_B()
                    if get_title_result and get_ID_B_result:
                        self.return_basic_info('json_url', self.url_json)
                        time.sleep(0.5)
                        return True  # 如果有ID_B和title就可以结束辣
                    else:  # 如果其中一项没有就继续尝试
                        self.warning = True
                else:
                    self.download_data_update(
                        'can not get json file from: ' + self.url_json + ' status_code: ' + str(requests.head(
                            self.url_json).status_code))
            except requests.exceptions.RequestException as e:
                self.download_data_update('can not get json file from: ' + self.url_json + ' because: ' + str(e))
                self.warning = True
        self.url_json = None
        return False

    def get_title(self):
        self.producer('state', 'getting title...')
        time.sleep(0.5)
        book_title = None
        book_vision = None
        if self.url_json is not None and self.title is None:
            data_json = requests.get(self.url_json).json()
            try:
                book_title = data_json["title"]  # 获取名字
                book_title_get = True
            except:
                self.download_data_update('can not get book_title from: ' + self.url_json)
                self.warning = True
                book_title_get = False
            try:
                book_vision = data_json['tag_list'][2]['tag_name']  # 获取版本
                book_vision_get = True
            except:
                self.download_data_update('can not get book_vision from: ' + self.url_json)
                self.warning = True
                book_vision_get = False
            if book_vision_get or book_title_get:
                self.title = book_title + ' ' + book_vision

                self.download_data_update('successfully getting title: ' + self.title + ' from: ' + self.url_json)
                self.return_basic_info('title', self.title)
                time.sleep(0.5)
                return True
            else:
                return False

    def get_ID_B(self):
        self.producer('state', 'getting ID_B...')
        time.sleep(0.5)
        if self.url_json is not None and self.ID_B is None:  # 避免重复获取ID_B
            data_json = requests.get(self.url_json).json()
            # 获取ID_B
            try:
                self.url_B = data_json['custom_properties']['thumbnails'][0]
                url_B_LEFT, url_B_TEMP = self.url_B.split('document/')
                self.ID_B, url_B_RIGHT = url_B_TEMP.split('/image')
                self.download_data_update('successfully getting ID_B: ' + self.ID_B + ' from: ' + self.url_json)
                self.return_basic_info('ID_B', self.ID_B)
                time.sleep(0.5)
                return True
            except:
                self.download_data_update('can not get ID_B at: ' + self.url_json)
                self.warning = True
                self.ID_B = None
                return False

    def verify_url_PDF(self):
        self.producer('state', 'verifying...')
        time.sleep(0.5)
        # 测试ID_A的网址
        self.url_PDF_A_Left = self.url_PDF_current_Left + self.url_PDF_A_Left
        for i in self.url_PDF_A_Left:
            self.url_PDF = i + '/esp/assets_document/' + self.ID_A + '.pkg/pdf.pdf'
            try:
                response = requests.head(self.url_PDF)
                if response.status_code == 200:
                    self.file_size = int(response.headers["Content-Length"])
                    if self.file_size > 1024:
                        self.download_data_update('successfully verifying url: ' + self.url_PDF + ' from: ' + self.ID_A)
                        return True
                    else:
                        self.download_data_update(
                            'can not verify url: ' + self.url_PDF + ' because of: ' + self.file_size)
                        self.warning = True
                else:
                    self.download_data_update(
                        'can not verify url: ' + self.url_PDF + ' status_code: ' + str(requests.head(
                            self.url_PDF).status_code))
            except requests.exceptions.RequestException as e:
                self.download_data_update('can not verify url: ' + self.url_PDF + ' because: ' + str(e))
                self.warning = True
        for i in self.url_PDF_current_Left:
            self.url_PDF = i + '/esp/assets/' + self.ID_A + '.pkg/pdf.pdf'
            try:
                response = requests.head(self.url_PDF)
                if response.status_code == 200:
                    self.file_size = int(response.headers["Content-Length"])
                    if self.file_size > 1024:
                        self.download_data_update('successfully verifying url: ' + self.url_PDF + ' from: ' + self.ID_A)
                        return True
                    else:
                        self.download_data_update(
                            'can not verify url: ' + self.url_PDF + ' because of: ' + self.file_size)
                        self.warning = True
                else:
                    self.download_data_update(
                        'can not verify url: ' + self.url_PDF + ' status_code: ' + str(requests.head(
                            self.url_PDF).status_code))
            except requests.exceptions.RequestException as e:
                self.download_data_update('can not verify url: ' + self.url_PDF + ' because: ' + str(e))
                self.warning = True
        if self.ID_B is not None:
            self.url_PDF_B_Left = self.url_PDF_current_Left + self.url_PDF_B_Left
            for i in self.url_PDF_B_Left:
                self.url_PDF = i + '/65/document/' + self.ID_B + '/pdf.pdf'
                try:
                    response = requests.head(self.url_PDF)
                    if response.status_code == 200:
                        file_size = int(response.headers["Content-Length"])
                        if file_size > 1024:
                            self.download_data_update(
                                'successfully verifying url: ' + self.url_PDF + ' from: ' + self.ID_B)
                            return True
                        else:
                            self.download_data_update(
                                'can not verify url: ' + self.url_PDF + ' because of: ' + file_size)
                            self.warning = True
                    else:
                        self.download_data_update(
                            'can not verify url: ' + self.url_PDF + ' status_code: ' + str(requests.head(
                                self.url_PDF).status_code))
                except requests.exceptions.RequestException as e:
                    self.download_data_update('can not verify url: ' + self.url_PDF + ' because: ' + str(e))
                    self.warning = True
        self.download_data_update('FINISH ERROR')
        return False

    def download_PDF(self):
        self.producer('state', 'downloading...')
        time.sleep(0.5)
        try:
            downloaded_size = 0
            with open(self.path_PDF, 'wb') as file:
                for chunk in requests.get(self.url_PDF, stream=True).iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        pre_progress = None
                        progress = int((downloaded_size / self.file_size) * 100)
                        if pre_progress != progress:
                            self.producer('progress', progress)
                            pre_progress = progress
            if os.path.exists(self.path_PDF):
                self.download_data_update('successfully saving: ' + self.path_PDF)
                self.download_data_update('FINISH', FINISH_STATE=self.warning)
                return True
            else:
                self.download_data_update('failed to save: ' + self.path_PDF + ' there is nothing saved!')
                self.download_data_update('FINISH ERROR')
                return False
        except Exception as e:
            self.download_data_update('failed to save: ' + self.path_PDF + ' because: ' + str(e))
            self.download_data_update('FINISH ERROR')
            return False

    def IDM_download(self):
        self.producer('state', 'sending to IDM...')
        time.sleep(0.5)
        print(self.IDM_path)
        command_1 = [f"{self.IDM_path}", "/d", f"{self.url_PDF}", "/p", f"{self.save_path}", f"/f",
                     f"{os.path.basename(self.path_PDF)}"]
        command_data = ''
        for i in command_1:
            command_data = command_data + i + ' '
        process = subprocess.Popen(command_1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = process.wait()
        stdout, stderr = process.communicate()
        if return_code == 0:
            self.download_data_update('successfully run: ' + command_data)
            self.download_data_update('FINISH', FINISH_STATE=self.warning)
            return True
        else:
            self.download_data_update(
                'failed to run: ' + command_data + ' return code: ' + str(return_code) + ' stderr: ' + str(stderr))
            self.download_data_update('FINISH ERROR')
            return False

    def Aria2_download(self):
        self.producer('state', 'sending to Aria2...')
        time.sleep(0.5)
        url_list = [self.url_PDF]
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "aria2.addUri",
            "params": [url_list, {"dir": self.save_path, "out": os.path.basename(self.path_PDF)}]
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.Aria2_url, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    self.download_data_update("added " + self.url_PDF + " to " + self.Aria2_url + " successfully.")
                    self.download_data_update('FINISH', FINISH_STATE=self.warning)
                    return True
                elif 'error' in result:
                    self.download_data_update("Error: " + result['error']['message'])
                    self.download_data_update('FINISH ERROR')
                    return False
            else:
                self.download_data_update(
                    "failed to communicate with Aria2 server, status_code : " + str(response.status_code))
                self.download_data_update('FINISH ERROR')
                return False
        except Exception as e:
            self.download_data_update(
                "failed to communicate with Aria2 server, because : " + str(e))
            self.download_data_update('FINISH ERROR')
            return False
