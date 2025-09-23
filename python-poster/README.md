# 图片生成服务

## 快速开始

### 安装依赖

```bash
pip3 install -r requirements.txt
```

### 启动服务

```bash
# 使用启动脚本
./start.sh

# 或直接运行
python3 app.py
```

服务将在 `http://localhost:5001` 启动

## API 接口

### 1. 生成手串商品图片

**POST** `/generate/product_image`

请求体示例：

```json
{
    "save_type": "webp",
    "width": 1024,
    "height": 1024,
    "bracelet_image": "https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp"
}
```

## 项目结构

```
python-poster/
├── app.py          # 主应用文件
├── image_service.py       # 图片生成服务
├── config.py             # 配置管理
├── utils.py              # 工具函数
├── generators/           # 图片生成器
│   ├── base.py          # 基础生成器
│   ├── poster.py        # 海报生成器
│   ├── product.py       # 商品图生成器
│   └── banner.py        # 横幅生成器
├── requirements.txt      # 依赖文件
└── start.sh      # 启动脚本
```

## 使用示例

### Python 代码示例

```python
import requests

# 生成海报
data = {
    "save_type": "webp",
    "width": 1024,
    "height": 1024,
    "bracelet_image": "https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp"
}

response = requests.post('http://localhost:5001/generate/product_image', json=data)
with open('output.jpg', 'wb') as f:
    f.write(response.content)
```

### cURL 示例

```bash
curl -X POST http://localhost:5001/product_image\
  -H "Content-Type: application/json" \
  -d '{
    "width": 1024,
    "height": 1024,
    "bracelet_image": "https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp"
  }' \
  --output product-image.jpg
```

## 配置

可以通过环境变量配置服务：

- `HOST`: 服务主机地址（默认：0.0.0.0）
- `PORT`: 服务端口（默认：5001）
- `FLASK_DEBUG`: 调试模式（默认：True）

