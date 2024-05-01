import subprocess
import os
import anchorpoint as ap
import apsync as aps

ctx = aps.context()


# get context and metadata
ui = ap.UI()
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
meta = project.get_metadata()

# check current context
ui.show_success('Test')
