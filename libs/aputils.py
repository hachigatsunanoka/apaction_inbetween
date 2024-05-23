import apsync as aps
import anchorpoint as ap
from pathlib import Path
import os

api = aps.get_api()


def get_current_pipeline_context(ctx: ap.Context):
    d = {}
    project = aps.get_project(ctx.path)
    d['project'] = project.name
    d['project_dir'] = project.path

    if ctx.filename:
        d['shot_dir'] = str(Path(ctx.path).parents[1])
    else:
        d['shot_dir'] = str(Path(ctx.path).parent)

    d['shot'] = Path(d['shot_dir']).name

    production_dir = d['project_dir'] + '/02_PRODUCTION'
    d['shared_dir'] = production_dir + '/shared'

    d['usd_shot_dir'] = production_dir + '/shots/' + d['shot']
    d['usd_asset_dir'] = production_dir + '/assets'

    d['start'] = '1001'
    d['range'] = '1100'

    d['width'] = project.get_metadata().get('width', '1920')
    d['height'] = project.get_metadata().get('height', '1080')
    d['fps'] = project.get_metadata().get('fps', '24')

    return d


def check_if_shot_context(ctx: ap.Context):
    if ctx.filename:
        production = str(Path(ctx.path).parents[2])
    else:
        production = str(Path(ctx.path).parents[1])

    if production.endswith('02_PRODUCTION'):
        return True
    else:
        return False


def declare_context_env(ctx):
    data = get_current_pipeline_context(ctx)
    # set project
    project = aps.get_project(ctx.path)
    os.environ['IB_PROJ'] = data['project']
    os.environ['IB_PROJDIR'] = data['project_dir']

    # set shot
    os.environ['IB_SHOTDIR'] = data['shot_dir']
    os.environ['IB_SHOT'] = data['shot']

    # set render
    os.environ['IB_RENDERDIR'] = data['shot_dir'] + '/render'

    # set shared
    os.environ['IB_SHAREDDIR'] = data['shared_dir']

    # set usd
    os.environ['IB_USDSHOTDIR'] = data['usd_shot_dir']
    os.environ['IB_USDASSETDIR'] = data['usd_asset_dir']


# def read_attributes(path):
#     # Get all attributes in the project (everything what is under "Recent Attributes")
#     proj_attributes = api.attributes.get_attributes()
#     # Collect the output in a string
#     output = {}

#     # Get the Attribute field of the file/folder
#     for attribute in proj_attributes:
#         atttribute_value = api.attributes.get_attribute_value(
#             path, attribute.name)

#         # If the Attribute field is not empty, add it to the output string. Add a linebreak at the end
#         output[attribute.name] = atttribute_value

#     return output


# def get_latest_preview_file(project, shot):
#     management_dir = project.path + '/00_MANAGEMENT'

#     files = [file
#              for file in glob.glob(management_dir + '/' + shot + '_v*.mp4')]
#     files = sorted(files)
#     file = files[-1]
#     return file


# def get_latest_preview_revision(project, shot):
#     management_dir = project.path + '/00_MANAGEMENT'

#     files = [file
#              for file in glob.glob(management_dir + '/' + shot + '_v*.mp4')]
#     files = sorted(files)
#     latest = files[-1]
#     revision = latest.split('_v')[1].split('.')[0]
#     # convert zero padded revision to integer
#     revision = str(int(revision))
#     return revision
