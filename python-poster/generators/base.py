"""
基础图片生成器
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional, List, Dict, Any
import os


class BaseImageGenerator:
    """基础图片生成器"""
    
    def __init__(self, width: int, height: int, background_color: Tuple[int, int, int] = (255, 255, 255)):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.image = Image.new('RGB', (width, height), background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {}
    
    def load_font(self, font_name: str, font_path: str, font_size: int):
        """加载字体"""
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"字体文件不存在: {font_path}")
        
        try:
            self.fonts[font_name] = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            raise Exception(f"加载字体失败: {e}")
    
    def add_text(self, text: str, position: Tuple[int, int], font_name: str = 'default', 
                 color: Tuple[int, int, int] = (0, 0, 0), align: str = 'left'):
        """添加文本"""
        if font_name not in self.fonts:
            raise ValueError(f"字体未加载: {font_name}")
        
        font = self.fonts[font_name]
        text_width, text_height = self.draw.textsize(text, font=font)
        
        if align == 'center':
            position = (position[0] - text_width // 2, position[1])
        elif align == 'right':
            position = (position[0] - text_width, position[1])
        
        self.draw.text(position, text, font=font, fill=color)
    
    def add_color_region(self, position: Tuple[int, int], size: Tuple[int, int], 
                        color: Tuple[int, int, int]):
        """添加颜色区域"""
        x1, y1 = position
        x2, y2 = x1 + size[0], y1 + size[1]
        self.draw.rectangle([x1, y1, x2, y2], fill=color)
    
    def add_image(self, image_path: str, position: Tuple[int, int], 
                  size: Optional[Tuple[int, int]] = None, 
                  crop: Optional[Dict[str, int]] = None):
        """添加图片
        
        Args:
            image_path: 图片路径
            position: 粘贴位置 (x, y)
            size: 调整后的尺寸 (width, height)
            crop: 裁剪参数 {'left': int, 'top': int, 'right': int, 'bottom': int}
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        try:
            img = Image.open(image_path)
            
            # 如果指定了裁剪参数，先进行裁剪
            if crop:
                left = crop.get('left', 0)
                top = crop.get('top', 0)
                right = crop.get('right', img.width)
                bottom = crop.get('bottom', img.height)
                
                # 确保裁剪区域在图片范围内
                left = max(0, min(left, img.width))
                top = max(0, min(top, img.height))
                right = max(left, min(right, img.width))
                bottom = max(top, min(bottom, img.height))
                
                img = img.crop((left, top, right, bottom))
            
            # 如果指定了尺寸，调整图片大小
            if size:
                img = img.resize(size)
            
            # 处理透明背景图片
            if img.mode == 'RGBA':
                # 对于RGBA图片，使用alpha_composite来保持透明度
                if self.image.mode != 'RGBA':
                    # 将背景转换为RGBA模式
                    self.image = self.image.convert('RGBA')
                
                # 创建一个临时图片用于合成
                temp_img = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
                temp_img.paste(img, position)
                
                # 使用alpha_composite合成图片
                self.image = Image.alpha_composite(self.image, temp_img)
            else:
                # 对于非透明图片，直接粘贴
                self.image.paste(img, position)
        except Exception as e:
            raise Exception(f"添加图片失败: {e}")
    
    def save(self, output_name: str, save_type: str):
        """保存图片"""
        try:
            if save_type == 'webp':
                output_path = output_name + '.webp'
                self.image.save(output_path, 'WEBP')
            # 根据图片模式选择合适的保存格式
            elif self.image.mode == 'RGBA':
                # 对于RGBA图片，保存为PNG格式以保持透明度
                output_path = output_name + '.png'
                self.image.save(output_path, 'PNG')
            else:
                # 对于RGB图片，保存为JPEG格式
                output_path = output_name + '.jpg'
                self.image.save(output_path, 'JPEG', quality=95)
            return output_path
        except Exception as e:
            raise Exception(f"保存图片失败: {e}")
    
    def generate_from_data(self, data: Dict[str, Any]):
        """根据数据生成图片"""
        # 加载字体
        for font in data.get('fonts', []):
            self.load_font(font['name'], font['path'], font.get('size', 24))
        
        # 添加颜色区域
        for region in data.get('color_regions', []):
            self.add_color_region(
                tuple(region['position']),
                tuple(region['size']),
                tuple(region['color'])
            )
        
        # 添加文本
        for text in data.get('texts', []):
            self.add_text(
                text['content'],
                tuple(text['position']),
                text.get('font_name', 'default'),
                tuple(text.get('color', (0, 0, 0))),
                text.get('align', 'left')
            )
        
        # 添加图片
        for image in data.get('images', []):
            self.add_image(
                image['path'],
                tuple(image['position']),
                tuple(image['size']) if image.get('size') else None,
                image.get('crop')
            )
        
        return self.image
