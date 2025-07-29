# 海报制作 Python 项目

这个项目提供了一个简单易用的海报生成器，可以通过HTTP服务和前端页面来创建包含图片、文字和颜色区域的海报。

## 功能特点

- 设置海报尺寸和背景颜色
- 添加图片并调整大小
- 加载自定义字体
- 添加文本并设置对齐方式
- 添加颜色区域
- 保存和预览海报
- 通过HTTP服务提供API接口
- 提供直观的前端操作页面

## 安装指南

1. 克隆或下载此项目到本地

2. 安装所需依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：使用HTTP服务和前端页面

1. 启动服务

```bash
# 赋予启动脚本执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

2. 打开浏览器，访问前端页面

在浏览器中输入 `http://localhost:5000`，然后点击页面中的链接打开海报生成器前端页面。

3. 使用前端页面创建海报

- 设置海报尺寸和背景颜色
- 添加颜色区域
- 添加文本内容
- 添加图片
- 点击生成海报按钮
- 下载生成的海报

### 方法二：直接使用Python代码

1. 导入 `PosterGenerator` 类

```python
from poster_generator import PosterGenerator
```

2. 创建海报生成器实例

```python
# 创建一个 800x600 的白色海报
poster = PosterGenerator(800, 600, background_color=(255, 255, 255))
```

3. 添加颜色区域

```python
# 在指定位置添加一个蓝色区域
poster.add_color_region((50, 50), (700, 100), (50, 150, 250))
```

4. 加载字体

```python
# 加载字体文件
poster.load_font('title_font', 'path/to/font.ttf', 40)
poster.load_font('body_font', 'path/to/font.ttf', 20)
```

5. 添加文本

```python
# 添加标题文本，居中对齐
poster.add_text('海报标题', (400, 80), 'title_font', color=(255, 255, 255), align='center')

# 添加正文文本，左对齐
poster.add_text('这是正文内容', (100, 200), 'body_font')
```

6. 添加图片

```python
# 添加图片并调整大小
poster.add_image('path/to/image.jpg', (200, 220), (400, 200))
```

7. 保存和显示海报

```python
# 保存海报
poster.save('output_poster.jpg')

# 显示海报
poster.show()
```

## API接口说明

### 生成海报

- URL: `/generate`
- 方法: `POST`
- 请求体参数:
  - `width`: 海报宽度
  - `height`: 海报高度
  - `background_color`: 背景颜色，RGB格式数组
  - `color_regions`: 颜色区域数组
  - `texts`: 文本数组
  - `images`: 图片数组

示例请求:

```json
{
  "width": 800,
  "height": 600,
  "background_color": [255, 255, 255],
  "color_regions": [
    {
      "position": [50, 50],
      "size": [700, 100],
      "color": [50, 150, 250]
    }
  ],
  "texts": [
    {
      "content": "海报标题",
      "position": [400, 80],
      "font_name": "default",
      "color": [255, 255, 255],
      "align": "center"
    }
  ],
  "images": []
}
```

## 示例

查看 `example.py` 文件，了解完整的代码使用示例。

## 注意事项

- 确保字体文件路径正确
- 确保图片文件路径正确
- 颜色使用 RGB 格式，范围为 0-255
- 启动服务前请确保已安装所有依赖