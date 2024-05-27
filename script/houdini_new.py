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


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new houdini scene file'
    dialog.add_text('<b>Task :</b>').add_input('main', var='task')
    dialog.add_info(
        'The task name will be used as the scene file name. It should be unique.')
    dialog.add_separator()
    dialog.add_switch(False, var='custom_template',
                      callback=callback_custom_template).add_text('<b>Use custom template</b>')
    dialog.add_text('Custom template path: ').add_input(default='',
                                                        placeholder='/path/to/template.hip',
                                                        var='custom_template_path',
                                                        browse=ap.BrowseType.Folder,
                                                        browse_path='C:/')
    dialog.hide_row('custom_template_path', True)
    dialog.add_info(
        'If you want to use specific template, enable this option.')
    dialog.add_text('<b>Launch houdini after creation<b>').add_checkbox(
        var='launch')
    dialog.add_button('Apply', press_apply)

    dialog.show()


def callback_custom_template(dialog, value):
    dialog.hide_row('custom_template_path', not value)


def press_apply(dialog):
    template = h_settings.get('template')

    # check if custom template is valid
    if dialog.get_value('custom_template'):
        custom_template = dialog.get_value('custom_template_path')
        if os.path.exists(custom_template):
            template = custom_template

    target = pu.copy_scenefile_from_template(template=template,
                                             ctx=ctx,
                                             task=dialog.get_value('task'))

    if dialog.get_value('launch'):
        ctx.run_async(pu.launch_program_with_context, exec, target)
        ui.show_success('Houdini', 'Houdini will be started')
    else:
        ui.show_success('Houdini', 'Houdini script created successfully.')

    dialog.close()


create_dialog()
