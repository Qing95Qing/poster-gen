#!/bin/bash

# 简化的图片生成服务启动脚本

echo "启动图片生成服务..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

# 创建必要的目录
echo "创建必要目录..."
mkdir -p uploads temp

# 启动服务
echo "启动服务..."
python3 app.py
