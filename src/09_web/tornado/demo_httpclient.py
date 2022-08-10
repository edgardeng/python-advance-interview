import time

from tornado import gen, httpclient
from tornado.ioloop import IOLoop
import asyncio

async def main():
    t = time.time()
    await fetch_url('http://127.0.0.1:8888')

    await fetch_url('http://127.0.0.1:8889')
    await asyncio.sleep(5)



async def fetch_url(url):
    t = time.time()
    response = await httpclient.AsyncHTTPClient().fetch(url)
    header = response.headers
    result =  'URL:              ' + url + '\r\n'
    result += 'Content-Type:     ' + header.get('Content-Type') + '\r\n'
    result += 'Content-Length:   ' + header.get('Content-Length') + '\r\n'
    result += 'Content-Encoding: ' + str(header.get('X-Consumed-Content-Encoding')) + '\r\n'

    html = response.body.decode(errors="ignore")
    result += html + '\r\n'
    print(result)
    print('time:', time.time() - t)
    return html

if __name__ == "__main__":

    io_loop = IOLoop.current()
    io_loop.run_sync(main)

