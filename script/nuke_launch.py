import anchorpoint as ap
import apsync as aps
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

settings = aps.Settings(name="nuke")

# Check if nuke path is set
if not settings.contains('nuke_path'):
    ui.show_error(
        'Nuke', 'Nuke is not setup. Please set the Nuke path in the settings.')
    raise Exception('Nuke path is not set')

# Check if nuke path is valid
if not os.path.exists(settings.get('nuke_path')):
    ui.show_error(
        'Nuke', 'Looks like the Nuke path is not valid. Please set the correct path in the settings.')
    raise Exception('Nuke path is not valid')


def launch_callback(dialog: ap.Dialog):
    target = ctx.path
    if dialog.get_value('new'):
        aps.toggle_version_control(ctx.folder, True)
        new_path = aps.get_next_version_path(ctx.path)
        if os.path.exists(new_path):
            ui.show_error(
                'Nuke Plugin', 'New version already exists. Please delete it first.')
            return

        try:
            shutil.copy(ctx.path, new_path)
        except Exception as e:
            ui.show_error('Nuke Plugin', str(e))
            return

        target = new_path

    exec = settings.get('nuke_path') + '/Nuke15.0.exe'
    ctx.run_async(pu.launch_program_with_context, exec, target, ctx)
    dialog.close()
    ui.show_info('Nuke', 'Nuke will be started')


dialog = pui.create_launch_dialog('Nuke', launch_callback)
dialog.show()

# exec = settings.get('nuke_path') + '/Nuke15.0.exe'
# ctx.run_async(pu.launch_program_with_context, exec, ctx)
