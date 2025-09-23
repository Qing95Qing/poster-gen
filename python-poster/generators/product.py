"""
商品图生成器
"""

from .base import BaseImageGenerator
from PIL import Image, ImageFilter, ImageDraw


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
