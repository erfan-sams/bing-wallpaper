import requests, os, sys, subprocess, shutil
from ctypes import windll
from tkinter import Tk, messagebox
import re
from time import sleep
import schedule, threading

start_pc = 0
picture_name = ''

### set your registery to autorun after restart pc!
def become_persistent():

    try:
        prgram_path = os.environ['appdata'] + '\\bingo'
        file_location = prgram_path + '\\bing_wallpaper.exe'
        if not os.path.exists(file_location):
            os.mkdir(prgram_path)
            shutil.copyfile(sys.executable, file_location)
            subprocess.call(
                'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v bing-wallpaper /t REG_SZ /d "'
                + file_location + '"',
                shell=True)

    except Exception:
        root = Tk()
        root.withdraw()
        messagebox.showerror('error', 'please run with administrator permission!')
        # sys.exit()

""" after setup pc this mechanism run every minute and when success to connect api and
    get picture run every 15 miniute again and again
"""
def schedule_day():
    schedule.every(15).minutes.do(background_changer)
    global start_pc

    while True:
        if start_pc == 0:
            timer = threading.Timer(1.0, background_changer)
            timer.start()
            sleep(59)
        else:
            schedule.run_pending()
            sleep(1)



def get_url():
    try:
        global picture_name
        api = requests.get('https://bing.biturl.top')
        img_url = api.json()['url']
        picture_name = re.search(r'th\?id=OHR\.(.*)?_ZH', img_url).group(1)
        return img_url

    except Exception:
        pass


def download(url):
    global start_pc
    """set timer to finish download process"""
    try:
        img = requests.get(url)
        start_pc = 1
        return img
    except requests.ConnectionError:
        start_pc = 0
        pass

### change your wall in windows:)
def background_changer():
    global path
    path = os.path.join(os.path.expanduser('~'), 'Pictures', 'Bing_WallPaper')
    try:
        file_exist()
        img_url = get_url()
        new_file = path + '\\' + picture_name + '.jpg'
        if not os.path.exists(new_file):
            picture = download(img_url)
            if picture.ok:
                with open(new_file, 'wb') as file:
                    file.write(picture.content)

            windll.user32.SystemParametersInfoW(20, 0, new_file, 1)

    except Exception:
        pass

# check file path
def file_exist():
    if not os.path.exists(path=path):
        os.mkdir(path=path)


# def check_execute():
#     file_path = os.path.abspath(__file__).split('\\')[-1]
#     x = file_path.split('.')
#     reg = x[0] + '.exe'
#     binary_data = subprocess.run('tasklist | findstr /R -i "' + reg + '"', shell=True, stdout=subprocess.PIPE)
#     utf8 = binary_data.stdout.decode()
#     # if utf8.find('.exe') != -1:
#     #     print('uffff')
#     if '.exe' in utf8:
#         print('hast')
#     # index_num = utf8.find('.exe') + 4
#     # result = utf8[0:index_num]
#     print(utf8)
#     # print(file_path)
#     if reg.lower() == utf8.lower():
#         return True
#     return False

"""if program execute don't run it again Ok!"""
# if check_execute():

root = Tk()
root.withdraw()
messagebox.showinfo('Info', 'bing_wallpaper start running!')
# become_persistent()
schedule_day()
