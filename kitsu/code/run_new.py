import gazu
import anchorpoint as ap
import apsync as aps
import sys
import os

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)
worker_initial = ''.join([i[0] for i in ctx.username.lower().split(' ')])

if ctx.path.endswith('production'):
    context = 'seq'
elif os.path.dirname(ctx.path).endswith('production'):
    context = 'shot'
elif os.path.dirname(os.path.dirname(ctx.path)).endswith('production'):
    context = 'task'
else:
    ui.show_error(
        'Kitsu', 'Context Error : Please select a right place to create')
    sys.exit()

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


def create_dialog(context):
    dialog = ap.Dialog()

    if context == 'seq':
        dialog.title = 'Create New Sequence'
        dialog.add_text('Sequence').add_input(
            'sq001', var='name')
        dialog.add_button('Apply', new_seq)

    if context == 'shot':
        dialog.title = 'Create New Shot'
        dialog.add_text('Shot').add_input(
            'sh001', var='name')
        dialog.add_text('Range').add_input('1001', var='fin').add_input(
            '1100', var='fout')
        dialog.add_button('Apply', new_shot)

    if context == 'task':
        dialog.title = 'Create New Task'
        dialog.add_text('Task Type').add_dropdown(
            'Houdini', ['Houdini', 'Nuke'], var='tasktype')
        dialog.add_text('Element').add_input('fx', var='element')
        dialog.add_button('Apply', new_task)

    dialog.show()


def new_seq(dialog):
    name = dialog.get_value('name')
    ui.show_info('Kitsu', 'Create Sequence : ' + name)
    kitsu_seq = gazu.shot.new_sequence(kitsu_project, name)

    dialog.close()


def new_shot(dialog):
    name = dialog.get_value('name')
    fin = int(dialog.get_value('fin'))
    fout = int(dialog.get_value('fout'))
    seq = ctx.path.split('/')[-1]
    kitsu_seq = gazu.shot.get_sequence_by_name(kitsu_project, seq)
    ui.show_info('Kitsu', 'Create Shot : ' + name + ' in ' + seq)
    kitsu_shot = gazu.shot.new_shot(
        kitsu_project, kitsu_seq, name, frame_in=fin, frame_out=fout)
    os.makedirs(ctx.path + '/' + name)
    dialog.close()


def new_task(dialog):
    name = dialog.get_value('tasktype')
    element = dialog.get_value('element')
    shot = ctx.path.split('/')[-1]
    seq = ctx.path.split('/')[-2]
    ui.show_info('Kitsu', 'Create Task : ' +
                 name + ' in ' + shot + 'in ' + seq)
    copy_template_file(seq, shot, name, element, worker_initial)
    dialog.close()


def copy_template_file(seq, shot, task, element, wi):

    ext = {'Houdini': '.hip', 'Nuke': '.nk'}[task]

    if element == '':
        ui.show_error('Error', 'Element is empty')
        return

    filename = '_'.join([seq+'-'+shot+'_', element, wi]) + ext

    if os.path.exists(ctx.path + '/' + filename):
        ui.show_error('Error', 'Hip file already exists')
        return

    templatefile = project.path + '/pipeline/houdini/_template.hip'
    aps.copy_file(templatefile, ctx.path + '/' + filename)

    # if launch:
    #     ui.show_info('Successfully create')

    # dialog.close()


create_dialog(context=context)
