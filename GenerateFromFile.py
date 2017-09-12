# -*- coding: utf-8 -*-
"""
This class is used to read a numpy archive (.npz) containing Data coming from
the LiDAR camera. To read data, instanciate a LidarDataInterpreter object with
the path to your archive. You can then call a method getXXX to receive a
generator object that generate InterestPoints from the data.

InterestPoints are points placed in the 3Dimensional euclidian space to which
you can attach an information of intensity and variation.

Created on Fri Jun 02 15:25:31 2017

@author: Maxime Piergiovanni
"""
import numpy as np
import os
import time


def display_time(func):
    def decorator(self, *args):
        startTime = time.time()
        try:
            toReturn = func(self,*args)
        except Exception as e:
            raise e
            print("Error {}".format(e.args[0]))
        finally:
            print('{0} terminated, took {1} seconds'.format(func, time.time() - startTime))
            return toReturn
    return decorator

class LidarDataInterpreter:
    def __init__(self, _folder):
        self.data = np.load(os.path.join(os.getcwd(), _folder, 'depthMap.npz'))
        self.distanceAxis = self.data['distanceAxis']
        self.dMin = 0
        self.dMax = self.distanceAxis.size-1
        

    """
    Place points in 3D space by reading the "average" matrix in the archive.
    "average" contains a depth map.
    Intensity is computed by summing all intensities for each pixel
    Sigma is precalculated from the variation between numerous captures, it is
    stored as "sigma" in the archive.
    """        
    def getPointsFromDepthMap(self):
        average = self.data['average']
        size = average.shape[0]
        alpha = np.radians(2.9)
        
        sumCountsAVG = np.sum(self.data['dataCubeAVG'][:,:,self.dMin:self.dMax],axis=2)
        sumCountsAVG[64:68,:] = np.ones([4,132])*np.nan
        sumCountsAVG[:,64:68] = np.ones([132,4])*np.nan
        
        sumCountsAVG /= np.nanmax(sumCountsAVG)
        
        sigma = self.data['sigma']
        sigma /= np.nanmax(sigma)
        
        def pointGenerator():
            for iy in range(size):
                for ix in range(size):
                    #ici image 1
                    z = average[iy,ix]
                    if np.isnan(z):
                        continue
                    x = -1 * (ix-size/2) * z * np.tan(alpha) / (size/2)
                    y = -1 * (iy-size/2) * z * np.tan(alpha) / (size/2)
                    point = InterestPoint((x,y,z))
                    point.intensity = sumCountsAVG[iy,ix]
                    point.sigma = sigma[iy,ix]
                    yield point
                    
        return pointGenerator()
    
    """
    Place a point for every single entry in the matrix 'dataCubeAVG'.
    Intensity for a point is simply the value from the matrix.
    Sigma is not computed so it is set to 1.0, could be 0.0.
    """        
    def getFullCube(self):
        dataCube = self.data['dataCubeAVG']
        size = dataCube.shape[0]
        alpha = np.radians(2.9)
        
        maxValue = np.max(dataCube)
        dataCube /= maxValue
        def pointGenerator():
            for iy in range(dataCube.shape[0]):
                if 64 <= iy < 68:
                    continue
                for ix in range(dataCube.shape[1]):
                    if 64 <= ix < 68:
                        continue
                    for iz in range(dataCube.shape[2]):
                        if dataCube[ix,iy,iz] == 0:
                            continue
                        z = self.distanceAxis[iz]
                        if np.isnan(z):
                            print("Found a isNan, not normal", ix, iy, iz)
                            continue
                        x = -1 * (ix-size/2) * z * np.tan(alpha) / (size/2)
                        y = -1 * (iy-size/2) * z * np.tan(alpha) / (size/2)
                        point = InterestPoint((x,y,z))
                        point.intensity = dataCube[iy,ix,iz]
                        point.sigma = 1.0
                        yield point
        return pointGenerator()

    """
    Customize this reader as you want.
    What's important is to not change the structure of the function
    Get the data you need before the PointGenerator() function.
    Interpret the data to create your own InterestPoints, then use yield
    to ensure the function is a Generator.
    """
    def getCustomReader(self):
        dataCube = self.data['dataCubeAVG']
        size = dataCube.shape[0]
        def pointGenerator():
            for iy in range(size):
                for ix in range(size):
                    point = InterestPoint((0,0,0))
                    point.intensity = 0
                    point.sigma = 0
                    yield point
        return pointGenerator()


class InterestPoint:
    def __init__(self, pos, intensity = None, variation = None):
        self.pos = pos
        self.intensity = intensity
        self.sigma = variation
        

    
