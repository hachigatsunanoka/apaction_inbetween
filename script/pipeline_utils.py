import apsync as aps
import anchorpoint as ap
from pathlib import Path
import os
import subprocess


def launch_program_with_context(exec: str, ctx: ap.Context, clear_python: bool = True):

    declare_context_env(ctx)

    if clear_python:
        os.environ['PYTHONPATH'] = ''

    try:
        subprocess.run([
            exec,
            ctx.path
        ])
    except Exception as e:
        raise Exception(f'Error launching program: {e}')

    return True


def get_current_pipeline_context(ctx: ap.Context):
    # this function is used to get the current pipeline context

    data = {}

    # get project metadata
    project = aps.get_project(ctx.path)
    data['project'] = project.name
    data['project_dir'] = project.path
    data['width'] = project.get_metadata().get('width', '1920')
    data['height'] = project.get_metadata().get('height', '1080')
    data['fps'] = project.get_metadata().get('fps', '24')

    # get shot metadata from context
    if ctx.filename:
        data['shot_dir'] = str(Path(ctx.path).parents[1]).replace(os.sep, '/')
    else:
        data['shot_dir'] = str(Path(ctx.path).parent).replace(os.sep, '/')

    data['shot'] = Path(data['shot_dir']).name

    start = aps.get_attribute_text(
        data['shot_dir'], 'Start', workspace_id=ctx.workspace_id)
    if start is None:
        start = '1001'

    data['start'] = start

    range = aps.get_attribute_text(
        data['shot_dir'], 'Range', workspace_id=ctx.workspace_id)
    if range is None:
        range = '100'

    data['range'] = aps.get_attribute_text(data['shot_dir'], 'Range',
                                           workspace_id=ctx.workspace_id)

    return data


def declare_context_env(ctx: ap.Context):
    data = get_current_pipeline_context(ctx)

    # set project
    project = aps.get_project(ctx.path)
    os.environ['IB_PROJ'] = data['project']
    os.environ['IB_PROJDIR'] = data['project_dir']

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
    os.environ['IB_FEND'] = str(int(data['start']) + int(data['range']))


def copy_scenefile_from_template(ext: str, ctx: ap.Context, task: str):

    if not ext.startswith('.'):
        ext = '.' + ext

    format = '[project]_[shot]_[task]_[worker]_[version]' + ext
    template = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')).replace(os.sep, '/') + '/template/_template' + ext

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
