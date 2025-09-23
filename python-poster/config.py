"""
配置管理
"""

import os
from typing import Dict, Any


class Config:
    """应用配置"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5001))
    
    # 文件配置
    UPLOAD_FOLDER = 'uploads'
    TEMP_FOLDER = 'temp'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 支持的图片类型
    IMAGE_TYPES = {
        'poster': {'name': '海报', 'default_size': (800, 600)},
        'product': {'name': '商品图', 'default_size': (400, 400)},
        'banner': {'name': '横幅', 'default_size': (1200, 300)},
        'thumbnail': {'name': '缩略图', 'default_size': (200, 200)}
    }
    
    # 默认字体路径
    DEFAULT_FONT_PATHS = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        'C:/Windows/Fonts/simhei.ttf',        # Windows
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # Linux
    ]
    
    @staticmethod
    def get_default_font():
        """获取默认字体路径"""
        for font_path in Config.DEFAULT_FONT_PATHS:
            if os.path.exists(font_path):
                return font_path
        return None
    
    @staticmethod
    def init_app(app):
        """初始化应用"""
        # 创建必要目录
        for folder in [Config.UPLOAD_FOLDER, Config.TEMP_FOLDER]:
            os.makedirs(folder, exist_ok=True)
