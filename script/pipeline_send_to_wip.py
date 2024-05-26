import anchorpoint as ap
import apsync as aps
import pipeline_utils as pu

import glob

ui = ap.UI()
ctx = ap.Context.instance()

data = pu.get_current_pipeline_context(ctx)

shot_preview_enabled = True
mp4_warning = False
context_warning = False
multiple_warning = False

if data['shot'] is None:
    shot_preview_enabled = False
    context_warning = True

if len(ctx.selected_files) > 1:
    shot_preview_enabled = False
    multiple_warning = True

if not any([f.endswith('.mp4') for f in ctx.selected_files]):
    shot_preview_enabled = False
    mp4_warning = True


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Send to WIP...'
    dialog.add_info('Current context: <b>' + data['shot'] + '</b>')
    dialog.add_info('Date: <b>' + pu.get_today() + '</b>')
    dialog.add_switch(shot_preview_enabled, var='shot_preview',
                      enabled=shot_preview_enabled).add_text('Shot preview')

    if mp4_warning:
        dialog.add_info(
            '- This option is disabled beacause <b>file must be mp4 format</b>.')

    if context_warning:
        dialog.add_info(
            '- This option is disabled beacause <b>current direcotry is not in any context</b>.')

    if multiple_warning:
        dialog.add_info(
            '- This option is disabled beacause <b>you selected multiple files</b>.')

    dialog.add_switch(False, var='delete').add_text('Delete source file')

    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    data = pu.get_current_pipeline_context(ctx)

    shot = data['shot']
    wip_folder = ctx.project_path + '/05_WIP/'

    files = [f.replace('\\', '/')
             for f in glob.glob(wip_folder + shot + '*.mp4')]

    latest_file = sorted(files)[-1]
    next_file = aps.get_next_version_path(latest_file)

    if dialog.get_value('shot_preview'):
        ctx.run_async(copy_file_async, ctx.selected_files[0], next_file)

    dialog.close()


def copy_file_async(src, dst):
    aps.copy_file(src, dst, workspace_id=ctx.workspace_id)
    ui.show_success('File copied successfully.')


create_dialog()
