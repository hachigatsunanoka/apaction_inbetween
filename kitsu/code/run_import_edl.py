import gazu
import anchorpoint as ap
import apsync as aps
import sys
import os
import glob
import ibffmpeg as ffmpeg

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)

# Login
try:
    kitsu = aps.Settings('kitsu')
    url = kitsu.get('url')
    email = kitsu.get('email')
    password = kitsu.get('password')

    gazu.client.set_host(url)
    gazu.log_in(email, password)

    kitsu_project = gazu.project.get_project_by_name(project.name)

    if kitsu_project is None:
        ui.show_error('Kitsu', 'Retrive Error : Project not found in Kitsu')
        sys.exit()
except:
    ui.show_error('Kitsu', 'Login Error : Please login to Kitsu first')
    sys.exit()


def edl_make(path):
    # find edl file
    progress = ap.Progress('EDL', 'Importing EDL...')
    edls = glob.glob(os.path.join(path, '**/*.edl'), recursive=True)
    for edl in edls:
        gazu.shot.import_edl(
            kitsu_project, edl_file_path=edl)
    progress.finish()


def upload_preview(path):
    progress = ap.Progress('Preview', 'Uploading Preview...')
    mp4s = glob.glob(os.path.join(path, '**/*.mp4'), recursive=True)
    i = 0
    l = len(mp4s)
    for mp4 in mp4s:
        i += 1
        # proj_name = os.path.basename(mp4).split('_')[0]
        seq_name = os.path.basename(mp4).split('-')[-2].split('_')[-1]
        shot_name = os.path.basename(mp4).split('-')[-1].split('.')[0]

        # get seq
        seq = gazu.shot.get_sequence_by_name(kitsu_project, seq_name)
        shot = gazu.shot.get_shot_by_name(seq, shot_name)

        # create task
        task_type = gazu.task.get_task_type_by_name('All')
        task_status = gazu.task.get_task_status_by_name('Previs')
        task = gazu.task.new_task(shot, task_type)
        preview = gazu.task.publish_preview(
            task,
            task_status,
            comment='Automatic upload from davinci',
            # preview_file_path='I:/IB-PROJECTS/23_011_GAMM/pipeline/preview/vasherran/c028.mov',
            preview_file_path=mp4
        )
        # gazu.task.set_main_preview(preview)
        progress.report_progress(i/l)
    progress.finish()


def create_shot_folder(project, seq_name, shot_name):
    seq_path = project.path + '/production' + 'seq_name'
    if os.path.exists(seq_path) is False:
        os.mkdir(seq_path)

    if os.path.exists(seq_path + '/' + shot_name) is False:
        os.mkdir(seq_path + '/' + seq_name)


def create_dialog():
    dialog = ap.Dialog()
    dialog.title = 'Create Shot'
    dialog.add_text('Folder').add_input(default='I:/IB-PROJECTS/23_011_GAMM/pipeline/preview',
                                        placeholder='path/to/houdini/directory',
                                        var='folder',
                                        browse=ap.BrowseType.Folder,
                                        browse_path='I:/IB-PROJECTS/23_011_GAMM/pipeline/preview',
                                        width=500)
    dialog.add_button('Create Shot', press_apply)
    dialog.show()


def press_apply(dialog):
    # ctx.run_async(edl_make, dialog.get_value('folder'))
    ctx.run_async(upload_preview, dialog.get_value('folder'))

    dialog.close()


create_dialog()
