#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
from time import sleep

def blit(dpy, im):
    im = cv2.resize(im, dsize=(64, 64)).reshape((4096, 3))
    #im = im.reshape((4096, 3))
    t = (im[:, 0] >> 6) << 4
    t |= (im[:, 1] >> 6) << 2
    t |= (im[:, 2] >> 6)
    os.write(dpy, t.tostring())

if __name__ == '__main__':
    dpy = os.open('/dev/gdpymod', os.O_RDWR)
    im = np.zeros((256, 256, 3), dtype=np.uint8)
    while True:
        c = np.random.randint(0, 256, 3)
        for r in range(1, 256, 4):
            cv2.circle(im, (128, 128), r, c, -1)
            blit(dpy, im)
            sleep(0.016)

    os.close(dpy)
