import anchorpoint as ap
import apsync as aps
import os

ui = ap.UI()
ctx = ap.Context.instance()

'''
This settings script is used to set the houdini path and template scene file path.

Settings are contain following:
- hfs: path to houdini installation directory
- template: path to template scene file

'''
HFS_DEFAULT = 'C:/Program Files/Side Effects Software/Houdini 20.0.653'
TEMPLATE_DEFAULT = 'I:/IB-PIPELINE/anchorpoint/template/_template.hip'

settings = aps.Settings(name="houdini")

if not settings.contains('hfs'):
    settings.set('hfs', HFS_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Houdini Settings'

    dialog.add_text('HFS').add_input(default=settings.get('hfs'),
                                     placeholder='path/to/houdini/directory',
                                     var='hfs',
                                     browse=ap.BrowseType.Folder,
                                     browse_path=settings.get('hfs'),
                                     width=500)

    dialog.add_info(text='Houdini installation directory')

    dialog.add_separator()

    dialog.add_text('Template scene file').add_input(default=settings.get('template'),
                                                     placeholder='path/to/template/scene/file',
                                                     var='template',
                                                     browse=ap.BrowseType.File,
                                                     browse_path=settings.get(
                                                         'template'),
                                                     width=500)

    dialog.add_button('Apply', press_apply)
    dialog.show()


def press_apply(dialog):

    hfs = dialog.get_value('hfs')
    template = dialog.get_value('template')

    if hfs is None or hfs == '' or os.path.exists(hfs) is False:
        ui.show_error('Houdini Plugin', 'HFS path is not valid.')
        return

    if template is None or template == '' or os.path.exists(template) is False:
        ui.show_error('Houdini Plugin', 'Template path is not valid.')
        return

    settings.set("hfs", hfs)
    settings.set("template", template)
    settings.store()

    ui.show_success('Houdini Plugin', 'Update houdini settings successfully.')

    dialog.close()


create_dialog()
