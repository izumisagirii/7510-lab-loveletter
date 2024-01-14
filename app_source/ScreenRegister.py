from kivy.uix.screenmanager import Screen
from app_source.Global import appData
import re  # 加入正则表达式
from app_source.Dialog import confirm_dialog


class ScreenRegister(Screen):

    def Regsiter(self):
        username = self.ids.username_field.text.strip()
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        repassword = self.ids.repassword_field.text.strip()
        phonenumber = self.ids.phonenumber_field.text.strip()
        userdata = {
            'account': {
                'email': email,
                'password': password,
                'phonenumber': phonenumber,
            },
        }

        # 检查输入的value
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(repassword) == 0 or len(phonenumber) == 0:
            # 若其中一项为长度为0，则为空
            confirm_dialog.show_dialog(title='Warning',
                                       text='Empty text field exists',)
            return
        if len(password) < 6 or len(repassword) < 6:  # 检查输入密码位数，不得小于六位
            confirm_dialog.show_dialog(title='Warning',
                                       text='The entered password/re-enter password is less than six digits',)
            return
        if password != repassword:  # 检查两次输入密码是否相同
            confirm_dialog.show_dialog(title='Warning',
                                       text='The password and re-enter password are different',)
            return
        if email.find("@") == -1 or not email.endswith(".com"):  # 验证邮箱格式，是否含有@并且以dotcom结尾
            confirm_dialog.show_dialog(title='Warning',
                                       text='Email format error',)
            return
        # 正则表达式：查看电话号码是否为香港号码格式，5、6、7、8开头的八位数字
        if len(phonenumber) != 8 or not re.match(r'5|6|7|8\d{7}', phonenumber):
            confirm_dialog.show_dialog(title='Warning',
                                       text='Phone number format error',)
            return
        # 验证用户名是否已被注册
        data = appData.db.get()
        # print(data)
        if not data == None:
            try:
                data[username]
                confirm_dialog.show_dialog(title='Warning',
                                           text='User name already used!',)
                return
            except KeyError:
                # continue
                ...
        appData.db.child(username).set(userdata)
        confirm_dialog.show_dialog(title='Congratulations!',
                                   text='You have successfully registered an account')
        appData.app.back_to_main()
        # print(appData.db.get())

    def Clear(self):
        self.ids.username_field.text = ""
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""
        self.ids.repassword_field.text = ""
        self.ids.phonenumber_field.text = ""

    def on_leave(self, *args):
        self.Clear()
        return super().on_leave(*args)
