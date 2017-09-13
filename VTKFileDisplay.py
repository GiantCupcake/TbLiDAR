# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:44:50 2017

@author: maxpi
"""

import vtk
from PointCloudVisualisator import PointCloudVisualisator
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VTKFileDisplay(PointCloudVisualisator):
    
    def __init__(self, fileName):
        QVTKRenderWindowInteractor.__init__(self)
        self.pointsData = vtk.vtkPolyData()
        self.colorMapPoints =  self.pointsData
        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.GetRenderWindow().GetInteractor()
        self.camera = vtk.vtkCamera ();
        self.ren.SetActiveCamera(self.camera)
        self.bannedIds = vtk.vtkIdTypeArray()
        self.bannedIds.SetNumberOfComponents(1)
        
        self.updatePoints(fileName)
        self.initPipeline()
        self.initOutline()
        self.showOutliningCube()
        self.initAxes()
        self.showAxes()
        self.initDepthIndicator()
        self.showDepthIndicator()
        self.initScalarBar()
        self.displayFrontView()

    def updatePoints(self, fileName):
        vtkReader = vtk.vtkPolyDataReader()
        vtkReader.SetFileName(fileName)
        vtkReader.Update()
        print(fileName)
        self.pointsData = vtkReader.GetOutput()
        print(self.pointsData)
        
    def initPipeline(self):
        self.firstAssignAttribute = vtk.vtkAssignAttribute()
        self.firstAssignAttribute.SetInputData(self.pointsData)
        self.firstAssignAttribute.Assign("Intensity", "SCALARS", "POINT_DATA")
        
        self.listPassThrough = [vtk.vtkPassThrough()]
        self.listPassThrough[0].SetInputConnection(self.firstAssignAttribute.GetOutputPort())
        
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
        self.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())      
        self.ren.AddActor(actor)               
        self.iren.Initialize()
        self.iren.Start()
        
        self.displaySideView()
    
    def init(self):
        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.GetRenderWindow().GetInteractor()

        vtkReader = vtk.vtkPolyDataReader()
        vtkReader.SetFileName(self.fileName)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(vtkReader.GetOutputPort())
                
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
          
        self.ren.AddActor(actor)               
        self.iren.Initialize()
        self.iren.Start()
