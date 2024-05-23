import anchorpoint as ap
import apsync as aps
import subprocess
import os
from pathlib import Path
import sys

# import utilities
lib_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')) + '/libs'
sys.path.append(lib_path)
import aputils  # noqa

# get context and metadata
ui = ap.UI()
ctx = ap.get_context()
project = aps.get_project(ctx.path)
metadata = project.get_metadata()

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


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new houdini scene file'
    dialog.add_text('Task').add_input('main', var='task')
    dialog.add_text('Launch houdini after creation').add_checkbox(var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    target = copy_template(dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(launch_houdini_async, target)
        ui.show_success('Houdini', 'Houdini will be started')
    else:
        ui.show_success('Houdini', 'Houdini script created successfully.')

    dialog.close()


def copy_template(task):
    format = '[project]_[shot]_[task]_[worker]_[version].hip'  # get template
    template_nk = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/template/_template.hip'

    data = aputils.get_current_pipeline_context(ctx)
    variables = {
        'project': data['project'],
        'shot': data['shot'],
        'task': task,
        'version': 'v001',
        'worker': aps.Settings('pipeline').get('worker'),
    }
    resolved = ctx.path + '/' + aps.resolve_variables(format, variables)
    aps.copy_file(source=template_nk, target=resolved)

    return resolved


def launch_houdini_async(file_path):

    # houdini settings
    exe = settings.get('hfs') + '/bin/houdinifx.exe'

    # fix python path
    os.environ['PYTHONPATH'] = ''

    # declare context environment variables
    aputils.declare_context_env(ctx)

    # launch nuke
    subprocess.run([
        exe,
        file_path
    ])


create_dialog()
