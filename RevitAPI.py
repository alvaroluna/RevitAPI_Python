# standard modules
import clr 
import math 
import os 
import re 
import sys 
import System 
import traceback 

# Revit API modules
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import Autodesk 
from Autodesk.Revit.UI import * 
from Autodesk.Revit.DB import * 
import Autodesk.Revit.UI.Selection 

######################
## GLOBAL VARIABLES ##
######################

# THIS NEEDS TO DIFFERENTIATE BETWEEN BEING CALLED FROM DYNAMO OR REVIT...
# THESE VARIABLES WILL CAUSE THE FILE TO FAIL IN DYNAMO
# revit doc paramFloatseters
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
version = __revit__.Application.VersionNumber.ToString()
uidoc = __revit__.ActiveUIDocument
currentView = __revit__.ActiveUIDocument.ActiveView

# transaction variables
t = Transaction(doc, "Generic Transaction")
tStart = t.Start()
tEnd = t.Commit()

# immediately needed global paramFloatseters
currentConfig = None
    
# pyRevit progress bar in console window
progressIndex = 0.0

# global paramFloatseters
user = str(System.Environment.UserName)
tol = 0.001
selectionType = None


#######################################################
## FUNDEMENTAL GEOMETRY & DERIVATIVES | DATA OBJECTS ##
## geometry objects, not drawn in model space        ##
#######################################################

# create
def CreateVector(xFloat=0.0, yFloat=0.0, zFloat=1.0): # -> XYZ
    # XYZ object | Z vector
    vectorObj = Autodesk.Revit.DB.XYZ(xFloat, yFloat, zFloat)
    return(vectorObj)

def CreateVectorByCoords(startCoordTupFloat=(0,0,0), endCoordTupFloat=(0,0,1)): # -> XYZ
    xFloat = endCoordTupFloat[0] - startCoordTupFloat[0]
    yFloat = endCoordTupFloat[1] - startCoordTupFloat[1]
    zFloat = endCoordTupFloat[2] - startCoordTupFloat[2]
    # XYZ object
    vectorObj = Autodesk.Revit.DB.XYZ(xFloat, yFloat, zFloat)
    return(vectorObj)

def CreateVectorByPts(ptObjStart=None, ptObjEnd=None, normalizeBoolBool=False): # -> XYZ
    xFloat = ptObjEnd.X - ptObjStart.X
    yFloat = ptObjEnd.Y - ptObjStart.Y
    zFloat = ptObjEnd.Z - ptObjStart.Z
    # XYZ object
    vectorObj = Autodesk.Revit.DB.XYZ(xFloat, yFloat, zFloat)
    return(vectorObj)

def CreateVectorXProduct(): # -> XYZ
    vectorObj = bEnd.CrossProduct(XYZ.BasisZ).normalizeBool()
    return(vectorObj)

def CreatePoint(xFloat=0.0, yFloat=0.0, zFloat=0.0): # -> XYZ
    # XYZ object
    ptObj = Autodesk.Revit.DB.XYZ(xFloat, yFloat, zFloat)
    return(ptObj)

def CreateCPlane(originPtObj=None, normalVectorObj=None, xVectorObj=None): # -> Plane
    # XYZ objects
    if not originPtObj:
        originPtObj = CreatePoint(0,0,0)
    if not normalVectorObj:
        normalVectorObj = CreateVector(0,0,1)
    if not xVectorObj:
        xVectorObj = CreateVector(1,0,0)
    # Plane object
    cPlaneObj = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(normalVectorObj, originPtObj)
    return(cPlaneObj)




################################################
## FUNDEMENTAL GEOMETRY | REVIT OBJECTS       ##
## geometry objects, not drawn in model space ##
################################################

# create
def CreateRefPlane(doc, xAxisVectorObj=None, originPtObj=None, yAxisVectorObj=None): # -> NewReferencePlane
    # constructs reference plane, different from Reference Plane object

    # Autodesk.Revit.Creation.ItemFactoryBase
    if not xAxisVectorObj:
        xAxisVectorObj = CreateVector(1,0,0)
    if not originPtObj:
        originPtObj = CreatePoint(0,0,0)
    if not yAxisVectorObj:
        yAxisVectorObj = CreateVector(0,1,0)
    # reference plane on the level of the active view
    t = Transaction(doc, "Generic Transaction")
    t.Start()
    refPlaneObj = doc.Create.NewReferencePlane(xAxisVectorObj, originPtObj, yAxisVectorObj, doc.ActiveView)
    t.Commit()
    return(refPlaneObj)

def CreateSketchPlane(doc, refPlaneId=None): # -> SketchPlane
    # sketch planes are based off of reference planes, which are revit objects analagous to C planes

    if not refPlaneId:
        refPlaneId = CreateRefPlane(doc).Id
    # Autodesk.Revit.DB.SketchPlane
    t = Transaction(doc, "Generic Transaction")
    t.Start()
    sketchPlaneObj = Autodesk.Revit.DB.SketchPlane.Create(doc, refPlaneId)
    t.Commit()
    return(sketchPlaneObj)




################################################
## CURVE OBJECTS & DERIVATIVES                ##
## geometry objects, not drawn in model space ##
################################################

# create
def CreateLine(ptObjStart, ptObjEnd): # -> Line
    if not ptObjStart or not ptObjEnd:
        print("Pass XYZ objects as input paramFloatseters")
    lineObj = Autodesk.Revit.DB.Line.CreateBound(ptObjStart, ptObjEnd)
    return(lineObj)

def CreateInterpCrv(crvObjList, reverseBool=False): # -> CurveByPoints | can convert to Curve
    intCrvObj = Autodesk.Revit.DB.CurveByPoints(crvObjList)
    return(intCrvObj)

def CreateNurbsCrv(ptList, degreeInt=3, knotFloatList=None, weightFloatList=None): # -> NurbsSpline
    crvObj = Autodesk.Revit.DB.NurbSpline.CreateCurve(degreeInt, knotFloatList, ptList, weightFloatList)
    return(crvObj)

# get properties
def CrvPtByparamFloats(crv, paramFloats=0.5, normalizeBool=True): # -> [XYZ]
    # pass single value or list of values | float
    if type(paramFloats) is not list:
        paramFloats = [paramFloats]
    
    # Autodesk.Revit.DB.Line.Evaluate(paramFloats, normalizeBool)
    ptObjList = [crv.Evaluate(t, normalizeBool) for t in paramFloats]
    return(ptObjList)

def JoinCrvs(crvObjList=None, reverseBool=False): # -> CurveLoop
    # empty curve loop
    # crvLoopObj = Autodesk.Revit.DB.CurveLoop()
    # crvLoopObj.Append(crvObj)
    crvLoopObj = Autodesk.Revit.DB.CurveLoop.Create(crvObjList) # WHY DOESNT IT NEED TO BE INSTANTIATED?

    # Autodesk.Revit.CurveLoop
    return(crvLoopObj)




#########################################
## MODEL CURVE OBJECTS & DERIVATIVES   ##
## revit objects, baked in model space ##
#########################################

# create
def CreateModelLine(doc, ptObjStart, ptObjEnd, sketchPlaneObj=None, lineStyleStr=None):
    if not sketchPlaneObj:
        sketchPlaneObj = CreateSketchPlane(doc)
    # doc.Create.NewModelCurve(Line.CreateBound(XYZ.Zero, new XYZ(10, 10, 10)), SketchPlane.Create(doc, refPlane.Id))
    t = Transaction(doc, "Generic Transaction")
    t.Start()
    modelLineObj = doc.Create.NewModelCurve(CreateLine(ptObjStart, ptObjEnd), sketchPlaneObj)
    
    if lineStyleStr:
        pass # changle linestyle method
    
    t.Commit()
    return(modelLineObj)

def CreateDetailLine(doc, ptObjStart, ptObjEnd, sketchPlaneObj=None, lineStyleStr=None):
    pass

def CreateDimension(doc):
    # create model curves to convert to dimensions
    # refArr.Append(modelCurve.GeometryCurve.GetEndPointReference(0))
    # dim = doc.Create.NewDimension(doc.ActiveView, Line.CreateBound(XYZ.Zero, new XYZ(10, 0, 0)), refArr)
    # ElementTransformUtils.MoveElement(doc, dim.Id, new XYZ(0, 0.1, 0))
    pass




##################################################
## SURFACE OBJECT & DERIVATIVES                 ##
## geometry objects, not drawn in model space   ##
## some of these only work in the family editor ##
##################################################

# create
def CreatePlanarSrf():
    pass

# get properties
def PlanarSrfArea(faceObj):
    # PlanarFace object
    if type(faceObj) is list:
        areaList = [i.Area for i in faceObj]
        return(areaList)
    else:
        return(faceObj.Area)






####################################################################
## SYSTEM FAMILY METHODS                                          ##
## it is possible to get the geo derivatives of geo directly, but ##
## with families you have to extract the base geometry by using   ##
## specific extraction classes within the Revit API               ##
####################################################################

# create
def CreateWallByFace(doc):
    pass

def CreateWallByCL(doc, clCrvObjs, levelId, structuralBool=True):
    # create ability to pass iterble or single paramFloatseter
    if type(clCrvObjs) is Autodesk.Revit.DB.CurveLoop:
            pass

    t = Transaction(doc, "Generic Transaction")
    t.Start()
    wallObj = Autodesk.Revit.DB.Wall.Create(doc, clCrvObjs, levelId, structuralBool)
    t.Commit()
    return(wallObj)

def CreateWallByCLAdvan(doc, clCrvObjs, levelId, heightFloat=10.0, wallTypeStr=None, offsetFloat=0.0, flipBool=False, structuralBool=True):
    # wall type
    
    if not wallTypeStr:
        pass

    t = Transaction(doc, "Generic Transaction")
    t.Start()
    wallObj = Autodesk.Revit.DB.Wall.Create(doc, wallType.Id, levelId, heightFloat, offsetFloat, flipBool, structuralBool)
    t.Commit()
    return(wallObj)


# get properties | further geometric processing must be done using that respective geo objects' methods
def GetWallCenterline(wallObjs, toDynamo=False): # -> lineObjList
    # ensure input is iterable
    if type(wallObjs) is not list:
        wallObjs = [wallObjs]
    
    # other option is to use .ToDSType(True)
    if toDynamo:
        locationCrvList = [i.Location.Curve.ToProtoType() for i in wallObjs]
    if not toDynamo:
        locationCrvList = [i.Location.Curve for i in wallObjs]
    
    return(locationCrvList)

def GetWallCenterlineAsModelLine(wallObjs):
    locationCrvList = GetWallCenterline(wallObjs)
    convert2ModelLines = None
    return(locationCrvList)

def GetFrontBackWallFace(doc, wallObj=None, front=True, test=False): # -> srfObjList
    # for testing purposes, select wall from model
    if test:
        wallObj = CollectUserSelectionObjs()
    
    faceObjList= []
    for i in wallObj:
        # Autodesk.Revit.DB.HostObjectUtils
        if front:
            # this returns a Reference obj
            wallFaceRefList = Autodesk.Revit.DB.HostObjectUtils.GetSideFaces(i, Autodesk.Revit.DB.ShellLayerType.Exterior)
        else:
            wallFaceRefList = Autodesk.Revit.DB.HostObjectUtils.GetSideFaces(i, Autodesk.Revit.DB.ShellLayerType.Interior)
        
        faceObj = doc.GetElement(wallFaceRefList[0]).GetGeometryObjectFromReference(wallFaceRefList[0])
        faceObjList.append(faceObj)
    
    return(faceObjList)

def GetWallFaceByIndex(doc):
    pass

def GetCeilingGridFaces(doc, ceilingObj=None, test=False):
    # for testing purposes, select wall from model
    if test:
        ceilingObj = CollectUserSelectionObjs()
    
    faceObjList= []
    for i in ceilingObj:
        # Autodesk.Revit.DB.HostObjectUtils
        # this returns a Reference obj
        cFaceRefList = Autodesk.Revit.DB.HostObjectUtils.GetBottomFaces(i)
        
        faceObj = doc.GetElement(cFaceRefList[0]).GetGeometryObjectFromReference(cFaceRefList[0])
        faceObjList.append(faceObj)
    
    return(faceObjList)

def GetCeilingGridLines(doc, ceilingObj=None, test=False):
    # for testing purposes, select wall from model
    if test:
        ceilingObj = CollectUserSelectionObjs()
    
    crvObjList= []
    for i in ceilingObj:
        ceilingType = doc.GetElement(i.GetTypeId())
        compoundStructure = ceilingType.GetCompoundStructure()
        for j in compoundStructure.GetLayers():
            # Autodesk.Revit.DB.Material 
            layerMaterial = doc.GetElement(j.MaterialId)

            # FillPatternElement | API CHANGE IN REVIT 2020!
            if version == "2020":
                # Material.SurfaceForegroundPatternId | Material.SurfaceBackgroundPatternId
                surfacePattern = layerMaterial.Document.GetElement(layerMaterial.SurfaceForegroundPatternId)
            else:
                surfacePattern = layerMaterial.Document.GetElement(layerMaterial.SurfacePatternId)

            if surfacePattern:
                print(surfacePattern.Name)
                fillPattern = surfacePattern.GetFillPattern()
                if fillPattern:
                    fillGridList = fillPattern.GetFillGrids()
                    # Autodesk.Revit.DB.FillGrid
                    for fillGrid in fillGridList:
                        print("Fill grid properties:")
                        gridOrigin = fillGrid.Origin
                        gridOffset = fillGrid.Offset
                        gridAngle = fillGrid.Angle
                        print("{0}\n{1}\n{2}\n".format(gridOrigin, gridOffset, gridAngle))

def ChangeLineStyle(modelLineObj, replaceLineStyle="<Hidden>"):
    # this function works with both detail and model lines
    
    # get catoegory object of object type you would like to edit
    # Autodesk.Revit.DB.Category
    lineCategoryObj = Category.GetCategory(doc, BuiltInCategory.OST_Lines)
    
    # Autodesk.Revit.DB.Category.GraphicsStyle() & Autodesk.Revit.DB.GraphicsStyle.GraphicsStyleType --> .Projection??? property of object property???
    lineGraphicStyleObj = lineCategoryObj.GetGraphicsStyle(GraphicsStyleType.Projection)
    
    # get category of lineGraphicsStyle
    # Autodesk.Revit.DB.GraphicsStyle.GraphicsStyleCategory.SubCategories --> .SubCategories??? property of object property???
    # returns --> Autodesk.Revit.DB.CategoryNameMap object
    lineGraphicStyleCategoryMapObj = lineGraphicStyleObj.GraphicsStyleCategory.SubCategories
    
    # collect all the line graphics style objects in document
    lineGraphicStyleObjsInDoc = [i.GetGraphicsStyle(GraphicsStyleType.Projection) for i in lineGraphicStyleCategoryMapObj]
    
    # loop through list of all graphics style objects in document and stop loop when match of replacement line style is found
    matchingLineGraphicsStyleObjList = []
    try:
        matchingLineGraphicsStyleObjList.append(next(i for i in lineGraphicStyleObjsInDoc if replaceLineStyle == i.Name))
    except StopIteration:
        pass
    
    t = Transaction(doc, "Change Line Style")
    t.Start()
    # replace the line style of input line with the - hopefully - single graphics style obj that matches the line style it will be replaced with
    modelLineObj.LineStyle = matchingLineGraphicsStyleObjList[0]
    t.Commit()




#############################
## LOADABLE FAMILY METHODS ##
#############################

# FIND EXAMPLES OF HOW TO ALGROITHMICALLY CONTROL THE 'FLEXING' OF 
# FAMILY PARAMETERS WITHIN REVT...EVEN THEIR INTRODUCTION INTO THE MODEL
# AND INITIAL SETTINGS https://primer.dynamobim.org/08_Dynamo-for-Revit/8-3_Editing.html




###########
## VIEWS ##
###########
def ResetOverridesByDuplicatingViews(doc):
    # collect views in doc
    viewObjs = [i for i in FilteredElementCollector(doc).OfClass(View)]
    print(viewObjs)
    
    # in loop: store name, duplicate view, delete view, rename duplicate view
    t = Transaction(doc, "Generic Transaction")
    tStart = t.Start()   
    for i,view in enumerate(viewObjs):
        try:
            currentViewName = view.Name
            duplicateCurrentViewId = view.Duplicate(ViewDuplicateOption().WithDetailing)
            duplicateCurrentViewObj = doc.GetElement(duplicateCurrentViewId)
            doc.Delete(view.Id)
            duplicateCurrentViewObj.Name = currentViewName

        except:
            # delete duplicate view if something failed
            try:
                doc.Delete(duplicateCurrentViewId)
            except:
                print("Delete of duplicate view also failed")
            print("View {0}, ID: {1} failed".format(view.Name, view.Id))
    tEnd = t.Commit()

def GetListOfLinestyles(doc):
    categoryObjs = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
    subCategoryObjs = categoryObjs.SubCategories
    
    for linestyle in subCategoryObjs:
        print("Linestyle {0} id:{1}".format(linestyle.Name, linestyle.Id))





##########################
## MODEL EXPORT METHODS ##
##########################

# IFC

# DWG

# google docs




#############################
## GEOMETRY IMPORT METHODS ##
#############################

# rhino




#################################
## DOCUMENT COLLECTION METHODS ##
#################################

# of class collector vs BuiltInCategory - this gives you whole category id instead of elements id

# notes encapsulated in a function - not for use in code
def OfClassDataTypes(objNameStr="Wall"):
    # not meant to be used, but as a record of common
    # OfClass selection options
    objDict = {
        "Wall" : Wall,
        "Level" : Level,
    }
    return(objDict[objNameStr])

# suspend revit to collect
def RequestUserSelectionId():
    reference = uidoc.Selection.PickObject(Selection.ObjectType.Element, "Generic comment")
    elementId = elementRef.ElementId
    return(elementId)

def RequestUserSelectionObj():
    elementRef = uidoc.Selection.PickObject(Selection.ObjectType.Element, "Generic comment")
    elementId = elementRef.ElementId
    elementObj = doc.GetElement(elementId)
    return(elementId)    

# preselection collection
def CollectUserSelectionIds():
    idList = [objId for objId in uidoc.Selection.GetElementIds()]
    return(idList)

def CollectUserSelectionObjs():
    objList = [doc.GetElement(objId) for objId in uidoc.Selection.GetElementIds()]
    return(objList)

def CollectLevels_Class(doc, nameStr="Level 1"):
    levelObjs = [i for i in FilteredElementCollector(doc).OfClass(Level) if nameStr.lower() in i.Name.lower()]
    if len(levelObjs) == 1:
        levelObjs = levelObjs[0]
    return(levelObjs)

def CollectWalls_Class(doc, nameStr="Level 1"):
    wallObjs = [i for i in FilteredElementCollector(doc).OfClass(Wall) if nameStr.lower() in i.Name.lower()]
    return(wallObjs)

def CollectDoors_Category(doc):
    doorObjs = [i for i in FilteredElementCollector(doc, vista).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)]
    return(doorObjs)




################################################
## DOCUMENT REFERENCE METHODS                 ##
## select parts of geometry from host objects ##
################################################

# see bookmark on personal mac

try:
    ###############
    ## TEST MAIN ##
    ###############
    def Main():
        # point
        print(CreatePoint())

        # vector
        print(CreateVectorByPts(CreatePoint(), CreatePoint(0,0,1)))

        # C plane
        testCplane = CreateCPlane()
        print(testCplane)

        # reference plane
        testRefPlane = CreateRefPlane(doc)
        print(testRefPlane)

        # sketch plane
        testSketchPlane = CreateSketchPlane(doc, testRefPlane.Id)
        print(testSketchPlane)

        # line
        testLine = CreateLine(CreatePoint(), CreatePoint(100,0,0))
        print(testLine)

        # interpolated curve
        # testInterpCrv = CreateInterpCrv()

        # model line
        print(CreateModelLine(doc, CreatePoint(), CreatePoint(100,0,0), testSketchPlane))

        # join curves
        line0 = CreateLine(CreatePoint(), CreatePoint(100,0,0))
        line1 = CreateLine(CreatePoint(100,0,0), CreatePoint(100,100,0))
        lineList = [line0,line1]
        testJoinedCrv = JoinCrvs(lineList)
        print(testJoinedCrv)

        # point at curve paramFloatseter
        print(CrvPtByparamFloats(testLine, [0.25, 0.5, 0.75]))

        # collect levels
        testLevel = CollectLevels_Class(doc, nameStr="Level 1")
        print(testLevel)

        # create walls
        wallObj = CreateWallByCL(doc, testLine, testLevel.Id, True)
        print(wallObj)

        # get wall centerline
        wallCL = GetWallCenterline(wallObj)
        print(wallCL)

        # user selection
        userObjs = CollectUserSelectionObjs()
        print("user selections: {0}".format(userObjs))

        # obtaining front or back wall face
        # print(GetFrontBackWallFace(doc=doc, wallObj=None, front=True, test=False))

        # obtaining ceiling face or lines
        print(GetCeilingGridLines(doc=doc, ceilingObj=None, test=True))
        
        # change line style
        reference = uidoc.Selection.PickObject(Selection.ObjectType.Element, "Select Line")
        modelLineObj = doc.GetElement(reference.ElementId)
        ChangeLineStyle(modelLineObj)        



    if __name__ == "__main__":
        Main()

except:
    # print traceback in order to debug file
    print(traceback.format_exc())