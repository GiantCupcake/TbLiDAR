# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 05:57:10 2017

@author: maxpi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:38:11 2017

@author: maxpi
"""

from PyQt5.QtWidgets import (QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider,
                             QApplication, QSplitter, QDoubleSpinBox, QCheckBox,
                             QTabWidget, QSpinBox, QGridLayout, QPushButton, QMainWindow) 
from PyQt5.QtGui import QImage, QColor, QPainter, QPixmap, QBrush
from PyQt5.QtCore import Qt, pyqtSignal

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
        #self.image.fill(QColor(0, 0, 0, 0))
        for y in range(self.size):
            for x in range(self.size):
                color = cmap.to_rgba(self.depthMap[y,x])
                col =  QColor()
                col.setRgbF(color[0], color[1], color[2])
                self.image.setPixelColor(x, y, col)
                
    
    def mousePressEvent(self, e):
        print("[HistogramViewer] pressEvent")
        plt.cla()
        ix = int(e.x() / float(self.width()) * self.size)
        iy = int(e.y() / float(self.height()) * self.size)
        plt.plot(self.distanceAxis, self.histograms[iy, ix])
        
    def mouseMoveEvent(self, e):
        plt.cla()
        ix = int(e.x() / float(self.width()) * self.size)
        iy = int(e.y() / float(self.height()) * self.size)
        plt.plot(self.distanceAxis, self.histograms[iy, ix])
        
        
    def paintEvent(self, event):
        print("[HistogramViewer] paintEvent")
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())
        painter.end()
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    mw = QMainWindow()
    mw.show()
    
    MainWindow = HistogramViewer('../Donnees_Brutes/tractopelle')
    
    MainWindow.show()
    

    sys.exit(app.exec_())