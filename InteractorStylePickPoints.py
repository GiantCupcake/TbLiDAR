# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:42:36 2017

@author: maxpi
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
        
        #self.SelectedActor.GetProperty().SetColor(1.0, 1.0, 1.0)
        #self.SelectedActor.GetProperty().SetPointSize(3)
        #self.GetCurrentRenderer().AddActor(self.SelectedActor)
        self.GetInteractor().GetRenderWindow().Render()
        self.HighlightProp(None)


if __name__ == "__main__":
    import sys
    # create source
    src = vtk.vtkPointSource()
    src.SetCenter(0,0,0)
    src.SetNumberOfPoints(50)
    src.SetRadius(5)
    src.Update()
    
    idFilter = vtk.vtkIdFilter()
    idFilter.SetInputConnection(src.GetOutputPort())
    idFilter.SetIdsArrayName("OriginalIds");
    idFilter.Update()
    
    idFilter2 = vtk.vtkIdFilter()
    idFilter2.SetInputData(idFilter.GetOutput())
    idFilter2.SetIdsArrayName("SecondArray");
    idFilter2.Update()
    """   
    surfaceFilter = vtk.vtkDataSetSurfaceFilter()
    surfaceFilter.SetInputConnection(idFilter.GetOutputPort())
    surfaceFilter.Update()
    """   
    #polyDataInput = surfaceFilter.GetOutput()
    polyDataInput = idFilter2.GetOutput()

    print(polyDataInput)
    
    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyDataInput)
    mapper.ScalarVisibilityOff()
    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    
    areaPicker = vtk.vtkAreaPicker()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetPicker(areaPicker)
    renderWindowInteractor.SetRenderWindow(renWin)
    
    
    # assign actor to the renderer
    ren.AddActor(actor)
    
    renWin.Render()
    
    #style = vtk.vtkInteractorStyleRubberBandPick()
    style = InteractorStylePickPoints()
    style.SetPoints(polyDataInput)
    #style = vtk.vtkInteractorStyleFlight()
    renderWindowInteractor.SetInteractorStyle(style)
      
    # enable user interface interactor
    renderWindowInteractor.Start()