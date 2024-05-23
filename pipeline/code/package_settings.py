import anchorpoint as ap
import apsync as aps
import os

ui = ap.UI()
ctx = ap.Context.instance()

settings = aps.Settings(name="pipeline")

ROOT_DEFAULT = 'I:/IB-PROJECTS'
TEMPLATE_DEFAULT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/template/_project'
WORKER_DEFAULT = ctx.username.split(
    ' ')[0][0].lower() + ctx.username.split(' ')[1][0].lower()

if not settings.contains('root'):
    settings.set('root', ROOT_DEFAULT)

if not settings.contains('template'):
    settings.set('template', TEMPLATE_DEFAULT)

if not settings.contains('worker_initial'):
    settings.set('worker_initial', WORKER_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Pipeline Settings'

    dialog.add_text(text='Project folder path').add_input(default=settings.get('root'),
                                                          placeholder='path/to/projects',
                                                          var='root',
                                                          browse=ap.BrowseType.Folder,
                                                          browse_path=settings.get(
        'root'))
    dialog.add_info(
        text='The folder contains all of your project. You should not change this unless you know what you are doing')

    dialog.add_empty()

    # TODO: add default dropdown
    dialog.add_text('Use default project template').add_switch(True, var='use_default_template',
                                                               callback=change_template_type)
    dialog.start_section('Custom template', folded=True,
                         enabled=False, var='template_folder_section')
    dialog.add_info(
        text='The folder where the project template is stored.You should not change this unless you know what you are doing.')
    dialog.add_text('Template folder path').add_input(default=settings.get('template_folder'),
                                                      placeholder='path/to/template',
                                                      var='template_folder',
                                                      browse=ap.BrowseType.Folder,
                                                      browse_path=settings.get(
        'template_folder'),
        enabled=False)
    dialog.end_section()

    dialog.add_empty()

    # TODO: add default dropdown
    dialog.add_text('Use default worker initial from username').add_switch(
        True, var='use_default_worker_initial', callback=change_worker_type)
    dialog.start_section('Custom worker initial', folded=True,
                         enabled=False, var='worker_initial_section')
    dialog.add_info(
        text='The initial of your first and last name. e.g. "ak" for Akira Kondo.')
    dialog.add_text('Worker Initial').add_input(default=settings.get('worker_initial'),
                                                placeholder='worker initial',
                                                var='worker_initial')
    dialog.end_section()

    dialog.add_empty()

    dialog.add_button('Apply', press_apply)

    dialog.show()


def change_template_type(dialog: ap.Dialog, value):
    if value:
        dialog.set_enabled('template_folder_section', True)
        dialog.set_folded('template_folder_section', True)
    else:
        dialog.set_enabled('template_folder_section', False)
        dialog.set_folded('template_folder_section', False)


def change_worker_type(dialog: ap.Dialog, value):
    if value:
        dialog.set_enabled('worker_initial_section', False)
        dialog.set_folded('worker_initial_section', True)
    else:
        dialog.set_enabled('worker_initial_section', True)
        dialog.set_folded('worker_initial_section', False)


def press_apply(dialog):
    settings = aps.Settings(name="pipeline")
    settings.set("root", dialog.get_value('root'))
    if dialog.get_value('use_default_template'):
        settings.set('template', TEMPLATE_DEFAULT)
    else:
        settings.set("template", dialog.get_value('template_folder'))
    if dialog.get_value('use_default_worker_initial'):
        settings.set('worker', WORKER_DEFAULT)
    else:
        settings.set('worker', dialog.get_value('worker_initial'))
    settings.store()

    ui.show_success('inbetween Pipeline', 'Update your settings successfully.')

    dialog.close()


create_dialog()
