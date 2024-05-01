import anchorpoint as ap
import apsync as aps

ctx = aps.context()


def get_pipeline_folder(porject_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), porject_name)


def get_shots(project_name):
    get_pipeline_folder(project_name)


def get_shots_metadata(shot_name):
    return ctx.get_shot(shot_name)


def get_current_context():
