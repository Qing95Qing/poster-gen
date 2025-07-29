from . import PosterGenerator
import os
from . import get_local_path

# 创建海报生成器实例
poster = PosterGenerator(800, 600, background_color=(240, 240, 240))

# 添加颜色区域
poster.add_color_region((50, 50), (700, 100), (50, 150, 250))
poster.add_color_region((50, 450), (700, 100), (50, 150, 250))

# 加载字体
# 可以使用本地路径或网络URL
font_path = 'https://zhuluoji.cn-sh2.ufileos.com/resources/%E8%83%A1%E6%99%93%E6%B3%A2%E6%B5%AA%E6%BC%AB%E5%AE%8B.ttf'
local_font_path = get_local_path(font_path)

# 如果上面的字体加载失败，可以尝试系统默认字体
if not local_font_path:
    # 如果你是 macOS 用户
    mac_font_path = '/System/Library/Fonts/PingFang.ttc'
    # 如果你是 Windows 用户
    windows_font_path = 'C:/Windows/Fonts/simhei.ttf'
    
    if os.path.exists(mac_font_path):
        local_font_path = mac_font_path
    elif os.path.exists(windows_font_path):
        local_font_path = windows_font_path
    else:
        local_font_path = None

if local_font_path:
    poster.load_font('title_font', local_font_path, 40)
    poster.load_font('body_font', local_font_path, 20)

    # 添加文本
    poster.add_text('海报标题', (400, 80), 'title_font', color=(255, 255, 255), align='center')
    poster.add_text('这是一个海报制作示例', (400, 180), 'body_font', align='center')
    poster.add_text('底部信息', (400, 480), 'body_font', color=(255, 255, 255), align='center')
else:
    print('未找到合适的字体文件，无法添加文本')

# 添加图片
# 可以使用本地路径或网络URL
image_path = 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/assistant-lg.png'
local_image_path = get_local_path(image_path)

if local_image_path:
    poster.add_image(local_image_path, (200, 220), (400, 200))
else:
    print(f'获取图片失败: {image_path}')
    # 添加一个占位符矩形
    poster.add_color_region((200, 220), (400, 200), (200, 200, 200))
    # 在占位符上添加文字
    if local_font_path:
        poster.add_text('图片占位符', (400, 320), 'body_font', align='center')

# 保存海报
output_path = 'output_poster.jpg'
poster.save(output_path)

# 显示海报
poster.show()

print(f'海报已生成并保存到: {output_path}')