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