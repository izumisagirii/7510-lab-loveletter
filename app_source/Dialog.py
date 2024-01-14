from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from app_source.Global import appData

appData.dialog = None


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        if instance_check.active:
            appData.theme_key = self.text

# put dialog used in app here


class confirm_dialog:

    @staticmethod
    def change_theme_dialog(MDApp):
        items = []
        for theme in appData.colors.keys():
            items.append(ItemConfirm(text=theme,
                                     theme_text_color="Custom",
                                     text_color=MDApp.theme['text'],))
        appData.dialog = MDDialog(
            title='[color=' + MDApp.theme['text'] + ']Choose theme[/color]',
            type="confirmation",
            md_bg_color=MDApp.theme['bg'],
            items=items,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=MDApp.theme['icon'],
                    md_bg_color=MDApp.theme['button'],
                    on_press=lambda x: appData.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=MDApp.theme['icon'],
                    md_bg_color=MDApp.theme['button'],
                    on_press=lambda x: (
                        appData.dialog.dismiss(),
                        appData.change_theme(),
                    ),
                ),
            ],
        )
        appData.dialog.open()

    @staticmethod
    def show_dialog(title: str, text: str):
        dialog = MDDialog(
            title='[color={color}]{text}[/color]'.format(
                color=appData.theme['text'],
                text=title,
            ),
            md_bg_color=appData.theme['bg'],
            text='[color={color}]{text}[/color]'.format(
                color=appData.theme['text'],
                text=text,
            ),
            buttons=[
                MDFlatButton(
                    text='OK',
                    text_color=appData.theme['icon'],
                    md_bg_color=appData.theme['button'],
                    on_press=lambda x: dialog.dismiss()),
            ]
        )
        dialog.open()
