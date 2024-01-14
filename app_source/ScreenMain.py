from kivy.uix.screenmanager import Screen
from app_source.Global import appData
from kivymd.uix.taptargetview import MDTapTargetView
import random
import time

appData.welcomeText = [
    'Write from the heart\n        Connect with the soul',
    'Express your feelings\n        Hare your dreams',
    'The art of romance\n        The gift of words',
    'Capture the moment\n        Cherish the memory',
    'Spark the passion\n        Ignite the flame',
    'A timeless treasure\n        A lasting legacy',
    'A personal touch\n        A special bond'
]


class ScreenMain(Screen):
    # def on_enter(self):
    #     # Reset the text field
    #     self.ids.txt_name.text = ''

    # def set_name(self):
    #     # Add the inputted name to appData.myname
    #     appData.myname = self.ids.txt_name.text.strip()
    text_welcome = 'Good '

    def __init__(self, **kw):
        mytime = time.localtime()
        hour = mytime.tm_hour
        if hour > 7 and hour < 12:
            self.text_welcome += 'Morning!'
        elif hour >= 12 and hour < 19:
            self.text_welcome += 'Afternoon!'
        else:
            self.text_welcome += 'Night!'
        super().__init__(**kw)
        self.tap_target_view = MDTapTargetView(
            widget=self.ids.help_button,
            outer_circle_color=appData.hex2rgb(appData.theme['button']),
            title_text="This is an help button",
            title_text_color=appData.hex2rgb(appData.theme['icon']),
            description_text="This is a description of the button",
            description_text_color=appData.hex2rgb(appData.theme['icon']),
            widget_position="right_top",
        )

    text = random.choice(appData.welcomeText)

    def tap_help_start(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()
