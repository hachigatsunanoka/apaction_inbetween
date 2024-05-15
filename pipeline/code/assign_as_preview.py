import anchorpoint as ap
import apsync as aps

import glob
import os

# get context and metadata
ui = ap.UI()
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
meta = project.get_metadata()

# check current context
# ui.show_success('Test')

# select shot or asset
settings = aps.Settings(name="pipeline")

shots = find_shot_entry(project)
assets = find_asset_entry(project)


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Assign as Preview'

    dialog.add_info('Select the type of asset you want to assign as preview:')
    dialog.section = dialog.add_dropdown(default='Shot', values=[
        'Shot', 'Asset'], var='type', callback=callback_section)

    dialog.add_dropdown(default='c056', values=[
        'c056', 'c057'], var='entity')

    dialog.add_button('Apply', callback=press_apply)

    dialog.show()


def press_apply(dialog):

    type = dialog.get_value('type')
    entity = dialog.get_value('entity')

    file = project.path + '/management/' + type + '/' + entity + '_v001.mov'

    file2 = glob.glob(file)

    ui.show_success(file)


def find_shot_entry(project):
    settings = aps.Settings(name="pipeline")

    folder = project.path + \
        settings.get('management') + '/' + settings.get('shots')
    files = [f for f in os.listdir(folder) if os.path.isfile(
        os.path.join(folder, f))]
    files = [f.split('_')[0] for f in files]
    files = sorted(list(set(files)))
    return files


def find_asset_entry(project):
    settings = aps.Settings(name="pipeline")

    folder = project.path + \
        settings.get('management') + '/' + settings.get('assets')
    files = [f for f in os.listdir(folder) if os.path.isfile(
        os.path.join(folder, f))]
    files = [f.split('_')[0] for f in files]
    files = sorted(list(set(files)))
    return files


def callback_section(dialog: ap.Dialog, value):

    if value == 'Shot':
        files = find_shot_entry(project)
    else:
        files = find_asset_entry(project)

    if files == []:
        ui.show_error('No shots found', 'Please create a shot first.')
    else:
        dialog.set_dropdown_values(
            var='entity', selected_value=files[0], entries=files)


create_dialog()
