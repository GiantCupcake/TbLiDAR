# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 06:12:13 2017

@author: maxpi
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QFileDialog, QColorDialog)

from centralWidget import CentralWidget
from VTKFileDisplay import VTKFileDisplay

class WidgetVTKFileDisplay(CentralWidget):
    
    def __init__(self, mainWindow, fileName):
        QWidget.__init__(self)
        self.parent = mainWindow
        self.pcv = None
        self.fileName = fileName

        self.initWidgets()
        self.hl = QHBoxLayout()
        self.hl.addWidget(self.pcv)
        self.setLayout(self.hl)
        
    def showFeatureNotAvailable(self):
        self.parent.statusbar.showMessage("This Action cannot be performed when reading VTK File", 5000)

    
    def replaceWidgets(self):
        self.showFeatureNotAvailable()
    
    def initWidgets(self): 
        self.pcv = VTKFileDisplay(self.fileName)
        
    def connectSlots(self):
        pass
        
    
    def activateOutliningFilter(self, s):
        self.showFeatureNotAvailable()
    
    def activateConfidenceFilter(self, s):
        self.showFeatureNotAvailable()
            
    def activateSigmaFilter(self, s):
        self.showFeatureNotAvailable()
    
    def activateOutlierFilter(self, s):
        self.showFeatureNotAvailable()
        
    def activateMesh(self, s):
        self.showFeatureNotAvailable()
        
    def activateSmoothing(self, s):
        self.showFeatureNotAvailable()
        
                     
    def fullCubeMode(self, s):
        self.showFeatureNotAvailable()
        
        
    def depthMapMode(self, s):
        self.showFeatureNotAvailable()
    
    def customModeOne(self, s):
        self.showFeatureNotAvailable()
        
    def customModeTwo(self, s):
        self.showFeatureNotAvailable()
        
    
    def buildCMFromFilteredPoints(self, s):
        self.showFeatureNotAvailable()

    def buildCMFromAllPoints(self, s):
        self.showFeatureNotAvailable()
    
        
    def restoreDeletedPoints(self, s):
        self.showFeatureNotAvailable()
    

    def histogramViewer(self, s):
        self.showFeatureNotAvailable()
