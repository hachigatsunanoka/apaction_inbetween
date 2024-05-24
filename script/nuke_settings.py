import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()

NUKE_DEFAULT = 'C:/Program Files/Nuke15.0v4'

settings = aps.Settings(name="nuke")

if not settings.contains('nuke_path'):
    settings.set('nuke_path', NUKE_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Nuke Settings'

    dialog.add_text('Nuke Path').add_input(default=settings.get('nuke_path'),
                                           placeholder='path/to/nuke/directory',
                                           var='nuke_path',
                                           browse=ap.BrowseType.Folder,
                                           browse_path=settings.get(
                                               'nuke_path'),
                                           width=500)

    dialog.add_info(text='Nuke installation directory')

    dialog.add_separator()

    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    path = dialog.get_value('nuke_path')

    settings = aps.Settings(name="nuke")
    settings.set("nuke_path", path)

    settings.store()

    ui.show_success('Nuke', 'Update nuke settings successfully.')

    dialog.close()


create_dialog()
