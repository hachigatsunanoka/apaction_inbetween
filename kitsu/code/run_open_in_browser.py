import gazu
import anchorpoint as ap
import apsync as aps
import sys
import webbrowser
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


url = gazu.project.get_project_url(kitsu_project, 'shots')

webbrowser.open(url)
