# import ssl
import os
import certifi
from app_source.Global import appData
from app_source.ScreenMain import ScreenMain
from app_source.ScreenLogin import ScreenLogin
from app_source.ScreenRegister import ScreenRegister
from app_source.ScreenBrowse import ScreenBrowse
from app_source.ScreenUpload import ScreenUpload
from app_source.Dialog import confirm_dialog
# kivy
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.window import Window
import firebase_admin
from firebase_admin import db
from firebase_admin import storage

# the following three lines are used for SSL problem on some computers.
# do NOT forget to add the following three lines to your code if you want to download something from the Internet
os.environ['SSL_CERT_FILE'] = certifi.where()
# ssl._create_default_https_context = ssl._create_stdlib_context

# add to android manifest to acess internet
# <uses-permission android:name="android.permission.INTERNET" />
# <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

# create a global variable
appData.IfLogin = False
appData.LoginName = ''
appData.IfMobile = False

# Set window size if the app runs on Windows or MacOS
if platform in ('win', 'macosx', 'linux'):
    if appData.IfMobile:
        Window.size = (414, 736)
    else:
        Window.size = (1080, 720)

cred_obj = firebase_admin.credentials.Certificate(
    'group_assets/dbkey/23459123.json')

firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://comp7510-12a87-default-rtdb.firebaseio.com/',
    'storageBucket': 'comp7510-12a87.appspot.com'
})
# clear db
# db.reference('/').set({'user': {}})
appData.db = db.reference('/user')
appData.sb = storage.bucket()


class MyApp(MDApp):

    def show_screen(self, screen_name):
        if not screen_name == 'ScreenLogin' and not appData.IfLogin and not screen_name == 'ScreenRegister':
            screen_name = 'ScreenLogin'
            confirm_dialog.show_dialog(title='Warning',
                                       text='You need to login first',)
        screenmanager = appData.screenmanager
        # set transition effect
        screenmanager.transition.direction = 'left'
        # change screen
        screenmanager.current = screen_name

    def back_to_main(self):
        screenmanager = appData.screenmanager
        # set transition effect
        screenmanager.transition.direction = 'right'
        # change screen
        screenmanager.current = 'ScreenMain'

    def change_theme(self, theme):
        appData.theme_key = theme
        appData.theme = appData.colors[theme]
        self.theme = appData.theme
    # Reload to change theme, tryed theming by overloading the color_definitions.py object, but It still can't be switched in real time
    # To be modified
        self.load_screens()

    def load_screens(self):
        scm = appData.screenmanager
        # in case of changing theme
        scm.clear_widgets()
        scm.add_widget(ScreenMain(name='ScreenMain'))
        scm.current = 'ScreenMain'
        scm.add_widget(ScreenLogin(name='ScreenLogin'))
        scm.add_widget(ScreenBrowse(name='ScreenBrowse'))
        scm.add_widget(ScreenUpload(name='ScreenUpload'))
        scm.add_widget(ScreenRegister(name='ScreenRegister'))

    def build(self):
        self.theme = appData.theme
        self.title = 'Little Love Letter'

        # load KV files individually
        Builder.load_file('app_source/ScreenMain.kv')
        Builder.load_file('app_source/ScreenLogin.kv')
        Builder.load_file('app_source/ScreenBrowse.kv')
        Builder.load_file('app_source/ScreenUpload.kv')
        Builder.load_file('app_source/ScreenRegister.kv')
        Builder.load_file('app_source/Dialog.kv')
        # Create screen instances and add them to the screen manager
        # With the screen manager, we can change the screens in the app
        appData.screenmanager = ScreenManager()
        self.load_screens()
        return appData.screenmanager

    def show_theme_dialog(self):
        confirm_dialog.change_theme_dialog(self)

    def logout(self):
        appData.IfLogin = False
        confirm_dialog.show_dialog(title='Message',
                                   text='You out',)


# appData is a global name defined in Global.py
# Now appData.app refers to the app
# We can add anything to appData and get them back in different py files
appData.topic = 'LittleLoveLetter'
appData.app = MyApp()
appData.app.run()
