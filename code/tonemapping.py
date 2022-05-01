import sys
import os
import cv2
import numpy as np

def adaptive_tone_mapping(lw, b, gamma):
    ldmax = 100
    lwmax = np.max(lw)/40
    ld = ldmax*0.01/np.log10(lwmax+1)
    ld = ld*np.log(lw+1)
    tmp = np.log(2+(lw/lwmax+1e-8)**(np.log(b)/np.log(0.7))*8)
    ld = ld/tmp
    ld = ld**(1/gamma)
    return ld

def get_ldr(hdr, bb, bg, br, gb, gg, gr):
    hdr_b = hdr[:, :, 0]
    hdr_g = hdr[:, :, 1]
    hdr_r = hdr[:, :, 2]
    ld_b = adaptive_tone_mapping(hdr_b, bb, gb)
    ld_g = adaptive_tone_mapping(hdr_g, bg, gg)
    ld_r = adaptive_tone_mapping(hdr_r, br, gr)

    ldr = np.zeros(hdr.shape, dtype=np.float32)
    ldr[:, :, 0] = ld_b/(np.max(ld_b)-np.min(ld_b))*255
    ldr[:, :, 1] = ld_g/(np.max(ld_g)-np.min(ld_g))*255
    ldr[:, :, 2] = ld_r/(np.max(ld_r)-np.min(ld_r))*255
    #ldr = ldr.astype('uint8')
    return ldr

if __name__=='__main__':
    filename = sys.argv[1]
    filedir = filename.split('/')[:-1]
    separator = '/'
    filedir = separator.join(filedir)+'/'
    hdr = cv2.imread(filename, cv2.IMREAD_ANYDEPTH)
    #please specify the parameters here
    bb = 10; bg = 10; br = 30;
    gb = 1.8; gg = 2.2; gr = 2.5;
    savename = filename.split('/')[-1].split('.')[0] + '.jpg'
    ldr = get_ldr(hdr, bb, bg, br, gb, gg, gr)
    cv2.imwrite('../result.png', ldr)
    cv2.imwrite('../data/tone_mapped.jpg', ldr)

