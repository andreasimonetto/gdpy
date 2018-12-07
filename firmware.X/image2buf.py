#!/usr/bin/env python

import sys
import numpy as np
import cv2

if __name__ == '__main__':
    assert len(sys.argv) > 1
    print '#include <stdint.h>\n'
    for n, path in enumerate(sys.argv[1:]):
        im = cv2.imread(path)
        assert im.shape == (64, 64, 3)
        print 'const uint8_t FRAME_%02d[] = { %s };' % (n, ', '.join([ '0x%02x' % (((b >> 6) << 4) | ((g >> 6) << 2) | (r >> 6)) for b, g, r in im.reshape(64*64, 3) ]))
    print '\nconst uint8_t* FRAMES[] = {\n  %s\n};' % (',\n  '.join([ 'FRAME_%02d' % i for i in range(n + 1) ]))
