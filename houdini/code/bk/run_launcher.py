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

os.environ['IB_KITSU_URL'] = settings.get('url')
os.environ['IB_KITSU_EMAIL'] = settings.get('email')
os.environ['IB_KITSU_PASS'] = settings.get('password')

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

    dialog.start_section('Houdini Packages', folded=False)

    dialog.add_switch(bool(settings.get('rs')), var='rs').add_text(
        'Redshift').add_info(text='GPU Biased Renderer')

    dialog.add_switch(bool(settings.get('axiom')), var='axiom').add_text('Axiom').add_info(
        text='GPU Sparse Fluid Solver')

    dialog.add_switch(bool(settings.get('labs')), var='labs').add_text('SideFXLabs').add_info(
        text='SideFX\'s official digital asset library')

    dialog.add_switch(bool(settings.get('mops')), var='mops').add_text('MOPs').add_info(
        text='An open source Houdini toolkit for motion designers.')

    dialog.add_switch(bool(settings.get('hpaint')), var='hpaint').add_text('HPaint').add_info(
        'Viewport drawing utility for Houdini 19.5, allowing you to digitally paint on any geometry')

    dialog.add_button('Run', press_apply)

    dialog.show()


def press_apply(dialog):
    hfs = dialog.get_value('hfs')
    rs = dialog.get_value('rs')
    axiom = dialog.get_value('axiom')
    labs = dialog.get_value('labs')
    mops = dialog.get_value('mops')
    hpaint = dialog.get_value('hpaint')

    settings = aps.Settings(name="houdini")
    settings.set("hfs", hfs)
    settings.set("rs", rs)
    settings.set("axiom", axiom)
    settings.set("labs", labs)
    settings.set("mops", mops)
    settings.set("hpaint", hpaint)
    settings.store()

    ui.show_success('Houdini', 'Houdini will be started')

    dialog.close()

    run_houdini()


def run_houdini():

    # houdini settings
    exe = settings.get('hfs') + '/bin/houdinifx.exe'

    # packages
    os.environ['IB_USE_IBPIPELINE'] = str('True')
    os.environ['IB_USE_IBFX'] = str('True')

    os.environ['IB_USE_REDSHIFT'] = str(settings.get('rs'))
    os.environ['IB_USE_MOPS'] = str(settings.get('mops'))
    os.environ['IB_USE_MLOPS'] = str(settings.get('mlops'))
    os.environ['IB_USE_LABS'] = str(settings.get('labs'))
    os.environ['IB_USE_AXIOM'] = str(settings.get('axiom'))

    os.environ['HOUDINI_PACKAGE_DIR'] = 'I:/IB-PIPELINE/plugins/houdini/_packages'

    # launch houdini
    process = subprocess.Popen([
        exe,
        ctx.path
    ])


create_dialog()
