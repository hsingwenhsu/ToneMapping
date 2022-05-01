import argparse
import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils


if __name__=='__main__':
    if len(sys.argv)<2:
        print("Usage: python3 main.py $filedir")
    filedir = sys.argv[1]+'/'
    if not os.path.exists(filedir):
        print("Directory "+ filedir+" does not exist!")
        quit()
    # parameters
    N = 900
    N_sqrt = 30
    lamb = 5 #smoothing factor
    photo_set = utils.exposure_set(filedir, N, N_sqrt, lamb)
    zb, zg, zr = photo_set.get_zsamps()
    
    gb = photo_set.get_g(zb)
    gg = photo_set.get_g(zg)
    gr = photo_set.get_g(zr)
    """
    plt.plot(gb, 'bo')
    plt.savefig(filedir+'b.png')
    plt.close()
    plt.plot(gg, 'go')
    plt.savefig(filedir+'g.png')
    plt.close()
    plt.plot(gr, 'ro')
    plt.savefig(filedir+'r.png')
    plt.close()
    """
    Eb = photo_set.get_E(gb, 0)
    Eg = photo_set.get_E(gg, 1)
    Er = photo_set.get_E(gr, 2)

    hdr_image = np.zeros(photo_set.img_list[0].shape, dtype=np.float32)
    hdr_image[:, :, 0] = Eb
    hdr_image[:, :, 1] = Eg
    hdr_image[:, :, 2] = Er
    cv2.imwrite('../data/'+'hdr.hdr', hdr_image)  
    