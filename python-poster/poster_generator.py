from PIL import Image, ImageDraw, ImageFont
import os

class PosterGenerator:
    def __init__(self, width, height, background_color=(255, 255, 255)):
        """初始化海报生成器

        Args:
            width (int): 海报宽度
            height (int): 海报高度
            background_color (tuple): 背景颜色，默认为白色
        """
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height), background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {}

    def add_image(self, image_path, position=(0, 0), size=None):
        """添加图片到海报

        Args:
            image_path (str): 图片路径
            position (tuple): 图片左上角位置，默认为(0, 0)
            size (tuple): 图片大小 (width, height)，默认为原图大小
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        try:
            img = Image.open(image_path)
            if size:
                img = img.resize(size)
            self.image.paste(img, position)
        except Exception as e:
            raise Exception(f"添加图片时出错: {e}")

    def load_font(self, font_name, font_path, font_size):
        """加载字体

        Args:
            font_name (str): 字体名称，用于后续引用
            font_path (str): 字体文件路径
            font_size (int): 字体大小
        """
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"字体文件不存在: {font_path}")

        try:
            self.fonts[font_name] = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            raise Exception(f"加载字体时出错: {e}")

    def add_text(self, text, position, font_name, color=(0, 0, 0), align='left'):
        """添加文本到海报

        Args:
            text (str): 文本内容
            position (tuple): 文本位置
            font_name (str): 已加载的字体名称
            color (tuple): 文本颜色，默认为黑色
            align (str): 文本对齐方式，可选 'left', 'center', 'right'
        """
        if font_name not in self.fonts:
            raise ValueError(f"字体未加载: {font_name}")

        font = self.fonts[font_name]

        # 计算文本尺寸和位置
        text_width, text_height = self.draw.textsize(text, font=font)

        if align == 'center':
            position = (position[0] - text_width // 2, position[1])
        elif align == 'right':
            position = (position[0] - text_width, position[1])

        self.draw.text(position, text, font=font, fill=color)

    def add_color_region(self, position, size, color):
        """添加颜色区域到海报

        Args:
            position (tuple): 区域左上角位置
            size (tuple): 区域大小 (width, height)
            color (tuple): 区域颜色
        """
        x1, y1 = position
        x2, y2 = x1 + size[0], y1 + size[1]
        self.draw.rectangle([x1, y1, x2, y2], fill=color)

    def save(self, output_path):
        """保存海报

        Args:
            output_path (str): 输出路径
        """
        try:
            self.image.save(output_path)
            print(f"海报已保存到: {output_path}")
            return output_path
        except Exception as e:
            raise Exception(f"保存海报时出错: {e}")

    def show(self):
        """显示海报"""
        self.image.show()