import apsync as aps
import anchorpoint as ap
import os
import pipeline_utils as pu
import importlib

importlib.reload(pu)

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

exec = h_settings.get('hfs') + '/bin/houdinifx.exe'
ctx.run_async(pu.launch_program_with_context, exec, ctx)

ui.show_info('Houdini', 'Houdini will be started with the current context.')
