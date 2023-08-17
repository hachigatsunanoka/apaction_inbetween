import apsync as aps
import anchorpoint as ap
import sys


ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)
meta = project.get_metadata()

settings = aps.Settings('houdini')
hfs = settings.get('hfs')
sys.path.append(hfs + r'\python39\lib\site-packages')
sys.path.append(hfs + r'\houdini\python3.9libs')

import hrpyc  # noqa
import hou  # noqa

# Get files
files = ctx.selected_files

# Connect to Houdini


def create_dialog():
    dialog = ap.Dialog()
    dialog.title = 'houdini settings'
    dialog.add_dropdown('Select Type...', [
                        'reference', 'sublayer'], var='type')

    dialog.add_button('Import', press_import)
    dialog.show()


def press_import(dialog):
    type = dialog.get_value('type')
    connection, hou = connect_houdini()
    create_lopnode(hou, type)
    # Delete connenction
    del connection
    # Create Dialog
    if len(files) == 1:
        name = ctx.filename
    else:
        name = 'Multiple assets'
    ui.show_success('Success!', name + ' send to lops')
    dialog.close()


def create_lopnode(hou, type):
    # --- Houdini ---
    lop = hou.node('/stage')
    layernode = lop.createNode(type)
    layernode.parm('num_files').set(len(files))
    i = 1
    for file in files:
        layernode.parm('filepath'+str(i)).set(file)
        i = i+1
    layernode.moveToGoodPosition()


def connect_houdini():
    try:
        connection, hou = hrpyc.import_remote_module(port=11188)
        return connection, hou
    except:
        ui.show_error(
            'Error!', 'Anchorpoint cannot connect to houdini instance. Please start houdini from anchorpoint first.')
        return
