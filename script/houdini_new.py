import anchorpoint as ap
import apsync as aps
import os
import importlib
import pipeline_utils as pu

importlib.reload(pu)

# get context and metadata
ui = ap.UI()
ctx = ap.get_context()

# get settings
h_settings = aps.Settings(name="houdini")

# Check if houdini path is set
if not h_settings.contains('hfs'):
    ui.show_error(
        'Houdini', 'Houdini is not setup. Please set the Houdini path in the settings.')
    raise Exception('Houdini path is not set')

# Check if houdini path is valid
if not os.path.exists(h_settings.get('hfs')):
    ui.show_error(
        'Houdini', 'Looks like the Houdini path is not valid. Please set the correct path in the settings.')
    raise Exception('Houdini path is not valid')

exec = h_settings.get('hfs') + '/bin/houdinifx.exe'


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new houdini scene file'
    dialog.add_text('Task').add_input('main', var='task')
    dialog.add_text('Launch houdini after creation').add_checkbox(var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    target = pu.copy_scenefile_from_template(ext='.hip',
                                                 ctx=ctx,
                                                 task=dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(pu.launch_program_with_context, exec, target)
        ui.show_success('Houdini', 'Houdini will be started')
    else:
        ui.show_success('Houdini', 'Houdini script created successfully.')

    dialog.close()


create_dialog()
