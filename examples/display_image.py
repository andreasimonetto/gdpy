#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
from time import sleep

if __name__ == '__main__':
    assert len(sys.argv) == 2

    fd = os.open('/dev/gdpymod', os.O_RDWR)
    im = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

    im = cv2.resize(im, dsize=(64, 64)).reshape((4096, 3))
    t = (im[:, 0] >> 6) << 4
    t |= (im[:, 1] >> 6) << 2
    t |= (im[:, 2] >> 6)
    os.write(fd, t.tostring())
    sleep(5)
    os.close(fd)
