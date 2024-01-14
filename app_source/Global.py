'''
Define a variable from storing values that will be accessed globally
If you want to share the values in different py files, 
you can put them in appData
e.g. exmample.py:
from Global import appData
appData.num = 100  
'''


class AppData:
    @staticmethod
    def hex2rgb(str):
        r = int(str[0:2], 16)/256
        g = int(str[2:4], 16)/256
        b = int(str[4:6], 16)/256
        return (r, g, b)

    @staticmethod
    def change_theme():
        appData.app.change_theme(appData.theme_key)

    @staticmethod
    def upload(name: str, file: str):
        blob = appData.sb.blob(
            'little_love_letter/app/'+name+'.'+file.split('.')[1])
        blob.upload_from_filename(file)
        blob.make_public()
        return blob.public_url


# The global variable
appData = AppData()
appData.colors = {
    "default": {
        "text": "111111",
        "button": "cca4e3",
        "icon": "56004f",
        "bg": "e4c6d0",
        "label": "3d3b4f"
    },
    "spring": {
        "text": "000000",
        "button": "9ed048",
        "icon": "0c8918",
        "bg": "eedeb0",
        "label": "f05654"
    },
    "dark": {
        "text": "EEEEEE",
        "button": "41555d",
        "icon": "c0ebd7",
        "bg": "161823",
        "label": "CCCCCC"
    },
}
appData.theme = appData.colors['default']
appData.theme_key = 'default'
