import anchorpoint as ap
import apsync as aps
import os

ui = ap.UI()
ctx = ap.Context.instance()

'''
This settings script is used to set the nuke path and template scene file path.

Settings are contain following:
- path: path to nuke installation directory
- template: path to template scene file

'''

NUKE_DEFAULT = 'C:/Program Files/Nuke15.0v4'
TEMPLATE_DEFAULT = 'I:/IB-PIPELINE/anchorpoint/template/_template.nk'

settings = aps.Settings(name="nuke")

# Check if settings contains nuke path and template path
if not settings.contains('path'):
    settings.set('path', NUKE_DEFAULT)
    settings.store()

if not settings.contains('template'):
    settings.set('template', TEMPLATE_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Nuke Settings'

    dialog.add_text('Nuke path').add_input(default=settings.get('path'),
                                           placeholder='path/to/nuke/directory',
                                           var='path',
                                           browse=ap.BrowseType.Folder,
                                           browse_path=settings.get(
                                               'path'),
                                           width=500)

    dialog.add_info(text='Nuke installation directory')

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

    path = dialog.get_value('path')
    template = dialog.get_value('template')
    if path is None or path == '':
        ui.show_error('Nuke Plugin', 'Nuke path is required.')
        return

    if os.path.exists(path) is False:
        ui.show_error('Nuke Plugin', 'Nuke path is not valid.')
        return

    if template is None or template == '':
        ui.show_error('Nuke Plugin', 'Template scene file path is required.')
        return

    if os.path.exists(template) is False:
        ui.show_error('Nuke Plugin', 'Template scene file path is not valid.')
        return

    settings.set("path", path)
    settings.set("template", template)
    settings.store()

    ui.show_success('Nuke Plugin', 'Update nuke settings successfully.')

    dialog.close()


create_dialog()
