def RevitDocSetup():
    # standard modules
    import clr
    import math
    import os
    import re
    import sys
    import System
    import traceback

    # Revit API
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    import Autodesk
    from Autodesk.Revit.UI import *
    from Autodesk.Revit.DB import *
    import Autodesk.Revit.UI.Selection

    # revit doc parameters
    # uidoc = __revit__.ActiveUIDocument
    uidoc = Autodesk.Revit.UI.UIApplication.ActiveUIDocument
    # doc = __revit__.ActiveUIDocument.Document
    doc = uidoc.Document
    # app = __revit__.Application
    app = Autodesk.Revit.ApplicationServices.Application
    version = app.VersionNumber.ToString()
    
    currentView = __revit__.ActiveUIDocument.ActiveView

    user = str(System.Environment.UserName)
    tol = 0.001

    # transaction variables
    t = Transaction(doc, "Generic Transaction")
    tStart = t.Start()
    tEnd = t.Commit()
            
def DynamoDocSetup():
    # MIGHT BE USEFUL, KEEPING HERE FOR REFERENCE
    from System.Reflection import Assembly
    dynamo = Assembly.Load('DynamoCore')
    if dynamo:
        print(dynamo)
        print("This is in Dynamo")
    else:
        print("This is not Dynamo")

    # standard modules
    import clr
    import math
    import os
    import re
    import sys
    import System
    import traceback

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

    """
    REMEMBER:
    UnwrapElement(IN[0]) 
    
    ... at input is needed to convert between
    dynamo and revit objects so that the api can be used
    on either environments geometric elements

    FOR OUTPUT TO DYNAMO:
    revitObj.ToProtoType()
    """



# traceback is used to report to console the exact line and reason python code failed
import traceback

# variable to keep track if code is being run in Dynamo or Revit
isDynamo = False

try:
    # standard modules - both Revit and Dynamo
    import clr
    import math
    import os
    import re
    import sys
    import System

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

        # switch toggle, code is being run in dynamo - above didn't fail
        isDynamo = not isDynamo # True

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


    # WRITE STUFF HERE


    if isDynamo:
        # this code is in Dynamo, do nothing; instantiate this code in Dynamo node
        pass

    else:
        def Main():
            # SHOULD LOOP BE HANDLED HERE OR IN CLASS???
            # RECOMMENDING THAT GET OPERATION BE MOVED OUTSIDE OF THIS CLASS AND LOOP MANAGED BY RUN
            # EVERY METHOD WITHIN THIS CLASS OPERATION ON JUST A SINGLE SYSTEM AT A TIME...
            # THE SUBELEMENTS WILL BE HANDLED BY METHODS, HOWEVER

            # insantiate ProcessPiping class
            pipeObj = ProcessPiping(doc)
            # run class entry point
            pipeObj.Run()


        if __name__ == "__main__":
            # program entry point
            Main()
        

except:
    # print traceback in order to debug file | OUT[-1] should always be print statements
    print(traceback.format_exc())