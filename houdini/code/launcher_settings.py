import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)
meta = project.get_metadata()

HFS_DEFAULT = 'I:/IB-PIPELINE/distro/houdini/20.0.653'

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

    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    hfs = dialog.get_value('hfs')

    settings = aps.Settings(name="houdini")
    settings.set("hfs", hfs)

    settings.store()

    ui.show_success('Houdini', 'Update Houdini settings successfully.')

    dialog.close()


create_dialog()
