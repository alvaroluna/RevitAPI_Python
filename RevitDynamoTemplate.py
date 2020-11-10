"""
MATCH THESE:

uiApp = extCmdData.Application  # UIApplication
uiDoc = uiApp.ActiveUIDocument  # UIDocument
app = uiApp.Application  # Application
doc = uiDoc.Document  # Document
docfamily = None  # Document
fam = None  # Family
famille = None  # Family
famSym = None  # FamilySymbol
"""

# traceback is used to report to console the exact line and reason python code failed
import traceback

# variable to keep track if code is being run in Dynamo or Revit
isDynamo = False

# print statements as list for output from Dynamo node
printList = []

try:
    # standard modules - both Dynamo and Revit
    import clr
    import math
    import os
    import re
    import sys
    import System
    from System import Array

    # is this being run in Dynamo?
    try:
        # RevitServices for Dynamo
        clr.AddReference("RevitServices")
        import RevitServices
        from RevitServices.Persistence import DocumentManager
        from RevitServices.Transactions import TransactionManager

        # Revit/Dynamo Nodes
        clr.AddReference("RevitNodes")
        import Revit
        clr.ImportExtensions(Revit.Elements)
        clr.ImportExtensions(Revit.GeometryConversion)

        # Dynamo Geometry nodes
        clr.AddReference("ProtoGeometry")
        from Autodesk.DesignScript.Geometry import *

        # Revit API
        clr.AddReference('RevitAPI')
        clr.AddReference('RevitAPIUI')
        import Autodesk
        from Autodesk.Revit.UI import *
        from Autodesk.Revit import DB
        import Autodesk.Revit.UI.Selection

        doc = DocumentManager.Instance.CurrentDBDocument
        uiapp = DocumentManager.Instance.CurrentUIApplication
        app = uiapp.Application
        uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
        
        user = str(System.Environment.UserName)
        tol = 0.001

        # transaction variables
        tStart = TransactionManager.Instance.EnsureInTransaction(doc)
        tEnd = TransactionManager.Instance.TransactionTaskDone()

        # switch toggle, code is being run in dynamo - above didn't fail
        isDynamo = not isDynamo # True

    # ... or Revit?
    except:
        import pprint # only useful within revitw

        print("We are using Revit")
        # Revit API
        clr.AddReference('RevitAPI')
        clr.AddReference('RevitAPIUI')
        import Autodesk
        import Autodesk.Revit.UI.Selection
        from Autodesk.Revit.UI import *
        from Autodesk.Revit.DB import *


        # revit doc parameters
        uidoc = __revit__.ActiveUIDocument
        doc = __revit__.ActiveUIDocument.Document
        app = __revit__.Application
        version = app.VersionNumber.ToString()

        currentView = __revit__.ActiveUIDocument.ActiveView

        user = str(System.Environment.UserName)
        tol = 0.001

        # transaction variables
        t = Transaction(doc, "Generic Transaction")
        tStart = t.Start()
        tEnd = t.Commit()

    # import project modules
    if isDynamo:
        # sys.path.append(IN[0])
        pass
    else:
        # sys.path.append(r"C:\Users\lunaa\OneDrive - Autodesk\ADVISORY SERVICES\Fluor\assets\py")
        pass

    # import python modules here
    # import PythonModule as PM

    if isDynamo:
        # -------------------------- #
        # DYNAMO PROGRAM ENTRY POINT #
        # -------------------------- #

        #region 
        """
        REMEMBER:

        TO USE A REVIT API OBJECT AS DYNAMO INPUT:
        UnwrapElement(IN[0]) 
        
        ... at input is needed to convert between
        dynamo and revit objects so that the api can be used
        on either environments geometric elements

        FOR OUTPUT TO DYNAMO:
        revitObj.ToProtoType()
        """
        #endregion

        # code goes here
        dynamoOutput = None
        
        # this is how you use print statements
        printList.append("Hello World")
        
        
        # outputs | OUT[-1] should always be print statements
        OUT = [dynamoOutput, printList]

    else:
        # ------------------------- #
        # REVIT PROGRAM ENTRY POINT #
        # ------------------------- #
        def Main():
            pass


        if __name__ == "__main__":
            # program entry point
            Main()

except:
    if isDynamo:
        # print traceback in order to debug file | OUT[-1] should always be print statements
	    OUT = ["Code Failed: {0}".format(traceback.format_exc()), printList]
    
    else:
        print(traceback.format_exc())