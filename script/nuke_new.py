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
    dialog.add_text('<b>Task: </b>').add_input('main', var='task')
    dialog.add_info(
        'The task name will be used as the scene file name. It should be unique.')
    dialog.add_separator()
    dialog.add_switch(False, var='custom_template', callback=callback_custom_template).add_text(
        '<b>Custom template</b>')
    dialog.add_text('Custom template path: ').add_input(default='',
                                                        placeholder='/path/to/template.nk',
                                                        var='custom_template_path',
                                                        browse=ap.BrowseType.Folder,
                                                        browse_path='C:/')
    dialog.hide_row('custom_template_path', True)
    dialog.add_info(
        'If you want to use specific template, enable this option.')
    dialog.add_text(
        '<b>Launch nuke after creation</b>').add_checkbox(var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def callback_custom_template(dialog, value):
    dialog.hide_row('custom_template_path', not value)


def press_apply(dialog):
    template = settings.get('template')

    # check if custom template is valid
    if dialog.get_value('custom_template'):
        custom_template = dialog.get_value('custom_template_path')
        if os.path.exists(custom_template):
            template = custom_template

    target = pu.copy_scenefile_from_template(template=template,
                                             ctx=ctx,
                                             task=dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(pu.launch_program_with_context, target)
        ui.show_success('Nuke', 'Nuke will be started')
    else:
        ui.show_success('Nuke', 'Nuke script created successfully.')

    dialog.close()


create_dialog()
