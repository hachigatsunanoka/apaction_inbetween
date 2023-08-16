import anchorpoint as ap
import apsync as aps
import os
import sys

ui = ap.UI()
ctx = ap.Context.instance()

project = aps.get_project(ctx.path)

file = ctx.path

if project is None:
    ui.show_message('Action only works with projects')
    sys.exit(0)


def version_up():
    progress = ap.Progress('Version Up', 'Creating a copy')

    try:
        version = int(aps.get_attribute_text(file, 'Version'))
        version += 1
    except:
        version = 1

    aps.set_attribute_text(file, 'Version', str(version))

    # Copy the file to the versions folder
    if not os.path.exists(ctx.folder + '/version'):
        os.makedirs(ctx.folder + '/version')

    aps.copy_file(file,
                  ctx.folder + '/version/' + ctx.filename + '_v' + str(version) + '.' + ctx.suffix)

    ui.show_success(f"Version {version} created", )
    progress.finish()


ctx.run_async(version_up)
