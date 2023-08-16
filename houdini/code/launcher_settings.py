import anchorpoint as ap
import apsync as aps

import os
import sys

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)
meta = project.get_metadata()

HFS_DEFAULT = 'I:/IB-PIPELINE/distro/houdini/19.5.605'

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

    dialog.add_button('Apply', press_apply)

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

    ui.show_success('Houdini', 'Update Houdini settings successfully.')

    dialog.close()


create_dialog()
