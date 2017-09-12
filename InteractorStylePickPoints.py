# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:42:36 2017

@author: Maxime Piergiovanni
"""
import vtk


class InteractorStylePickPoints(vtk.vtkInteractorStyleRubberBandPick):
    def __init__(self, pointCloudVisualisator):
        self.pointCloudVisualisator = pointCloudVisualisator
        self.SelectedMapper = vtk.vtkDataSetMapper()
        self.SelectedActor = vtk.vtkActor()
        self.SelectedActor.SetMapper(self.SelectedMapper)
        self.Points = None
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        
    def SetPoints(self, points):
        self.Points = points
    
        
    def leftButtonReleaseEvent(self, obj, event):
        self.OnLeftButtonUp()
        frustum = self.GetInteractor().GetPicker().GetFrustum()
        extractGeometry = vtk.vtkExtractGeometry()
        extractGeometry.SetImplicitFunction(frustum)
        extractGeometry.SetInputData(self.Points)
        extractGeometry.Update()
        
        glyphFilter = vtk.vtkVertexGlyphFilter()
        glyphFilter.SetInputConnection(extractGeometry.GetOutputPort())
        glyphFilter.Update()
        
        selected = glyphFilter.GetOutput()
        self.SelectedMapper.SetInputData(selected)
        self.SelectedMapper.ScalarVisibilityOff()
        
        ids = vtk.vtkIdTypeArray.SafeDownCast(selected.GetPointData().GetAbstractArray("vtkOriginalPointIds"))
        #Envoi des donnees au visualiser
        self.pointCloudVisualisator.addBannedIds(ids)

        self.GetInteractor().GetRenderWindow().Render()
        self.HighlightProp(None)

