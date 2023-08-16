import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()

KITSU_DATA_SOURCE_URL = 'http://0.0.0.0:80/api'
KITSU_DATA_SOURCE_USER_EMAIL = 'your@adress.com'
KITSU_DATA_SOURCE_USER_PASSWORD = 'yoursecretpassword'

settings = aps.Settings(name="kitsu")
if settings.get('url') != '':
    KITSU_DATA_SOURCE_URL = settings.get('url')
if settings.get('email') != '':
    KITSU_DATA_SOURCE_USER_EMAIL = settings.get('email')
if settings.get('password') != '':
    KITSU_DATA_SOURCE_USER_PASSWORD = settings.get('password')


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'Kitsu API Settings'
    dialog.add_text('URL').add_input(
        KITSU_DATA_SOURCE_URL, var='url', width=500)
    dialog.add_text('Email').add_input(
        KITSU_DATA_SOURCE_USER_EMAIL, var='email', width=500)
    dialog.add_text('Password').add_input(
        KITSU_DATA_SOURCE_USER_PASSWORD, var='password', width=500)

    dialog.add_button('Apply', press_apply)
    dialog.show()


def press_apply(dialog):
    url = dialog.get_value('url')
    email = dialog.get_value('email')
    password = dialog.get_value('password')

    settings.set("url", url)
    settings.set("email", email)
    settings.set("password", password)
    settings.store()

    ui.show_success('Kitsu', 'Update API settings successfully.')

    dialog.close()


create_dialog()
