#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 启动Flask服务
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000