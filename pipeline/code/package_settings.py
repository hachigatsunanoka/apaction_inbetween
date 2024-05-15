import anchorpoint as ap
import apsync as aps

ui = ap.UI()
ctx = ap.Context.instance()


settings = aps.Settings(name="pipeline")


def create_dialog():
    dialog = ap.Dialog()

    dialog.title = 'inbetween Pipeline Settings'
    dialog.add_info('Default path for assets and shots')
    dialog.add_text('Management path').add_input(
        '/management', var='management', width=500)
    dialog.add_separator()
    dialog.add_info('Default path for assets and shots')
    dialog.add_text('Assets folder name').add_input(
        'assets', var='assets', width=500)
    dialog.add_info('Default path for assets and shots')
    dialog.add_text('Shots folder name').add_input(
        'shots', var='shots', width=500)
    dialog.add_separator()

    dialog.add_text('Version formant').add_input(
        'v###', var='version', width=500)
    dialog.add_button('Apply', press_apply)
    dialog.show()


def press_apply(dialog):
    management = dialog.get_value('management')
    assets = dialog.get_value('assets')
    shots = dialog.get_value('shots')
    version = dialog.get_value('version')
    print(management, assets, shots, version)

    settings.set("management", management)
    settings.set("assets", assets)
    settings.set("shots", shots)
    settings.set("version", version)
    settings.store()

    ui.show_success('Pipeline Settings', 'Update settings successfully.')

    dialog.close()


create_dialog()
