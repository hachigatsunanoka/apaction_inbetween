import anchorpoint as ap
import apsync as aps
import subprocess
import os
import sys

# import utilities
lib_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')) + '/libs'
sys.path.append(lib_path)
import aputils  # noqa

# get context and metadata
ui = ap.UI()
ctx = ap.get_context()

# get settings
settings = aps.Settings(name="houdini")

# Check if houdini path is set
if not settings.contains('hfs'):
    ui.show_error(
        'Houdini', 'Houdini is not setup. Please set the Houdini path in the settings.')
    raise Exception('Houdini path is not set')

# Check if houdini path is valid
if not os.path.exists(settings.get('hfs')):
    ui.show_error(
        'Houdini', 'Looks like the Houdini path is not valid. Please set the correct path in the settings.')
    raise Exception('Houdini path is not valid')


def launch_houdini_async(file_path):

    # houdini settings
    exe = settings.get('hfs') + '/bin/houdinifx.exe'

    # fix python path
    os.environ['PYTHONPATH'] = ''

    # declare context environment variables
    aputils.declare_context_env(ctx)

    # launch houdini
    subprocess.run([
        exe,
        file_path
    ])


ctx.run_async(launch_houdini_async, ctx.path)

ui.show_success('Houdini', 'Houdini will be started')
