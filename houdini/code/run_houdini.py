import anchorpoint as ap
import apsync as aps
# import utils.anchorpoint_utils as apu

import os
import subprocess

# get context and metadata
ui = ap.UI()
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
meta = project.get_metadata()

# check for kitsu settings
settings = aps.Settings(name="kitsu")

# check context
shot = os.path.basename(os.path.dirname(ctx.path))
seq = os.path.basename(os.path.dirname(os.path.dirname(ctx.path)))

os.environ['IB_SHOT'] = shot
os.environ['IB_SEQ'] = seq

# check houdini settings
HFS_DEFAULT = 'C:/'

if not settings.contains('hfs'):
    settings.set('hfs', HFS_DEFAULT)
    settings.store()

settings = aps.Settings(name="houdini")


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Houdini Settings'

    if os.environ['IB_KITSU_URL'] == '':
        dialog.add_info(
            'Kitsu is not setup. Houdini instance will not be able to connect to Kitsu.')

    dialog.add_text('HFS').add_input(default=settings.get('hfs'),
                                     placeholder='path/to/houdini/directory',
                                     var='hfs',
                                     browse=ap.BrowseType.Folder,
                                     browse_path=settings.get('hfs'),
                                     width=500)

    dialog.add_info(text='Houdini installation directory')

    dialog.add_separator()

    dialog.add_button('Run', press_apply)

    dialog.show()


def press_apply(dialog):
    hfs = dialog.get_value('hfs')
    ui.show_success('Houdini', 'Houdini will be started')

    dialog.close()

    # run_houdini()


def get_context():
    shot = os.path.basename(os.path.dirname(ctx.path))
    seq = os.path.basename(os.path.dirname(os.path.dirname(ctx.path)))

    # get project

    # get pipeline

    # get attribute value from pipeline
    start = aps.get_attribute_value('Start', shot)
    range = aps.get_attribute_value('Range', shot)
    width = aps.get_attribute_value('Width', shot)
    height = aps.get_attribute_value('Height', shot)
    fps = aps.get_attribute_value('FPS', shot)
    overscan = aps.get_attribute_value('Overscan', shot)
    prerole = aps.get_attribute_value('Preroll', shot)
    postrole = aps.get_attribute_value('Postroll', shot)


def run_houdini():

    # houdini settings
    exe = settings.get('hfs') + '/bin/houdinifx.exe'

    # packages
    os.environ['IB_USE_IBPIPELINE'] = str('True')

    os.envrion['IB_START'] =

    # launch houdini
    process = subprocess.Popen([
        exe,
        ctx.path
    ])


create_dialog()
