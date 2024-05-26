import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
metadata = project.get_metadata()


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Modify Project Metadata'

    # FPS
    dialog.add_text('FPS :').add_input(
        default=metadata.get('fps', '24'),
        placeholder='FPS',
        var='fps',
        width=100)

    # Resolution
    dialog.add_text('Resolution :').add_input(
        default=metadata.get('width', '1920'),
        placeholder='Width',
        var='width',
        width=100).add_info('*').add_input(default=metadata.get('height', '1080'),
                                           placeholder='Height',
                                           var='height',
                                           width=100)

    dialog.add_separator()

    # Shot Format
    dialog.add_text('Shot Format :').add_input(
        metadata.get('shot_format', 'sh###'),
        var='format',
        callback=change_format)
    dialog.add_text('Shot Number Increment:').add_input(
        metadata.get('shot_increment', '1'),
        var='increment',
        callback=change_format)
    dialog.add_info(text='(Preview : ' +
                    'sh001, sh002, sh003, ...)', var='preview')

    dialog.add_separator()

    # OCIO
    dialog.add_switch(default=False, var='custom_ocio',
                      callback=change_ocio).add_text('Use custom OCIO config')
    dialog.add_text('Config path :', var='custom_ocio_text').add_input(
        default='', placeholder='path/to/config.ocio', var='custom_ocio_path', browse=ap.BrowseType.File)
    dialog.hide_row('custom_ocio_text', True)
    dialog.add_button('Apply', press_apply)
    dialog.show()


def change_ocio(dialog: ap.Dialog, value):
    if value:
        dialog.hide_row('custom_ocio_text', False)
    else:
        dialog.hide_row('custom_ocio_text', True)


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


def press_apply(dialog):

    metadata['fps'] = dialog.get_value('fps')
    metadata['width'] = dialog.get_value('width')
    metadata['height'] = dialog.get_value('height')

    if dialog.get_value('custom_ocio'):
        metadata['ocio'] = dialog.get_value('custom_ocio_path')

    project.update_metadata(metadata)

    ui.show_success('Pipeline', 'Update metadata successfully.')

    dialog.close()


create_dialog()
