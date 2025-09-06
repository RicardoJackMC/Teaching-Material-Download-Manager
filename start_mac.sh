#!/bin/bash

# Teaching Material Download Manager for macOS
# 教材下载管理器 macOS启动脚本

echo "欢迎使用教材下载管理器 (macOS版本)"
echo "======================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "错误: 请在源代码目录下运行此脚本"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
    echo "虚拟环境创建完成"
fi

# 激活虚拟环境
source venv/bin/activate

# 检查是否安装了依赖
if ! python -c "import PyQt5" 2>/dev/null; then
    echo "安装依赖包..."
    pip install --upgrade pip
    pip install --only-binary :all: PyQt5
    pip install requests PyQt-Fluent-Widgets darkdetect
    echo "依赖安装完成"
fi

# 设置默认下载路径
if [ ! -f "config.json" ]; then
    echo '{"download_mode": 0, "Aria2_url": "", "open_folder": true, "folder": "'$HOME'/Downloads/", "save_mode": 1, "first_open": true, "chunk_size": 1024, "IDM_path": "", "SegmentedWidget_show": "basic_info"}' > config.json
    echo "已创建配置文件，默认下载路径: ~/Downloads/"
fi

echo ""
echo "启动程序..."
echo "提示: 程序将在后台运行"
echo "默认下载路径: ~/Downloads/"
echo ""

# 运行程序
python main.py

# 如果程序退出，询问是否重新启动
echo ""
echo "程序已退出"
read -p "是否重新启动? (y/n): " restart
if [ "$restart" = "y" ] || [ "$restart" = "Y" ]; then
    exec "$0"
fi
