import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_service import ImageService
from utils import preprocess_product_data
from PIL import Image

# 使用工具函数预处理数据
input_data = {
    'save_type': 'webp',
    'width': 1024,
    'height': 1024,
    'bracelet_image': 'https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp'
}

data = preprocess_product_data(input_data)

image_service = ImageService()

print("开始生成图片...")
start_time = time.time()

output_path = image_service.generate_image('product', data)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"图片生成完成，保存路径: {output_path}")
print(f"生成耗时: {elapsed_time:.2f} 秒")

# 预览图片
try:
    image = Image.open(output_path)
    print(f"图片尺寸: {image.size}")
    image.show()
except Exception as e:
    print(f"预览图片失败: {e}")