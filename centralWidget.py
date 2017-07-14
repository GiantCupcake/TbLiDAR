# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:20:25 2017

@author: maxpi
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QLabel, QComboBox,QLineEdit,
                            QApplication, QWidget, QPushButton, QDoubleSpinBox,
                            QHBoxLayout, QVBoxLayout, QSlider, QFileDialog,
                            QColorDialog, QDockWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from GenerateFromFile import LidarDataInterpreter, display_time
from RangeSliders import ControlsWidget
from matplotlib import cm, colors

import os
import warnings


from PointCloudVisualisator import PointCloudVisualisator

def waiting_effects(func):
    def decorator(self, *args):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            func(self,*args)
        except Exception as e:
            raise e
            print("Error {}".format(e.args[0]))
        finally:
            QApplication.restoreOverrideCursor()
    return decorator


class CentralWidget(QWidget):
    
    def __init__(self, mainWindow):
        super().__init__()
        self.parent = mainWindow
        self.pcv = None
        self.controlsWidget = None

        self.currentFolder = os.path.join(os.getcwd(), 'Donnees_brutes/tractopelle')
        self.initWidgets()
        self.hl = QHBoxLayout()
        self.hl.addWidget(self.pcv)
        self.setLayout(self.hl)
    
    def replaceWidgets(self):
        self.hl.removeWidget(self.pcv)
        del(self.pcv)
        self.controlsWidget.destroy()
        self.initWidgets()
        self.hl.addWidget(self.pcv)
    
    def initWidgets(self): 
        interpreter = LidarDataInterpreter(self.currentFolder)
        #generator = interpreter.getPointsFromDepthMap()
        generator = interpreter.getPointsFromDepthMap()
        self.pcv = PointCloudVisualisator(generator)
        
        bounds = self.pcv.pointsData.GetBounds()
        self.controlsWidget = ControlsWidget()
        self.controlsWidget.distanceFilter.widget.setMinMax(bounds[4], bounds[5])
        self.parent.dockWidget.setWidget(self.controlsWidget)
        self.connectSlots()
        self.parent.activateCheckedActions()

        
        
    def connectSlots(self):
        self.controlsWidget.distanceFilter.activateBox.stateChanged.connect(self.activateOutliningFilter)
        self.controlsWidget.confidenceFilter.activateBox.stateChanged.connect(self.activateConfidenceFilter)
        self.controlsWidget.outlierFilter.activateBox.stateChanged.connect(self.activateOutlierFilter)
        self.controlsWidget.meshOptions.activateBox.stateChanged.connect(self.activateMesh)
        self.controlsWidget.meshOptions.widget.smoothingWidget.activateBox.stateChanged.connect(self.activateSmoothing)
        
        self.controlsWidget.distanceFilter.widget.rangeChanged.connect(self.pcv.setZBounds)
        self.controlsWidget.confidenceFilter.widget.valueChanged.connect(self.pcv.setConfidenceThreshold)
        self.controlsWidget.outlierFilter.widget.optionsChanged.connect(self.pcv.setOutlierOptions)
        self.controlsWidget.meshOptions.widget.alphaChanged.connect(self.pcv.setMeshAlpha)
        self.controlsWidget.meshOptions.widget.smoothOptionsChanged.connect(self.pcv.setSmoothingOptions)

    
    def activateOutliningFilter(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableDepthFilter()
        if s == Qt.Checked:
            self.pcv.enableDepthFilter()
    
    def activateConfidenceFilter(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableConfidenceFilter()
        if s == Qt.Checked:
            self.pcv.enableConfidenceFilter()
    
    def activateOutlierFilter(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableOutlierFilter()
        if s == Qt.Checked:
            self.pcv.enableOutlierFilter()   
        
    def activateMesh(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableMesh()
        if s == Qt.Checked:
            self.pcv.enableMesh()  
        
    def activateSmoothing(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableMeshSmoothing()
        if s == Qt.Checked:
            self.pcv.enableMeshSmoothing()
        
    @display_time
    def openDirectory(self, s):
        #TODO: Rewrite properly
        print("[CentralWidget] openDirectory")
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.Directory)
        if fd.exec():

            self.currentFolder = fd.selectedFiles()[0]
            self.replaceWidgets()
            
    @display_time
    @waiting_effects           
    def fullCubeMode(self, s):
        #TODO: Rewrite properly
        print("[CentralWidget] fullCubeMode")
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getFullCube())
        
        
    @display_time
    def depthMapMode(self, s):
        #TODO: Rewrite properly
        print("[CentralWidget] depthMapMode")
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getPointsFromDepthMap())
        
        
    
    def writeSTL(self, s):
        fd = QFileDialog()
        fd.setAcceptMode(QFileDialog.AcceptSave)
        fd.setNameFilter("STL format file (*.stl)");
        if fd.exec():
            fileNames = fd.selectedFiles()
            print("Saving to {0}".format(fileNames[0]))
            self.pcv.writeSTL(fileNames[0])
    
    def writePLY(self, s):
        fd = QFileDialog()
        fd.setAcceptMode(QFileDialog.AcceptSave)
        fd.setNameFilter("PLY format file (*.ply)");
        if fd.exec():
            fileNames = fd.selectedFiles()
            print("Saving to {0}".format(fileNames[0]))
            self.pcv.writePLY(fileNames[0])
        
    def customColoriser(self, s):
        warnings.warn("Not Implemented", Warning)
    
        
    def colorSchemeDefaultVTK(self, s):
        self.pcv.defaultColoriser()
        
    def colorSchemeHot(self, s):
        print("[CentralWidget] colorSchemeHot")
        colormap = cm.ScalarMappable(colors.Normalize(0, 20), 'hot')
        points = colormap.to_rgba(range(20))
        self.pcv.customColoriser(points)
        
    def colorSchemeJet(self, s):
        print("[CentralWidget] colorSchemeJet")
        colormap = cm.ScalarMappable(colors.Normalize(0, 20), 'jet')
        points = colormap.to_rgba(range(20))
        self.pcv.customColoriser(points)
        
    def colorSchemeWhite(self, s):
        print("[CentralWidget] colorSchemeWhite")
        self.pcv.customAlphaColoriser()
        #self.pcv.customColoriser(((1.,1.,1.,0.),(1.,1.,1.,1.)))
        
        
    def depthColoriser(self, s):
        self.pcv.coloriser = self.pcv.getDepthColoriser()

    def variationColoriser(self,s):
        warnings.warn("Not Implemented", Warning)

    def confidenceColoriser(self, s):
        warnings.warn("Not Implemented", Warning)
    
    def setBackgroundColor(self, s):
        cd = QColorDialog()
        cd.setOption(QColorDialog.ShowAlphaChannel, False)
        if cd.exec():
            qColor = cd.selectedColor()
            print((qColor.redF(), qColor.greenF(), qColor.blueF()))
            self.pcv.setBackgroundColor((qColor.redF(), qColor.greenF(), qColor.blueF()))
    
    
    def showOutliningCube(self, s):
        print(s)
        if s == True:
            self.pcv.showOutliningCube()
        if s == False:
            self.pcv.hideOutliningCube()
            
    
    def showAxes(self, s):
        print(s)
        if s == True:
            self.pcv.showAxes()
        if s == False:
            self.pcv.hideAxes()

    
    def showDepthIndicator(self, s):
        print(s)
        if s == True:
            self.pcv.showDepthIndicator()
        if s == False:
            self.pcv.hideDepthIndicator()
            
    def showLookupTable(self, s):
        print(s)
        if s == True:
            self.pcv.showLookupTable()
        if s == False:
            self.pcv.hideLookupTable()
        
    def restoreDeletedPoints(self, s):
        print("[CentralWidget] restoreDeletedPoints")
        self.pcv.clearBannedIds()
    
    def displayFrontView(self, s):
        self.pcv.displayFrontView()
    
    def displaySideView(self, s):
        self.pcv.displaySideView()
    
    def displayTopView(self, s):
        self.pcv.displayTopView()
        
    def displayIsometricView(self,s):
        self.pcv.displayIsometricView()
        
   
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = CentralWidget(None)
    ex.show()
    ex.openDirectory("ex")
    sys.exit(app.exec_())