from kivy.uix.screenmanager import Screen
from app_source.Global import appData
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.card.card import MDCard


class MySwiper(MDSwiperItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MySwiperHD(MDSwiperItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def NewSwiperItem(*args, **kwargs):
    if appData.IfMobile:
        M = MySwiper
    else:
        M = MySwiperHD

    profile = 'group_assets/images/image.png'
    pic = 'group_assets/images/l_hires.jpg'
    heart = 0
    name = 'lenna'
    text = 'this is a sample'
    db = appData.db.get()

    class SI(M):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ids.text.text = text
            self.hearted = False
            self.heartNum = heart
            self.ids.textName.text = name
            self.ids.profile.source = profile
            self.ids.image.source = pic
            self.ids.heart_button.text = str(heart)

        def heart(self):
            ref = appData.db.child(self.ids.textName.text+'/uploads')
            if not self.hearted:
                self.ids.heart_button.icon = "cards-heart"
                self.ids.heart_button.icon_color = 'FF0000'
                self.ids.heart_button.text = str(self.heartNum+1)
                ref.update({
                    'heart': self.heartNum+1
                })
                self.hearted = True
            else:
                self.ids.heart_button.icon = "cards-heart-outline"
                self.ids.heart_button.icon_color = '000000'
                self.ids.heart_button.text = str(self.heartNum)
                ref.update({
                    'heart': self.heartNum
                })
                self.hearted = False
    while True:
        flag = False
        for obj in db:
            try:
                data = db[obj]['uploads']
                profile = data['profile']
                pic = data['pic']
                heart = data['heart']
                name = obj
                text = data['text']
                flag = True
                yield SI()
            except KeyError:
                ...
        if db == None or not flag:
            yield SI()

# use a window to load picture


class ScreenBrowse(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        appData.screenSwiper = self.ids.swiper
        self.num = 0

    def on_enter(self, *args):
        self.itemGenerator = NewSwiperItem()
        for i in range(6):
            self.add_new()
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.ids.swiper.set_current(0)
        for widget in self.ids.swiper.get_items():
            self.ids.swiper.remove_widget(widget)
        return super().on_leave(*args)

    def add_new(self):
        self.ids.swiper.add_widget(next(self.itemGenerator))
        # print(num)

    def swipe(self):
        num = self.ids.swiper.get_current_index()
        # print(num)
        if num > 3:
            self.ids.swiper.set_current(3)
            for i in range(num - 3):
                self.ids.swiper.remove_widget(self.ids.swiper.get_items()[0])
                self.add_new()
