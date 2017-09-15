# -*- coding: utf-8 -*-
"""
This is the entry point of the program, run this file to launch the application
All UI setting and the slot connection is done in UI_MainWindow.py

Created on Fri Jun 23 15:15:29 2017

@author: Maxime Piergiovanni
"""

from PyQt5 import QtWidgets, QtCore

import UI_MainWindow
from centralWidget import CentralWidget
from VTKFileDisplay import VTKFileDisplay
from WidgetVTKFileDisplay import WidgetVTKFileDisplay


class MainWindow(QtWidgets.QMainWindow, UI_MainWindow.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("CSEM", "LiDARViewer")
        self.setupUi(self)
        self.readSettings()

        
    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)
      
    def openDirectory(self, s):
        try:
            fd = QtWidgets.QFileDialog()
            fd.setFileMode(QtWidgets.QFileDialog.Directory)
            if fd.exec():
                self.centralWidget = CentralWidget(self, fd.selectedFiles()[0])
                self.setupSlots(self.centralWidget)
                self.setCentralWidget(self.centralWidget)
                self.activateCheckedActions()
        except:
            self.statusbar.showMessage("There was an error opening this folder", 3000)

    def openVTKFile(self, s):
        try:
            fd = QtWidgets.QFileDialog()
            fd.setFileMode(QtWidgets.QFileDialog.AnyFile)
            if fd.exec():
                print("After exec")
                self.centralWidget = WidgetVTKFileDisplay(self, fd.selectedFiles()[0])
                print("After object construct")
                self.setCentralWidget(self.centralWidget)
                self.setupSlots(self.centralWidget)
                self.centralWidget.show()
        except Exception as e:
            self.statusbar.showMessage("There was an error opening this file", 3000)
            print(e)
        
        
    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", type = QtCore.QByteArray))
        self.restoreState(self.settings.value("windowState", type = QtCore.QByteArray))
        
    def activateCheckedActions(self):
        self.actionGroupDataReader.checkedAction().trigger()
        self.actionGroupColorsScheme.checkedAction().trigger()
        
        if self.actionBox.isChecked():    
            self.actionBox.trigger()
            self.actionBox.trigger()
        if self.actionAxes.isChecked():    
            self.actionAxes.trigger()
            self.actionAxes.trigger()
        if self.actionDepth_Indicator.isChecked():    
            self.actionDepth_Indicator.trigger()
            self.actionDepth_Indicator.trigger()
        if self.actionColorScale.isChecked():    
            self.actionColorScale.trigger()
            self.actionColorScale.trigger()

        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())