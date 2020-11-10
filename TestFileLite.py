import traceback
try:
    # standard modules
    import clr # noqa E402
    import math # noqa E402
    import os # noqa E402
    import re # noqa E402
    import sys # noqa E402
    import System # noqa E402
    
    from System.Collections.Generic import * # noqa E402, start including this?
    
    # Revit API
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    import Autodesk # noqa E402
    from Autodesk.Revit.UI import * # noqa E402
    from Autodesk.Revit.DB import * # noqa E402
    import Autodesk.Revit.UI.Selection # noqa E402
    
    # revit doc parameters
    doc = __revit__.ActiveUIDocument.Document
    app = __revit__.Application
    version = __revit__.Application.VersionNumber.ToString()
    uidoc = __revit__.ActiveUIDocument
    currentView = __revit__.ActiveUIDocument.ActiveView
    
    user = str(System.Environment.UserName)
    tol = 0.001
    
    # transaction variables
    t = Transaction(doc, "Generic Transaction")
    tStart = t.Start()
    tEnd = t.Commit()
    
    def RemoveInvisibleLines(lineObj=None, lineStyle=None):
        pass
    
    
    def ChangeLineStyle(modelLineObj, replaceLineStyle="<Hidden>"):
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
    
    def RemoveInvisibleLines(doc, replacementLineStyle="Lines"):
        element = None # search walls, floors, etc
        linePatternElements = [i.Name for i in FilteredElementCollector(doc).OfClass(LinePatternElement)]
        print(linePatternElements)
        print(len(linePatternElements))
        categories = doc.Settings.Categories
        lineCategories = categories.get_Item(BuiltInCategory.OST_Lines)
        subCategories = lineCategories.SubCategories
        
        matchedItem = subCategories.get_Item(replacementLineStyle)
        
        t = Transaction(doc, "Change Line Style")
        t.Start()
        # replace the line style of input line with the - hopefully - single graphics style obj that matches the line style it will be replaced with
        # CHANGE LINESTYLE HERE
        t.Commit()
        
    def SearchViewForOverrides(doc):
        # Autodesk.Revit.DB.View 
        vista = doc.ActiveView
        # ICollection<ElementId>
        lstFilterView = vista.GetFilters()
        print(lstFilterView)
        for filterId in lstFilterView:
            # FilterElement
            fel = doc.GetElement(filterId)
            print(fel)
            # OverrideGraphicSettings
            cfg = vista.GetFilterOverrides(fel.Id)
            print(cfg)
    
    def SearchViewForOverrides2(doc, elements):
        if type(elements) is not list:
            elements = [elements]
        
        output = []
        for element in elements:
            activeview = doc.ActiveView
            #override = [i for i in activeview.GetElementOverrides(element.Id).SetProjectionLinePatternId]
            #override = activeview.GetElementOverrides(element.Id).SetProjectionLinePatternId
            override = activeview.GetElementOverrides(element.Id)
            print(override.ProjectionLinePatternId)
            #color = None
            #if override.ProjectionFillColor.IsValid:
                #color = ','.join(override.ProjectionFillColor.Red.ToString(),override.ProjectionFillColor.Blue.ToString(),override.ProjectionFillColor.Green.ToString())
            #else:
                #fels = activeview.GetFilters()
                #for fel in fels:
                    #filtercats = [x for x in doc.GetElement(fel).GetCategories()]
                    ## Check if element category corresponds to filter category
                    #if element.Category.Id in filtercats:
                        #filterrules = doc.GetElement(fel).GetRules()
                        #rulepassed = []
                        ## Check if element passes all filter rules
                        #for frule in filterrules:
                            #rulepassed.append(frule.ElementPasses(element))
                        #if all(rulepassed):
                            #override = activeview.GetFilterOverrides(fel)
                            ## BEWARE: THIS PART ASSUMES THAT MULTIPLE FILTERS DOES NOT COLLIDE IN REGARDS TO COLOR DEFINITION OF THE ELEMENT
                            #if override.ProjectionFillColor.IsValid:
                                #color = ','.join([override.ProjectionFillColor.Red.ToString(),override.ProjectionFillColor.Blue.ToString(),override.ProjectionFillColor.Green.ToString()])
                            #else:
                                #pass
                        ## Otherwise element does not satisfy the filter
                        #else:
                            #pass
                    ## Otherwise the element category does not correspond to the filter category
                    #else:
                        #pass
                ## Check if color has been previously defined.
                ## If the color is retrieved based on material, our element may consist of multiple materials.
                #if not color:
                    #color = list()
                    #mats = [doc.GetElement(x) for x in element.GetMaterialIds(False)]
                    #for mat in mats:
                        #color.append(','.join([mat.Color.Red.ToString(),mat.Color.Blue.ToString(),mat.Color.Green.ToString()]))
                #else:
                    #pass
            #output.append(color)
            #return(output)
    
    def SearchViewForOverrides3(doc, ID):
        ogs = OverrideGraphicSettings();
        ogs.SetProjectionLineColor(Color(0,255,0));
        
        t = Transaction(doc, "Set Element Override")
        t.Start()
        doc.ActiveView.SetElementOverrides(ID, ogs)
        t.Commit()
    def SearchViewForOverrides5(doc):
        ogs = OverrideGraphicSettings();
        
        t = Transaction(doc, "Set Element Override")
        t.Start()
        doc.ActiveView.SetElementOverrides(ogs)
        t.Commit()
    
    def findlinestyle(replaceLineStyle="<Hidden>"):
        _styles = [i for i in FilteredElementCollector(doc).OfClass(GraphicsStyle)]
        invisibleLineStyle = None
        for g in _styles:
            if (g.Name == "<Invisible lines>"):
                invisibleLineStyle = g;
                print(type(g.Id))

        print(invisibleLineStyle)
        blah = LinePatternElement.GetLinePattern(doc, invisibleLineStyle.Id)
        return(blah)
        
    def SearchViewForOverrides4(doc, ID):
        ogs = OverrideGraphicSettings()
        # what is SearchViewForOverrides???
        ogs.SetProjectionLinePatternId(findlinestyle())
        
        t = Transaction(doc, "Set Element Override")
        t.Start()
        doc.ActiveView.SetElementOverrides(ID, ogs)
        #doc.ActiveView.SetCategoryOverrides(ID, ogs)
        t.Commit()   
        
    def LineStyleStuffandLinePattern():
        pass
        """
        var linePatternElements = new FilteredElementCollector(doc).OfClass(typeof(LinePatternElement)).ToList();
        var categories = doc.Settings.Categories;
        var lineCat = categories.get_Item(BuiltInCategory.OST_Lines);
        var subcats = lineCat.SubCategories;
        Category matchedItem = subcats.get_Item(LineStyleName);
        matchedItem.SetLineWeight(LineWidth,GraphicsStyleType.Projection);
        matchedItem.LineColor = new Color(red, green, blue);
        var linePatternElem = linePatternElements.FirstOrDefault(x => x.Name == LineStyleName);
        if (linePatternElem != null)
        {
            matchedItem.SetLinePatternId(linePatternElem.Id,GraphicsStyleType.Projection);
        }
         if you want to change Line Pattern, you can use:
        
        var lpElement = matchedItem as LinePatternElement;
        var oldPattern = lpElement.GetLinePattern();
        var lineSegs = new List<LinePatternSegment>();
        foreach (var seg in mydata)
        {
             var segType = (LinePatternSegmentType)Enum.Parse(typeof(LinePatternSegmentType), seg.Key);
             var segValue = Convert.ToDouble(seg.Value);
             lineSegs.Add(new LinePatternSegment(segType, segValue));
        }
        try
        {
             oldPattern.SetSegments(lineSegs);
             lpElement.SetLinePattern(oldPattern);
        }
        catch{ }
        """
    
    
    def DeleteImportedLineStyles(doc):
        
        
        
        #The inputs to this node will be stored as a list in the IN variable.
        dataEnteringNode = IN
        
        #unwrap all elements to use with API
        elements = []
        for i in IN[0]:
            elements.append(UnwrapElement(i))
        
        idsToDelete = List[Autodesk.Revit.DB.ElementId]()
        for i in elements:
            idsToDelete.Add(i.Id)
        
        # "Start" the transaction
        TransactionManager.Instance.EnsureInTransaction(doc)
        
        doc.Delete(idsToDelete)
        
        # "End" the transaction
        TransactionManager.Instance.TransactionTaskDone()
        
        message = "You have successfully deleted n " + str(idsToDelete.Count) + " elements from Revit model."
        
        OUT = 'n'.join('{:^35}'.format(s) for s in message.split('n'))    
    
    def DeleteUnusedLineStyles(doc):
        # get category object for lines
        lineCategories = categories.get_Item(BuiltInCategory.OST_Lines)
        # get category object for 
        
    
    def ViewOptions():
        viewOpt = ViewDuplicateOption()
        
    
    def GetElemOverridesInView2(doc, elemId):
        # collect all views in doc that are not view templates
        viewObjs = [i for i in FilteredElementCollector(doc).OfClass(View) if not i.IsTemplate]
        
        # collect all elements in all collected views
        elementsInViews = [FilteredElementCollector(doc, i.Id) for i in viewObjs]
        
        #elemOverridesInViews = [i.GetElementOverrides
        
        overrides = doc.ActiveView.GetElementOverrides(elemId)
        print(overrides)
    
    def GetListOfLinestyles(doc):
        categoryObjs = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
        subCategoryObjs = categoryObjs.SubCategories
        
        for linestyle in subCategoryObjs:
            print("Linestyle {0} id:{1}".format(linestyle.Name, linestyle.Id))
    
    def GetElemOverridesInView(doc, elemId):
        # collect all elements in all collected views
        elementsInView = [i for i in FilteredElementCollector(doc, doc.ActiveView.Id)]
        print(len(elementsInView))
        
        elementOverrideObjs = [doc.ActiveView.GetElementOverrides(i.Id) for i in elementsInView] # --> OverrideGraphicSettings object
        print(len(elementOverrideObjs))
        
        testOver = doc.ActiveView.GetElementOverrides(elemId)
        print(testOver.ProjectionLinePatternId)
         
        
        
    # change line style
    reference = uidoc.Selection.PickObject(Selection.ObjectType.Element, "Select Line")
    elemId = reference.ElementId
    elemObj = doc.GetElement(elemId)
    #print(elemObj)
    
    
    GetListOfLinestyles(doc)
    GetElemOverridesInView(doc, elemId)
    

except:
    # print traceback in order to debug file
    print(traceback.format_exc())    