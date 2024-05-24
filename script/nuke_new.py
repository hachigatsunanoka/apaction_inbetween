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


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new nuke scene file'
    dialog.add_text('Task').add_input('main', var='task')
    dialog.add_text('Launch nuke after creation').add_checkbox(var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    target = pu.copy_scenefile_from_template(ext='.nk',
                                             ctx=ctx,
                                             task=dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(pu.launch_program_with_context, target)
        ui.show_success('Nuke', 'Nuke will be started')
    else:
        ui.show_success('Nuke', 'Nuke script created successfully.')

    dialog.close()


create_dialog()
