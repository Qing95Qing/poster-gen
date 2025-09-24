"""
简化的图片生成服务
"""

from flask import Flask, request, jsonify, send_file
from image_service import ImageService
from config import Config
import os
import uuid
import base64


app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# 创建服务实例
image_service = ImageService()


@app.route('/')
def index():
    """首页"""
    return jsonify({
        'service': '图片生成服务',
        'version': '1.0.0',
        'description': '支持拼接手串图、手串商品图',
        'endpoints': {
            'POST /generate/product_image': '生成手串商品图片',
        }
    })


@app.route('/generate/product_image', methods=['POST'])
def generate_product_image():
    """生成手串商品图片"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        if 'width' not in data or 'height' not in data:
            return jsonify({'error': '缺少width或height参数'}), 400

        if 'bracelet_image' not in data:
            return jsonify({'error': '缺少bracelet_image参数'}), 400

        if 'background_image' not in data:
            return jsonify({'error': '缺少background_image参数'}), 400
        
        # 生成图片（数据预处理在image_service中统一处理）
        output_path = image_service.generate_image(
            'product',
            data
        )
        # 返回图片的base64编码
        with open(output_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
