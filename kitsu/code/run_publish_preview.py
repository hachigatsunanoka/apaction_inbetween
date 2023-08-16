import gazu
import anchorpoint as ap
import apsync as aps
import sys
import aputils as apu

gazu.cache.enable()

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)

# Login
try:
    kitsu_setting = aps.Settings('kitsu')
    url = kitsu_setting.get('url')
    email = kitsu_setting.get('email')
    password = kitsu_setting.get('password')

    gazu.client.set_host(url)
    gazu.log_in(email, password)

    kitsu_project = gazu.project.get_project_by_name(project.name)

    if kitsu_project is None:
        ui.show_error('Kitsu', 'Retrive Error : Project not found in Kitsu')
        sys.exit()
except:
    ui.show_error('Kitsu', 'Login Error : Please login to Kitsu first')
    sys.exit()


# Get sequence and shot
seq_name, shot_name = apu.get_file_context(ctx=ctx)
seq = gazu.shot.get_sequence_by_name(kitsu_project, seq_name)
shot = gazu.shot.get_shot_by_name(seq, shot_name)


def upload_preview(task_status_name, comment):
    '''
    upload preview to kitsu
    '''
    progress = ap.Progress('Upload preview', show_loading_screen=True)

    # set task
    task_type = gazu.task.get_task_type_by_name('All')
    task_status = gazu.task.get_task_status_by_name(task_status_name)
    task = gazu.task.new_task(shot, task_type)

    # Add file name and location to comment
    comment = comment + '\n' + ctx.path

    # publish preview
    preview = gazu.task.publish_preview(
        task,
        task_status,
        comment=comment,
        preview_file_path=ctx.path
    )

    progress.finish()

    gazu.cache.clear_all()
    gazu.cache.disable()

    ui.show_success('Publish', 'Preview published successfully')


def create_dialog():
    '''
    just a simple dialog to publish preview
    '''
    dialog = ap.Dialog()
    dialog.title = 'Publish'

    dialog.add_info('Publish Preview for ' + seq_name + '-' + shot_name)

    ttl = [i['name'] for i in gazu.task.all_task_types_for_shot(shot)]

    dialog.add_text('Task Type').add_dropdown(default=ttl[0],
                                              values=ttl,
                                              var='task_type_name')
    tsl = [i['name'] for i in
           gazu.task.all_task_statuses_for_project(kitsu_project)]

    dialog.add_text('Task Status').add_dropdown(default=tsl[0],
                                                values=tsl,
                                                var='task_status_name')

    dialog.add_text('Comment').add_input(default='',
                                         placeholder='Update position',
                                         var='comment',
                                         width=500)

    dialog.add_button('Publish', press_apply)
    dialog.show()


def press_apply(dialog):
    ctx.run_async(upload_preview, dialog.get_value(
        'task_status_name'), dialog.get_value('comment'))

    dialog.close()


create_dialog()
