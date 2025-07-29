from flask import Flask, request, jsonify, send_file
from . import PosterGenerator
import os
import tempfile
import uuid
from . import get_local_path

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# 默认字体路径（根据不同系统调整）
DEFAULT_FONT_PATHS = [
    '/System/Library/Fonts/PingFang.ttc',  # macOS
    'C:/Windows/Fonts/simhei.ttf',        # Windows
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # Linux
]

# 找到可用的字体路径
DEFAULT_FONT_PATH = None
for font_path in DEFAULT_FONT_PATHS:
    if os.path.exists(font_path):
        DEFAULT_FONT_PATH = font_path
        break

@app.route('/')
def index():
    return '海报生成服务已启动，请访问 /generate 接口生成海报'

@app.route('/generate', methods=['POST'])
def generate_poster():
    try:
        # 获取请求参数
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400

        # 验证必要参数
        required_fields = ['width', 'height']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要参数: {field}'}), 400

        # 创建海报生成器
        width = int(data['width'])
        height = int(data['height'])
        background_color = tuple(data.get('background_color', (255, 255, 255)))
        poster = PosterGenerator(width, height, background_color)

        # 加载字体
        fonts = data.get('fonts', [])
        if not fonts and DEFAULT_FONT_PATH:
            # 使用默认字体
            poster.load_font('default', DEFAULT_FONT_PATH, 24)
        else:
            for font in fonts:
                font_name = font.get('name')
                font_path = font.get('path')
                font_size = font.get('size', 24)
                if font_name and font_path:
                    # 处理字体路径（支持网络路径）
                    local_font_path = get_local_path(font_path)
                    if local_font_path:
                        poster.load_font(font_name, local_font_path, font_size)
                    else:
                        app.logger.warning(f'无法加载字体: {font_path}')

        # 添加颜色区域
        color_regions = data.get('color_regions', [])
        for region in color_regions:
            position = tuple(region.get('position', (0, 0)))
            size = tuple(region.get('size', (100, 100)))
            color = tuple(region.get('color', (0, 0, 0)))
            poster.add_color_region(position, size, color)

        # 添加文本
        texts = data.get('texts', [])
        for text in texts:
            content = text.get('content', '')
            position = tuple(text.get('position', (0, 0)))
            font_name = text.get('font_name', 'default')
            color = tuple(text.get('color', (0, 0, 0)))
            align = text.get('align', 'left')
            poster.add_text(content, position, font_name, color, align)

        # 添加图片
        images = data.get('images', [])
        for image in images:
            image_path = image.get('path')
            position = tuple(image.get('position', (0, 0)))
            size = image.get('size')
            if image_path:
                # 处理图片路径（支持网络路径）
                local_image_path = get_local_path(image_path)
                if local_image_path:
                    poster.add_image(local_image_path, position, size)
                else:
                    app.logger.warning(f'无法获取图片: {image_path}')
            else:
                app.logger.warning('图片路径为空')

        # 保存海报到临时文件
        temp_filename = f'{uuid.uuid4()}.jpg'
        temp_filepath = os.path.join(TEMP_FOLDER, temp_filename)
        poster.save(temp_filepath)

        # 返回海报文件
        return send_file(temp_filepath, mimetype='image/jpeg', as_attachment=True, download_name='poster.jpg')

    except Exception as e:
        app.logger.error(f'生成海报时出错: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)