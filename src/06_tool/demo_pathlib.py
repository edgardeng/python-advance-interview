# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-06-01
# @file:   demo for pathlib usage
import os
import pathlib
from pathlib import Path


def main():
    print('os', '*' * 30)
    me = os.getcwd()
    print('当前文件路径:', me)
    print('上层目录:', os.path.dirname(me))
    print('拼接目录:', os.path.join(os.path.dirname(me), 'test'))

    print()
    print('pathlib', '-' * 30)
    v = Path.cwd()
    print('当前文件路径:', v)
    print('上层目录:', v.parent, v.parent.parent)
    paths = ["test", "test.txt"]
    print('拼接目录:', v.parent.joinpath(*paths))
    test = v.joinpath('test', 'a', 'b')
    print('创建目录:', test)
    test.mkdir(parents=True, exist_ok=True)
    print('重命名:', test)
    # Path('demo_pathlib.py').rename('test/demo_pathlib.txt') # = move
    p = Path(__file__)
    print(p)
    print('递归:', [child for child in v.iterdir()])
    print('查找:', [child.name for child in v.rglob('*')])
    print('查找:', [child.name for child in v.glob('demo_*')])
    print('查找:', [child.name for child in v.glob('**/*')]) # 一直往下

# pathlib的常用基本方法
# Path.parents　　# 返回所有上级目录的列表
# Path.parts　　# 分割路径 类似os.path.split(), 不过返回元组
# Path.root　　# 返回路径的根目录
# Path.is_dir()　　# 判断是否是目录
#
# Path.is_file()　　# 是否是文件
#
# Path.exists()　　# 判断路径是否存在
#
# Path.open()　　# 打开文件(支持with)
#
# Path.resolve()　　# 返回绝对路径
#
# Path.cwd()　　# 返回当前目录
#
# Path.iterdir()　　# 遍历目录的子目录或者文件
#
# Path.mkdir()　　# 创建目录
# Path.rename()　　# 重命名路径
# Path.unlink()　　# 删除文件或目录(目录非空触发异常)
# Path.joinpath()　　# 拼接路径


if __name__ == '__main__':
    main()
