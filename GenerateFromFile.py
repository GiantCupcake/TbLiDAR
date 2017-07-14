# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 15:25:31 2017

@author: maxpi
"""
import numpy as np
import os
from matplotlib import cm, colors
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
        self.oneImage = np.load(os.path.join(os.getcwd(), _folder, 'image000.npz'))
        self.correction = np.load('../Donnees_brutes/ref1.npz')['correction']
        #On veut les indices dans l'histogramme correspondant aux distances min / max
        self.distanceAxis = self.oneImage['distanceAxis']
        #self.dMin = int((np.abs(distanceAxis - _dmin)).argmin())
        #self.dMax = int((np.abs(distanceAxis - _dmax)).argmin())
        self.dMin = 0
        self.dMax = self.distanceAxis.size-1
        

             
    def getPointsFromDepthMap(self):
        ###TODO: Doit-on enlever la correction ?
        ###TODO: Pas besoin de passer par un generateur dans notre cas
        average = self.data['average']
        size = average.shape[0]
        alpha = 2.9 * np.pi / 180
        
        sumCountsAVG = np.sum(self.data['dataCubeAVG'][:,:,self.dMin:self.dMax],axis=2)
        sumCountsAVG[64:68,:] = np.ones([4,132])*np.nan
        sumCountsAVG[:,64:68] = np.ones([132,4])*np.nan
        
        sumCountsAVG /= np.nanmax(sumCountsAVG)
        
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
                    yield point
                    
        return pointGenerator()
    
    
    def getFullCube(self):
        dataCube = self.data['dataCubeAVG']
        size = dataCube.shape[0]
        alpha = 2.9 * np.pi / 180
        
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
                        yield point
        return pointGenerator()

    def getHalfFullCube(self):
        dataCube = self.data['dataCubeAVG']
        size = dataCube.shape[0]
        alpha = 2.9 * np.pi / 180
        
        maxValue = np.max(dataCube)
        dataCube /= maxValue
        def pointGenerator():
            for iy in range(int(size/2)):
                if 64 <= iy < 68:
                    continue
                for ix in range(size):
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
                        yield point
        return pointGenerator()

    
class InterestPoint:
    #TODO: Verifier tous les inputs, raise les erreurs appropriees
    def __init__(self, _pos, _intensity = None, _variation = None):
        self.pos = _pos
        self.intensity = _intensity
        self.var = _variation

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, val):
        if len(val) != 3:
            raise TypeError('Was expecting container containing 3 floats')
        self.__pos = val
        
    @property
    def intensity(self):
        return self.__intensity

    @intensity.setter
    def intensity(self, val):
        self.__intensity = val
        
    @property
    def var(self):
        return self.__var

    @var.setter
    def var(self, val):
        self.__var = val
    

class OLD__DataInterpreter:
    def __init__(self, _folder, _dmin = 0, _dmax = float('inf')):
        self.data = np.load(os.path.join(os.getcwd(), _folder, 'depthMap.npz'))
        self.oneImage = np.load(os.path.join(os.getcwd(), _folder, 'image000.npz'))
        self.correction = np.load('Donnees_brutes/ref1.npz')['correction']
        #On veut les indices dans l'histogramme correspondant aux distances min / max
        distanceAxis = self.oneImage['distanceAxis']
        self.dMin = int((np.abs(distanceAxis - _dmin)).argmin())
        self.dMax = int((np.abs(distanceAxis - _dmax)).argmin())
    
    
    def getColorsFromIntensity(self):
        sumCountsAVG = np.sum(self.data['dataCubeAVG'][:,:,self.dMin:self.dMax],axis=2)
        sumCountsAVG[64:68,:] = np.ones([4,132])*np.nan
        sumCountsAVG[:,64:68] = np.ones([132,4])*np.nan
        
        size = sumCountsAVG.shape[0]
        #Color scheme
        #vmin = sumCountsAVG[~np.isnan(sumCountsAVG)].min()
        #vmax = sumCountsAVG[~np.isnan(sumCountsAVG)].max()
        vmin = np.nanmin(sumCountsAVG)
        vmax = np.nanmax(sumCountsAVG)
        colormap = cm.ScalarMappable(colors.Normalize(vmin,vmax), 'hot')
        def colorGenerator():
            for ix in range(size):
                for iy in range(size):
                    count = sumCountsAVG[ix,iy]
                    if np.isnan(count):
                        continue
                    yield colormap.to_rgba(count, bytes = True)
        return colorGenerator()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import (QMainWindow, QLabel, QComboBox,QLineEdit,
                                QApplication, QWidget, QPushButton, QDoubleSpinBox,
                                QHBoxLayout, QVBoxLayout, QSlider, QFileDialog,
                                QColorDialog, QDockWidget)
    app = QApplication(sys.argv)
    ex = CentralWidget(None)
    folder = 'Donnees_brutes/staticDLR'
          
    interpreter = LidarDataInterpreter(os.path.join(os.getcwd(), folder))
    generator = interpreter.getFullCube()
    print("done")
    ex.show()
    ex.openDirectory("ex")
    sys.exit(app.exec_())
