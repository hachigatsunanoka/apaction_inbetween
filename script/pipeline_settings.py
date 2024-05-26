import anchorpoint as ap
import apsync as aps
import os

ui = ap.UI()
ctx = ap.Context.instance()

settings = aps.Settings(name="pipeline")

ROOT_DEFAULT = 'I:/IB-PROJECTS'
TEMPLATE_DEFAULT = 'I:/IB-PIPELINE/anchorpoint/template/_project'
WORKER_DEFAULT = ctx.username.split(
    ' ')[0][0].lower() + ctx.username.split(' ')[1][0].lower()

if not settings.contains('root'):
    settings.set('root', ROOT_DEFAULT)

if not settings.contains('template'):
    settings.set('template', TEMPLATE_DEFAULT)

if not settings.contains('worker'):
    settings.set('worker', WORKER_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Pipeline Settings'

    dialog.add_text(text='Project folder').add_input(default=settings.get('root'),
                                                     placeholder='path/to/projects',
                                                     var='root',
                                                     browse=ap.BrowseType.Folder,
                                                     browse_path=settings.get(
        'root'))
    dialog.add_info(
        text='The folder contains all of your project. <b>You should not change this unless you know what you are doing.</b>')

    dialog.add_empty()

    # Template Section
    dialog.add_text('Project template folder').add_input(default=settings.get('template'),
                                                         placeholder='path/to/template',
                                                         var='template',
                                                         browse=ap.BrowseType.Folder,
                                                         browse_path=settings.get(
        'template'))
    dialog.add_info(
        text='The folder where the project template is stored.<b>You should not change this unless you know what you are doing.</b>')

    dialog.add_empty()

    # Worker Section
    dialog.add_switch(default=False, var='use_default_worker',
                      callback=change_worker_type).add_text('Use custom worker initial')
    dialog.add_text('Worker Initial').add_input(default=settings.get('worker'),
                                                placeholder='worker initial',
                                                var='worker')
    dialog.add_info(
        text='The initial of your first and last name. Your default worker initial is <b>"' + WORKER_DEFAULT + '"</b>.')
    dialog.hide_row('worker', True)

    dialog.add_empty()

    dialog.add_button('Apply', press_apply)

    dialog.show()


def change_worker_type(dialog: ap.Dialog, value):
    if value:
        dialog.hide_row('worker', False)
    else:
        dialog.hide_row('worker', True)


def press_apply(dialog):
    settings = aps.Settings(name="pipeline")
    settings.set("root", dialog.get_value('root'))
    settings.set("template", dialog.get_value('template'))
    if dialog.get_value('use_default_worker'):
        settings.set('worker', WORKER_DEFAULT)
    else:
        settings.set('worker', dialog.get_value('worker'))
    settings.store()

    ui.show_success('inbetween Pipeline', 'Update your settings successfully.')

    dialog.close()


create_dialog()
