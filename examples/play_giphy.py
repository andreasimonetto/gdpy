#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
from PIL import Image
from urllib import urlencode
from urllib2 import urlopen
from time import time, sleep
import json
from StringIO import StringIO
from random import choice

GIPHY_API_KEY = 'yourkeyhere'

fname = "tmp.gif"

if __name__ == '__main__':
    tags = sys.argv[1:] if len(sys.argv) >= 2 else []

    fd = os.open('/dev/gdpymod', os.O_RDWR)
    #im = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

    while True:
        try:
            #print 'Getting random gif'
            ## Read the gif from the web, save to the disk
            params = { 'api_key': GIPHY_API_KEY }
            if len(tags) > 0:
                params['tag'] = choice(tags)
            immeta = json.loads(urlopen('http://api.giphy.com/v1/gifs/random?%s' % (urlencode(params)), timeout=3).read())
            imurl = immeta.get('data').get('images').get('fixed_height').get('url')
            print 'Downloading %s' % (imurl)
            imtitle = immeta.get('data').get('title')
            imp = StringIO(urlopen(imurl, timeout=3).read())

            #print .get('meta', {}).get('url')
            #imbytes = bytearray(imdata)
            #open(fname,"wb+").write(imdata)

            ## Read the gif from disk to `RGB`s using `imageio.miread`
            #print 'Opening'
            frame = Image.open(imp)
            #gif = imageio.mimread(fname)
            #nums = len(gif)
            #print("Total {} frames in the gif!".format(nums))

            # convert form RGB to BGR

            # Get FPS
            #print 'Get FPS'
            try:
                nframes = 0
                while True:
                    nframes += 1
                    frame.seek(frame.tell() + 1)
            except EOFError:
                frame.seek(0)
            framerate = min(60, max(nframes, 1000. / frame.info.get('duration', 10)))
            loop = bool(frame.info.get('loop')) # Returns always False :(

            imtitle = imtitle.strip()
            if len(imtitle) == 0:
                imtitle = '<no title>'
            print imtitle
            print
            # Scrolling text
            x = 70
            exiting = False
            while True:
                t = np.zeros((64, 64), dtype=np.uint8)
                cv2.putText(t, imtitle, (x, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0x3f, 2)
                os.write(fd, t.tostring())
                sleep(.016)

                x -= 1
                if exiting:
                    if np.all(t == 0):
                        break
                else:
                    if np.any(t != 0):
                        exiting = True

            sleep(1)

            k = 0
            t = time()
            while True:
                #for frame in [ cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif ]:
                im = cv2.resize(np.uint8(frame.convert('RGB')), dsize=(64, 64))
                t = im[:, :, 0] >> 6
                t |= (im[:, :, 1] >> 6) << 2
                t |= (im[:, :, 2] >> 6) << 4

                sys.stderr.write('+\r' if k % 2 == 0 else '-\r')
                sys.stderr.flush()
                k = (k + 1) % 2

                os.write(fd, t.tostring())
                try:
                    frame.seek(frame.tell() + 1)
                except EOFError:
                    frame.seek(0)
                    if not loop:
                        break
                sleep(float(framerate)**-1)
                if loop and time() - t > 5:
                    break

        except KeyboardInterrupt:
            break
        except Exception:
            pass

    os.close(fd)
