"""
商品图生成器
"""

from .base import BaseImageGenerator
from PIL import Image, ImageFilter, ImageDraw
from typing import Dict, Any


class ProductGenerator(BaseImageGenerator):
    """商品图生成器"""
    
    def __init__(self, width: int, height: int, background_color=(255, 255, 255)):
        super().__init__(width, height, background_color)
        self.type = "product"
    
    def add_border(self, border_color=(200, 200, 200), border_width=2):
        """添加边框"""
        for i in range(border_width):
            self.draw.rectangle(
                [i, i, self.width - i - 1, self.height - i - 1],
                outline=border_color,
                width=1
            )
    
    def add_shadow_effect(self):
        """添加阴影效果"""
        # 简单的阴影效果
        shadow = self.image.filter(ImageFilter.GaussianBlur(radius=1))
        return shadow
    
    @staticmethod
    def create_data_template(save_type='webp', width=1024, height=1024, 
                           bracelet_image_path=None, background_image_path=None):
        """创建商品图片生成的data模板
        
        Args:
            save_type (str): 保存类型，默认为'webp'
            width (int): 图片宽度，默认为1024
            height (int): 图片高度，默认为1024
            bracelet_image_path (str): 手镯图片路径，如果为None则使用默认路径
            background_image_path (str): 背景图片路径，如果为None则使用默认路径
        
        Returns:
            dict: 处理后的data字典
        """
        # 默认的手镯图片路径
        default_bracelet_path = 'https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp'
        default_background_path = 'https://zhuluoji.cn-sh2.ufileos.com/dev/background/265.webp'
        
        # 使用提供的路径或默认路径
        bracelet_path = bracelet_image_path if bracelet_image_path else default_bracelet_path
        background_path = background_image_path if background_image_path else default_background_path
        
        data_template = {
            'width': width,
            'height': height,
            'background_color': (240, 240, 240),
            'save_type': save_type,
            'images': [
                {
                    'key': 'background-texture-image',
                    'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/result-image-texture.png',
                    'position': (0, 0),
                    'size': (width, height),
                },
                {
                    'key': 'side-background',
                    'path': background_path,
                    'position': (0, 0),
                    'crop': {
                        'left': 200,
                        'right': 542,
                        'top': 0,
                        'bottom': height
                    }
                },
                {
                    'key': 'brand-logo',
                    'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/reuslt-image-logo.png',
                    'size': (64, 106),
                    'position': (651, 459),
                },
                {
                    'key': 'bracelet-image',
                    'path': bracelet_path,
                    'size': (740, 740),
                    'position': (312, 142),
                },
                {
                    'key': 'slogan-image',
                    'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/result-image-slogan.png',
                    'size': (256, 33),
                    'position': (555, 925),
                }
            ]
        }
        
        return data_template
    
    @staticmethod
    def preprocess_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """预处理商品图片生成数据
        
        Args:
            input_data (dict): 输入的数据，包含以下可选字段：
                - save_type: 保存类型
                - width: 图片宽度
                - height: 图片高度
                - bracelet_image: 手镯图片路径
                - background_image: 背景图片路径
        
        Returns:
            dict: 处理后的完整data字典
        """
        # 从输入数据中提取参数，如果没有提供则使用默认值
        save_type = input_data.get('save_type', 'webp')
        width = input_data.get('width', 1024)
        height = input_data.get('height', 1024)
        bracelet_image = input_data.get('bracelet_image')
        background_image = input_data.get('background_image')
        
        # 创建模板数据
        processed_data = ProductGenerator.create_data_template(
            save_type=save_type,
            width=width,
            height=height,
            bracelet_image_path=bracelet_image,
            background_image_path=background_image
        )
        
        return processed_data
