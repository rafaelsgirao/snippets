#pip install pyperclip win10toast
import pyperclip as clip
from time import sleep
#from win10toast import ToastNotifier
#from pynput.keyboard import Key, Listener, Controller
#from win32gui import GetWindowText, GetForegroundWindow
import os
evil_char = "\u200d"
i=0

def get_active_window():
    cmd = r"""id=$(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}') && name=$(xprop -id $id | awk '/_NET_WM_NAME/{$1=$2="";print}' | cut -d'"' -f2) && echo "$name"
"""
    return os.popen(cmd).read()

print("Running.")
while True: 
    #if "Discord" in GetWindowText(GetForegroundWindow()) (windows only):
    print(get_active_window())
    if "Discord" in get_active_window():
        orig_data = clip.paste()
        if evil_char not in orig_data:
            data = orig_data[:-1] + evil_char * int(2000-len(orig_data)) + \
                orig_data[-1]
            clip.copy(data)
            print(data)
            i+=1
            print("Changed {} . Total this session: {}".format(orig_data, i))
            os.system("notify-send Clipboard changed.")
    sleep(0.5)
