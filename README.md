<p align="center">
  <img width="18%" align="center" src="https://raw.githubusercontent.com/RicardoJackMC/Teaching-Material-Download-Manager/main/recourse/logo.png" alt="logo">
</p>
  <h1 align="center">
  Teaching-Material-Download-Manager
</h1>
<p align="center">
  优雅地下载电子教材
</p>
<p align="center">
<a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>  
<a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32-blue?color=#4ec820" alt="Platform Win32"/>
  </a>
</p>
<p align="center">
下载地址: <a href="https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/releases">GitHub release</a> | <a href="https://www.123pan.com/s/Y59qVv-uuubd.html">123网盘</a>
</p>




## 食用方法🍕

从[release](https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/releases)页面选择最新版本, 点击`Teaching-Material-Download-Manager.zip`或者前往[123网盘](https://www.123pan.com/s/Y59qVv-uuubd.html)选择最新版本, 下载`Teaching-Material-Download-Manager.zip`, 下载完成后解压, 双击`main.exe`即可使用.

## 演示视频📽️

在B站看本软件的[演示视频]()

## 敏感行为🛡️

本软件的某些行为可能会被杀毒软件识别为危险行为, 下表列出了程序的敏感行为

| 行为                                                         | 具体描述                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 对与 main.exe 同级的 config.json 进行读取与写入              | 位于与 main.exe 同一目录下的 config.json 为本软件的配置文件, 上面记载了用户对软件的设置, 例如: 是否开启队列, 是否开启自动下载等. |
| 将 JSON 文件保存至用户指定的位置                             | 被保存的 JSON 文件为软件的下载日志, 上面记载了下载时的信息, 例如: 未能获取要保存的教材 pdf 文件标题的原因, 下载失败文件的链接等. 用户可以自行决定是否生成 JSON 文件,  JSON 文件的保存位置, 以及是否将 JSON 文件自行发送给开发者 |
| 与多个网站通讯                                               | 软件需要与多个网站通讯才可获得 ID_B, 教材 pdf 文件的标题, 部分下载链接及下载教材, 具体通讯的网站可查看[软件原理](#软件原理) |
| 读取注册表: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize 下 AppsUseLightTheme 的值 | 判断软件是否应启用暗黑模式使其与系统应用相同                 |
| 读取注册表: HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM 下 AccentColor 的值 | 设置软件的主题色使其与系统应用相同                           |

## 软件原理📒

### 基础

研究发现教材详情页网址的组成如下

```url
https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId={id}&catalogType=tchMaterial&subCatalog=tchMaterial
```

我们把 {id} 的值记为 ID_A

可以发现使用 ID_A 的值替换下列网址中的 {ID_A} 后形成的新网址即为 pdf 教材教材的下载链接:

| 使用ID_A的下载链接                                           |
| ------------------------------------------------------------ |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/{ID_A}.pkg/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/{ID_A}.pkg/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/{ID_A}.pkg/pdf.pdf |
| https://c1.ykt.cbern.com.cn/edu_product/esp/assets_document/{ID_A}.pkg/pdf.pdf |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets/{ID_A}.pkg/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets/{ID_A}.pkg/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/esp/assets/{ID_A}.pkg/pdf.pdf |

例如:

```url
https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=b8e9a3fe-dae7-49c0-86cb-d146f883fd8e&catalogType=tchMaterial&subCatalog=tchMaterial
```

其中 ID_A 的值为: 

```ID_A
b8e9a3fe-dae7-49c0-86cb-d146f883fd8e
```

则该教材有以下下载链接:

| 示例下载链接                                                 |
| ------------------------------------------------------------ |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://c1.ykt.cbern.com.cn/edu_product/esp/assets_document/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |

至此, 该教材已有 7 个下载链接.

### 高阶

使用 ID_A 的值替换下列网址中的 {ID_A} 后形成的新网址为 JSON 文件:

| JSON文件链接                                                 |
| ------------------------------------------------------------ |
| https://s-file-3.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/{ID_A}.json |
| https://s-file-2.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/{ID_A}.json |
| https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/{ID_A}.json |

此时, 可以在此 JSON 中获得教材的标题, 版本和 ID_B, 其中, 如果将 JSON 文件保存为一个名为 json_data 的 Python 字典, 则可以通过: 

```python
json_data["title"]  # 获取教材标题
json_data['tag_list'][2]['tag_name']  # 获取教材版本
json_data['custom_properties']['thumbnails'][0]  # 获取一个网址, 我们把它记为url_B, 我们会用url_B获取ID_B
```

其中, url_B 组成通常如下: 

```url
https://r3-ndr.ykt.cbern.com.cn/edu_product/65/document/{id}/image/1.jpg
```

我们把上述网址 {id} 的值记为 ID_B

> **Note**
> 这仅仅只是其中的一种获取 ID_B 的方法, 据开发者所知还有其他更稳定的方法可以获取 ID_B

可以发现使用 ID_B 的值替换下列网址中的 {ID_B} 后形成的新网址即为 pdf 教材教材的下载链接:

| 使用 ID_B 的下载链接                                         |
| ------------------------------------------------------------ |
| https://v1.ykt.cbern.com.cn/65/document/{ID_B}/pdf.pdf       |
| https://v2.ykt.cbern.com.cn/65/document/{ID_B}/pdf.pdf       |
| https://v3.ykt.cbern.com.cn/65/document/{ID_B}/pdf.pdf       |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/65/document/{ID_B}/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/65/document/{ID_B}/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/65/document/{ID_B}/pdf.pdf |

> **Warning**
> 通过 JSON 获取的 ID_B, 教材标题, 教材版本出错的可能性较大, 不同的教材对应的 JSON 文件基本都具有差异, 尽管差异很小, 也会造成程序无法正确获取 ID_B, 教材标题, 教材版本.

仍然以[基础](#基础)中使用的教材为例子, 可从以下链接获取 JSON 文件

| JSON文件链接                                                 |
| ------------------------------------------------------------ |
| https://s-file-3.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.json |
| https://s-file-2.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.json |
| https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/details/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.json |

讲 JSON 文件保存为名为 json_data 的 Python 字典, 则

```py
print(json_data["title"])
# 输出 普通高中教科书·语文必修 上册
print(json_data['tag_list'][2]['tag_name'])  
# 输出 统编版
print(json_data['custom_properties']['thumbnails'][0])  
# 输出 https://r1-ndr.ykt.cbern.com.cn/edu_product/65/document/7a69755810bb492c9e44f94a213b7e5e/image/1.jpg
```

通过 url_B 获取 ID_B 为

```ID_B
7a69755810bb492c9e44f94a213b7e5e
```

则可获得以下下载链接: 

| 示例下载链接                                                 |
| ------------------------------------------------------------ |
| https://v1.ykt.cbern.com.cn/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |
| https://v2.ykt.cbern.com.cn/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |
| https://v3.ykt.cbern.com.cn/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |
| https://r1-ndr.ykt.cbern.com.cn/edu_product/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |
| https://r2-ndr.ykt.cbern.com.cn/edu_product/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |
| https://r3-ndr.ykt.cbern.com.cn/edu_product/65/document/7a69755810bb492c9e44f94a213b7e5e/pdf.pdf |

综上所述, 一个教材目前最多有 13 个下载链接.

> **Note**
> 当程序无法获得ID_B, 标题, JSON文件, 或某个下载链接失效时会弹出警告信息
> 当无法识别ID_A, 或所有下载链接失效时, 程序会弹出错误信息

### 总结

一个教材最多有 13 个下载链接, 若您的设备不支持本软件, 建议使用[基础](#基础)中的操作自行获取下载链接, 同时, 建议使用程序自动化完成[高阶](#高阶)中的操作获取下载链接. 如果发现下载链接失效了或发现新的下载链接, 请发邮件到 ricardojackmc@gmail.com 告诉作者, 谢谢啦

## 许可证

Teaching-Material-Download-Manager 使用 [GPLv3](https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/blob/main/LICENSE) 许可证.

Copyright 2023 by RicardoJackMC
