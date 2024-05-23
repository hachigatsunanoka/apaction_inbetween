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

# Check if shot context
IN_SHOT_CONTEXT = aputils.check_if_shot_context(ctx)


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new nuke script'
    dialog.add_text('Task').add_input('main', var='task')
    dialog.add_text('Launch nuke after creation').add_checkbox(var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    target = copy_template(dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(launch_nuke_async, target)
        ui.show_success('Nuke', 'Nuke will be started')
    else:
        ui.show_success('Nuke', 'Nuke script created successfully.')

    dialog.close()


def copy_template(task):
    format = '[project]_[shot]_[task]_[worker]_[version].nk'  # get template
    template_nk = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/template/_template.nk'

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


create_dialog()
