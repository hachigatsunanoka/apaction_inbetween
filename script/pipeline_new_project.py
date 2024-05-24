import anchorpoint as ap
import apsync as aps
import os

ui = ap.UI()
ctx = ap.get_context()

settings = aps.Settings(name="pipeline")

ocios = ['ACES1.3 (cg)', 'ACES1.3 (studio)', 'Custom']
ICON = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace(
    os.sep, '/') + '/resource/ib.svg'


def create_dialog():
    dialog = ap.Dialog()

    dialog.icon = ICON
    dialog.title = 'Create New Project'

    dialog.add_text('Project Code :').add_input(default='24000',
                                                placeholder='Unique 5 digits',
                                                var='code',
                                                width=100).add_text('_').add_input(default='NAME',
                                                                                   placeholder='Name of the project',
                                                                                   var='name')
    dialog.add_info(
        'Project name should be uppercase and no space, no underscore.')
    dialog.add_separator()
    dialog.add_text('FPS :').add_input(
        default='24', placeholder='FPS', var='fps', width=100)
    dialog.add_text('Resolution :').add_input(
        default='1920', placeholder='Width', var='width', width=100).add_info('*').add_input(default='1080', placeholder='Height', var='height', width=100)

    dialog.add_separator()

    dialog.add_text('Shot Format :').add_input(
        'sh###', var='format', callback=change_format)
    dialog.add_text('Shot Number Increment:').add_input(
        '1', var='increment', callback=change_format)
    dialog.add_info(text='(Preview : ' +
                    'sh001, sh002, sh003, ...)', var='preview')
    dialog.add_switch(True, var='use_default_shot_template').add_text(
        'Use default shot template')

    dialog.add_separator()
    dialog.add_text('OCIO Config :').add_dropdown(
        ocios[0], ocios, var='ocio', callback=change_ocio)
    dialog.add_text('Custom config path :', var='custom_ocio_text').add_input(
        default='path/to/config.ocio', placeholder='path/to/config.ocio', var='custom_ocio_path', browse=ap.BrowseType.File)
    dialog.hide_row('custom_ocio_text', True)

    dialog.add_button('Create', press_create)

    dialog.show()


def change_ocio(dialog: ap.Dialog, value):
    ocio = dialog.get_value('ocio')
    if ocio == 'Custom':
        dialog.hide_row('custom_ocio_text', False)
        dialog.hide_row('custom_ocio_path', False)
    else:
        dialog.hide_row('custom_ocio_text', True)
        dialog.hide_row('custom_ocio_path', True)


def change_format(dialog: ap.Dialog, value):
    format = dialog.get_value('format')
    skip = dialog.get_value('increment')

    num = format.count('#')

    shots = []
    for i in range(1, 4):
        shotnum = i * int(skip)
        shot = format.replace('#' * num, f'{shotnum:0{num}d}')
        shots.append(shot)
    shots_str = ', '.join(shots)

    dialog.set_value('preview', '(Preview : ' + shots_str + ', ...)')


def create_project_from_template_async(code, name, fps, width, height, shot_format, shot_increment, shot_template, ocio):

    progress = ap.Progress('Creating Project', 'This may take a while...',
                           infinite=False, cancelable=False, show_loading_screen=True)

    source = settings.get('template')
    target = settings.get('root') + '/' + code + '_' + name

    project = ctx.create_project(
        target, name, workspace_id=ctx.workspace_id)

    aps.copy_from_template(source, target, workspace_id=ctx.workspace_id)

    metadata = {}
    metadata['fps'] = fps
    metadata['width'] = width
    metadata['height'] = height
    metadata['shot_format'] = shot_format
    metadata['shot_increment'] = shot_increment
    metadata['shot_template'] = shot_template
    metadata['ocio'] = ocio

    project.update_metadata(metadata)

    progress.finish()


def press_create(dialog):
    # get values from dialog
    code = dialog.get_value('code')
    name = dialog.get_value('name')
    fps = dialog.get_value('fps')
    width = dialog.get_value('width')
    height = dialog.get_value('height')
    shot_format = dialog.get_value('format')
    shot_increment = dialog.get_value('increment')

    # get shot template
    if dialog.get_value('use_default_shot_template'):
        shot_template = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/template/_shot'
    else:
        shot_template = None

    # get ocio config
    ocio_type = dialog.get_value('ocio')
    if ocio_type == 'Custom':
        ocio = dialog.get_value('custom_ocio_path')
    else:
        folder = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/resource/ocio/'
        if ocio_type == 'ACES1.3 (cg)':
            ocio = folder + 'cg-config.ocio'
        else:
            ocio = folder + 'studio-config.ocio'

    # create project
    ctx.run_async(create_project_from_template_async,
                  code, name, fps, width, height, shot_format, shot_increment, shot_template, ocio)

    dialog.close()


create_dialog()
