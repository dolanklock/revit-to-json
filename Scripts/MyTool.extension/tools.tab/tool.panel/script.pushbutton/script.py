#IronPython
import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('AdWindows')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')


import Autodesk
import Autodesk.Windows as aw
from Autodesk.Revit import DB
from Autodesk.Revit import UI

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
doc = uiapp.ActiveUIDocument.Document

lections.Generic import List

import json
import sys
# sys.path.append('M:\\600 VWCC\\ARCHITECTURAL\\BIM\\pykTools\\pyKTools\\MyTool.extension\\lib')
sys.path.append('Y:\\pyKTools\\2024-02-17\\pyKTools\\MyTool.extension\\lib')
sys.path.append('./modules')
import Selection
import GUI
import SelectionFilters

from .modules import get_room_shapes
import pick_parameters
from send_dict import send_dict

__author__ = "Anna Milczarek, Dolan Klock"


if __name__ == "__main__":
    #Change directory to script folder
    cur_dir = sys.path[0]
    pathToScript = cur_dir+"\\scriptCPython.py"
    
    all_rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()
    all_rooms_placed = [room for room in all_rooms if room.Area != 0]
    room_selection = GUI.UI_three_options(title="Room Selection",
                                                main_instruction="Choose how you want to select rooms by",
                                                commandlink1="All",
                                                commandlink2="By Level",
                                                commandlink3="By Selection")
    if room_selection == '1':
        rooms = Selection.GetElementsFromDoc.all_rooms(doc, is_placed_only=True)
    elif room_selection == '2':
        all_levels = [l for l in DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType()]
        all_level_names = [l.get_Parameter(DB.BuiltInParameter.DATUM_TEXT).AsValueString() for l in all_levels]
        chosen_level = GUI.user_prompt_get_object_from_names(all_levels, all_level_names, title="Choose level to get views at", multiselect=False)
        rooms = [room for room in all_rooms_placed if room.LookupParameter('Level').AsValueString() == chosen_level.Name]
        # chosen_views = Selection.get_views_by_level(chosen_level.get_Parameter(DB.BuiltInParameter.DATUM_TEXT).AsValueString(), plan_views=True)
    elif room_selection == '3':
        # selectionFilter = SelectionFilters.
        # selectionFilter = SelectionFilters.CustomISelectionFilter("Rooms").AllowElement()
        # rooms = Autodesk.Revit.UI.Selection.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element,
        #                                                            SelectionFilters.ISelectionFilter('Rooms'))
        # rooms = uidoc.Selection.PickElementsByRectangle(selectionFilter, "Select Rooms")
        rooms = [doc.GetElement(ref_id.ElementId) for ref_id in uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element, "Select Rooms")]
    else:
        sys.exit()

    output_rooms = get_room_shapes.get_room_shapes(rooms, outside_boundary_only=True)
    print(output_rooms)
    
    # output_dict = {"data": {"test": 'testing'}}
    output_dict = {"data": output_rooms, 'properties': pick_parameters.pick_parameters()}
    send_dict(output_dict, pathToScript)



#TODO: test
#TODO: pick parameters function pass in object to cpython

#TODO: getting windows error when getting all rooms at level, figure out work around. Try
    #  putting code in try except block and if fails then shop list in half and save the other half and send the other half again to
    # cpython

#TODO: allow selection of multiple levles
    
#TODO: prompt user to choose rooms with columns cut out or ignore columns (need
    #  to figure out "get_room_shapes" above function. currently it ignores int column outline and
    #  only gets the outside room boundary. I had it where it got both, need to tweak code to achieve that)

# outside boundary counter clockwise and inner clockwise