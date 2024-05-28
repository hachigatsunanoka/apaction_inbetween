import anchorpoint as ap
import apsync as aps
import pipeline_utils as pu
import os
import glob
import importlib
importlib.reload(pu)

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

    if data['shot'] is not None:
        dialog.add_info('Current context: <b>' + data['shot'] + '</b>')
    else:
        dialog.add_info(
            '<font color="grey">Current context: <b>Not in any context</b></font>')
    dialog.add_info('Date: <b>' + pu.get_today() + '</b>')
    dialog.add_separator()
    dialog.add_info('Selected files go to <b>05_WIP</b> folder.')
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

    if shot_preview_enabled:
        dialog.add_info('Shot preview will be saved to <b>05_WIP</b> folder.')

    dialog.add_switch(False, var='delete').add_text('Delete source file')

    dialog.add_button('Apply', press_apply)

    dialog.show()


def press_apply(dialog):
    delete = dialog.get_value('delete')
    shot_preview = dialog.get_value('shot_preview')

    data = pu.get_current_pipeline_context(ctx)

    shot = data['shot']
    wip_folder = ctx.project_path + '/05_WIP/'

    if shot_preview:
        # copy file to just under th wip folder and rename it to <shot>_v<version>.mp4
        files = [f.replace('\\', '/')
                 for f in glob.glob(wip_folder + shot + '*.mp4')]

        if len(files) == 0:
            next_file = wip_folder + shot + '_v1.mp4'
        else:
            latest_file = sorted(files)[-1]
            next_file = aps.get_next_version_path(latest_file)

        ctx.run_async(copy_file_async,
                      ctx.selected_files[0], next_file, delete)

    else:
        # copy file to today's folder
        dst_folder = wip_folder + 'daily/' + pu.get_today()
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        ctx.run_async(copy_files_async, ctx.selected_files, dst_folder, delete)

    dialog.close()


def copy_file_async(src: str, dst: str, delete: bool = False):
    progress = ap.Progress('Copying file...', show_loading_screen=True)
    try:
        aps.copy_file(src, dst, workspace_id=ctx.workspace_id)

        if delete:
            os.remove(src)
    except Exception as e:
        progress.finish()
        ui.show_error('Pipeline', f'Error copying file: {e}')

    progress.finish()
    ui.show_success('Pipeline', 'File copied successfully.')


def copy_files_async(srcs: list, dst_dir: str, delete: bool = False):

    progress = ap.Progress('Copying file...', show_loading_screen=True)

    try:
        for src in srcs:
            dst = dst_dir + '/' + os.path.basename(src)
            aps.copy_file(src, dst, workspace_id=ctx.workspace_id)

            if delete:
                os.remove(src)
    except Exception as e:
        progress.finish()
        ui.show_error('Pipeline', f'Error copying file: {e}')

    progress.finish()

    ui.show_success('Pipeline', 'Files copied successfully.')


create_dialog()
