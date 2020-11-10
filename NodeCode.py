"""
Notes: yes, this looks scary but it makes development in dynamo easier!
"""

import traceback

# print list
printOUT = []

try:
    # standard modules
    import clr
    import math
    import os
    import re
    import sys
    import System

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

    # dynamo document management
    doc = DocumentManager.Instance.CurrentDBDocument
    uiapp = DocumentManager.Instance.CurrentUIApplication
    app = uiapp.Application
    uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

    user = str(System.Environment.UserName)
    tol = 0.001

    # transaction variables
    tStart = TransactionManager.Instance.EnsureInTransaction(doc)
    tEnd = TransactionManager.Instance.TransactionTaskDone()

    ####################
    ## CODE GOES HERE ##
    ####################

    # some class
    class Foo:
        def __init__(self):
            # inputs
            pass

        def Method(self):
            pass

    # some function 
    def Bar():
        pass



    ##########
    ## MAIN ##
    ##########

    # node inputs | IN[0] is reserved for directory input in case above code needs to be externally referenced
    directory = IN[0]
    A = IN[1]

    # call classes/functions above
    mainOutput = None

    # output
    OUT = [mainOutput, printOut]


except:
    # print traceback in order to debug file | OUT[-1] should always be print statements
    OUT = ["Code Failed: {0}".format(traceback.format_exc()), printOUT]