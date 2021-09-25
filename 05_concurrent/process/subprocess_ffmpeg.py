# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-08
# @file:
import time

import cv2, subprocess
import threading, queue


class Live(object):
    def __init__(self, rtmp_url, rtsp_url, fps):

        self.command = ""
        self.rtmp_url = rtmp_url
        self.rtsp_url = rtsp_url
        self.fps = fps
        print(self.rtsp_url, self.rtmp_url, self.fps)
        super(Live, self).__init__()

    def read_frame(self):
        print("开启推流")
        cap = cv2.VideoCapture(self.rtsp_url)
        # Get video information
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(fps, width, height)
        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(self.fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmp_url]
        # read webcamera
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                print("Opening camera is failed")
                break
            self.frame_queue.put(frame.tobytes())

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = subprocess.Popen(self.command, stdin=subprocess.PIPE)
                break
        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                # write to pipe
                t0 = time.time()
                p.stdin.write(frame)
                p.stdin.flush()
                t1 = time.time()
                if t1 - t0 > 0.2:
                    print('use:' + str(t1 - t0))

    def start(self):
        self.frame_queue = queue.Queue()
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.start() for thread in threads]


if __name__ == '__main__':
    rtsp_url = 'rtsp://admin:juliang1234@10.30.21.230:443/rtsp/streaming?channel=1&subtype=0'
    rtmp_url = 'rtmp://localhost:1935/stream/test'
    Live(rtmp_url, rtsp_url, 25).start()
