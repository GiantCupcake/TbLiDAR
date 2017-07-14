# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:38:11 2017

@author: maxpi
"""

from PyQt5.QtWidgets import (QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider,
                             QApplication, QSplitter, QDoubleSpinBox, QCheckBox,
                             QTabWidget, QSpinBox)

from PyQt5.QtCore import Qt, pyqtSignal

class FiltersWidget(QWidget):
    
    def __init__(self, vmin, vmax):
        super().__init__()
        vl = QVBoxLayout()
        labelOutliningBox =  QLabel("<b>Reduce Outlining Box</b>")
        labelOutliningBox.textFormat = Qt.RichText
        vl.addWidget(labelOutliningBox)
        self.rangeSliders = RangeSliders(vmin, vmax)
        vl.addWidget(self.rangeSliders)
        labelConfidence = QLabel("<b>Filter by Confidence [%]</b>")
        labelConfidence.textFormat = Qt.RichText
        vl.addWidget(labelConfidence)
        self.confidenceSlider = LabeledSlider()
        vl.addWidget(self.confidenceSlider)
        labelOutlinerRadius = QLabel("<b>Outlined Radius [m]</b>")
        labelOutlinerRadius.textFormat = Qt.RichText
        vl.addWidget(labelOutlinerRadius)
        self.spinBoxRadius = QDoubleSpinBox()
        self.spinBoxRadius.setDecimals(5)
        self.spinBoxRadius.setSingleStep(0.035)
        vl.addWidget(self.spinBoxRadius)
        vl.addStretch()
        vl.addStretch()
        vl.addStretch()
        
        self.setLayout(vl)

class ControlsWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        #First page : filters
        vlFilters = QVBoxLayout()
        self.distanceFilter = ActivableWidget(QLabel("Reduce Visible Depth"), RangeSliders(0.0, 1.0))
        self.confidenceFilter = ActivableWidget(QLabel("Filter By Confidence [%]"), LabeledSlider())
        
        self.outlierFilter =  ActivableWidget(QLabel("Filter Outliers"), OutlierFilterWidget())
        vlFilters.addWidget(self.distanceFilter)
        vlFilters.addWidget(self.confidenceFilter)
        vlFilters.addWidget(self.outlierFilter)
        vlFilters.addStretch()
        
        filterWidget = QWidget()
        filterWidget.setLayout(vlFilters)
        self.addTab(filterWidget, "Filters")
        
        #second page : Mesh
        vlMesh =  QVBoxLayout()
        self.meshOptions = ActivableWidget(QLabel("Mesh Mode"), MeshOptionsWidget())
        
        vlMesh.addWidget(self.meshOptions)
        vlMesh.addStretch()
        meshWidget = QWidget()
        meshWidget.setLayout(vlMesh)
        
        self.addTab(meshWidget, "Meshing")



class ActivableWidget(QWidget):
    def __init__(self, label, widget):
        super().__init__()
        vl = QVBoxLayout()
        hl1 = QHBoxLayout()
        hl1.addWidget(label)
        hl1.addStretch()
        self.activateBox = QCheckBox()
        self.widget = widget
        self.widget.setVisible(False)
        self.activateBox.stateChanged.connect(self.activateWidget)
        hl1.addWidget(self.activateBox)
        vl.addLayout(hl1)
        vl.addWidget(self.widget)
        vl.addStretch()
        self.setLayout(vl)
        
    def activateWidget(self, s):
        if s == Qt.Unchecked:
            self.widget.setVisible(False)
        if s ==  Qt.Checked:
            self.widget.setVisible(True)


class MeshOptionsWidget(QWidget):
    alphaChanged = pyqtSignal(float)
    smoothOptionsChanged = pyqtSignal(int, float)

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        vl = QVBoxLayout()
        vl.addWidget(QLabel("Alpha Value"))
        self.alphaValue = QDoubleSpinBox()
        self.alphaValue.setSingleStep(0.1)
        vl.addWidget(self.alphaValue)
        
        #Smoothing
        vls = QVBoxLayout()
        self.iterationNumber = QSpinBox()
        self.iterationNumber.setValue(15)
        self.relaxationFactor = QDoubleSpinBox()
        self.relaxationFactor.setSingleStep(0.1)
        self.relaxationFactor.setValue(0.1)
        
        vls.addWidget(QLabel("Number of Iteration"))
        vls.addWidget(self.iterationNumber)
        vls.addWidget(QLabel("Relaxation Factor"))
        vls.addWidget(self.relaxationFactor)
        
        smoothingW = QWidget()
        smoothingW.setLayout(vls)
        
        self.smoothingWidget = ActivableWidget(QLabel("Smoothing"), smoothingW)
        
        vl.addWidget(self.smoothingWidget)
        vl.addStretch()
        
        self.setLayout(vl)
        
        self.alphaValue.valueChanged.connect(self.emitAlphaChanged)
        self.iterationNumber.valueChanged.connect(self.iterationNumberChanged)
        self.relaxationFactor.valueChanged.connect(self.relaxationChanged)
        
    def emitAlphaChanged(self, s):
        print("[MeshOptionsWidget] emitting alphaChanged :", s)
        self.alphaChanged.emit(s)
        
    def iterationNumberChanged(self, s):
        print("[MeshOptionsWidget] emitting smoothOptionsChanged :", s, self.relaxationFactor.value())
        self.smoothOptionsChanged.emit(s, self.relaxationFactor.value())
    
    def relaxationChanged(self, s):
        print("[MeshOptionsWidget] emitting alphaChanged :", self.iterationNumber.value(), s)
        self.smoothOptionsChanged.emit(self.iterationNumber.value(), s)

   
class OutlierFilterWidget(QWidget):
    optionsChanged = pyqtSignal(int, float)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        vl = QVBoxLayout()
        hl1 = QHBoxLayout()
        self.neighborCount = QSpinBox()
        self.neighborCount.setValue(1)
        hl1.addWidget(self.neighborCount)
        hl1.addWidget(QLabel("Neighbors"))
        vl.addLayout(hl1)

        vl.addWidget(QLabel(" In radius [m]"))
        self.spinBoxRadius = QDoubleSpinBox()
        self.spinBoxRadius.setValue(1.0)
        self.spinBoxRadius.setDecimals(5)
        self.spinBoxRadius.setSingleStep(0.035)
        vl.addWidget(self.spinBoxRadius)
        self.setLayout(vl)
        
        self.neighborCount.valueChanged.connect(self.neighborsChanged)
        self.spinBoxRadius.valueChanged.connect(self.radiusChanged)
        
    def neighborsChanged(self, s):
        print("[OutlierFilterWidget] emitting : ", s, self.spinBoxRadius.value())
        self.optionsChanged.emit(s, self.spinBoxRadius.value())
        
    def radiusChanged(self, s):
        print("[OutlierFilterWidget] emitting : ", self.neighborCount.value(), s)
        self.optionsChanged.emit(self.neighborCount.value(), s)


class RangeSliders(QWidget):
    rangeChanged = pyqtSignal(float, float)

    def __init__(self, minVal, maxVal):
        
        super().__init__()
        self._currentMin = minVal
        self._currentMax = maxVal
        self.minSlider = LabeledSlider()
        self.maxSlider = LabeledSlider()
        
        
        self.minSlider.setMinimum(minVal)
        self.minSlider.setMaximum(maxVal)
        self.maxSlider.setMinimum(minVal)
        self.maxSlider.setMaximum(maxVal)
        
        self.minSlider.setSliderPosition(minVal)
        self.maxSlider.setSliderPosition(maxVal)
                
        self.initUI()
        
    def initUI(self):
        self.minSlider.valueChanged.connect(self.maxSlider.setMinimum)
        self.maxSlider.valueChanged.connect(self.minSlider.setMaximum)
        
        self.minSlider.valueChanged.connect(self.minSliderChanged)
        self.maxSlider.valueChanged.connect(self.maxSliderChanged)
        vl = QVBoxLayout()
        vl.addWidget(self.minSlider)
        vl.addWidget(self.maxSlider)
        self.setLayout(vl)
        
    def minSliderChanged(self, s):
        self._currentMin = s
        self.rangeChanged.emit(s, self._currentMax)
        
    def maxSliderChanged(self, s):
        self._currentMax = s
        self.rangeChanged.emit(self._currentMin, s)
        
    def setMinMax(self, vmin, vmax):
        self.minSlider.setMinimum(vmin)
        self.minSlider.setMaximum(vmax)
        self.maxSlider.setMinimum(vmin)
        self.maxSlider.setMaximum(vmax)
        self.maxSlider.setSliderPosition(vmax)


        
class LabeledSlider(QWidget):
    valueChanged = pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.slider = QSlider(Qt.Horizontal)
        #self.slider.setTracking(False)
        self.minLabel = QLabel()
        self.maxLabel = QLabel()
        self.currentLabel = QLabel(self)
        
        self.initUI()
        
    def initUI(self):
        self.setMaximumHeight(60)
        self.setMinimumHeight(60)
        
        self.minLabel.setText(str(self.slider.minimum()))
        self.maxLabel.setText(str(self.slider.maximum()))
        self.currentLabel.setText(str(self.slider.value()))
        self.positionCurrentLabel(self.slider.value())
        self.hl = QHBoxLayout()
        self.hl.addWidget(self.minLabel)
        self.hl.addWidget(self.slider)
        self.hl.addWidget(self.maxLabel)
        self.vl = QVBoxLayout()
        self.vl.addStretch()
        self.vl.addLayout(self.hl)
        self.setLayout(self.vl)
        self.slider.valueChanged.connect(self.positionCurrentLabel)
        self.slider.valueChanged.connect(self.emitFloat)

    def setSliderPosition(self, val):
        self.slider.setSliderPosition(val * 100)
    
    def emitFloat(self, s):
        self.valueChanged.emit(s / 100.0)
        
    def setMinimum(self, n):
        self.slider.setMinimum(n * 100.0)
        self.minLabel.setText('{:.3}'.format(float(n)))
        self.positionCurrentLabel(self.slider.value())
        
    def setMaximum(self, n):
        self.slider.setMaximum(n * 100.0)
        self.maxLabel.setText('{:.3}'.format(float(n)))
        self.positionCurrentLabel(self.slider.value())

    
    def positionCurrentLabel(self,s):
        self.currentLabel.setText('{:.3}'.format(s / 100.0))
        x = self.slider.width() * ((s - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum() + 1))
        self.currentLabel.move(x + 25, 0)
     

def printChanged(b, a):
    print(b, a)            
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = ControlsWidget()
    
    MainWindow.outlierFilter.widget.optionsChanged.connect(printChanged)
    #MainWindow = MeshOptionsWidget()

    MainWindow.show()

    sys.exit(app.exec_())