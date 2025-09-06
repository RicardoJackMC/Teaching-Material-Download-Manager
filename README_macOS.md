# 教材下载管理器 - macOS版本

## 概述
这是Teaching Material Download Manager的macOS适配版本，已经过修改以完全兼容macOS系统。

## 主要修改内容

### 1. 系统兼容性
- ✅ 移除了Windows注册表(winreg)依赖
- ✅ 修复了路径分隔符问题（使用`os.sep`代替`\\`）
- ✅ 适配了macOS的暗黑模式检测
- ✅ 修复了打开文件夹功能（使用`open`命令）

### 2. 下载功能调整
- ✅ IDM下载器在macOS上自动禁用（IDM仅支持Windows）
- ✅ 内置下载功能完全正常
- ✅ Aria2下载功能正常（需要单独安装Aria2）
- ✅ 获取下载链接功能正常

### 3. 默认设置
- 默认下载路径：`~/Downloads/`
- 当路径无效时自动使用`~/Downloads/`作为备用路径

## 使用方法

### 快速启动
```bash
# 在源代码目录下运行
./start_mac.sh
```

### 手动启动
```bash
# 1. 创建虚拟环境（首次运行）
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖（首次运行）
pip install --upgrade pip
pip install --only-binary :all: PyQt5
pip install requests PyQt-Fluent-Widgets darkdetect

# 4. 运行程序
python main.py
```

## 功能说明

### 下载模式
1. **内置下载**（推荐）：使用程序内置的下载功能
2. **IDM下载**：在macOS上不可用，会自动切换到内置下载
3. **Aria2下载**：需要先安装并配置Aria2服务器
4. **仅获取链接**：只获取教材的下载链接，不执行下载

### 保存设置
- 程序会自动记住您的设置
- 配置文件保存在：`config.json`
- 默认下载路径：`~/Downloads/`

## 注意事项

1. **首次运行**：程序会提示同意使用协议，请仔细阅读
2. **下载路径**：如果设置的路径无效，程序会自动使用`~/Downloads/`
3. **IDM功能**：IDM是Windows专用软件，在macOS上无法使用
4. **Aria2**：如需使用Aria2，请先安装：
   ```bash
   brew install aria2
   ```

## 已知问题和解决方案

### 问题1：程序无法启动
- 确保已安装Python 3.7或更高版本
- 确保已正确安装所有依赖包

### 问题2：下载失败
- 检查网络连接
- 尝试使用不同的下载模式
- 确保下载路径有写入权限

### 问题3：界面显示问题
- 程序会自动适配系统的亮/暗模式
- 如有显示问题，可尝试重启程序

## 技术细节

### 依赖包
- PyQt5: GUI框架
- PyQt-Fluent-Widgets: 现代化UI组件
- requests: 网络请求
- darkdetect: 检测系统暗黑模式

### Python版本
- 最低要求：Python 3.7
- 推荐版本：Python 3.9+

## 支持和反馈

原项目地址：
- GitHub: https://github.com/RicardoJackMC/Teaching-Material-Download-Manager
- Gitee: https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager

## 许可证
本软件使用GPLv3许可证
