import anchorpoint as ap
import apsync as aps

import os
import subprocess

# get context and metadata
ui = ap.UI()
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
meta = project.get_metadata()

# check context
shot = os.path.basename(os.path.dirname(ctx.path))
seq = os.path.basename(os.path.dirname(os.path.dirname(ctx.path)))

os.environ['IB_SHOT'] = shot
os.environ['IB_SEQ'] = seq

settings = aps.Settings(name="houdini")


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

    dialog.add_button('Run', press_apply)

    dialog.show()


def press_apply(dialog):
    hfs = dialog.get_value('hfs')
    ui.show_success('Houdini', 'Houdini will be started')

    dialog.close()

    ctx.run_async(run_houdini)


def run_houdini():

    # houdini settings
    exe = settings.get('hfs') + '/bin/houdinifx.exe'

    # packages
    os.environ['IB_USE_IBPIPELINE'] = str('True')

    # fix python path
    os.environ['PYTHONPATH'] = settings.get(
        'hfs') + '/houdini/python3.10/lib/site-packages'

    # launch houdini
    subprocess.run([
        exe,
        ctx.path
    ])


create_dialog()
