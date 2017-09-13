# -*- coding: utf-8 -*-
"""
This is the core class of the application.
When constructed, this objects will setup an almost empty VTK pipeline, you then
have to call one of the numerous functions that will add parts to the pipeline
to treat your data.

The class is very easily interfaceable with any GUI library out there, you will
have to change the parent class from QVTKRenderWindowInteractor to the one
that will more suit your need.

Then, it is only a case of linking the methods of this class to your GUI.

Created on Fri Jun 16 11:13:43 2017

@author: Maxime Piergiovanni
"""

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np


from InteractorStylePickPoints import InteractorStylePickPoints
from GenerateFromFile import display_time
 
class PointCloudVisualisator(QVTKRenderWindowInteractor):
        
    def updatePoints(self, interestPoints):
        # Create the geometry of a point (the coordinate)
        points = vtk.vtkPoints()
        # Create the topology of the point (a vertex)
        vertices = vtk.vtkCellArray()
        intensityData = vtk.vtkDoubleArray()
        intensityData.SetNumberOfComponents(1)
        intensityData.SetName("Intensity")
        
        sigmaData = vtk.vtkDoubleArray()
        sigmaData.SetNumberOfComponents(1)
        sigmaData.SetName("Sigma")
        
        depthData = vtk.vtkDoubleArray()
        depthData.SetNumberOfComponents(1)
        depthData.SetName('Depth')
        
        for pi in interestPoints: 
            id = points.InsertNextPoint(pi.pos)
            #vtkCellArray::InsertNextCell	(	vtkIdType 	npts,const vtkIdType * 	pts )
            #Nombre de points puis tableau d'id des points
            vertices.InsertNextCell(1)
            vertices.InsertCellPoint(id)
            intensityData.InsertNextValue(pi.intensity)
            sigmaData.InsertNextValue(pi.sigma)
            depthData.InsertNextValue(pi.pos[2])
            
        
        # Set the points and vertices we created as the geometry and topology of the polydata
        self.pointsData.SetPoints(points)
        self.pointsData.SetVerts(vertices)
        self.pointsData.GetPointData().AddArray(intensityData)
        self.pointsData.GetPointData().AddArray(sigmaData)
        self.pointsData.GetPointData().AddArray(depthData)
        
        
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
        self.scalarBar.SetTitle("Intensity")
        self.scalarBar.SetNumberOfLabels(3)
        self.scalarBar.SetDragable(True)
        self.scalarBar.SetVisibility(False)
        self.ren.AddActor2D(self.scalarBar)
        
        
    def initPipeline(self):
        """
        Create an empty pipeline which will be used to insert different filters
        between the passThrougs
        """

        self.firstAssignAttribute = vtk.vtkAssignAttribute()
        self.firstAssignAttribute.SetInputData(self.pointsData)
        self.firstAssignAttribute.Assign("Intensity", "SCALARS", "POINT_DATA")

        self.selectionNode = vtk.vtkSelectionNode()
        self.selectionNode.SetFieldType(1) # POINT
        self.selectionNode.SetContentType(4) #INDICES
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)
        self.selection = vtk.vtkSelection()
        self.selection.AddNode(self.selectionNode)        
        self.extractSelection = vtk.vtkExtractSelection()
        self.extractSelection.SetInputConnection(0, self.firstAssignAttribute.GetOutputPort())
        self.extractSelection.SetInputData(1, self.selection)
        
        self.geometryFilter = vtk.vtkGeometryFilter()
        self.geometryFilter.SetInputConnection(self.extractSelection.GetOutputPort())
        
        self.listPassThrough = [vtk.vtkPassThrough()]
        self.listPassThrough[0].SetInputConnection(self.geometryFilter.GetOutputPort())
        
        for n in range(6):
            newPassThrough = vtk.vtkPassThrough()
            newPassThrough.SetInputConnection(self.listPassThrough[n].GetOutputPort())
            self.listPassThrough.append(newPassThrough)
                
        #We need to be able to change the scalars right before the mapper
        self.lastAssignAttribute = vtk.vtkAssignAttribute()
        self.lastAssignAttribute.SetInputConnection(self.listPassThrough[-1].GetOutputPort())
        self.lastAssignAttribute.Assign("Intensity", "SCALARS", "POINT_DATA")
        
        #Connecting the mapper to the last element of the list
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.lastAssignAttribute.GetOutputPort())
        self.mapper.SetScalarModeToUsePointData()
                
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
        self.repaint()
    
    def enableConfidenceFilter(self):
        aa = vtk.vtkAssignAttribute()
        aa.SetInputConnection(self.listPassThrough[1].GetOutputPort())
        aa.Assign("Intensity", "SCALARS", "POINT_DATA")
        aa.Update()
        
        self.thresholdIntensity = vtk.vtkThresholdPoints()
        self.thresholdIntensity.SetInputConnection(aa.GetOutputPort())
        self.listPassThrough[2].SetInputConnection(self.thresholdIntensity.GetOutputPort())
        self.thresholdIntensity.ThresholdByUpper(0)
             
    def disableConfidenceFilter(self):
        self.listPassThrough[2].SetInputConnection(self.listPassThrough[1].GetOutputPort())
        self.repaint()
        
    def enableSigmaFilter(self):
        aa = vtk.vtkAssignAttribute()
        aa.SetInputConnection(self.listPassThrough[2].GetOutputPort())
        aa.Assign("Sigma", "SCALARS", "POINT_DATA")
        aa.Update()
        
        self.thresholdSigma = vtk.vtkThresholdPoints()
        self.thresholdSigma.SetInputConnection(aa.GetOutputPort())
        self.listPassThrough[3].SetInputConnection(self.thresholdSigma.GetOutputPort())
        self.thresholdSigma.ThresholdByUpper(0)
    
    def disableSigmaFilter(self):
        self.listPassThrough[3].SetInputConnection(self.listPassThrough[2].GetOutputPort())
        self.repaint()
    
    def enableOutlierFilter(self):
        self.outlierFilter =  vtk.vtkRadiusOutlierRemoval()
        self.outlierFilter.SetNumberOfNeighbors(0)
        self.outlierFilter.SetRadius(0)
        self.outlierFilter.GenerateVerticesOn()
        self.outlierFilter.SetInputConnection(self.listPassThrough[3].GetOutputPort()) 
        self.listPassThrough[4].SetInputConnection(self.outlierFilter.GetOutputPort())
        
    def disableOutlierFilter(self):
        self.listPassThrough[4].SetInputConnection(self.listPassThrough[3].GetOutputPort())
        self.repaint()
        
    def enableMesh(self):
        self.meshFilter = vtk.vtkDelaunay2D()
        self.meshFilter.SetAlpha(0)
        self.meshFilter.SetInputConnection(self.listPassThrough[4].GetOutputPort())      
        self.listPassThrough[5].SetInputConnection(self.meshFilter.GetOutputPort())

    def disableMesh(self):
        self.listPassThrough[5].SetInputConnection(self.listPassThrough[4].GetOutputPort())
        self.repaint()
        
    def enableMeshSmoothing(self):
        self.smoothFilter = vtk.vtkSmoothPolyDataFilter()
        self.smoothFilter.SetNumberOfIterations(0)
        self.smoothFilter.SetRelaxationFactor(0)
        self.smoothFilter.FeatureEdgeSmoothingOff()
        self.smoothFilter.BoundarySmoothingOn()
        self.smoothFilter.SetInputConnection(self.listPassThrough[5].GetOutputPort())
        self.listPassThrough[6].SetInputConnection(self.smoothFilter.GetOutputPort())

    def disableMeshSmoothing(self):
        self.listPassThrough[6].SetInputConnection(self.listPassThrough[5].GetOutputPort())
        self.repaint()
    
    
    def setZBounds(self, z1, z2):
        bounds = self.listPassThrough[0].GetOutput().GetBounds()
        boundingBox = vtk.vtkBox()
        boundingBox.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], float(z1), float(z2))
        self.extractVolume.SetImplicitFunction(boundingBox)
        self.extractVolume.Modified()
        self.repaint()
        
    def setConfidenceThreshold(self, thres):
        self.thresholdIntensity.ThresholdByUpper(thres)
        self.thresholdIntensity.Modified()
        self.repaint()
        
    def setSigmaThreshold(self, thres):
        self.thresholdSigma.ThresholdByLower(thres)
        self.thresholdSigma.Modified()
        self.repaint()
        
    def setOutlierOptions(self, neighbors, rad):
        self.outlierFilter.SetRadius(rad)
        self.outlierFilter.SetNumberOfNeighbors(neighbors)
        self.outlierFilter.Modified()
        self.repaint()

        
    def setMeshAlpha(self, alpha):
        self.meshFilter.SetAlpha(alpha)
        self.meshFilter.Modified()
        self.repaint()

        
    def setSmoothingOptions(self, iterations, relaxation):

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
        
    def writeVTK(self, fileName):
        vtkWriter = vtk.vtkPolyDataWriter()
        vtkWriter.SetFileName(fileName)
        vtkWriter.SetInputData(self.listPassThrough[-1].GetOutput())
        vtkWriter.Write()

    
    @display_time
    def colorByIntensity(self):
        self.scalarBar.SetTitle("Intensity [%]")
        self.lastAssignAttribute.Assign("Intensity", "SCALARS", "POINT_DATA")
        self.firstAssignAttribute.Assign("Intensity", "SCALARS", "POINT_DATA")
        self.mapper.SetScalarRange(self.colorMapPoints.GetPointData().GetAbstractArray('Intensity').GetRange())

    
    @display_time
    def colorBySigma(self):
        self.scalarBar.SetTitle("Sigma [%]")
        self.lastAssignAttribute.Assign("Sigma", "SCALARS", "POINT_DATA")
        self.firstAssignAttribute.Assign("Sigma", "SCALARS", "POINT_DATA")
        self.mapper.SetScalarRange(self.colorMapPoints.GetPointData().GetAbstractArray('Sigma').GetRange())


    @display_time
    def colorByDepth(self):
        self.scalarBar.SetTitle("Depth [m]")
        self.lastAssignAttribute.Assign("Depth", "SCALARS", "POINT_DATA")
        self.firstAssignAttribute.Assign("Depth", "SCALARS", "POINT_DATA")
        self.mapper.SetScalarRange(self.colorMapPoints.GetPointData().GetAbstractArray('Depth').GetRange())

    
    def customColoriser2(self, RGBlistColor):
        lut = vtk.vtkColorTransferFunction()
        scalarRange = self.pointsData.GetScalarRange()
        x = np.linspace(scalarRange[0], scalarRange[1], len(RGBlistColor))
        for i in range(len(RGBlistColor)):
            lut.AddRGBPoint(x[i], RGBlistColor[i][0], RGBlistColor[i][1], RGBlistColor[i][2])
        lut.Build()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())

    def customColoriser(self, RGBlistColor):
        lut = vtk.vtkLookupTable()
        lut.IndexedLookupOff()
        lut.SetTableRange(self.pointsData.GetScalarRange())
        lut.SetNumberOfTableValues(len(RGBlistColor))

        for i in range(len(RGBlistColor)):
            lut.SetTableValue(i, RGBlistColor[i][0], RGBlistColor[i][1], RGBlistColor[i][2])
        lut.Build()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())

        
    def defaultColoriser(self):
        lut = vtk.vtkLookupTable()
        self.mapper.SetLookupTable(lut)
        self.scalarBar.SetLookupTable(self.mapper.GetLookupTable())

    def customAlphaColoriser(self):
        lut = vtk.vtkLookupTable()
        lut.SetAlphaRange(0.0, 1.0)
        lut.SetSaturationRange(0.0,0.0)
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
            self.bannedIds.InsertNextValue(ids.GetValue(i))
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.Modified()
        
    def clearBannedIds(self):
        self.bannedIds = vtk.vtkIdTypeArray()
        self.selectionNode.SetSelectionList(self.bannedIds)
        self.selectionNode.Modified()
        
    @display_time
    def mapColorsFromFilteredPoints(self):
        self.colorMapPoints = self.lastAssignAttribute.GetOutput()
        self.mapper.SetScalarRange(self.colorMapPoints.GetScalarRange())
    
    @display_time
    def mapColorsFromAllPoints(self):
        self.colorMapPoints = self.firstAssignAttribute.GetOutput()
        self.mapper.SetScalarRange(self.colorMapPoints.GetScalarRange())

 
    def __init__(self, generator):
        super().__init__()
        self.pointsData = vtk.vtkPolyData()
        self.colorMapPoints =  self.pointsData
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

  