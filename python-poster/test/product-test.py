import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_service import ImageService
from PIL import Image

# 输入数据（数据预处理在image_service中统一处理）
input_data = {
    'save_type': 'webp',
    'width': 1024,
    'height': 1024,
    'bracelet_image': 'https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-d155d548090ed80.webp',
    'background_image': 'https://zhuluoji.cn-sh2.ufileos.com/dev/background/255.webp'
}

image_service = ImageService()

print("开始生成图片...")
start_time = time.time()

output_path = image_service.generate_image('product', input_data)

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