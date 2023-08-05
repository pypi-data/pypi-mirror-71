import requests, vk_api, re, random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

class vkstarti:
	def __init__( self, token ):
		self.token = token
		vk = vk = vk_api.VkApi(token=token)
		
		vk = vk.get_api()
	def smsk(ui,message):
		try:
		    global keyboard
		    vk.messages.send(
		        peer_id=ui,
		        random_id=0,
		        keyboard=keyboard.get_keyboard(),
		        message=message
		    )
		except:
			raise NotReg("Возможно вы не вставили токен")
	def longpoll(self):
     self.longpoll = longpoll = VkLongPoll(vk)
     return self.longpoll
	def keyboard_set(self, ot, i):
	    global keyboard
	    keyboard = VkKeyboard(one_time=ot, inline=i)
	
	def gk(self,t):
	    keyboard.add_button( t, color=VkKeyboardColor.POSITIVE)
	def rk(self, t):
	    keyboard.add_button(t, color=VkKeyboardColor.NEGATIVE)
	def bk(self, t):
	    keyboard.add_button(t, color=VkKeyboardColor.PRIMARY)
	def wk(self, t):
	    keyboard.add_button(t, color=VkKeyboardColor.DEFAULT)
	def nsk(self):
	    keyboard.add_line()
	def red(self, c,m):
	    pattern="r"+'"'+c+'"'
	    pattern=eval(pattern)
	    string=re.sub(pattern,"",m)
	    return(string)
