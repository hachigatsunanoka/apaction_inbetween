import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()

settings = aps.Settings(name="pipeline")

ROOT_DEFAULT = 'I:/IB-PROJECTS'
TEMPLATE_DEFAULT = 'I:/IB-PIPELINE/anchorpoint/template/_project'
SHOT_DEFAULT = 'I:/IB-PIPELINE/anchorpoint/template/_shot'
OCIO_DEFAULT = 'I:/IB-PIPELINE/color/ib_aces/ib_aces_cg_config.ocio'

WORKER_DEFAULT = ctx.username.split(
    ' ')[0][0].lower() + ctx.username.split(' ')[1][0].lower()

if not settings.contains('root'):
    settings.set('root', ROOT_DEFAULT)
    settings.store()

if not settings.contains('template'):
    settings.set('template', TEMPLATE_DEFAULT)
    settings.store()

if not settings.contains('shot'):
    settings.set('shot', SHOT_DEFAULT)
    settings.store()

if not settings.contains('ocio'):
    settings.set('ocio', OCIO_DEFAULT)
    settings.store()

if not settings.contains('worker'):
    settings.set('worker', WORKER_DEFAULT)
    settings.store()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Pipeline Settings'

    dialog.add_text('<b>Project folder: </b>').add_input(default=settings.get('root'),
                                                         placeholder='path/to/projects',
                                                         var='root',
                                                         browse=ap.BrowseType.Folder,
                                                         browse_path=settings.get(
        'root'),
        width=500)
    dialog.add_info(
        text='The folder contains all of your project. <b>You should not change this unless you know what you are doing.</b>')

    dialog.add_empty()

    # Template Section
    dialog.add_text('<b>Project template folder: </b>').add_input(default=settings.get('template'),
                                                                  placeholder='path/to/template',
                                                                  var='template',
                                                                  browse=ap.BrowseType.Folder,
                                                                  browse_path=settings.get(
        'template'),
        width=500)
    dialog.add_info(
        text='The folder where the project template is stored.<b>You should not change this unless you know what you are doing.</b>')
    # Shot Section
    dialog.add_text('<b>Shot template folder: </b>').add_input(default=settings.get('shot'),
                                                               placeholder='path/to/template',
                                                               var='shot',
                                                               browse=ap.BrowseType.Folder,
                                                               browse_path=settings.get(
                                                                   'shot'),
                                                               width=500)
    dialog.add_info(
        text='The folder where the shot template is stored.<b>You should not change this unless you know what you are doing.</b>')

    dialog.add_empty()

    # OCIO Section
    dialog.add_text('<b>OCIO Config: </b>').add_input(default=settings.get('ocio'),
                                                      placeholder='path/to/config.ocio',
                                                      var='ocio',
                                                      browse=ap.BrowseType.File,
                                                      browse_path=settings.get(
                                                          'ocio'),
                                                      width=500)
    dialog.add_info(
        'OCIO config to be used by default when a new project is created. <b>You should not change this unless you know what you are doing.</b>')

    # Worker Section
    dialog.add_switch(default=False, var='use_default_worker',
                      callback=change_worker_type).add_text('Use custom worker initial')
    dialog.add_text('<b>Worker Initial: </b>').add_input(default=settings.get('worker'),
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
    settings.set("shot", dialog.get_value('shot'))
    settings.set("ocio", dialog.get_value('ocio'))

    if dialog.get_value('use_default_worker'):
        settings.set('worker', WORKER_DEFAULT)
    else:
        settings.set('worker', dialog.get_value('worker'))
    settings.store()

    ui.show_success('inbetween Pipeline', 'Update your settings successfully.')

    dialog.close()


create_dialog()
