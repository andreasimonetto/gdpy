#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
from threading import Thread
from Queue import Queue

class ConsumerThread(Thread):
    def __init__(self, n):
        Thread.__init__(self)
        self.cap = cv2.VideoCapture(n)
        self.queue = Queue()
        self.running = True
        self.start()

    def run(self):
        while self.cap.isOpened() and self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            self.queue.put(frame)
        self.cap.release()
        self.running = False

    def get(self):
        return self.queue.get()

    def frames_num(self):
        return self.queue.qsize()

if __name__ == '__main__':
    fd = os.open('/dev/gdpymod', os.O_RDWR)
    #im = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

    cam = ConsumerThread(0)
    try:
        while cam.is_alive():
            frame = cam.get()
            while cam.frames_num() > 0:
                print 'SKIP'
                frame = cam.get()
            h, w = frame.shape[:2]
            h = (int(round(h * 1.08)) >> 1) << 1
            frame = cv2.flip(cv2.resize(frame[:, ((w - h) // 2):h], dsize=(64, 64)), 1).reshape((4096, 3))
            t = (frame[:, 0] >> 6) << 4
            t |= (frame[:, 1] >> 6) << 2
            t |= (frame[:, 2] >> 6)
            os.write(fd, t.tostring())
    except:
        pass

    cam.running = False
    #cam.join()
    os.close(fd)
