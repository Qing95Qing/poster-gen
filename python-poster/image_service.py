"""
图片生成服务
"""

import os
import uuid
from typing import Dict, Any, Optional
from generators.product import ProductGenerator
from generators.base import BaseImageGenerator
from utils import get_local_path


class ImageService:
    """图片生成服务"""
    
    def __init__(self):
        self.generators = {
            'product': ProductGenerator,
            'custom': BaseImageGenerator
        }
    
    def generate_image(self, image_type: str, data: Dict[str, Any]) -> str:
        """生成图片"""
        # 预处理数据
        processed_data = self._preprocess_data(image_type, data)
        
        # 获取生成器类
        generator_class = self.generators.get(image_type, BaseImageGenerator)
        
        # 创建生成器实例
        generator = generator_class(
            width=processed_data['width'],
            height=processed_data['height'],
            background_color=tuple(processed_data.get('background_color', (255, 255, 255)))
        )
        
        # 加载默认字体
        self._load_default_font(generator)
        
        # 处理字体和图片路径
        self._process_paths(processed_data)
        
        # 生成图片
        generator.generate_from_data(processed_data)
        
        # 保存图片
        output_path = self._save_image(generator, image_type, processed_data.get('save_type'))
        
        return output_path
    
    def _preprocess_data(self, image_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """预处理数据
        
        Args:
            image_type (str): 图片类型
            data (dict): 原始数据
            
        Returns:
            dict: 预处理后的数据
        """
        if image_type == 'product':
            return ProductGenerator.preprocess_data(data)
        else:
            # 对于其他类型，返回原始数据或进行基本处理
            return data
    
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
