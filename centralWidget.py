# -*- coding: utf-8 -*-
"""
This class will be the bridge between each QtWidgets, and the MainWindow.
Every function corresponds to a certain signal coming from the filter panel
or the menu from MainWindow. Each action will have an effect on the 
PointCloudVisualisator.

Created on Fri Jun 23 14:20:25 2017

@author: Maxime Piergiovanni
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QFileDialog, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from GenerateFromFile import LidarDataInterpreter, display_time
from RangeSliders import ControlsWidget
from HistogramViewer import HistogramViewer
from matplotlib import cm, colors

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
    
    def __init__(self, mainWindow, folder):
        super().__init__()
        self.parent = mainWindow
        self.pcv = None
        self.controlsWidget = None

        self.currentFolder = folder
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
        self.controlsWidget.sigmaFilter.activateBox.stateChanged.connect(self.activateSigmaFilter)
        self.controlsWidget.outlierFilter.activateBox.stateChanged.connect(self.activateOutlierFilter)
        self.controlsWidget.meshOptions.activateBox.stateChanged.connect(self.activateMesh)
        self.controlsWidget.meshOptions.widget.smoothingWidget.activateBox.stateChanged.connect(self.activateSmoothing)
        
        self.controlsWidget.distanceFilter.widget.rangeChanged.connect(self.pcv.setZBounds)
        self.controlsWidget.confidenceFilter.widget.valueChanged.connect(self.pcv.setConfidenceThreshold)
        self.controlsWidget.sigmaFilter.widget.valueChanged.connect(self.pcv.setSigmaThreshold)
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
            
    def activateSigmaFilter(self, s):
        if s == Qt.Unchecked:
            self.pcv.disableSigmaFilter()
        if s == Qt.Checked:
            self.pcv.enableSigmaFilter()
    
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
    @waiting_effects         
    def fullCubeMode(self, s):
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getFullCube())
        
        
    @display_time
    def depthMapMode(self, s):
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getPointsFromDepthMap())
    
    @display_time
    def customModeOne(self, s):
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getCustomReaderOne())
        
    @display_time    
    def customModeTwo(self, s):
        interpreter = LidarDataInterpreter(self.currentFolder)
        self.pcv.updatePoints(interpreter.getCustomReaderOne())
        
        
    
    def writeSTL(self, s):
        fd = QFileDialog()
        fd.setAcceptMode(QFileDialog.AcceptSave)
        fd.setNameFilter("STL format file (*.stl)")
        if fd.exec():
            fileNames = fd.selectedFiles()
            self.pcv.writeSTL(fileNames[0])
    
    def writePLY(self, s):
        fd = QFileDialog()
        fd.setAcceptMode(QFileDialog.AcceptSave)
        fd.setNameFilter("PLY format file (*.ply)")
        if fd.exec():
            fileNames = fd.selectedFiles()
            self.pcv.writePLY(fileNames[0])
            
            
    def writeVTK(self, s):
        fd = QFileDialog()
        fd.setAcceptMode(QFileDialog.AcceptSave)
        fd.setNameFilter("VTK format file (*.vtk)")
        if fd.exec():
            fileNames = fd.selectedFiles()
            self.pcv.writeVTK(fileNames[0])

            

        
    def customColoriser(self, s):
        warnings.warn("Not Implemented", Warning)
    
        
    def colorSchemeDefaultVTK(self, s):
        self.pcv.defaultColoriser()
        
    def colorSchemeHot(self, s):
        colormap = cm.ScalarMappable(colors.Normalize(0, 20), 'hot')
        points = colormap.to_rgba(range(20))
        self.pcv.customColoriser(points)
        
    def colorSchemeJet(self, s):
        colormap = cm.ScalarMappable(colors.Normalize(0, 20), 'jet')
        points = colormap.to_rgba(range(20))
        self.pcv.customColoriser(points)
        
    def colorSchemeWhite(self, s):
        self.pcv.customAlphaColoriser()
        #self.pcv.customColoriser(((1.,1.,1.,0.),(1.,1.,1.,1.)))
        
        
    def depthColoriser(self, s):
        self.pcv.colorByDepth()

    def variationColoriser(self,s):
        self.pcv.colorBySigma()

    def intensityColoriser(self, s):
        self.pcv.colorByIntensity()
    
    def setBackgroundColor(self, s):
        cd = QColorDialog()
        cd.setOption(QColorDialog.ShowAlphaChannel, False)
        if cd.exec():
            qColor = cd.selectedColor()
            self.pcv.setBackgroundColor((qColor.redF(), qColor.greenF(), qColor.blueF()))
    
    def buildCMFromFilteredPoints(self, s):
        self.pcv.mapColorsFromFilteredPoints()
    

    def buildCMFromAllPoints(self, s):
        self.pcv.mapColorsFromAllPoints()
    
    def showOutliningCube(self, s):
        if s == True:
            self.pcv.showOutliningCube()
        if s == False:
            self.pcv.hideOutliningCube()
            
    
    def showAxes(self, s):
        if s == True:
            self.pcv.showAxes()
        if s == False:
            self.pcv.hideAxes()

    
    def showDepthIndicator(self, s):
        if s == True:
            self.pcv.showDepthIndicator()
        if s == False:
            self.pcv.hideDepthIndicator()
            
    def showLookupTable(self, s):
        if s == True:
            self.pcv.showLookupTable()
        if s == False:
            self.pcv.hideLookupTable()
        
    def restoreDeletedPoints(self, s):
        self.pcv.clearBannedIds()
    
    def displayFrontView(self, s):
        self.pcv.displayFrontView()
    
    def displaySideView(self, s):
        self.pcv.displaySideView()
    
    def displayTopView(self, s):
        self.pcv.displayTopView()
        
    def displayIsometricView(self,s):
        self.pcv.displayIsometricView()
        
    def histogramViewer(self, s):
        self.hs = HistogramViewer(self.currentFolder)
        self.hs.show()
        
 