import anchorpoint as ap
import apsync as aps
import os
import pipeline_utils as pu
import importlib

importlib.reload(pu)

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

exec = settings.get('nuke_path') + '/Nuke15.0.exe'
ctx.run_async(pu.launch_program_with_context, exec, ctx)

ui.show_info('Nuke', 'Nuke will be started')
