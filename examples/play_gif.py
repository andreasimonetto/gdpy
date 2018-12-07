#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
from PIL import Image
import urllib2
from time import time, sleep

fname = "tmp.gif"

if __name__ == '__main__':
    assert len(sys.argv) in [ 2, 3 ]

    framerate = int(sys.argv[2]) if len(sys.argv) == 3 else 1

    fd = os.open('/dev/gdpymod', os.O_RDWR)
    #im = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)


    ## Read the gif from the web, save to the disk
    imdata = urllib2.urlopen(sys.argv[1]).read()
    imbytes = bytearray(imdata)
    open(fname,"wb+").write(imdata)

    ## Read the gif from disk to `RGB`s using `imageio.miread`
    frame = Image.open(fname)
    #gif = imageio.mimread(fname)
    #nums = len(gif)
    #print("Total {} frames in the gif!".format(nums))

    # convert form RGB to BGR

    # Get FPS
    try:
        nframes = 0
        while True:
            nframes += 1
            frame.seek(frame.tell() + 1)
    except EOFError:
        frame.seek(0)
    framerate = max(.5, nframes * 10. / frame.info.get('duration', 10))

    while True:
    #for frame in [ cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif ]:
        d = cv2.resize(np.uint8(frame.convert('RGB')), dsize=(64, 64)).reshape((4096, 3))
        t = d[:, 0] >> 6
        t |= (d[:, 1] >> 6) << 2
        t |= (d[:, 2] >> 6) << 4
        os.write(fd, t.tostring())
        try:
            frame.seek(frame.tell() + 1)
        except EOFError:
            frame.seek(0)
        sleep(float(framerate)**-1)

    os.close(fd)
