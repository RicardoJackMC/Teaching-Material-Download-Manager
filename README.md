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
  for Ver.1.1.0_202308281300
</p>
<p align="center">
<a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>  
<a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32-blue?color=#4ec820" alt="Platform Win32"/>
  </a>
<a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.9.13-blue?color=#4ec820" alt="Python 3.9.13"/>
  </a>
</p>
<p align="center">
源代码: <a href="https://github.com/RicardoJackMC/Teaching-Material-Download-Manager">GitHub 仓库</a> | <a href="https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager">Gitee 仓库</a>
</p>
<p align="center">
下载地址: <a href="https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/releases">GitHub release</a> | <a href="https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager/releases">Gitee release</a> | <a href="https://www.123pan.com/s/Y59qVv-uuubd.html">123网盘</a>
</p>  
<h4 align="center">
  如果你的设备不受支持, 可以查看<a href="#pt1-下载原理">下载原理</a>自行获取教材下载链接！
</h4>








## 食用方法🍕

从 [Github release](https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/releases) 或 [Gitee release](https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager/releases) 页面选择最新版本, 点击`Teaching-Material-Download-Manager.zip`, 或者前往 [123网盘](https://www.123pan.com/s/Y59qVv-uuubd.html) 选择最新版本的文件夹, 下载`Teaching-Material-Download-Manager.zip`, 下载完成后解压, 双击`main.exe`即可使用.

## 演示视频📽️

在B站看本软件的[演示视频]()

## 敏感行为🛡️

本软件的某些行为可能会被杀毒软件识别为危险行为, 下表列出了程序的敏感行为

| 行为                                                         | 触发方式                                                     | 具体描述                                                     |
| ------------------------------------------------------------ | :----------------------------------------------------------- | ------------------------------------------------------------ |
| 对与 main.exe 同个目录下的的 config.json 进行读取与写入      | 当软件第一次启动时, 或当用户更改任意设置使自动触发           | 位于与 main.exe 同一目录下的 config.json 为本软件的配置文件, 上面记载了用户对软件的设置, 例如: 是否开启队列, 是否开启自动下载等. |
| 将 JSON 文件保存至用户指定的位置                             | 当用户点击“导出下载日志按钮时”在用户选定保存位置后触发       | 被保存的 JSON 文件为软件的下载日志, 上面记载了下载时的信息, 例如: 未能获取要保存的教材 pdf 文件标题的原因, 下载失败文件的链接等. 用户可以自行决定是否生成 JSON 文件,  JSON 文件的保存位置, 以及是否将 JSON 文件自行发送给开发者 |
| 与多个智慧教育平台 api (网址)通讯                            | 当处理任意任务时, 自动触发, 使用到 api (网址)详见[下载原理](#pt1-下载原理) | 软件需要与多个网站通讯才可获得 ID_B, 教材 pdf 文件的标题, 教材下载链接及下载教材, 具体通讯的网站可查看[下载原理](#pt1-下载原理) |
| 与 https://api.github.com/repos/RicardoJackMC/Teaching-Material-Download-Manager/releases/latest 和 https://gitee.com/api/v5/repos/RicardoJackMC/Teaching-Material-Download-Manager/releases/latest 通讯 | 当用户点击“检查更新”时触发                                   | 这两个链接为 GitHub 和 Gitee 的 api,  软件通过此 api 获取版本号判断是否有新版本 |
| 读取注册表: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize 下 AppsUseLightTheme 的值 | 每次当软件启动时自动触发                                     | 判断软件是否应启用暗黑模式使其与系统应用的外观同步           |
| 读取注册表: HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM 下 AccentColor 的值 | 每次当软件启动时自动触发                                     | 设置软件的主题色使其与系统应用同步                           |

## 软件原理📒

### Pt.1 下载原理

#### · 基础

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
| * https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| * https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |
| * https://r3-ndr.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/pdf.pdf |

至此, 该教材已有 4 个下载链接.

> **Note**
> 在上述例子中, 前面带星号的下载链接已经不可用, 但是在下载 https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=2600a906-afca-43bc-9070-5d962b92c85c&catalogType=tchMaterial&subCatalog=tchMaterial 时, 前面不带星号的下载链接不可用, 但是带星号的下载链接可以使用, 固本软件仍保留带星号的下载链接

#### · 高阶

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
json_data['custom_properties']['thumbnails'][0]  # 获取教材的图片, 我们把它记为url_B, 我们会用url_B获取ID_B
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

仍然以[基础](#· 基础)中使用的教材为例子, 可从以下链接获取 JSON 文件

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

#### · 总结

一个教材最多有 13 个下载链接, 若您的设备不支持本软件, 建议使用[基础](#·-基础)中的操作自行获取下载链接, 同时, 建议使用程序自动化完成[高阶](#·-高阶)中的操作获取下载链接. 如果发现下载链接失效了或发现新的下载链接, 请发邮件到 ricardojackmc@gmail.com 告诉作者, 谢谢啦 ！

### Pt.2 运行原理

本软件使用多进程 (multiprocessing) + 多线程 (QThread) 的方式运行

主进程 UI_Process 负责 UI 界面的刷新, 另有下载进程 Manager_Process 专门负责下载功能

使用 multiprocessing 中的 Queue 实现进程间的通讯, 其中 queue 负责向 UI_Process 传递下载进度, 下载状态等基本信息, queue_admin 负责向 UI_Process 传递结束指令, 下载链接, queue_command 负责向 Manager_Process 传递下载的配置项以及关闭指令

主进程下又有子线程 normal_info, admin_info 专门监听 queue 和 queue_admin, 另外还有子线程 update_func 专门负责检查软件更新. 

## 软件前瞻 (前方大型画饼现场)🍪

此外, 作者正在研究 智慧教育平台的课程的下载方法, 以及国家智慧教育读书平台, Library Genesis, Sci-Hub, Z-Library 等网站的下载方法.

可能会在下个版本支持 智慧教育平台课程 和 国家智慧教育读书平台 的下载.

(要开学啦, 开学后作者不一定更新, 可能要寒假才可以更新😥)

## 许可证🏛️

Teaching-Material-Download-Manager 使用 [GPLv3](https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/blob/main/LICENSE) 许可证.

Copyright 2023 by RicardoJackMC

> **Note**
> 如果您是在阅读[软件原理](#软件原理)或软件源码后自行编写程序然后分发, 则您的程序可以不必使用使用 [GPLv3](https://github.com/RicardoJackMC/Teaching-Material-Download-Manager/blob/main/LICENSE) 许可证. 

## 坚决反对日本排放福岛核污染水！！！☢️

> **Warning**
> 本条目不涉及歧视或引战, 更与政治无关 ! ! ! 本条与整个人类的存亡有关 ! ! ! 

首先, 对于 国内外舆论迫使日本政府停止排放福岛核污染水 这一可能事件, 本人持消极态度

并且, 对于 我们普通人通过各种努力与斗争迫使日本政府停止排放福岛核污染水 这一可能事件, 本人同样持消极态度

**但是, 不代表本人会消极应对此事！！！**

**普通人的力量太小, 不能改变什么, 但是, 群众的力量是强大的**

**我们也许不能改变日本排放福岛核污染水这一事实, 但是我们可以通过自己的行动, 让自己的子孙, 或者说, 人类的后代记住这件事！！！使他们不至于消失得这么不明不白！！！**

当然, 最好的结果是 迫使日本政府停止排放福岛核污染水 (尽管可能性很小)

**但是即使可能性很小, 我们也要去尝试, 去斗争！！！**

**本人这样做不是为了挑起任何冲突与矛盾, 也不想看到任何歧视与暴力的发生, 本人始终坚信, 日本人民, 甚至是日本政府内部, 仍然有人知道这件事的危害, 仍然有人在试图制止这一切的继续！！！**

**本人的诉求十分简单: **

**1. 日本政府停止继续通过排海的方式处理福岛核污染水, 使用更负责任的方式处理福岛核污染水 (本人清楚的知道实现这一条的概率很低)**

**2. 若第一条未能实现, 本人希望全人类都能记住, 在公元2023年8月24日, 日本正式启动福岛核污染水排海 (本人将致力于实现本条诉求)**

最后祝愿各位顺利可以成功通关地球OL😶‍🌫️！！！

