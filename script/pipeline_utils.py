import apsync as aps
import anchorpoint as ap
import os
import subprocess
import datetime


def launch_program_with_context(exec: str, target: str, ctx: ap.Context, clear_python: bool = True):

    declare_context_env(ctx)

    if clear_python:
        os.environ['PYTHONPATH'] = ''

    try:
        subprocess.run([
            exec,
            target
        ])
    except Exception as e:
        raise Exception(f'Error launching program: {e}')

    return True


def get_current_pipeline_context(ctx: ap.Context):
    # this function is used to get the current pipeline context

    data = {}

    # get project metadata
    project = aps.get_project(ctx.path)
    data['project'] = project.get_metadata().get('short_name', 'unk')
    data['project_dir'] = project.path
    data['width'] = project.get_metadata().get('width', '1920')
    data['height'] = project.get_metadata().get('height', '1080')
    data['fps'] = project.get_metadata().get('fps', '24')
    data['ocio'] = project.get_metadata().get('ocio', None)

    # get shot metadata from context
    data['shot'] = None
    data['shot_dir'] = None
    data['start'] = None
    data['range'] = None

    parts = ctx.path.split('/')
    for i in range(len(parts)):
        if parts[i] == '02_PRODUCTION':
            if i + 1 < len(parts):
                data['shot'] = parts[i + 1]
                break

    if data['shot'] is not None:
        data['shot_dir'] = '/'.join(parts[:i + 2])

        start = aps.get_attribute_text(
            data['shot_dir'], 'Start', workspace_id=ctx.workspace_id)
        if start is None:
            start = '1001'

        data['start'] = start

        frame_range = aps.get_attribute_text(
            data['shot_dir'], 'Range', workspace_id=ctx.workspace_id)
        if frame_range is None:
            frame_range = '100'

        data['range'] = frame_range
    
    print(data)

    return data


def declare_context_env(ctx: ap.Context):
    data = get_current_pipeline_context(ctx)

    # set project
    os.environ['IB_PROJ'] = data['project']
    os.environ['IB_PROJDIR'] = data['project_dir']
    os.environ['IB_FPS'] = data['fps']

    # set shot
    os.environ['IB_SHOT'] = data['shot']
    os.environ['IB_SHOTDIR'] = data['shot_dir']
    os.environ['IB_RENDERDIR'] = data['shot_dir'] + '/render'

    # set shared
    production_dir = data['project_dir'] + '/02_PRODUCTION'
    os.environ['IB_SHAREDDIR'] = production_dir + '/_shared'
    os.environ['IB_USDSHOTDIR'] = production_dir + \
        '/_usd/shots/' + data['shot']
    os.environ['IB_USDASSETDIR'] = production_dir + '/_usd/assets'

    os.environ['IB_RESX'] = data['width']
    os.environ['IB_RESY'] = data['height']
    os.environ['IB_FSTART'] = data['start']
    os.environ['IB_FRANGE'] = data['range']
    os.environ['IB_FEND'] = str(int(data['start']) + int(data['range']) - 1)
    os.environ['IB_WORKER'] = aps.Settings('pipeline').get('worker')
    os.environ['IB_TODAY'] = get_today()

    os.environ['OCIO'] = data['ocio']


def copy_scenefile_from_template(template: str, ctx: ap.Context, task: str):

    ext = template.split('.')[-1]
    format = '[project]_[shot]_[task]_[worker]_[version].' + ext

    data = get_current_pipeline_context(ctx)
    variables = {
        'project': data['project'],
        'shot': data['shot'],
        'task': task,
        'version': 'v1',
        'worker': aps.Settings('pipeline').get('worker'),
    }
    resolved = ctx.path + '/' + aps.resolve_variables(format, variables)

    aps.copy_file(template, resolved)
    return resolved


def get_today():
    '''
    Get today's date in the format of 'yymmdd'

    Returns:
        str: today's date in the format of 'yymmdd'
    '''

    today = str(datetime.date.today()).split('-')
    foldername = today[0][-2:]+today[1]+today[2]

    return foldername


def add_suffix_to_filename(file_path):
    base, ext = os.path.splitext(file_path)
    suffix = '_0'
    count = 0

    new_file_path = base + suffix + ext
    while os.path.exists(new_file_path):
        count += 1
        suffix = f'_{count}'
        new_file_path = base + suffix + ext

    return new_file_path
