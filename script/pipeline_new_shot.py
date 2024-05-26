import anchorpoint as ap
import apsync as aps
import shutil

ui = ap.UI()
ctx = ap.get_context()
project = aps.get_project(ctx.path)
metadata = project.get_metadata()
format = metadata.get('shot_format')
increment = metadata.get('shot_increment')

settings = aps.Settings(name="pipeline")
shot_template = settings.get('shot')


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Create new shots'
    dialog.add_text('Range :').add_input(
        '1', var='start').add_input('10', var='end')
    dialog.add_button('Create', press_create)

    dialog.show()


def create_shot_folder_async(start, end):

    num = format.count('#')

    progress = ap.Progress('Creating Shots', 'This may take a while because of all metadata.',
                           infinite=False, cancelable=False, show_loading_screen=True)

    for i in range(start, end+1):
        shotnum = i * int(increment)
        shot = format.replace('#' * num, f'{shotnum:0{num}d}')
        # aps.copy_from_template(shot_template, ctx.path +
        #                        '/'+shot, workspace_id=ctx.workspace_id)
        shutil.copytree(shot_template, ctx.path + '/' + shot)
        progress.set_text(str(i) + ' / ' + str(end) + ' shots created')

    progress.finish()


def press_create(dialog):
    start = int(dialog.get_value('start'))
    end = int(dialog.get_value('end'))
    ctx.run_async(create_shot_folder_async, start, end)

    ui.show_success('Shot', 'Shots created successfully.')

    dialog.close()


create_dialog()
