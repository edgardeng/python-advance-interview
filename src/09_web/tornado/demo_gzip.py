# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-09-27
# @file:   09_web.tornado
from typing import List

from tornado.web import RequestHandler, Application, GZipContentEncoding
from tornado.ioloop import IOLoop


class MainHandler(RequestHandler):

    def get(self):
        d = {}
        letter = '1234567890qqwweerrttyyuuiioopp'
        for i in range(30):
            d[letter[i % 30]] = letter * 10
            d[letter[i % 30:-1]] = letter * 20
            d[letter[i % 30:-2]] = letter * 30
            d[letter[i % 30:-3]] = letter * 40

        self.write(d)

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get('exc_info')
        msg = exc_info[1] if exc_info else '系统错误'
        exc_info[2]
        self.write(f'Error:{status_code} with:{msg}')


def main():
    port = 8888
    app = Application(
        [
            (r"/", MainHandler),
        ],
        autoreload=True,
        transforms=[GZipContentEncoding]
    )
    app.listen(port)
    print(f'http://127.0.0.1:{port}')
    IOLoop.current().start()


if __name__ == "__main__":
    main()
