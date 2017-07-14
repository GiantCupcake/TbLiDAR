# -*- coding: utf-8 -*-
"""
Attempt to find peaks from our data, then fitting a gaussian over those peaks.
This should give us a list of peaks sorted by height.
But more than having the information on just the peak, we will try to fit a 
gaussian over each peak in order to find its center.
"""
import numpy as np
import matplotlib.pyplot as plt
import peakutils.peak as peak
import peakutils.plot as peakplot
import os
import sys

folder = 'Donnees_brutes/tractopelle'
data1 = np.load(os.path.join(os.getcwd(), folder,'depthMap.npz'))
#['dataCubeAVG', 'sigma', 'depthMap', 'average']

data2 = np.load(os.path.join(os.getcwd(), folder,'image000.npz'))
#['tof', 'tdc1', 'tofAxis', 'info', 'dataCube', 'distanceAxis', 'cnt', 'tdc2']

#Dans ref1.npz, uniquement correction
data3 = np.load('Donnees_brutes/ref1.npz')


cube = data1['dataCubeAVG']
distAxis = data2['distanceAxis']
corrections = data3['correction']



def depthMapFromPeaks(dataCube, distanceAxis):
    nbPix = dataCube.shape[0]
    depthMap = np.zeros([nbPix,nbPix])
    for indX in range(nbPix):
        for indY in range(nbPix):
            if not np.any(np.isnan(dataCube[indX,indY,:])):
                imax = peak.indexes(dataCube[indX,indY,:], thres = 0.95, min_dist = 20)[0]
                print("Not stuck")
                minPeak = imax - 20 if imax - 20 >= 0 else 0
                maxPeak  = imax + 20 if imax + 20 < distanceAxis.size else distanceAxis.size -1
                A, mu, sigma = peak.gaussian_fit(distanceAxis[minPeak:maxPeak], dataCube[indX,indY,minPeak:maxPeak], center_only = False)
                
                depthMap[indX,indY] = mu
                print("gaussian at : ", mu)
            else:
                print("No gaussian found")
                depthMap[indX,indY] = np.nan
    return depthMap



def depthMapFromConvolution(dataCube, distanceAxis):
    # Filter for correlation (Depth Map calculation)
    distanceAxisFilter = np.arange(-2,2,3.75e-2)
    mu = 0
    sigma = 0.15
    gaussFilter = np.exp(-(distanceAxisFilter-mu)**2/(2*sigma**2))
    
    nbPix = dataCube.shape[0]
    depthMap = np.zeros([nbPix,nbPix])
    for indX in range(nbPix):
        for indY in range(nbPix):
            tt = np.correlate(dataCube[indX,indY,:], gaussFilter, "full")
            argMaxTT = tt.argmax(axis=0)-53 # -53 because gaussFilter = 106 elements, shift of 53 in correlation
            if(0 <= argMaxTT and argMaxTT <= (len(distanceAxis)-1)):
                depthMap[indX,indY] = distanceAxis[argMaxTT]
            else:
                depthMap[indX,indY] = np.nan
    return depthMap

            
depthMap = depthMapFromConvolution(cube, distAxis) - corrections
#depthMap2 = depthMapFromPeaks(cube, distAxis) - corrections


#Redondant ?
depthMap[64:68,:] = np.ones([4,132])*np.nan
depthMap[:,64:68] = np.ones([132,4])*np.nan

print("Done building from convolution")
        

         
distanceMin = 60
distanceMax = 120

fig=plt.figure()
plt.title('Depth Map', fontsize=18)
ax1 = plt.subplot(1,1,1)
im = ax1.imshow(depthMap,vmin=distanceMin, vmax=distanceMax, interpolation='none', cmap=plt.get_cmap('jet'))
plt.axis('off')
cb = plt.colorbar(im, ax=ax1)
cb.set_label('Height [m]',fontsize=16)


