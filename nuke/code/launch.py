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


def launch_nuke_async(script_path):

    # nuke settings
    exe = settings.get('nuke_path') + '/Nuke15.0.exe'

    # fix python path
    os.environ['PYTHONPATH'] = ''

    # declare context environment variables
    aputils.declare_context_env(ctx)

    # launch nuke
    subprocess.run([
        exe,
        script_path
    ])


ctx.run_async(launch_nuke_async, ctx.path)

ui.show_success('Nuke', 'Nuke will be started')
