import anchorpoint as ap
import datetime
import os

ui = ap.UI()
ctx = ap.get_context()

today = str(datetime.date.today()).split('-')

foldername = today[0][-2:]+today[1]+today[2]

if not os.path.exists(ctx.path + '/'+foldername):
    os.makedirs(ctx.path + '/'+foldername)
    ui.show_success('Today', 'Folder created: '+foldername)
else:
    ui.show_error('Today', 'Folder already exists: '+foldername)
