# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-09-27
# @file:   09_web.tornado
from typing import List

from tornado.web import RequestHandler, Application, GZipContentEncoding
from tornado.ioloop import IOLoop
import time

class MainHandler(RequestHandler):
    def get(self):

        d = {}
        letter = '1234567890abcdefghijklmnopqrst'
        for i in range(30):
            d[letter[i]] = letter * (i % 5 + 50)
        d['timestamp'] = time.strftime('Y%Y-%m-%d %H:%M:%S', time.localtime())
        self.write(d)

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get('exc_info')
        msg = exc_info[1] if exc_info else '系统错误'
        # exc_info[2]
        self.write(f'Error:{status_code} with:{msg}')


def main(gz, port):
    app = Application(
        [
            (r"/", MainHandler),
        ],
        autoreload=True,
        transforms=[GZipContentEncoding] if gz else []
    )
    app.listen(port)
    print(f'http://127.0.0.1:{port}', gz)
    IOLoop.current().start()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'this is a description')
    parser.add_argument('--gz', '-z', action = 'store_true', help = 'open gzip')
    parser.add_argument('--port', '-p', type=str,default=8888)
    # 将变量以标签-值的字典形式存入args字典
    args = parser.parse_args()


    main(args.gz,args.port)
