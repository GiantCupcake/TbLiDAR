# -*- coding: utf-8 -*-
"""
This Qt Widget can be used to easily see the histogramm behind a certain sensor
Click on any pixel to open a matplotlib visualisation of the histogram.

Created on Fri Jul 21 05:57:10 2017

@author: Maxime Piergiovanni
"""


from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QImage, QColor, QPainter

import matplotlib.pyplot as plt
from matplotlib import cm, colors

import numpy as np
import os

class HistogramViewer(QWidget):
    
    def __init__(self, _folder):
        super().__init__()
        self.data = np.load(os.path.join(os.getcwd(), _folder, 'depthMap.npz'))
        self.depthMap = self.data['average']
        self.histograms = self.data['dataCubeAVG']
        self.distanceAxis = self.data['distanceAxis']
        self.initUI()
        
    def initUI(self): 
        self.size = self.depthMap.shape[0]
        self.image = QImage(self.size, self.size, QImage.Format_ARGB32)

        cmap = cm.ScalarMappable(colors.Normalize(np.nanmin(self.depthMap), np.nanmax(self.depthMap)), 'jet')
        for y in range(self.size):
            for x in range(self.size):
                color = cmap.to_rgba(self.depthMap[y,x])
                col =  QColor()
                col.setRgbF(color[0], color[1], color[2])
                self.image.setPixelColor(x, y, col)
                
    
    def mousePressEvent(self, e):
        try:
            self.updateHist(e.x(), e.y())
        except:
            pass
        
    def mouseMoveEvent(self, e):
        try:
            self.updateHist(e.x(), e.y())
        except:
            pass
        
    def updateHist(self, x, y):
        plt.cla()
        plt.xlabel('Distance [m]')
        plt.ylabel('Luminous Intensity')
        ix = int(x / float(self.width()) * self.size)
        iy = int(y / float(self.height()) * self.size)
        plt.plot(self.distanceAxis, self.histograms[iy, ix])

        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())
        painter.end()
        
        