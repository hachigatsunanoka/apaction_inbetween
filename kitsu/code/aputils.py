import anchorpoint as ap
import apsync as aps

import os


# def get_context(ctx):
#     type = ctx.type


def get_file_context(ctx):
    pl = ctx.path.split('/')
    try:
        i = pl.index('production')
        seq = pl[i+1]
        shot = pl[i+2]
    except ValueError:
        return None, None

    return seq, shot


def get_folder_contex(ctx):
    seq = None
    context = None
    shot = None
    if ctx.path.endswith('production'):
        context = 'seq'
    elif os.path.dirname(ctx.path).endswith('production'):
        context = 'shot'
    elif os.path.dirname(os.path.dirname(ctx.path)).endswith('production'):
        context = 'task'
    else:
        pass

    if context:
        if context == 'seq':
            seq = os.path.basename(ctx.path)
        elif context == 'shot':
            seq = os.path.basename(os.path.dirname(ctx.path))
            shot = os.path.basename(ctx.path)
        elif context == 'task':
            seq = os.path.basename(os.path.dirname(os.path.dirname(ctx.path)))
            shot = os.path.basename(os.path.dirname(ctx.path))
        else:
            pass

    return context, seq, shot
# if context == 'seq':
#         dialog.title = 'Create New Sequence'
#         dialog.add_text('Sequence').add_input(
#             'sq001', var='name')
#         dialog.add_button('Apply', new_seq)

#     if context == 'shot':
#         dialog.title = 'Create New Shot'
#         dialog.add_text('Shot').add_input(
#             'sh001', var='name')
#         dialog.add_text('Range').add_input('1001', var='fin').add_input(
#             '1100', var='fout')
#         dialog.add_button('Apply', new_shot)

#     if context == 'task':
#         dialog.title = 'Create New Task'
#         dialog.add_text('Task Type').add_dropdown(
#             'Houdini', ['Houdini', 'Nuke'], var='tasktype')
#         dialog.add_button('Apply', new_task)
