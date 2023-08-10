"""
Copyright 2023 by RicardoJackMC
Teaching Material Download Manager 使用 GPLv3 许可证
本文件是 Teaching Material Download Manager 的一部分
请自行前往 https://github.com/RicardoJackMC/Teaching-Material-Download-Manager 根据版本号校验本文件MD5
"""

import os
import time
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime


class TEXTBOOK_FILE():

    def __init__(self):
        # 对变量初始化设置
        self.url_A = 'Unknown'
        self.url_B = 'Unknown'
        self.json_LEFT = ['https://s-file-3.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/',
                          'https://s-file-2.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/',
                          'https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/']

        self.ID_universal_LEFT = ['https://r1-ndr.ykt.cbern.com.cn/edu_product',
                                  'https://r2-ndr.ykt.cbern.com.cn/edu_product',
                                  'https://r3-ndr.ykt.cbern.com.cn/edu_product', ]

        self.ID_B_LEFT = ['https://v1.ykt.cbern.com.cn',
                          'https://v2.ykt.cbern.com.cn',
                          'https://v3.ykt.cbern.com.cn', ]

        self.json_url = 'Unknown'  # json文件的网址
        self.title = 'pdf'  # pdf文件的标题
        self.ID_A = 'Unknown'
        self.ID_B = 'Unknown'
        self.result_data = {}  # 日志
        self.save_path = ''  # pdf文件的保存路径
        self.pdf_file = ''  # pdf文件的保存位置
        self.pdf_url = 'Unknown'  # pdf文件网址
        self.save_mode = 1  # 发现同名文件的处理方式, 0为覆盖, 1为加上数字后缀, 2为加上时间后缀
        self.warning = 0

    def get_ID_A(self, url_a):
        self.url_A = url_a
        key = time.time()
        while key in self.result_data:
            key += 0.000001
        self.result_data[key] = 'trying to get ID_A...'
        if 'tchMaterial' in self.url_A and 'contentId=' in self.url_A:
            try:
                ID_A_query_params = parse_qs(urlparse(self.url_A).query)
                self.ID_A = ID_A_query_params['contentId'][0]
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'successfully get ID_A:' + self.ID_A + ' ' + 'from:' + self.url_A
                return True
            except:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'failed get ID_A from:' + self.url_A
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'finish'
                return False
        else:
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'failed get ID_A from:' + self.url_A
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'finish'
            return False

    def analyse_json_url(self):
        # 依次从三个json文件来源获取ID_B和title
        # 下面是判断json文件地址是否有效
        for i in self.json_LEFT:
            self.json_url = i + self.ID_A + '.json'
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'trying to get json file at:' + self.json_url
            try:
                if requests.get(self.json_url).status_code == 200:
                    # 如果json文件地址有效，则开始获取ID_B和title
                    key = time.time()
                    while key in self.result_data:
                        key += 0.000001
                    self.result_data[key] = 'successfully get json file at:' + self.json_url
                    key = time.time()
                    while key in self.result_data:
                        key += 0.000001
                    self.result_data[key] = 'trying to get title and ID_B from:' + self.json_url
                    get_title_result = self.get_title()
                    get_ID_B_result = self.get_ID_B()
                    if get_title_result and get_ID_B_result:
                        return True  # 如果有ID_B和title就可以结束辣
                    else:  # 如果其中一项没有就继续尝试
                        continue
            except requests.exceptions.RequestException as e:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get json at:' + self.json_url + 'status_code' + str(e)
                self.warning = 1
                self.json_url = 'Unknown'
                continue
        return False  # 说明无ID_B和title

    def get_title(self):
        if self.json_url != 'Unknown' and self.title == 'pdf':  # 避免重复获取title
            json_data = requests.get(self.json_url).json()

            # 获取title, 应由教材名字和教材版本构成
            book_title = 'Unknown Title'
            book_vision = 'Unknown Vision'
            try:
                book_title = json_data["title"]  # 获取名字
                book_title_get = True
            except:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get book_title at:' + self.json_url
                self.warning = 1
                book_title_get = False
            try:
                book_vision = json_data['tag_list'][2]['tag_name']  # 获取版本
                book_vision_get = True
            except:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get book_vision at:' + self.json_url
                self.warning = 1
                book_vision_get = False
            if book_vision_get or book_title_get:
                self.title = book_title + ' ' + book_vision
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'successfully get title:' + self.title + ' ' + 'from:' + self.json_url
                
                return True
            else:
                return False

    def get_ID_B(self):
        if self.json_url != 'Unknown' and self.ID_B == 'Unknown':  # 避免重复获取ID_B
            json_data = requests.get(self.json_url).json()
            # 获取ID_B
            try:
                self.url_B = json_data['custom_properties']['thumbnails'][0]
                url_B_LEFT, url_B_TEMP = self.url_B.split('document/')
                self.ID_B, url_B_RIGHT = url_B_TEMP.split('/image')
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'successfully get ID_B:' + self.ID_B + ' ' + 'from:' + self.json_url
                
                return True
            except:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get ID_B at:' + self.json_url
                self.warning = 1
                self.ID_B = 'Unknown'
                return False

    def download_pdf_file(self):
        # 首先先对ID_A进行测试
        for i in self.ID_universal_LEFT:
            # 判断当前通用网址加上/esp/assets_document/是否有效
            self.pdf_url = i + '/esp/assets_document/' + self.ID_A + '.pkg/pdf.pdf'
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'trying to get pdf at:' + self.pdf_url
            try:
                if requests.get(self.pdf_url).status_code == 200:
                    break
            except requests.exceptions.RequestException as e:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get pdf at:' + self.pdf_url + 'status_code' + str(e)
                self.warning = 1
                # 顺便判断当前通用网址加上/esp/assets/是否有效
                
                self.pdf_url = i + '/esp/assets/' + self.ID_A + '.pkg/pdf.pdf'
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'trying to get pdf at:' + self.pdf_url
                try:
                    if requests.get(self.pdf_url).status_code == 200:
                        break
                except requests.exceptions.RequestException as e:
                    key = time.time()
                    while key in self.result_data:
                        key += 0.000001
                    self.result_data[key] = 'can not get pdf at:' + self.pdf_url + 'status_code' + str(e)
                    self.warning = 1
                    self.pdf_url = 'Unknown'
        # 单独判断c1.ykt.cbern.com.cn
        if self.pdf_url == 'Unknown':
            self.pdf_url = 'https://c1.ykt.cbern.com.cn/edu_product' + '/esp/assets_document/' + self.ID_B + '.pkg/pdf.pdf'
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'trying to get pdf at:' + self.pdf_url
            try:
                if requests.get(self.pdf_url).status_code == 200:
                    pass
            except requests.exceptions.RequestException as e:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not get pdf at:' + self.pdf_url + 'status_code' + str(e)
                self.warning = 1
                self.pdf_url = 'Unknown'
        # ID_A全军覆没, 判断ID_B
        if self.pdf_url == 'Unknown':
            if self.ID_B != 'Unknown':
                self.ID_B_LEFT = self.ID_B_LEFT + self.ID_universal_LEFT  # 把通用网址和仅使用ID_B的网址全部合起来可以偷懒[doge]
                for i in self.ID_B_LEFT:
                    self.pdf_url = i + '/65/document/' + self.ID_B + '/pdf.pdf'
                    key = time.time()
                    while key in self.result_data:
                        key += 0.000001
                    self.result_data[key] = 'trying to get pdf at:' + self.pdf_url
                    try:
                        if requests.get(self.pdf_url).status_code == 200:
                            break
                    except requests.exceptions.RequestException as e:
                        key = time.time()
                        while key in self.result_data:
                            key += 0.000001
                        self.result_data[key] = 'can not get pdf at:' + self.pdf_url + 'status_code' + str(e)
                        self.warning = 1
                        self.pdf_url = 'Unknown'
        # 如果pdf_url的值不是Unknown, 那么就可以开始下载辣
        if self.pdf_url != 'Unknown':
            self.pdf_file = self.save_path + self.title + '.pdf'
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'successfully recognize:' + self.pdf_url
            
            n = 0
            if self.save_mode == 0:
                pass
            else:
                while os.path.exists(self.pdf_file):
                    if self.save_mode == 1:
                        n += 1
                        self.pdf_file = self.save_path + self.title + ' ' + '(' + str(n) + ')' + '.pdf'
                    elif self.save_mode == 2:
                        self.pdf_file = self.save_path + self.title + ' ' + str(datetime.now()).replace(':', '-') + '.pdf'
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'trying to save pdf at:' + self.pdf_file
            try:
                with open(self.pdf_file, 'wb') as file:
                    for chunk in requests.get(self.pdf_url, stream=True).iter_content(chunk_size=8192):
                        file.write(chunk)
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'successfully save file at:' + self.pdf_file
                
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'finish'
                return True
            except requests.exceptions.RequestException as e:
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'can not save pdf file:' + str(e)
                key = time.time()
                while key in self.result_data:
                    key += 0.000001
                self.result_data[key] = 'finish'
                return False
        else:
            key = time.time()
            while key in self.result_data:
                key += 0.000001
            self.result_data[key] = 'finish'
            return False
