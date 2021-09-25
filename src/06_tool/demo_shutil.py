"""
@author: edgardeng
@date:   2021-01-04.
-  shutil — High-level file operations https://docs.python.org/3.3/library/shutil.html
"""
import shutil
from pathlib import Path


# print(shutil.__version__)

def basic_usage():
    # copy
    shutil.copyfile('index.py', 'b.txt')

    # move
    shutil.move('b.txt', 'c.txt')
    # copy dir
    shutil.copytree('test', 'test2')
    # del dir
    shutil.rmtree('test2')

    # 查找文件 (Finding files)


def others():
    print(shutil.which('python'))  # 返回当给定的 cmd 被调用时将要运行的可执行文件的路径


def copy_obj():
    """ 多个文件复制到一个文件 """
    bufsize = 16 * 1024

    with open('test.txt', 'wb') as out_file:
        cwd = Path.cwd()
        for child in cwd.iterdir(): # 当心死循环
            print(child)
            if child.is_file() and child.name != 'test.txt':
                with child.open('rb') as in_file:
                    shutil.copyfileobj(in_file, out_file)


def archiving_operations():
    # shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])

    # shutil.make_archive('test', format='tar', root_dir='test')
    # shutil.make_archive('test', format='gztar', root_dir='test')
    # shutil.make_archive('test', format='zip', root_dir='test')

    shutil.unpack_archive('test.zip', r'D:\workspace\hello-python\part02_python_advance\abc')
    # shutil.unpack_archive('test.tar.gz', 'test-gz')
    # shutil.unpack_archive('test.tar', 'test-tar')


if __name__ == '__main__':
    # basic_usage()
    archiving_operations()
    # others()
    # copy_obj()
