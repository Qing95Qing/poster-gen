"""
简化的图片生成服务
"""

from flask import Flask, request, jsonify, send_file
from image_service import ImageService
from config import Config
from utils import preprocess_product_data
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
    """生成图片"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        if 'width' not in data or 'height' not in data:
            return jsonify({'error': '缺少width或height参数'}), 400

        if 'bracelet_image' not in data:
            return jsonify({'error': '缺少bracelet_image参数'}), 400
        
        processed_data = preprocess_product_data(data)
        # 生成图片
        output_path = image_service.generate_image(
            'product',
            processed_data
        )
        # 返回图片的base64编码
        with open(output_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    """预览图片信息"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        # 生成图片
        output_path = image_service.generate_image(
            data['image_type'],
            data
        )
        
        # 获取文件信息
        file_size = os.path.getsize(output_path)
        
        return jsonify({
            'success': True,
            'image_type': data['image_type'],
            'dimensions': {
                'width': data['width'],
                'height': data['height']
            },
            'file_size': file_size,
            'message': '图片生成成功'
        })
        
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
