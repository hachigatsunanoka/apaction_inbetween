import apsync as aps
import anchorpoint as ap
import os
import pipeline_utils as pu
import pipeline_ui as pui
import importlib
import shutil

importlib.reload(pu)
importlib.reload(pui)

# get context and metadata
ui = ap.UI()
ctx = ap.get_context()

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


def launch_callback(dialog: ap.Dialog):
    target = ctx.path
    if dialog.get_value('new'):
        aps.toggle_version_control(ctx.folder, True)
        new_path = aps.get_next_version_path(ctx.path)
        if os.path.exists(new_path):
            ui.show_error(
                'Houdini Plugin', 'New version already exists. Please delete it first.')
            return

        try:
            shutil.copy(ctx.path, new_path)
        except Exception as e:
            ui.show_error('Hudini Plugin', str(e))
            return

        target = new_path

    exec = h_settings.get('hfs') + '/bin/houdinifx.exe'
    ctx.run_async(pu.launch_program_with_context, exec, target, ctx)
    dialog.close()
    ui.show_info('Houdini Plugin', 'Houdini will be started')


dialog = pui.create_launch_dialog('Houdini', launch_callback)
dialog.show()
