"""
图片生成服务
"""

import os
import uuid
from typing import Dict, Any, Optional
from generators.poster import PosterGenerator
from generators.product import ProductGenerator
from generators.banner import BannerGenerator
from generators.base import BaseImageGenerator
from utils import get_local_path


class ImageService:
    """图片生成服务"""
    
    def __init__(self):
        self.generators = {
            'poster': PosterGenerator,
            'product': ProductGenerator,
            'banner': BannerGenerator,
            'custom': BaseImageGenerator
        }
    
    def generate_image(self, image_type: str, data: Dict[str, Any]) -> str:
        """生成图片"""
        # 获取生成器类
        generator_class = self.generators.get(image_type, BaseImageGenerator)
        
        # 创建生成器实例
        generator = generator_class(
            width=data['width'],
            height=data['height'],
            background_color=tuple(data.get('background_color', (255, 255, 255)))
        )
        
        # 加载默认字体
        self._load_default_font(generator)
        
        # 处理字体和图片路径
        self._process_paths(data)
        
        # 生成图片
        generator.generate_from_data(data)
        
        # 保存图片
        output_path = self._save_image(generator, image_type, data.get('save_type'))
        
        return output_path
    
    def _load_default_font(self, generator):
        """加载默认字体"""
        from config import Config
        default_font = Config.get_default_font()
        if default_font:
            try:
                generator.load_font('default', default_font, 24)
            except Exception as e:
                print(f"加载默认字体失败: {e}")
    
    def _process_paths(self, data):
        """处理字体和图片路径"""
        # 处理字体路径
        for font in data.get('fonts', []):
            if font.get('path'):
                local_path = get_local_path(font['path'])
                if local_path:
                    font['path'] = local_path
        
        # 处理图片路径
        for image in data.get('images', []):
            if image.get('path'):
                local_path = get_local_path(image['path'])
                if local_path:
                    image['path'] = local_path
    
    def _save_image(self, generator, image_type: str, save_type: str) -> str:
        """保存图片"""
        filename = f"{image_type}_{uuid.uuid4().hex}"
        output_name = os.path.join('temp', filename)
        output_path = generator.save(output_name, save_type)
        return output_path
    
    def get_supported_types(self) -> Dict[str, Any]:
        """获取支持的图片类型"""
        from config import Config
        return {
            'types': list(Config.IMAGE_TYPES.keys()),
            'type_info': Config.IMAGE_TYPES
        }
