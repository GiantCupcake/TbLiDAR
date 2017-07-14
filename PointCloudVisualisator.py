# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:13:43 2017

@author: maxpi
"""

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
import warnings

from InteractorStylePickPoints import InteractorStylePickPoints

 
class PointCloudVisualisator(QVTKRenderWindowInteractor):
        
    def updatePoints(self, interestPoints):
        # Create the geometry of a point (the coordinate)
        points = vtk.vtkPoints()
        # Create the topology of the point (a vertex)
        vertices = vtk.vtkCellArray()
        additionalData = vtk.vtkDoubleArray()
        additionalData.SetNumberOfComponents(1)
        additionalData.SetName("Intensity")
        for pi in interestPoints: 
            id = points.InsertNextPoint(pi.pos)
            #vtkCellArray::InsertNextCell	(	vtkIdType 	npts,const vtkIdType * 	pts )
            #Nombre de points puis tableau d'id des points
            vertices.InsertNextCell(1)
            vertices.InsertCellPoint(id)
            additionalData.InsertNextValue(pi.intensity)
        
        # Set the points and vertices we created as the geometry and topology of the polydata
        self.pointsData.SetPoints(points)
        self.pointsData.SetVerts(vertices)
        self.pointsData.GetPointData().SetScalars(additionalData)
        
        
    def initOutline(self):
        #outline
        outline = vtk.vtkOutlineFilter()
        outline.SetInputData(self.listPassThrough[-1].GetOutput())
        mapperOutline = vtk.vtkPolyDataMapper()
        mapperOutline.SetInputConnection(outline.GetOutputPort())
         
        self.actorOutline = vtk.vtkActor()
        self.actorOutline.SetMapper(mapperOutline)
        self.actorOutline.GetProperty().SetColor(128, 128, 128)
        self.actorOutline.SetVisibility(False)
        
        self.ren.AddActor(self.actorOutline)
        
 
    def initAxes(self):
        #Axes on the corner of the window
        self.actorAxes = vtk.vtkAxesActor()
        self.orientationWidget = vtk.vtkOrientationMarkerWidget()
        self.orientationWidget.SetDefaultRenderer(self.ren)
        self.orientationWidget.SetInteractor(self.iren)
        self.orientationWidget.SetOrientationMarker(self.actorAxes)
        self.orientationWidget.On()
        self.actorAxes.SetVisibility(False)
        
    def initDepthIndicator(self):
        # Create a text property for both cube axes
        tprop = vtk.vtkTextProperty()
        tprop.SetColor(1, 1, 1)
        tprop.ShadowOn()
        
        # Create a vtkCubeAxesActor2D.  Use the outer edges of the bounding box to
        # draw the axes.  Add the actor to the renderer.
        self.actorZAxis = vtk.vtkCubeAxesActor2D()
        #On ne veut que l-axe Z
        self.actorZAxis.XAxisVisibilityOff ()
        self.actorZAxis.YAxisVisibilityOff ()
        self.actorZAxis.SetInputData(self.listPassThrough[-1].GetOutput())
        #A besoin de la camera pour determiner comment placer les labels
        self.actorZAxis.SetCamera(self.ren.GetActiveCamera())
        self.actorZAxis.SetLabelFormat("%6.4g")
        #FlyMode { VTK_FLY_OUTER_EDGES = 0, VTK_FLY_CLOSEST_TRIAD = 1, VTK_FLY_NONE = 2 }
        #Si fly mode active, il va chercher a display les axes X et Y
        #axes.SetFlyModeToNone ()
        #axes.SetFlyModeToClosestTriad()

        self.actorZAxis.SetFontFactor(0.8)
        self.actorZAxis.SetAxisTitleTextProperty(tprop)
        self.actorZAxis.SetAxisLabelTextProperty(tprop)
        self.actorZAxis.SetVisibility(False)
        
        self.ren.AddViewProp(self.actorZAxis)
        
    def initScalarBar(self):
        self.scalarBar = vtk.vtkScalarBarActor()
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())
        self.scalarBar.SetTitle("Confidence")
        self.scalarBar.SetNumberOfLabels(3)
        self.scalarBar.SetDragable(True)
        self.scalarBar.SetVisibility(False)
        self.ren.AddActor2D(self.scalarBar)
        
        
    def initPipeline(self):
        """
        Create an empty pipeline which will be used to insert different filters
        between the passThrougs
        """

        self.selectionNode = vtk.vtkSelectionNode()
        self.selectionNode.SetFieldType(1) # POINT
        self.selectionNode.SetContentType(4) #INDICES
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)
        self.selection = vtk.vtkSelection()
        self.selection.AddNode(self.selectionNode)        
        self.extractSelection = vtk.vtkExtractSelection()
        self.extractSelection.SetInputData(0, self.pointsData)
        self.extractSelection.SetInputData(1, self.selection)
        
        self.geometryFilter = vtk.vtkGeometryFilter()
        self.geometryFilter.SetInputConnection(self.extractSelection.GetOutputPort())
        
        
        self.listPassThrough = [vtk.vtkPassThrough()]
        self.listPassThrough[0].SetInputConnection(self.geometryFilter.GetOutputPort())
        
        for n in range(5):
            newPassThrough = vtk.vtkPassThrough()
            newPassThrough.SetInputConnection(self.listPassThrough[n].GetOutputPort())
            self.listPassThrough.append(newPassThrough)
                
        
        #Connecting the mapper to the last element of the list
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.listPassThrough[-1].GetOutputPort())
                
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().SetPointSize(2)
        
        #Ici on change le style d'interaction de la caméra
        self.style = InteractorStylePickPoints(self)
        self.style.SetPoints(self.extractSelection.GetOutput())
        self.SetInteractorStyle(self.style)
        
        areaPicker = vtk.vtkAreaPicker()
        self.iren.SetPicker(areaPicker)        
        self.ren.AddActor(actor)               
        self.iren.Initialize()
        self.iren.Start()
        
        self.displaySideView()

    def enableDepthFilter(self):
        
        #Filter within bounding box
        self.extractVolume = vtk.vtkExtractPolyDataGeometry()
        self.extractVolume.SetInputConnection(self.listPassThrough[0].GetOutputPort())
        boundingBox = vtk.vtkBox()
        boundingBox.SetBounds(self.extractSelection.GetOutput().GetBounds())
        self.extractVolume.SetImplicitFunction(boundingBox)
        self.listPassThrough[1].SetInputConnection(self.extractVolume.GetOutputPort())
    def disableDepthFilter(self):
        self.listPassThrough[1].SetInputConnection(self.listPassThrough[0].GetOutputPort())
    
    def enableConfidenceFilter(self):
        self.thresholdIn = vtk.vtkThresholdPoints()
        self.thresholdIn.SetInputConnection(self.listPassThrough[1].GetOutputPort())
        self.listPassThrough[2].SetInputConnection(self.thresholdIn.GetOutputPort())
        self.thresholdIn.ThresholdByUpper(0)
             
    def disableConfidenceFilter(self):
        self.listPassThrough[2].SetInputConnection(self.listPassThrough[1].GetOutputPort())
    
    def enableOutlierFilter(self):
        self.outlierFilter =  vtk.vtkRadiusOutlierRemoval()
        self.outlierFilter.SetNumberOfNeighbors(0)
        self.outlierFilter.SetRadius(0)
        self.outlierFilter.GenerateVerticesOn()
        self.outlierFilter.SetInputConnection(self.listPassThrough[2].GetOutputPort()) 
        self.listPassThrough[3].SetInputConnection(self.outlierFilter.GetOutputPort())
        
    def disableOutlierFilter(self):
        self.listPassThrough[3].SetInputConnection(self.listPassThrough[2].GetOutputPort())
        
    def enableMesh(self):
        self.meshFilter = vtk.vtkDelaunay2D()
        self.meshFilter.SetAlpha(0)
        self.meshFilter.SetInputConnection(self.listPassThrough[3].GetOutputPort())      
        self.listPassThrough[4].SetInputConnection(self.meshFilter.GetOutputPort())

    def disableMesh(self):
        self.listPassThrough[4].SetInputConnection(self.listPassThrough[3].GetOutputPort())
        
    def enableMeshSmoothing(self):
        self.smoothFilter = vtk.vtkSmoothPolyDataFilter()
        self.smoothFilter.SetNumberOfIterations(0)
        self.smoothFilter.SetRelaxationFactor(0)
        self.smoothFilter.FeatureEdgeSmoothingOff()
        self.smoothFilter.BoundarySmoothingOn()
        self.smoothFilter.SetInputConnection(self.listPassThrough[4].GetOutputPort())
        self.listPassThrough[5].SetInputConnection(self.smoothFilter.GetOutputPort())

    def disableMeshSmoothing(self):
        self.listPassThrough[5].SetInputConnection(self.listPassThrough[4].GetOutputPort())
    
    
    def centerCamera(self):
        """
        Recentre la caméra en (0, 0, 0), fait face aux points
        """
        pass
    
    def setZBounds(self, z1, z2):
        print("[PointCloudsVisualisator] setZBounds ", z1, z2)
        bounds = self.listPassThrough[0].GetOutput().GetBounds()
        boundingBox = vtk.vtkBox()
        boundingBox.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], float(z1), float(z2))
        self.extractVolume.SetImplicitFunction(boundingBox)
        self.extractVolume.Modified()
        self.repaint()
        
    def setConfidenceThreshold(self, thres):
        self.thresholdIn.ThresholdByUpper(thres)
        self.thresholdIn.Modified()
        self.repaint()
        
    def setOutlierOptions(self, neighbors, rad):
        self.outlierFilter.SetRadius(rad)
        self.outlierFilter.SetNumberOfNeighbors(neighbors)
        self.outlierFilter.Modified()
        self.repaint()

        
    def setMeshAlpha(self, alpha):
        print("[PCV] setMeshAlpha", alpha)
        self.meshFilter.SetAlpha(alpha)
        self.meshFilter.Modified()
        self.repaint()

        
    def setSmoothingOptions(self, iterations, relaxation):
        print("[PCV] setSmoothingOptions", iterations, relaxation)

        self.smoothFilter.SetNumberOfIterations(iterations)
        self.smoothFilter.SetRelaxationFactor(relaxation)
        self.smoothFilter.Modified()
        self.repaint()

    def writeSTL(self, fileName):
        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName(fileName)
        stlWriter.SetInputData(self.listPassThrough[-1].GetOutput())
        stlWriter.Write()
    
    def writePLY(self, fileName):
        plyWriter = vtk.vtkPLYWriter()
        plyWriter.SetFileName(fileName)
        plyWriter.SetInputData(self.listPassThrough[-1].GetOutput())
        plyWriter.Write()
    
    def customColoriser(self, RGBlistColor):
        lut = vtk.vtkColorTransferFunction()
        scalarRange = self.pointsData.GetScalarRange()
        x = np.linspace(scalarRange[0], scalarRange[1], len(RGBlistColor))
        for i in range(len(RGBlistColor)):
            lut.AddRGBPoint(x[i], RGBlistColor[i][0], RGBlistColor[i][1], RGBlistColor[i][2])
        lut.Build()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())
        
    def defaultColoriser(self):
        lut = vtk.vtkLookupTable()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())

    def customAlphaColoriser(self):
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.0,1.0)
        lut.SetAlphaRange(0.0, 1.0)
        lut.SetRampToSCurve()
        lut.Build()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())
    
    def setBackgroundColor(self, color):
        self.ren.SetBackground(color)
    
    def hideOutliningCube(self):
        self.actorOutline.SetVisibility(False)
    
    def showOutliningCube(self):
        self.actorOutline.SetVisibility(True)
    
    def hideAxes(self):
        self.actorAxes.SetVisibility(False)
    
    def showAxes(self):
        self.actorAxes.SetVisibility(True)
    
    def hideDepthIndicator(self):
        self.actorZAxis.SetVisibility(False)
    
    def showDepthIndicator(self):
        self.actorZAxis.SetVisibility(True)
        
    def showLookupTable(self):
        self.scalarBar.SetVisibility(True)
        
    def hideLookupTable(self):
        self.scalarBar.SetVisibility(False)

    def displayFrontView(self):
        self.camera.SetPosition(0, 0, 0)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.SetFocalPoint(0, 0, 1)
        self.ren.ResetCamera()
    
    def displaySideView(self):
        self.camera.SetPosition(0, 0, 0)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.SetFocalPoint(1, 0, 0)
        self.ren.ResetCamera()
    
    def displayTopView(self):
        self.camera.SetPosition(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)
        self.camera.SetFocalPoint(0, -1, 0)
        self.ren.ResetCamera()
        
    def displayIsometricView(self):
        self.camera.SetPosition(0, 0, 0)
        self.camera.SetViewUp(1, 1, 1)
        self.camera.SetFocalPoint(1, -1, 1)
        self.ren.ResetCamera()
        
    def addBannedIds(self, ids):
        for i in range(ids.GetNumberOfTuples()):
            #print(ids.GetValue(i))
            self.bannedIds.InsertNextValue(ids.GetValue(i))
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.Modified()
        
    def clearBannedIds(self):
        self.bannedIds = vtk.vtkIdTypeArray()
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.Modified()

 
    def __init__(self, generator):
        super().__init__()
        self.pointsData = vtk.vtkPolyData()
        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.GetRenderWindow().GetInteractor()
        self.camera = vtk.vtkCamera ();
        self.camera.SetPosition(0, 0, 0);
        self.camera.SetFocalPoint(1, 0, 0);
        self.ren.SetActiveCamera(self.camera)
        self.bannedIds = vtk.vtkIdTypeArray()
        self.bannedIds.SetNumberOfComponents(1)
        
        self.updatePoints(generator)
        del(generator)
        self.initPipeline()
        self.initOutline()
        self.initAxes()
        self.initDepthIndicator()
        self.initScalarBar()

  
    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, val):
        self._generator = val
        
    @property
    def dataFilter(self):
        return self._dataFilter

    @dataFilter.setter
    def dataFilter(self, val):
        self._dataFilter = val
        self.updatePoints()
    
    @property
    def coloriser(self):
        return self._coloriser

    @coloriser.setter
    def coloriser(self, val):
        self._coloriser = val
        self.updateColors()
 