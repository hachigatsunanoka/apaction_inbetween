import anchorpoint as ap
import apsync as aps
# import utils.anchorpoint_utils as apu

import os
import subprocess

# get context and metadata
ctx = ap.Context.instance()
project = aps.get_project(ctx.path)
meta = project.get_metadata()

# check for kitsu settings
settings = aps.Settings(name="kitsu")

os.environ['IB_KITSU_URL'] = settings.get('url')
os.environ['IB_KITSU_EMAIL'] = settings.get('email')
os.environ['IB_KITSU_PASS'] = settings.get('password')

# check context
shot = os.path.basename(os.path.dirname(ctx.path))
seq = os.path.basename(os.path.dirname(os.path.dirname(ctx.path)))

os.environ['IB_SHOT'] = shot
os.environ['IB_SEQ'] = seq

# houdini settings
settings = aps.Settings(name="houdini")
exe = settings.get('hfs') + '/bin/houdinifx.exe'

# packages
os.environ['IB_USE_IBPIPELINE'] = str('True')
os.environ['IB_USE_IBFX'] = str('True')

os.environ['IB_USE_REDSHIFT'] = str(settings.get('rs'))
os.environ['IB_USE_MOPS'] = str(settings.get('mops'))
os.environ['IB_USE_MLOPS'] = str(settings.get('mlops'))
os.environ['IB_USE_LABS'] = str(settings.get('labs'))
os.environ['IB_USE_AXIOM'] = str(settings.get('axiom'))

os.environ['HOUDINI_PACKAGE_DIR'] = 'I:/IB-PIPELINE/plugins/houdini/_packages'

# launch houdini
process = subprocess.Popen([
    exe,
    ctx.path
])
