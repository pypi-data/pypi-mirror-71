import threading,vk_api,re
from colorama import Fore
from vk_api.longpoll import VkLongPoll ,VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def red(c,m):
	pattern="r"+'"'+c+'"'
	pattern=eval(pattern)
	string=re.sub(pattern,"",m)
	return(string)

def num1(num1):
	num1=num1[::-1]
	b=0
	p=""
	for i in num1:
		if b==3:
			p+=","
			b=0
		p+=i
		b+=1
	p=p[::-1]
	return(p)

def potok(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper
  


class Bot:
	num=0
	def __init__(self,token):
		self.vk_s=vk_api.VkApi(token=token)
		self.longpoll=VkLongPoll(self.vk_s)
		self.vk=self.vk_s.get_api()
		self.name=Bot.num
		Bot.num+=1
		print("["+ Fore.BLUE  + "MyVkApi|" + str( self.name ) + Fore.WHITE+"] Hello world!")
	def on(self):
		for event in self.longpoll.listen():
			m=red("vkeventtype.",str(event.type).lower())
			print("[" + Fore.BLUE + "MyVkApi|" + str( self.name ) + Fore.WHITE +"] "+m)
			self.event=event
			return(event)
			
	#messages
	def sms(self,message,id="none"):
		if id=="none":
			id=self.event.peer_id
		self.vk.messages.send(peer_id=id,random_id=get_random_id(),message=message)

	def frendsadd(self,peer_id,text):
		self.vk.friends.add(peer_id=peer_id,text=text)

	def stik(self,ids,id="none"):
		if id == "none":
			id = self.event.peer_id
		self.vk.messages.send(peer_id=id,random_id=get_random_id(),sticker_id=ids)

	def sms_pin(self,peer_id,message_id):
		self.vk.messages.pin(peer_id=peer_id,message_id=message_id)
	
	def sms_unpin(self,peer_id):
		self.vk.messages.unpin(peer_id=peer_id)
		
	def sms_editChat(self,title,chat_id="none"):
		if chat_id=="none":
			chat_id=self.event.chat_id
		self.vk.messages.editChat(chat_id=chat_id,title=title)
	
	def sms_delete(self,id,for_all=0):
		self.vk.messages.delete(message_ids=id,delete_for_all=for_all)
		
	def sms_edit(self,text,peer_id="none",sms_id="none"):
		if peer_id=="none":
			peer_id=self.event.peer_id
		if sms_id=="none":
			sms_id=self.event.message_id
		self.vk.messages.edit(peer_id=peer_id,message=text,message_id=sms_id)
	
	def sms_ban(self,chat_id="none",member_id="none"):
		if chat_id=="none":
			chat_id=self.event.chat_id
		if member_id=="none":
			member_id=self.event.member_id
		self.vk.messages.removeChatUser(chat_id=chat_id,member_id=member_id)
	#Account
	def acc_ban(self,*id):
		if id==( ):
			id=[self.event.user_id]
		for i in id:
			self.vk.account.ban(owner_id=i)
			
	def acc_unban(self,*id):
		if id==( ):
			id=[self.event.user_id]
		for i in id:
			self.vk.account.unban(owner_id=i)
	


class Event:
	def __init__(self,event):
		self.event=event
	def message(self,message=True,lower=False,start=False):
		if self.event.type==VkEventType.MESSAGE_NEW:
			if message==True:
				return(True)
			if lower:self.event.text=self.event.text.lower()
			if start and self.event.text.startswith(message):
				return(True)
			elif self.event.text==message:
				return(True)
			else:
				return(False)