# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\maxpi\Documents\TB_LIDAR\17dlm-tb-222\QtDesignerUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    def setupSlots(self, mainWidget):
        self.action_Open.triggered.connect(mainWidget.openDirectory)
        #self.action_empty.triggered.connect()
        self.actionDepthMap.triggered.connect(mainWidget.depthMapMode)
        #self.actionConvolution.triggered.connect()
        #self.actionGaussian_Fit.triggered.connect()
        self.actionFull_Cube.triggered.connect(mainWidget.fullCubeMode)
        #self.actionIntensity.triggered.connect(mainWidget.)
        self.actionVariation.triggered.connect(mainWidget.variationColoriser)
        self.actionConfidence.triggered.connect(mainWidget.confidenceColoriser)
        self.actionDepth.triggered.connect(mainWidget.depthColoriser)
        self.actionDefaultColor.triggered.connect(mainWidget.colorSchemeDefaultVTK)
        self.actionJet.triggered.connect(mainWidget.colorSchemeJet)
        self.actionHot.triggered.connect(mainWidget.colorSchemeHot)
        #self.actionCustom_Color_Scheme.triggered.connect()
        self.actionBlank.triggered.connect(mainWidget.colorSchemeWhite)
        self.actionBox.triggered.connect(mainWidget.showOutliningCube)
        self.actionAxes.triggered.connect(mainWidget.showAxes)
        self.actionDepth_Indicator.triggered.connect(mainWidget.showDepthIndicator)       
        self.actionColorScale.triggered.connect(mainWidget.showLookupTable)
        self.actionRestore_Points.triggered.connect(mainWidget.restoreDeletedPoints)
        
        
        self.actionFront_View.triggered.connect(mainWidget.displayFrontView)        
        self.actionSide_View.triggered.connect(mainWidget.displaySideView)        
        self.actionTop_VIew.triggered.connect(mainWidget.displayTopView)   
        self.actionIsometric_View.triggered.connect(mainWidget.displayIsometricView)
        self.actionBackground_Color.triggered.connect(mainWidget.setBackgroundColor)       
        self.actionSTL.triggered.connect(mainWidget.writeSTL)
        self.action_PLY.triggered.connect(mainWidget.writePLY)
        
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 207)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Recents = QtWidgets.QMenu(self.menu_File)
        self.menu_Recents.setObjectName("menu_Recents")
        self.menu_Export = QtWidgets.QMenu(self.menu_File)
        self.menu_Export.setObjectName("menu_Export")
        self.menu_DataReader = QtWidgets.QMenu(self.menubar)
        self.menu_DataReader.setObjectName("menu_DataReader")
        self.menuColors = QtWidgets.QMenu(self.menubar)
        self.menuColors.setObjectName("menuColors")
        self.menuVisualisation = QtWidgets.QMenu(self.menubar)
        self.menuVisualisation.setObjectName("menuVisualisation")
        self.menuCamera = QtWidgets.QMenu(self.menubar)
        self.menuCamera.setObjectName("menuCamera")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_empty = QtWidgets.QAction(MainWindow)
        self.action_empty.setEnabled(False)
        self.action_empty.setObjectName("action_empty")
        self.actionDepthMap = QtWidgets.QAction(MainWindow)
        self.actionDepthMap.setCheckable(True)
        self.actionDepthMap.setChecked(True)
        self.actionDepthMap.setStatusTip("")
        self.actionDepthMap.setObjectName("actionDepthMap")
        self.actionConvolution = QtWidgets.QAction(MainWindow)
        self.actionConvolution.setCheckable(True)
        self.actionConvolution.setEnabled(False)
        self.actionConvolution.setObjectName("actionConvolution")
        self.actionGaussian_Fit = QtWidgets.QAction(MainWindow)
        self.actionGaussian_Fit.setCheckable(True)
        self.actionGaussian_Fit.setEnabled(False)
        self.actionGaussian_Fit.setObjectName("actionGaussian_Fit")
        self.actionFull_Cube = QtWidgets.QAction(MainWindow)
        self.actionFull_Cube.setCheckable(True)
        self.actionFull_Cube.setObjectName("actionFull_Cube")
        self.actionGroupDataReader = QtWidgets.QActionGroup(MainWindow)
        self.actionGroupDataReader.addAction(self.actionDepthMap)
        self.actionGroupDataReader.addAction(self.actionConvolution)
        self.actionGroupDataReader.addAction(self.actionGaussian_Fit)
        self.actionGroupDataReader.addAction(self.actionFull_Cube)
        self.actionIntensity = QtWidgets.QAction(MainWindow)
        self.actionIntensity.setCheckable(True)
        self.actionIntensity.setChecked(True)
        self.actionIntensity.setObjectName("actionIntensity")
        self.actionVariation = QtWidgets.QAction(MainWindow)
        self.actionVariation.setCheckable(True)
        self.actionVariation.setEnabled(False)
        self.actionVariation.setObjectName("actionVariation")
        self.actionConfidence = QtWidgets.QAction(MainWindow)
        self.actionConfidence.setCheckable(True)
        self.actionConfidence.setEnabled(False)
        self.actionConfidence.setObjectName("actionConfidence")
        self.actionDepth = QtWidgets.QAction(MainWindow)
        self.actionDepth.setCheckable(True)
        self.actionDepth.setObjectName("actionDepth")
        self.actionGroupColorsFrom = QtWidgets.QActionGroup(MainWindow)
        self.actionGroupColorsFrom.addAction(self.actionIntensity)
        self.actionGroupColorsFrom.addAction(self.actionVariation)
        self.actionGroupColorsFrom.addAction(self.actionConfidence)
        self.actionGroupColorsFrom.addAction(self.actionDepth)
        
        self.actionJet = QtWidgets.QAction(MainWindow)
        self.actionJet.setCheckable(True)
        self.actionJet.setObjectName("actionJet")
        self.actionHot = QtWidgets.QAction(MainWindow)
        self.actionHot.setCheckable(True)
        self.actionHot.setChecked(False)
        self.actionHot.setObjectName("actionHot")
        self.actionCustom_Color_Scheme = QtWidgets.QAction(MainWindow)
        self.actionCustom_Color_Scheme.setCheckable(True)
        self.actionCustom_Color_Scheme.setEnabled(False)
        self.actionCustom_Color_Scheme.setObjectName("actionCustom_Color_Scheme")
        self.actionBlank = QtWidgets.QAction(MainWindow)
        self.actionBlank.setCheckable(True)
        self.actionBlank.setChecked(False)
        self.actionBlank.setObjectName("actionBlank")
        self.actionDefaultColor = QtWidgets.QAction(MainWindow)
        self.actionDefaultColor.setCheckable(True)
        self.actionDefaultColor.setChecked(True)
        self.actionDefaultColor.setObjectName("actionDefaultColor")
        
        self.actionGroupColorsScheme = QtWidgets.QActionGroup(MainWindow)
        self.actionGroupColorsScheme.addAction(self.actionDefaultColor)
        self.actionGroupColorsScheme.addAction(self.actionBlank)
        self.actionGroupColorsScheme.addAction(self.actionHot)
        self.actionGroupColorsScheme.addAction(self.actionJet)
        self.actionGroupColorsScheme.addAction(self.actionCustom_Color_Scheme)
        
        self.actionBox = QtWidgets.QAction(MainWindow)
        self.actionBox.setObjectName("actionBox")
        self.actionBox.setCheckable(True)
        self.actionBox.setChecked(True)
        self.actionAxes = QtWidgets.QAction(MainWindow)
        self.actionAxes.setObjectName("actionAxes")
        self.actionAxes.setCheckable(True)
        self.actionAxes.setChecked(True)
        self.actionDepth_Indicator = QtWidgets.QAction(MainWindow)
        self.actionDepth_Indicator.setObjectName("actionDepth_Indicator")
        self.actionDepth_Indicator.setCheckable(True)
        self.actionDepth_Indicator.setChecked(True)
        self.actionColorScale = QtWidgets.QAction(MainWindow)
        self.actionColorScale.setCheckable(True)
        self.actionColorScale.setObjectName("actionColorScale")
        self.actionRestore_Points = QtWidgets.QAction(MainWindow)
        self.actionRestore_Points.setObjectName("actionRestore_Points")
        
        self.actionFront_View = QtWidgets.QAction(MainWindow)
        self.actionFront_View.setObjectName("actionFront_View")
        self.actionSide_View = QtWidgets.QAction(MainWindow)
        self.actionSide_View.setObjectName("actionSide_View")
        self.actionTop_VIew = QtWidgets.QAction(MainWindow)
        self.actionTop_VIew.setObjectName("actionTop_VIew")
        self.actionIsometric_View = QtWidgets.QAction(MainWindow)
        self.actionIsometric_View.setObjectName("actionIsometric_View")
        
        self.actionBackground_Color = QtWidgets.QAction(MainWindow)
        self.actionBackground_Color.setObjectName("actionBackground_Color")
        self.actionSTL = QtWidgets.QAction(MainWindow)
        self.actionSTL.setObjectName("actionSTL")
        self.action_PLY = QtWidgets.QAction(MainWindow)
        self.action_PLY.setObjectName("action_PLY")
        self.menu_Recents.addAction(self.action_empty)
        self.menu_Export.addAction(self.actionSTL)
        self.menu_Export.addAction(self.action_PLY)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.menu_Recents.menuAction())
        self.menu_File.addAction(self.menu_Export.menuAction())
        self.menu_DataReader.addAction(self.actionDepthMap)
        self.menu_DataReader.addAction(self.actionConvolution)
        self.menu_DataReader.addAction(self.actionGaussian_Fit)
        self.menu_DataReader.addAction(self.actionFull_Cube)
        self.menuColors.addAction(self.actionIntensity)
        self.menuColors.addAction(self.actionVariation)
        self.menuColors.addAction(self.actionConfidence)
        self.menuColors.addAction(self.actionDepth)
        self.menuColors.addSeparator()
        self.menuColors.addAction(self.actionDefaultColor)
        self.menuColors.addAction(self.actionBlank)
        self.menuColors.addAction(self.actionHot)
        self.menuColors.addAction(self.actionJet)
        self.menuColors.addAction(self.actionCustom_Color_Scheme)
        self.menuColors.addSeparator()
        self.menuColors.addAction(self.actionBackground_Color)
        self.menuVisualisation.addAction(self.actionBox)
        self.menuVisualisation.addAction(self.actionAxes)
        self.menuVisualisation.addAction(self.actionDepth_Indicator)
        self.menuVisualisation.addAction(self.actionColorScale)
        self.menuVisualisation.addSeparator()
        self.menuVisualisation.addAction(self.actionRestore_Points)
        self.menuCamera.addAction(self.actionFront_View)
        self.menuCamera.addAction(self.actionSide_View)
        self.menuCamera.addAction(self.actionTop_VIew)
        self.menuCamera.addAction(self.actionIsometric_View)
        
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_DataReader.menuAction())
        self.menubar.addAction(self.menuColors.menuAction())
        self.menubar.addAction(self.menuVisualisation.menuAction())
        self.menubar.addAction(self.menuCamera.menuAction())
        
        self.dockWidget = QtWidgets.QDockWidget("FilterData", MainWindow)
        self.dockWidget.setFloating(False)
        self.dockWidget.setFixedWidth(230)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        
        def dockHide(self, event):
            #self.hide()
            event.ignore()
            print("Rewrote Func closeEvent")
        
        QtWidgets.QDockWidget.closeEvent = dockHide
        MainWindow.destroyed.connect(self.dockWidget.destroy)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CSEM - LiDAR Viewer"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Recents.setStatusTip(_translate("MainWindow", "Recently Opened Folder"))
        self.menu_Recents.setTitle(_translate("MainWindow", "&Recents"))
        self.menu_Export.setStatusTip(_translate("MainWindow", "Export the viewed data to a file"))
        self.menu_Export.setTitle(_translate("MainWindow", "&Export To..."))
        self.menu_DataReader.setTitle(_translate("MainWindow", "&DataReader"))
        self.menuColors.setTitle(_translate("MainWindow", "C&olors"))
        self.menuVisualisation.setTitle(_translate("MainWindow", "&Visualisation"))
        self.menuCamera.setTitle(_translate("MainWindow", "&Camera"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Open.setStatusTip(_translate("MainWindow", "Open Folder containing the Numpy archives"))
        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_empty.setText(_translate("MainWindow", "(empty)"))
        self.actionDepthMap.setText(_translate("MainWindow", "DepthMap"))
        self.actionConvolution.setText(_translate("MainWindow", "Convolution"))
        self.actionGaussian_Fit.setText(_translate("MainWindow", "Gaussian Fit"))
        self.actionFull_Cube.setText(_translate("MainWindow", "Full Cube"))
        self.actionIntensity.setText(_translate("MainWindow", "Intensity"))
        self.actionIntensity.setStatusTip(_translate("MainWindow", "Color of a point will be determined by the number of photons received"))
        self.actionVariation.setText(_translate("MainWindow", "Variation"))
        self.actionConfidence.setText(_translate("MainWindow", "Confidence"))
        self.actionDepth.setText(_translate("MainWindow", "Depth"))
        self.actionDepth.setStatusTip(_translate("MainWindow", "Color of a point will be determined by its position along the Z axis"))
        self.actionDefaultColor.setText(_translate("MainWindow", "Default"))
        self.actionJet.setText(_translate("MainWindow", "Jet"))
        self.actionHot.setText(_translate("MainWindow", "Hot"))
        self.actionCustom_Color_Scheme.setText(_translate("MainWindow", "Custom..."))
        self.actionBlank.setText(_translate("MainWindow", "White"))
        self.actionBox.setText(_translate("MainWindow", "Outlining Cube"))
        self.actionBox.setStatusTip(_translate("MainWindow", "Show / hide the outlining box around the data"))
        self.actionAxes.setText(_translate("MainWindow", "Axes"))
        self.actionAxes.setStatusTip(_translate("MainWindow", "Show / hide the rotating axes in the corner"))
        self.actionDepth_Indicator.setText(_translate("MainWindow", "Depth Indicator"))
        self.actionDepth_Indicator.setStatusTip(_translate("MainWindow", "Show / hide the indication of depth along the Z axis"))
        self.actionColorScale.setText(_translate("MainWindow", "ColorScale"))
        self.actionRestore_Points.setText(_translate("MainWindow", "Restore Points"))
        self.actionRestore_Points.setStatusTip(_translate("MainWindow", "Restore Points that were deleted with selection"))
        self.actionRestore_Points.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionFront_View.setText(_translate("MainWindow", "Front View"))
        self.actionFront_View.setStatusTip(_translate("MainWindow", "Set the camera facing the data from the front"))
        self.actionFront_View.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionSide_View.setText(_translate("MainWindow", "Side View"))
        self.actionSide_View.setStatusTip(_translate("MainWindow", "Set the camera facing the data from the right side"))
        self.actionSide_View.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionTop_VIew.setText(_translate("MainWindow", "Top VIew"))
        self.actionTop_VIew.setStatusTip(_translate("MainWindow", "Set the camera facing the data from the top"))
        self.actionTop_VIew.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionIsometric_View.setText(_translate("MainWindow", "Isometric View"))
        self.actionIsometric_View.setStatusTip(_translate("MainWindow", "Set the camera facing in an isometric view"))
        self.actionIsometric_View.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionBackground_Color.setText(_translate("MainWindow", "&Background Color..."))
        self.actionBackground_Color.setStatusTip(_translate("MainWindow", "Change the color of the background"))
        self.actionSTL.setText(_translate("MainWindow", ".STL"))
        self.actionSTL.setStatusTip(_translate("MainWindow", "Export to the .STL format"))
        self.action_PLY.setText(_translate("MainWindow", ".PLY"))
        self.action_PLY.setStatusTip(_translate("MainWindow", "Export to the .PLY format"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

