import random
import json
import os
logindex =0
logging=False
def log(logitm):
	global logindex
	global logging
	if logging:
		filepath="todlog.txt"
		if os.path.exists(filepath):
			mode="a"	
		else:
			mode="w"
		with open(filepath,mode) as f:
			f.write("%s log: %s\r\n"%(logindex,json.dumps(jsoncrunch(logitm))))
			f.close()
		logindex+=1
def jsoncrunch(item):
	try:
		json.dumps(item)
		return item
	except:
		if type(item) is list:
			return [jsoncrunch(x) for x in item]
		elif type(item) is dict:
			itmdic={}
			for k in item.keys():
				itmdic[k]=jsoncrunch(item[k])
			return itmdic
		else:
			return jsoncrunch(item.__dict__)


class truthdarecard(object):
	def clone(self):
		card = truthdarecard(self.aplicablegenders)
		card.__dict__.update(self.__dict__)
		log(card.aplicablegenders)
		return card
	def __init__(self,genders):
		log(genders)
		assert type(genders) is list
		self.targetno=1
		self.question="/p0 default question"
		self.points=100
		self.aplicablegenders=genders
		self.themes=[]
		log(self)
	def formatquestion(self):
		log(self)
		assert self.__dict__.get("affectedplayers") !=	None
		assert len(self.affectedplayers)==self.targetno
		responce =self.question
		for i in range(self.targetno):
			responce=responce.replace("/p"+str(i),self.affectedplayers[i])
		responce+="\r\nvalue: "+str(self.points)+"\r\n"
		log(self)
		return responce
	def __str__(self):
		if  self.__dict__.get("affectedplayers") ==None:
			return self.question
		else:
			return self.formatquestion
		__repr__=__str__
class player(object):
	def __str__(self):
		return self.name
	@staticmethod
	def getgenders():
		return ["m","f"]
	def __init__(self,name):
		self.forfits=[]
		self.name=name
		self.score=0
		self.carddeck=[]
		self.gender=player.getgenders()[0]
		self.maxforfits=3
		log(self)
	def freeforfitspace(self):
		length = len(self.forfits)
		if length<self.maxforfits:
			return True
		elif length==self.maxforfits:
			assert not (length>self.maxforfits)
			return False
	def switchforfit(self,card,forfitindex):
		log(self)
		log(card)
		log(forfitindex)
		assert forfitindex>=0
		assert forfitindex<=self.maxforfits
		assert type(card) is truthdarecard
		assert forfitindex<len(self.forfits)
		_forfit=self.forfits[forfitindex]
		self.forfits[forfitindex]=card
		log(self)
		log(_forfit)
		return _forfit
	def drawcard(self):
		log("drawcard")
		log(self)
		assert len(self.carddeck)!=0
		return self.carddeck.pop()
	def shuffle(self):
		random.shuffle(self.carddeck)
class gamecore(object):
	def __init__(self,arg):
		self.arg=arg
		self.allcards=self.loadcards()
		if len(self.allcards)==0:
			input()
			exit()
		self.players=self.setupplayers()
	def loadfromjson(self,jtext):
		raw =json.loads(jtext)
		formattedcards=[]
		for card_dict in raw:
			card =truthdarecard(player.getgenders())
			card.__dict__.update(card_dict)
			formattedcards.append(card)
		return formattedcards

	def loadcards(self):
		folder="cards"
		if not os.path.isdir(folder):
			os.makedirs(folder)
			with open(folder+"/readme.txt", "w") as f:
				f.write('''save json card packs in here with the structure:\r\n[{"targetno": 2, "points": 100, "themes": [], "question": "/p0 /p1 are in this one", "aplicablegenders": ["m", "f"]}, 
{"targetno": 1, "points": 100, "themes": [], "question": "/p0 is the only player in this question and for girls only", "aplicablegenders": ["f"]}]''')
				f.close()
			with open(folder+"/default.json","w") as f:
				f.write('''[{"targetno": 1, "points": 10, "themes": [], "question": "truth: /p0 what is your first memory?", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Truth: /p0 Who was your first crush, or who is your current crush?", "aplicablegenders": ["m","f"]},{"targetno": 2, "points": 100, "themes": [], "question": "Truth: /p0 What were your first impressions of /p1", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Truth: /p0 Have you ever had a crush on anyone here?", "aplicablegenders": ["m","f"]},{"targetno": 2, "points": 100, "themes": [], "question": "Truth: /p0 If you could be a superhero, what would your power be? and would /p1 be a side kick or villan", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Truth: /p0 What would you do if you were invisible for a day?", "aplicablegenders": ["m","f"]},{"targetno": 2, "points": 100, "themes": [], "question": "Dare: /p0 Exchange shirts with /p1 for the next round of questions.", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Dare: /p0 Sing instead of speaking for the next two rounds of the game.", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Dare: /p0 Run around the room imitating a monkey.", "aplicablegenders": ["m","f"]},{"targetno": 2, "points": 100, "themes": [], "question": "Dare: /p0 you must do everything /p1 asks for the next round", "aplicablegenders": ["m","f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Truth: /p0 what would you do if you where a man for the day?", "aplicablegenders": ["f"]},{"targetno": 1, "points": 100, "themes": [], "question": "Truth: /p0 have you ever looked at someone else while using a public toilet?", "aplicablegenders": ["m"]}]''')
				f.close()
		cardpacks= [folder+"/"+txtname for txtname in os.listdir(folder) if ".json" in txtname]
		cards=[]
		if len(cardpacks)==0:
			print("no card packs found")
			return cards
		for pack in cardpacks:
			with open(pack) as f:
				cards+=self.loadfromjson(f.read())
				f.close()
		return cards
	def setupplayers(self):
		self.screenrefresh()
		invalidplayersetup=True
		_playerlist=[]
		while invalidplayersetup:
			print("player%s's name?"%str(len(_playerlist)+1))
			name=""
			while name=="":
				name=input()
			currentplayer=player(name)
			print("what is your gender?")
			for i in player.getgenders():
				print(str(player.getgenders().index(i)+1)+": "+i)
			_action=self.getaction(len(player.getgenders()))-1
			self.screenrefresh()
			currentplayer.gender=player.getgenders()[_action]
			_playerlist.append(currentplayer)
			if len(_playerlist)>=2:
				print("1: add another?")
				print("2: im done adding.")
				_action=self.getaction(2)
				if _action==2:
					invalidplayersetup=False
		for _player in _playerlist:
			_deck=[x.clone() for x in self.allcards if _player.gender in x.aplicablegenders and len(_playerlist)>= x.targetno]
			random.shuffle(_deck)
			_player.carddeck=_deck
		return _playerlist
	def screenrefresh(self):
		if not self.arg.get("debug"):
			os.system('cls' if os.name == 'nt' else 'clear')
	def drawplayercard(self,currentplayer):
		invalidcard=True
		while invalidcard:
			if len(currentplayer.carddeck)==0:
				invalidcard=False
				card=None
			else:
				card = currentplayer.drawcard()
				if card.targetno<=len(self.players):
					invalidcard=False
		return card
	def start(self):
		assert len(self.players)>1
		self.screenrefresh()
		active= True
		random.shuffle(self.players)
		playersturn=0;
		while active:
			player_index=playersturn%len(self.players)
			currentplayer=self.players[player_index]
			card = self.drawplayercard(currentplayer)
			if card != None:
				targetplayers=[currentplayer.name]+random.sample([x.name for x in self.players if x!=currentplayer],card.targetno-1)
				card.affectedplayers=targetplayers
				print("%s your card is:"%currentplayer.name)
				print(card.formatquestion())
				print("1: view forfits")
				print("2: I did it")
				if currentplayer.freeforfitspace():
					print("3: make it a forfit")
				else:
					print("3: I'll do a forfit insted")
				action= self.getaction(3)
				self.screenrefresh()
				if action ==1:
					print(currentplayer.name+" your forfits are:")
					print("\r\n".join([x.formatquestion() for x in currentplayer.forfits]))
					print("the current card is:\r\n%s"%card.formatquestion())
					print("1: I did it")
					if currentplayer.freeforfitspace():
						print("2: make it a forfit")
					else:
						print("2: I'll do a forfit insted")
					action= self.getaction(2)+1
					self.screenrefresh()
				if action ==2:
					currentplayer.score+=card.points
				if action==3:
					if currentplayer.freeforfitspace():
						currentplayer.forfits.append(card)
					else:
						print("you'll need to swap it")
						for c in currentplayer.forfits:
							print(str(currentplayer.forfits.index(c)+1)+":"+c.formatquestion())
						_action=self.getaction(len(currentplayer.forfits))-1
						newcard=currentplayer.switchforfit(card,_action)
						print(newcard.formatquestion())
						print("1: I did it")
						print("2: i lose")
						_action=self.getaction(2)
						self.screenrefresh()
						if _action==2:
							print("player %s is out"%currentplayer.name)
							self.players.remove(currentplayer)
							if len(self.players)==1:
								print("the winner is %s"%self.players[0])
								active=False
				playersturn+=1
			else:
				active=False
	def getaction(self,maxval):
		invalidinput=True
		while invalidinput:
			valin=input("action: ")
			try:
				if int(valin)<=maxval and int(valin)>0:
					invalidinput=False
			except:
				pass
		return int(valin)
if __name__ == "__main__":
	arg ={"debug":False,"logging":False}
	logging=arg.get("logging")
	_gamecore=gamecore(arg)
	_gamecore.start()
			




