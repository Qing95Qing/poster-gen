import os
import tempfile
import urllib.request
import uuid

def is_url(path):
    """检查路径是否为URL

    Args:
        path (str): 路径

    Returns:
        bool: 是否为URL
    """
    return path.startswith('http://') or path.startswith('https://')


def download_file(url):
    """下载网络文件到临时目录

    Args:
        url (str): 文件URL

    Returns:
        str: 临时文件路径，如果下载失败则返回None
    """
    try:
        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        file_ext = os.path.splitext(url)[1]
        temp_filename = f'{uuid.uuid4()}{file_ext}'
        temp_filepath = os.path.join(temp_dir, temp_filename)

        # 下载文件
        urllib.request.urlretrieve(url, temp_filepath)
        return temp_filepath
    except Exception as e:
        print(f'下载文件失败: {e}')
        return None


def get_local_path(path):
    """获取本地文件路径，如果是URL则下载到临时目录

    Args:
        path (str): 文件路径或URL

    Returns:
        str: 本地文件路径，如果失败则返回None
    """
    if is_url(path):
        return download_file(path)
    elif os.path.exists(path):
        return path
    else:
        return None


def create_product_data_template(save_type='webp', width=1024, height=1024, bracelet_image_path=None):
    """创建商品图片生成的data模板
    
    Args:
        save_type (str): 保存类型，默认为'webp'
        width (int): 图片宽度，默认为1024
        height (int): 图片高度，默认为1024
        bracelet_image_path (str): 手镯图片路径，如果为None则使用默认路径
    
    Returns:
        dict: 处理后的data字典
    """
    # 默认的手镯图片路径
    default_bracelet_path = 'https://zhuluoji.cn-sh2.ufileos.com/dev/drafts/draft-bc553a2cef56dc0.webp'
    
    # 使用提供的路径或默认路径
    bracelet_path = bracelet_image_path if bracelet_image_path else default_bracelet_path
    
    data_template = {
        'width': width,
        'height': height,
        'background_color': (240, 240, 240),
        'save_type': save_type,
        'images': [
            {
                'key': 'background-image',
                'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/result-image-texture.png',
                'position': (0, 0),
                'size': (width, height),
            },
            {
                'key': 'side-background',
                'path': 'https://zhuluoji.cn-sh2.ufileos.com/dev/background/265.webp',
                'position': (0, 0),
                'crop': {
                    'left': 200,
                    'right': 542,
                    'top': 0,
                    'bottom': height
                }
            },
            {
                'key': 'brand-logo',
                'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/reuslt-image-logo.png',
                'size': (64, 106),
                'position': (651, 459),
            },
            {
                'key': 'bracelet-image',
                'path': bracelet_path,
                'size': (480, 480),
                'position': (443, 272),
            },
            {
                'key': 'slogan-image',
                'path': 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/result-image-slogan.png',
                'size': (256, 33),
                'position': (555, 925),
            }
        ]
    }
    
    return data_template


def preprocess_product_data(input_data):
    """预处理商品图片生成数据
    
    Args:
        input_data (dict): 输入的数据，包含以下可选字段：
            - save_type: 保存类型
            - width: 图片宽度
            - height: 图片高度
            - bracelet_image: 手镯图片路径
    
    Returns:
        dict: 处理后的完整data字典
    """
    # 从输入数据中提取参数，如果没有提供则使用默认值
    save_type = input_data.get('save_type', 'webp')
    width = input_data.get('width', 1024)
    height = input_data.get('height', 1024)
    bracelet_image = input_data.get('bracelet_image')
    
    # 创建模板数据
    processed_data = create_product_data_template(
        save_type=save_type,
        width=width,
        height=height,
        bracelet_image_path=bracelet_image
    )
    
    # 如果输入数据中有其他字段，可以在这里进行合并
    # 例如：processed_data.update(input_data)
    
    return processed_data