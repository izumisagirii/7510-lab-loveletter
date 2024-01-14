# author:LiWentao
from kivy.uix.screenmanager import Screen

from app_source.Global import appData
from app_source.Dialog import confirm_dialog
import re  # 加入正则表达式
from firebase_admin import db
# from firebase_admin import storage


class ScreenLogin(Screen):
    def LoginIn(self):
        # Get values from the text fields
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()
        if len(username) == 0 or len(password) == 0 or len(password) < 6:
            confirm_dialog.show_dialog(title='Warning',
                                       text='The input is empty or incorrect',)
            return
        data = appData.db.get()
        if not data == None:
            try:
                if not data[username]['account']['password'] == password:
                    confirm_dialog.show_dialog(title='Warning',
                                               text='Wrong password!',)
                    return
                appData.IfLogin = True
                appData.LoginName = username
                confirm_dialog.show_dialog(title='Welcome',
                                           text='{name}, you are logging in!'.format(name=username),)
                appData.app.back_to_main()
                return
            except KeyError:
                ...
        confirm_dialog.show_dialog(title='Warning',
                                   text='User doesn\'t exist!',)

    def on_leave(self, *args):
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""
        return super().on_leave(*args)
