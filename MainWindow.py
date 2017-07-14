# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:15:29 2017

@author: maxpi
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

import UI_MainWindow
from centralWidget import CentralWidget


class MainWindow(QtWidgets.QMainWindow, UI_MainWindow.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("CSEM", "LiDARViewer")
        self.setupUi(self)
        self.centralWidget = None

        self.readSettings()
        self.activateCheckedActions()

        
    def closeEvent(self, event):        
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)
       
        
    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", type = QtCore.QByteArray))
        self.restoreState(self.settings.value("windowState", type = QtCore.QByteArray))
        
    def activateCheckedActions(self):
        self.actionGroupDataReader.checkedAction().trigger()
        self.actionGroupColorsFrom.checkedAction().trigger()
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


    def openDirectory(self, s):
        #TODO: Rewrite properly
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.Directory)
        if fd.exec():
            self.centralWidget = CentralWidget(self, fd.selectedFiles()[0])
            self.setupSlots(self.centralWidget)
            self.setCentralWidget(self.centralWidget)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())