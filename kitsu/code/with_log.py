import ap
import gazu
import sys
import getpass
import hashlib
import logging
import logging.handlers
import os
import datetime


def create_dialog():
    '''
    just a simple dialog to publish preview
    '''
    dialog = ap.Dialog()
    dialog.title = 'Publish'

    dialog.add_info('Publish Preview for ' + seq_name + '-' + shot_name)

    ttl = [i['name'] for i in gazu.task.all_task_types_for_shot(shot)]

    dialog.add_text('Task Type').add_dropdown(default=ttl[0],
                                              values=ttl,
                                              var='task_type_name')
    tsl = [i['name'] for i in
           gazu.task.all_task_statuses_for_project(kitsu_project)]

    dialog.add_text('Task Status').add_dropdown(default=tsl[0],
                                                values=tsl,
                                                var='task_status_name')

    dialog.add_text('Comment').add_input(default='',
                                         placeholder='Update position',
                                         var='comment',
                                         width=500)

    dialog.add_text('Username').add_input(default='',
                                          var='username',
                                          width=500)

    dialog.add_text('Password').add_password_input(default='',
                                                   var='password',
                                                   width=500)

    dialog.add_button('Publish', press_apply)
    dialog.show()


def press_apply(dialog):
    try:
        task_type_name = dialog.get_control_value('task_type_name')
        task_status_name = dialog.get_control_value('task_status_name')
        comment = dialog.get_control_value('comment')
        username = dialog.get_control_value('username')
        password = dialog.get_control_value('password')

        task_type = gazu.task.get_task_type_by_name(task_type_name)
        task_status = gazu.task.get_task_status_by_name(task_status_name)

        if not task_type:
            raise ValueError('Invalid task type')

        if not task_status:
            raise ValueError('Invalid task status')

        # パスワードをハッシュ化する
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # ユーザー認証を行う
        if not authenticate_user(username, hashed_password):
            raise ValueError('Invalid username or password')

        gazu.task.create_task(shot, task_type, task_status, comment)

        # ログ出力を行う
        logger.info('Task created for shot %s with task type %s and task status %s',
                    shot_name, task_type_name, task_status_name)

    except Exception as e:
        ap.display_error('Error: ' + str(e))
        logger.error('Error: %s', str(e))
        sys.exit(1)
    finally:
        dialog.close()


def authenticate_user(username, hashed_password):
    # ユーザー認証を行うための関数
    # ユーザー名とパスワードを比較する
    # ここでは、ユーザー名が'admin'、パスワードが'password'の場合に認証を許可する
    if username == 'admin' and hashed_password == '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8':
        return True
    else:
        return False


# ログファイルの設定
log_file = os.path.join(os.path.dirname(__file__), 'run_publish_preview.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(
    log_file, when='D', interval=1, backupCount=7)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

create_dialog()
