# RevitAPI_python WIP
THIS IS A WORK IN PROGRESS AND I HATE WRITING READMEs.

Revit API code snippets written in Python for use as an external library, sorta like a wrapper for the api, but mostly for reference about how geometry is handled in Revit.

## Notes
All the Autodesk APIs have their own geometry objects and methods. Dynamo has APIs that allow translation of these object for use in the Dynamo environment. Inside of Dynamo, you can also use these to speak directly to the Revit / Civil3D / Navisworks document. In adition to providing this graphical, node based method of accessing the respective APIs, DynamoCore (the Dynamo API) provides additional Geometry objects that are not available in the host program. Revit for example, while having some Nurb capabilities forbids through its API to create these elements outside of the family editor. Dynamo bypasses this limitation and allows the user to create this geometry in Dynamo to define other objects which can be then loaded into Revit. 

Revit API   Civil3D API
    |          |
    |          |
    v          v
 -----DynamoCore-----> Application Doc
