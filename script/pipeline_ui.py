import anchorpoint as ap
import pipeline_utils as pu


def create_launch_dialog(program_name: str, callback: callable = None):

    ctx = ap.get_context()
    data = pu.get_current_pipeline_context(ctx)

    is_in_context = True
    if data['shot'] is None:
        is_in_context = False

    dialog = ap.Dialog()

    dialog.title = f'Launch {program_name}'

    dialog.add_info('<b>Current context: </b><b>' + data['shot'] + '</b>')

    text = 'Launch with current context'
    if not is_in_context:
        text = '<font color="grey">' + text + '</font>'
    dialog.add_checkbox(default=is_in_context, var='in_context',
                        enabled=is_in_context).add_text(text)
    dialog.add_info(
        '<font color="yellow"> This option is disabled because the current context is not a shot.</font>', var='context_warning')
    dialog.hide_row('context_warning', is_in_context)
    dialog.add_separator()
    dialog.add_checkbox(var='new').add_text('<b>Open as new version</b>')
    dialog.add_info(
        'This option will enable version control for current folder.')

    dialog.add_button('Launch', callback=callback)

    return dialog
