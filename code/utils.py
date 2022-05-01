import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

zmin = 0.0
zmax = 255.0

def weight(val):
    if val<=128:
        return val-zmin
    else: 
        return zmax-val

class exposure_set:
    def __init__(self, filedir, N, N_sqrt, lamb):
        #read the csv files
        self.filedir = filedir
        self.filenames = [line.rstrip() for line in open('filenames.csv')]
        self.speeds = [float(line.rstrip()) for line in open('speed.csv')]
        self.img_list = []
        self.N = N #number of sample points
        self.N_sqrt = N_sqrt 
        self.lamb = lamb #smoothing factor
        
        #read images
        for name in self.filenames:
            img = cv2.imread(filedir+name)
            self.img_list.append(img)

        self.p = len(self.img_list) #number of images
        self.height, self.width = self.img_list[0].shape[:2]
        
    def get_zsamps(self):
        zb_samps = []
        zg_samps = []
        zr_samps = []
        hspace = math.floor(self.height/self.N_sqrt)
        wspace = math.floor(self.width/self.N_sqrt)
        for img in self.img_list:
            zb = []
            zg = []
            zr = []
            for i in range(self.N_sqrt):
                for j in range(self.N_sqrt):
                    zb.append(img[i*hspace, j*wspace, 0])
                    zg.append(img[i*hspace, j*wspace, 1])
                    zr.append(img[i*hspace, j*wspace, 2])
            zb_samps.append(zb)
            zg_samps.append(zg)
            zr_samps.append(zr)

        zb_samps = np.array(zb_samps)
        zg_samps = np.array(zg_samps)
        zr_samps = np.array(zr_samps)

        return zb_samps, zg_samps, zr_samps

    def get_g(self, zsamp):
        n = 256
        A = np.zeros((self.N*self.p+n+1, n+self.N), dtype=np.float32)
        b = np.zeros((self.N*self.p+n+1), dtype=np.float32)
        k = 0
        
        for i in range(self.N):
            for j in range(self.p):
                zij = zsamp[j, i]
                wij = weight(zij)
                A[k, zij] = wij
                A[k, n+i] = -wij
                b[k] = wij*math.log(self.speeds[j])
                k = k+1
        
        A[k, 128] = 1
        k = k+1
        for i in range(n-2):
            A[k, i] = self.lamb*weight(i+1)
            A[k, i+1] = -2*self.lamb*weight(i+1)
            A[k, i+2] = self.lamb*weight(i+1)
            k = k+1

        x = np.linalg.lstsq(A, b)[0]
        g = x[:256]

        return g

    def get_E(self, g, channel): 
        """
        g: the computed g
        channel: the color channel we are dealing with 
        """
        E = np.zeros((self.height, self.width), dtype=np.float32)
        for hh in range(self.height):
            for ww in range(self.width):
                deno = 0
                numer = 0
                for j in range(self.p):
                    zij = self.img_list[j][hh, ww, channel]
                    wij = weight(zij)
                    deno+=wij
                    numer+= (wij*(g[zij]-math.log(self.speeds[j])))
                    if deno==0:
                        E[hh, ww] = math.exp(numer)
                    else:
                        E[hh, ww] = math.exp(numer/deno)
        return E