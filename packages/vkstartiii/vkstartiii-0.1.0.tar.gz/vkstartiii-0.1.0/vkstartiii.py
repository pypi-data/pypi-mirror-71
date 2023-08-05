import requests, vk_api, re, random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
def smsk(ui,message):
    global keyboard
    vk.messages.send(
        peer_id=ui,
        random_id=0,
        keyboard=keyboard.get_keyboard(),
        message=message
    )

def keyboard_set(ot, i):
    global keyboard
    keyboard = VkKeyboard(one_time=ot, inline=i)

def gk(t):
    keyboard.add_button(t, color=VkKeyboardColor.POSITIVE)
def rk(t):
    keyboard.add_button(t, color=VkKeyboardColor.NEGATIVE)
def bk(t):
    keyboard.add_button(t, color=VkKeyboardColor.PRIMARY)
def wk(t):
    keyboard.add_button(t, color=VkKeyboardColor.DEFAULT)
def nsk():
    keyboard.add_line()
def red(c,m):
    pattern="r"+'"'+c+'"'
    pattern=eval(pattern)
    string=re.sub(pattern,"",m)
    return(string)