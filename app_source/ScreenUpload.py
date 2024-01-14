import os
from kivy.uix.screenmanager import Screen
from app_source.Global import appData
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from app_source.Dialog import confirm_dialog


class ScreenUpload(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            background_color_selection_button=appData.theme['button'],
            background_color_toolbar=appData.theme['button'],
            preview=True,
        )

    def change_pic(self, id: str):
        self.fm_id = id
        if appData.IfMobile:
            # permissions choosing pic on android, don't mind this warning
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            # Add below to android manifext xml file
            # Or you can't open file
            # android:requestLegacyExternalStorage="true"
            # android:preserveLegacyExternalStorage="true"
            # FUCK
            PATH = "/storage/emulated/0/"  # app_folder
            # PATH = os.path.dirname(os.path.abspath(__file__))
            # self.file_manager.show_disks()  # output manager to the screen
            self.file_manager.show(PATH)
        else:
            self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path: str):
        if self.fm_id == 'profile':
            self.ids.profile.source = path
        if self.fm_id == 'pic':
            self.ids.pic.source = path
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def upload(self):
        text = self.ids.input.text
        if text == '':
            text = 'This person too lazy to write a intro'
        # handle error I don't know
        try:
            # handle error if already uploaded
            try:
                profile = appData.upload(
                    file=self.ids.profile.source, name=appData.LoginName+'_profile')
            except FileNotFoundError:
                profile = self.ids.profile.source
            try:
                pic = appData.upload(
                    file=self.ids.pic.source, name=appData.LoginName+'_pic')
            except FileNotFoundError:
                pic = self.ids.pic.source
            uploadData = {
                'text': text,
                'profile': profile,
                'pic': pic,
                'heart': 0,
            }
            appData.db.child(appData.LoginName+'/uploads').set(uploadData)
            confirm_dialog.show_dialog(title='Congratulations!',
                                       text='You have successfully upload your profile!')
        except OSError as e:
            confirm_dialog.show_dialog(title='Fail uploading',
                                       text=repr(e))
        # print(appData.db.get())

    def on_enter(self, *args):
        data = appData.db.get()
        if not data == None:
            try:
                self.ids.input.text = data[appData.LoginName]['uploads']['text']
                self.ids.profile.source = data[appData.LoginName]['uploads']['profile']
                self.ids.pic.source = data[appData.LoginName]['uploads']['pic']
            except KeyError:
                ...
        return super().on_enter(*args)
