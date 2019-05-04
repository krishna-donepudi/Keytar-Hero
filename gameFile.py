#master file for the game
#draws, moves, and does all the operations


import pygame, os, sys, math, time, random
from pygame.locals import *
from readLeaderboard import makeLeaderboard
import songAnalysis
from gameObjects import Target, Button
from record import record

#draws surface1 onto surface2 with center at position
def drawCentered(surface1, surface2, position):
	width = surface1.get_width()
	height = surface1.get_height()
	xCoord = position[0] - width//2
	yCoord = position[1] - height//2
	surface2.blit(surface1, (xCoord, yCoord))

#returns the center coordinates of an image
def getCenter(x, y, width, height):
	return (x + width//2, y + height//2)

#returns the distance between to points
def distance(x1, y1, x2, y2):
	return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

#class of the full game
class Game(object):
	#initializes the variables required for the game
	def __init__(self):
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
		self.pauseFont = pygame.font.SysFont('Comic Sans MS', 100)
		pygame.init() #initializes pygame and its mixer
		pygame.mixer.init()
		self.window = pygame.display.set_mode((800, 800))
		self.clock = pygame.time.Clock() 
		pygame.display.set_caption("Keytar Hero")
		self.timeStep = 100
		self.timeSum = 0
		self.endTime = 0
		self.recordSong = "recorded song"
		self.recordTime = "20"
		self.difficulty = None
		self.introbg = pygame.image.load(os.path.join('images', 
			'introbg.jpg')).convert_alpha()
		self.introtext = pygame.image.load(os.path.join('images', 
			'introtext.png')).convert_alpha()
		self.playtext = pygame.image.load(os.path.join('images', 
			'playtext.png')).convert_alpha()
		self.helptext = pygame.image.load(os.path.join('images', 
			'helptext.png')).convert_alpha()
		self.leaderboardtext = pygame.image.load(os.path.join('images', 
			'leaderboardtext.png')).convert_alpha()
		self.bg = pygame.image.load(os.path.join('images', 
			'bg.png')).convert_alpha()
		self.difficultyImage = pygame.image.load(os.path.join('images',
			'difficulty.png')).convert_alpha()
		self.help = pygame.image.load(os.path.join('images', 
			'helpscreen.png')).convert_alpha()
		self.width = self.bg.get_width()
		self.height = self.bg.get_height()
		self.input = ""
		self.inputActive = False
		self.buttons = []
		self.targets = []
		self.targets0 = []
		self.targets1 = []
		self.targets2 = []
		self.targets3 = []
		self.button0 = None
		self.button1 = None
		self.button2 = None
		self.button3 = None
		self.combo = 0
		self.button0image = pygame.image.load(os.path.join("images", 
			"button0.png")).convert_alpha()
		self.button1image = pygame.image.load(os.path.join("images", 
			"button0.png")).convert_alpha()
		self.button2image = pygame.image.load(os.path.join("images", 
			"button0.png")).convert_alpha()
		self.button3image = pygame.image.load(os.path.join("images", 
			"button0.png")).convert_alpha()
		self.score = 0
		self.misses = 0
		self.paused = False
		self.comboBool = True
		self.target0 = pygame.image.load(os.path.join("images", 
			"target0.png")).convert_alpha()
		self.target1 = pygame.image.load(os.path.join("images", 
			"target1.png")).convert_alpha()
		self.target2 = pygame.image.load(os.path.join("images", 
			"target2.png")).convert_alpha()
		self.target3 = pygame.image.load(os.path.join("images", 
			"target3.png")).convert_alpha()
		self.target0yellow = pygame.image.load(os.path.join("images", 
			"target0yellow.png")).convert_alpha()
		self.target1yellow = pygame.image.load(os.path.join("images", 
			"target1yellow.png")).convert_alpha()
		self.target2yellow = pygame.image.load(os.path.join("images", 
			"target2yellow.png")).convert_alpha()
		self.target3yellow = pygame.image.load(os.path.join("images", 
			"target3yellow.png")).convert_alpha()
		self.target0green = pygame.image.load(os.path.join("images", 
			"target0green.png")).convert_alpha()
		self.target1green = pygame.image.load(os.path.join("images", 
			"target1green.png")).convert_alpha()
		self.target2green = pygame.image.load(os.path.join("images", 
			"target2green.png")).convert_alpha()
		self.target3green = pygame.image.load(os.path.join("images", 
			"target3green.png")).convert_alpha()
		self.recordButton = pygame.image.load(os.path.join("images",
			"recordButton.png")).convert_alpha()
		self.intro = True
		self.username = ""
		self.userActive = False
		self.recordLengthActive = False
		self.recordActive = False
		Game.startScreen(self)

	#returns a button of the right index
	def makeButton(self, num, image):
		return Button(num, self.width, self.height, image)

	#draws the game over screen and displays the results
	def gameOver(self):
		self.endTime += self.timeStep
		#checks if time is over for the game and draws the game
		if self.endTime > self.lastBeat + 1200:
			while True:
				self.window.blit(self.introbg, (0, 0))
				if (self.score - 5 * self.misses) <= 0:
					totalScore = str(0)
				else:
					totalScore = str(self.score - 5 * self.misses)
				gameEndImage = pygame.image.load(os.path.join("images", 
					"gameOver.png"))
				resultText = self.pauseFont.render("Results:",\
				False, (255, 255, 255))
				rawScoreText = self.myfont.render("Raw Score: " + \
					str(self.score), False, (255, 255, 255))
				missesText = self.myfont.render("Misses: " + \
					str(self.misses), False, (255, 255, 255))
				totalScoreText = self.myfont.render("Total Score: " + \
					totalScore, False, (255, 255, 255))
				textBack = self.myfont.render("Back", False, (0, 0, 0))
				self.window.blit(textBack, (5, 5))
				drawCentered(gameEndImage, self.window, (self.width//2, 
					self.height//5))
				drawCentered(resultText, self.window, (self.width//2, 
					self.height//3))
				drawCentered(rawScoreText, self.window, (self.width//2, 
					self.height//2))
				drawCentered(missesText, self.window, (self.width//2, 
					self.height//2 + 60))
				drawCentered(totalScoreText, self.window, (self.width//2, 
					self.height//2 + 120))
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						#writes the score to the leaderboard
						file = open("leaderboard.txt", "a+")
						file.write(self.username + '\t' + str(self.score - \
							5 * self.misses) + '\n')
						file.close()
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						file = open("leaderboard.txt", "a+")
						file.write(self.username + '\t' + str(self.score - \
							5 * self.misses) + '\n')
						file.close()
						x, y = event.pos[0], event.pos[1]
						#checks if the click is on the back button
						if 5 < x < 5 + textBack.get_width() \
						and 5 < y < 5 + textBack.get_height():
							Game.__init__(self)
				self.clock.tick()
				pygame.display.update()

	#makes a target according to the pitch
	def makeTarget(self):
		num, speed = self.categories[0], self.speed
		if num == 0:
			image = self.target0
		elif num == 1:
			image = self.target1
		elif num == 2:
			image = self.target2
		elif num == 3:
			image = self.target3
		return Target(num, self.speed, self.height, self.width, image)

	#draws the window
	def drawWindow(self):
		self.window.blit(self.bg, (0, 0))
		for i in range(4):
			if i == 0:
				newButton = Game.makeButton(self, i, self.button0image)
				self.button0 = newButton
			elif i == 1:
				newButton = Game.makeButton(self, i, self.button1image)
				self.button1 = newButton
			elif i == 2:
				newButton = Game.makeButton(self, i, self.button2image)
				self.button2 = newButton
			elif i == 3:
				newButton = Game.makeButton(self, i, self.button3image)
				self.button3 = newButton
			newButton.draw(self.window)
			self.buttons.append(newButton)

	#draws the targets
	def drawTargets(self):
		for target in self.targets:
			target.draw(self.window)

	#moves the targets down
	def moveTargets(self):
		for target in self.targets:
			target.drop(self.timeStep)

	#removes the target from self.targets if the target goes off screen
	def removeTargets(self):
		for target in self.targets:
			if target.y > self.height:
				self.targets.remove(target)
				if not target.seen:
					self.combo = 0
					self.misses += 1

	#creates a target according to the beat and the pitch
	def createTarget(self):
		if not self.paused:
			self.timeSum += self.timeStep*1000
			if self.beats == []:
				Game.gameOver(self)
			elif self.timeSum + 5500 > self.beats[0]:
				target = Game.makeTarget(self)
				self.targets.append(target)
				if target.num == 0:
					self.targets0.append(target)
				elif target.num == 1:
					self.targets1.append(target)
				elif target.num == 2:
					self.targets2.append(target)
				elif target.num == 3:
					self.targets3.append(target)
				self.categories.pop(0)
				self.beats.pop(0)
				if self.beats == []:
						Game.gameOver(self)
				#every third beat in easy mode
				if self.difficulty == "easy" and len(self.beats) >= 3:
					self.categories.pop(0)
					self.beats.pop(0)
					self.categories.pop(0)
					self.categories.pop(0)
					self.beats.pop(0)
					self.beats.pop(0)
				#every other beat for medium mode
				elif self.difficulty == "medium" and len(self.beats) >= 2:
					self.categories.pop(0)
					self.beats.pop(0)
					self.categories.pop(0)
					self.beats.pop(0)
				#every beat for hard difficulty
				elif self.difficulty == "hard" and len(self.beats) >= 1:
					self.categories.pop(0)
					self.beats.pop(0)

	#checks if the targets are over the buttons
	def checkHits(self, target, button):
		x1, y1 = getCenter(target.x, target.y, target.image.get_width(),
			target.image.get_height())
		x2, y2 = getCenter(button.x, button.y, button.image.get_width(),
			button.image.get_height())
		#orange color targets for perfection
		if distance(x1, y1, x2, y2) < 15 and not target.seen:
			self.score += 10
			target.seen = True
			if target.num == 0:
				image = self.target0green
			elif target.num == 1:
				image = self.target1green
			elif target.num == 2:
				image = self.target2green
			elif target.num == 3:
				image = self.target3green
			target.image = image
			self.combo += 1
			return True
		#yellow color targets for perfection
		elif distance(x1, y1, x2, y2) < 40 and not target.seen:
			self.score += 5
			target.seen = True
			if target.num == 0:
				image = self.target0yellow
			elif target.num == 1:
				image = self.target1yellow
			elif target.num == 2:
				image = self.target2yellow
			elif target.num == 3:
				image = self.target3yellow
			target.image = image
			return True
		return False

	#checks for when the arrow keys are pressed
	def checkCollisions(self, pressed):
		if pressed == pygame.K_LEFT:
			for target in self.targets0:
				if Game.checkHits(self, target, self.button0):
					return
			self.combo = 0
			if self.score > 0:
				self.score -= 10
			self.misses += 1
		elif pressed == pygame.K_UP:
			for target in self.targets1:
				if Game.checkHits(self, target, self.button1):
					return
			self.combo = 0
			if self.score > 0:
				self.score -= 10
			self.misses += 1
		elif pressed == pygame.K_DOWN:
			for target in self.targets2:
				if Game.checkHits(self, target, self.button2):
					return
			self.combo = 0
			if self.score > 0:
				self.score -= 10
			self.misses += 1
		elif pressed == pygame.K_RIGHT:
			for target in self.targets3:
				if Game.checkHits(self, target, self.button3):
					return
			self.combo = 0
			self.misses += 1

	#draws the score
	def drawScore(self):
		textScore = self.myfont.render("Score: " + str(self.score),\
			False, (255, 255, 255))
		self.window.blit(textScore, (5, 5))

	#draws the combo count
	def drawCombos(self):
		textCombos = self.myfont.render("Combo: " + str(self.combo), \
			False, (255, 255, 255))
		self.window.blit(textCombos, (5, 55))

	#draws the misses
	def drawMisses(self):
		textMisses = self.myfont.render("Misses: " + str(self.misses), \
			False, (255, 255, 255))
		self.window.blit(textMisses, (self.bg.get_width() - \
			self.bg.get_width()/4, 5))

	#draws the paused text if paused
	def drawPaused(self):
		self.textPaused = self.pauseFont.render("Paused", False, (100, 255, 125))
		self.textExit = self.myfont.render("Exit", False, (255, 0, 0))
		drawCentered(self.textExit, self.window, (self.bg.get_width()//2,\
			self.bg.get_height()//2 + self.textPaused.get_height()))
		drawCentered(self.textPaused, self.window, (self.bg.get_width()//2,\
			self.bg.get_height()//2))
			
	#calculates the combo and adds to the points total
	def checkCombo(self):
		if self.combo == 20:
			self.score += self.combo*5
			self.combo = 0
		elif self.combo == 15 and self.comboBool:
			self.score += self.combo*5
			self.comboBool = False
		elif self.combo == 10 and not self.comboBool:
			self.score += self.combo*5
			self.comboBool = True
		elif self.combo == 5 and self.comboBool:
			self.score += self.combo*5
			self.comboBool = False

	#checks the song exists in the directory
	def checkSong(self):
		if os.path.isfile(os.path.join("songs", self.song + ".wav")):
			return True
		return False

	#game difficulty screen
	def gameDifficulty(self):
		while True:
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			self.window.blit(textBack, (5, 5))
			self.window.blit(self.introbg, (0, 0))
			drawCentered(self.difficultyImage, self.window, 
				(self.width//2, self.height//5))
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			self.window.blit(textBack, (5, 5))
			textEasy = self.myfont.render("Easy", False, (255, 255, 255))
			textMedium = self.myfont.render("Medium", False, (255, 255, 255))
			textHard = self.myfont.render("Impossible", False, (255, 255, 255))
			easyWidth = textEasy.get_width()
			easyHeight = textEasy.get_height()
			mediumWidth = textMedium.get_width()
			mediumHeight = textMedium.get_height()
			hardWidth = textHard.get_width()
			hardHeight = textHard.get_height()
			drawCentered(textEasy, self.window, 
				(self.width//2, 2*self.height//3))
			drawCentered(textMedium, self.window,
				(self.width//2, 2*self.height//3 + 60))
			drawCentered(textHard, self.window,
				(self.width//2, 2*self.height//3 + 120))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					#runs in easy mode
					if self.width//2 - easyWidth/2 < x < self.width//2 + \
					easyWidth/2 and 2*self.height//3 - easyHeight/2 < y < \
					2*self.height//3 + easyHeight/2:
						self.difficulty = "easy"
						Game.run(self)
					#runs in medium mode
					if self.width//2 - mediumWidth/2 < x < self.width//2 + \
					mediumWidth/2 and 2*self.height//3 + 60 \
					- mediumHeight < y < 2*self.height//3 + 60 + mediumHeight:
						self.difficulty = "medium"
						Game.run(self)
					#runs in hard mode
					if self.width//2 - hardWidth/2 < x < self.width//2 + \
					hardWidth/2 and 2*self.height//3 + 120 \
					- hardHeight < y < 2*self.height//3 + 120 + hardHeight:
						self.difficulty = "hard"
						Game.run(self)
					#goes back
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						Game.selectSong(self)
			self.clock.tick()
			pygame.display.update()

	#help screen
	def helpScreen(self):
		while True:
			self.window.blit(self.introbg, (0, 0))
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			drawCentered(self.help, self.window, (self.width//2, \
				self.height//2))
			self.window.blit(textBack, (5, 5))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					#check to go back
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						Game.startScreen(self)
			self.clock.tick()
			pygame.display.update()

	#draws the record screen and calls record function if record button is
	#pressed
	def recordSong(self):
		while True:
			self.window.blit(self.introbg, (0, 0))
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			textRecordLength = self.myfont.render(\
				"Enter your recording length in seconds",
				False, (255, 255, 255))
			textRecordName = self.myfont.render(\
				"Enter the name of your recording",
				False, (255, 255, 255))
			self.window.blit(self.recordButton, 
				(self.width//2 - 62, self.height - 150))
			length = self.myfont.render(self.recordTime, False, (0, 255, 0))
			name = self.myfont.render(self.recordSong, False, (0, 255, 0))
			self.window.blit(textBack, (5, 5))
			if self.recordLengthActive:
				pygame.draw.rect(self.window, (0, 0, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			else:
				pygame.draw.rect(self.window, (255, 255, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			drawCentered(textRecordLength, self.window, (self.width//2,
				2*self.height//3+25+textRecordLength.get_height()//2))
			if self.recordActive:
				pygame.draw.rect(self.window, (0, 0, 255),
					(self.width//2-150, self.height//3-25, 300, 50))
			else:
				pygame.draw.rect(self.window, (255, 255, 255),
					(self.width//2-150, self.height//3-25, 300, 50))
			drawCentered(textRecordName, self.window, (self.width//2,
				self.height//3+25+textRecordLength.get_height()//2))
			drawCentered(length, self.window, 
				(self.width//2, 2*self.height//3))
			drawCentered(name, self.window,
				(self.width//2, self.height//3))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						Game.selectSong(self)
					elif self.width//2-150 < x < self.width//2-150 + 300 and \
					2*self.height//3-25 < y < 2*self.height//3-25 + 50:
						self.recordLengthActive = not self.recordLengthActive
						if self.recordLengthActive:
							self.recordActive = False
					elif self.width//2-150 < x < self.width//2-150 + 300 and \
					self.height//3-25-25 < y < self.height//3-25 + 50:
						self.recordActive = not self.recordActive
						if self.recordActive:
							self.recordLengthActive = False
					elif self.width//2-62 < x < self.width//2+62 and \
					self.height - 150 < y < self.height - 25:
						record(self.recordSong, self.recordTime)
#logic from
#https://stackoverflow.com/questions/46390231/
#how-to-create-a-text-input-box-with-pygame
				if event.type == pygame.KEYDOWN:
					if self.recordLengthActive:
						if event.key == pygame.K_RETURN:
							self.recordLengthActive = False
						elif event.key == pygame.K_BACKSPACE:
							self.recordTime = self.recordTime [:-1]
						else:
							self.recordTime += event.unicode
					if self.recordActive:
						if event.key == pygame.K_RETURN:
							self.recordActive = False
						elif event.key == pygame.K_BACKSPACE:
							self.recordSong = self.recordSong [:-1]
						else:
							self.recordSong += event.unicode
			self.clock.tick()
			pygame.display.update()

	#song select screen
	def selectSong(self):
		while True:
			self.window.blit(self.introbg, (0, 0))
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			inputText = self.myfont.render(self.input, False, 
				(0, 255, 0))
			textPrompt = self.myfont.render(\
				"Please click and enter the song you want to play", 
				False, (255, 255, 255))
			textRecord = self.pauseFont.render("Record your own song",
				False, (255, 255, 255))
			recordWidth = textRecord.get_width()
			recordHeight = textRecord.get_height()
			self.window.blit(textBack, (5, 5))
			if self.inputActive:
				pygame.draw.rect(self.window, (0, 0, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			else:
				pygame.draw.rect(self.window, (255, 255, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			drawCentered(textRecord, self.window, (self.width//2, 
				7*self.height//8))
			drawCentered(self.playtext, self.window, 
				(self.width//2, self.height//5))
			drawCentered(textPrompt, self.window, 
				(self.width//2, 2*self.height//3 + 75))
			drawCentered(inputText, self.window, 
				(self.width//2, 2*self.height//3))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						self.input = ""
						Game.signIn(self)
					elif self.width//2-150 < x < self.width//2-150 + 300 and \
					2*self.height//3-25 < y < 2*self.height//3-25 + 50:
						self.inputActive = not self.inputActive
					elif self.width//2 - recordWidth//2 < x < self.width//2 + \
					recordWidth//2 and 7*self.height//8 - recordHeight//2 < y \
					< 7*self.height//8 + recordHeight//2:
						Game.recordSong(self)
#logic from
#https://stackoverflow.com/questions/46390231/
#how-to-create-a-text-input-box-with-pygame
				if event.type == pygame.KEYDOWN:
					if self.inputActive:
						if event.key == pygame.K_RETURN:
							self.song = self.input
							#goes to the difficulty screen
							if Game.checkSong(self):
								songAnalysis.createBeats(self.song)
								songAnalysis.createPitches(self.song)
								songAnalysis.createBPM(self.song)
								Game.gameDifficulty(self)
							self.input = ""
							self.song = ""
							Game.selectSong(self)
						elif event.key == pygame.K_BACKSPACE:
							self.input = self.input [:-1]
						else:
							self.input += event.unicode
			self.clock.tick()
			pygame.display.update()

	def signIn(self):
		while True:
			self.window.blit(self.introbg, (0, 0))
			textPrompt = self.myfont.render(\
				"Please click and enter your username", 
				False, (255, 255, 255))
			textBack = self.myfont.render("Back", False, (0, 0, 0))
			inputText = self.myfont.render(self.username, False, 
				(0, 255, 0))
			self.window.blit(textBack, (5, 5))
			drawCentered(textPrompt, self.window, 
				(self.width//2, 2*self.height//3 + 75))
			if self.userActive:
				pygame.draw.rect(self.window, (0, 0, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			else:
				pygame.draw.rect(self.window, (255, 255, 255),
					(self.width//2-150, 2*self.height//3-25, 300, 50))
			drawCentered(inputText, self.window, 
				(self.width//2, 2*self.height//3))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						self.username = ""
						Game.startScreen(self)
					if self.width//2-150 < x < self.width//2-150 + 300 and \
					2*self.height//3-25 < y < 2*self.height//3-25 + 50:
						self.userActive = not self.userActive
#logic from
#https://stackoverflow.com/questions/46390231/
#how-to-create-a-text-input-box-with-pygame
				if event.type == pygame.KEYDOWN:
					if self.userActive:
						if event.key == pygame.K_RETURN:
							Game.selectSong(self)
						elif event.key == pygame.K_BACKSPACE:
							self.username = self.username[:-1]
						else:
							self.username += event.unicode
				self.clock.tick()
				pygame.display.update()

	#draws the leaderboard screen
	def leaderboardScreen(self):
		while True:
			self.window.blit(self.bg, (0, 0))
			textBack = self.myfont.render("Back", False, (100, 230, 78))
			self.window.blit(textBack, (5, 5))
			drawCentered(self.leaderboardtext, self.window, 
				(self.width//2, self.height//5))
			leaders = makeLeaderboard("leaderboard.txt")
			leader1, score1 = leaders[0]
			leader2, score2 = leaders[1]
			leader3, score3 = leaders[2]
			leader4, score4 = leaders[3]
			leader1Text = self.pauseFont.render("1. " + \
				leader1, False, (255, 255, 255))
			score1Text = self.pauseFont.render(score1, False, (255, 255, 255))
			leader2Text = self.pauseFont.render("2. " + \
				leader2, False, (255, 255, 255))
			score2Text = self.pauseFont.render(score2, False, (255, 255, 255))
			leader3Text = self.pauseFont.render("3. " + \
				leader3, False, (255, 255, 255))
			score3Text = self.pauseFont.render(score3, False, (255, 255, 255))
			leader4Text = self.pauseFont.render("4. " + \
				leader4, False, (255, 255, 255))
			score4Text = self.pauseFont.render(score4, False, (255, 255, 255))
			height = leader1Text.get_height() + 20
			width = score1Text.get_width()
			self.window.blit(leader1Text, 
				(self.width//7 - 20, self.height//3))
			self.window.blit(leader2Text, 
				(self.width//7 - 20, self.height//3 + height))
			self.window.blit(leader3Text, 
				(self.width//7 - 20, self.height//3 + 2*height))
			self.window.blit(leader4Text, 
				(self.width//7 - 20, self.height//3 + 3*height))
			self.window.blit(score1Text, 
				(self.width - self.width//7 - 20 - width, self.height//3))
			self.window.blit(score2Text, 
				(self.width - self.width//7 - 20 - width, 
					self.height//3 + height))
			self.window.blit(score3Text, 
				(self.width - self.width//7 - 20 - width, 
					self.height//3 + 2*height))
			self.window.blit(score4Text, 
				(self.width - self.width//7 - 20 - width, 
					self.height//3 + 3*height))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					if 5 < x < 5 + textBack.get_width() \
					and 5 < y < 5 + textBack.get_height():
						Game.startScreen(self)
			self.clock.tick()
			pygame.display.update()

	#checks what button are presses in the intro
	def checkIntroButton(self, pos):
		x, y = pos
		playWidth = self.playtext.get_width()
		playHeight = self.playtext.get_height()
		helpWidth = self.helptext.get_width()
		helpHeight = self.helptext.get_height()
		leaderWidth = self.leaderboardtext.get_width()
		leaderHeight = self.leaderboardtext.get_height()
		if (self.width//3 - playWidth/2 < x < self.width//3 + playWidth/2)\
		and (2*self.height//3 - playHeight/2 < y < \
			2*self.height//3 + playHeight/2):
			self.intro = False
			Game.signIn(self)
		elif (2*self.width//3 - helpWidth/2 < x < \
			2*self.width//3 + helpWidth/2) and \
			(2*self.height//3 - 20 - helpHeight/2 < y < \
			2*self.height//3 - 20 + helpHeight/2):
			self.intro = False
			Game.helpScreen(self)
		elif (self.width//2 - leaderWidth/2 < x < self.width//2 + \
			leaderWidth/2) and (5*self.height//6 - leaderHeight/2 < y < \
			5*self.height//6 + leaderHeight/2):
			Game.leaderboardScreen(self)
			self.intro = False

	#draws the start sceen
	def startScreen(self):
		self.intro = True
		while self.intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					Game.checkIntroButton(self, event.pos)
			self.window.blit(self.introbg, (0, 0))
			drawCentered(self.introtext, self.window, 
				(self.width//2, self.height//5))
			drawCentered(self.playtext, self.window, 
				(self.width//3, 2*self.height//3))
			drawCentered(self.helptext, self.window, 
				(2*self.width//3, 2*self.height//3 - 20))
			drawCentered(self.leaderboardtext, self.window, 
				(self.width//2, 5*self.height//6))
			self.clock.tick()
			pygame.display.update()

	#removes the first beats that cannot reach the button in time
	def removeFirstBeats(self):
		i = 0
		while i < len(self.beats):
			if self.beats[i] < 5500:
				self.beats.pop(i)
				self.categories.pop(i)
			else:
				i += 1

	#removes the last beats so that no beats are created when the song is not
	#playing
	def removeLastBeats(self):
		lastBeat = self.beats[len(self.beats) - 1]
		self.lastBeat = lastBeat
		threshold = lastBeat + 5500
		i = len(self.beats) - 1
		while i > 0:
			if self.beats[i] > threshold:
				self.beats.pop(i)
				self.categories.pop(i)
			else:
				i -= 1

	#the main run function of the game
	def run(self):
		try:
			self.BPM = songAnalysis.readBPM("songs/BPM" + self.song + ".txt")
		except:
			self.BPM = 115 #default BPM
		self.speed = self.BPM
		try:
			self.categories = songAnalysis.buckets(self.song)
		except:
			print("your song was not defined well enough to analyse")
			Game.selectSong(self)
		self.beats = songAnalysis.readBeats("songs/beats" + self.song + ".txt")
		Game.removeFirstBeats(self)
		Game.removeLastBeats(self)
		pygame.mixer.music.load("songs/" + self.song + ".wav")
		pygame.mixer.music.play()
		while len(self.beats) >= 0:
			self.timeStep = self.clock.tick()
			if not self.paused:
				Game.gameOver(self)
			self.timeStep /= 1000
			Game.drawWindow(self)
			Game.drawTargets(self)
			if not self.paused:
				pygame.mixer.music.unpause()
				Game.createTarget(self)
				Game.moveTargets(self)
				Game.removeTargets(self)
				Game.checkCombo(self)
			if self.paused:
				pygame.mixer.music.pause()
				Game.drawPaused(self)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					if (self.score - 5 * self.misses) <= 0:
						totalScore = str(0)
					else:
						totalScore = str(self.score - 5 * self.misses)
					file = open("leaderboard.txt", "a+")
					file.write(self.username + '\t' + str(totalScore) + '\n')
					file.close()
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if not self.paused:
						Game.checkCollisions(self, event.key)
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos[0], event.pos[1]
					if  self.bg.get_width()//2 - self.textExit.get_width()//2\
					< x < self.bg.get_width()//2 + \
					self.textExit.get_width()//2 and self.bg.get_height()//2 + \
					self.textPaused.get_height() - \
					self.textExit.get_height()//2 < y < \
					self.bg.get_height()//2 + self.textPaused.get_height() + \
					self.textPaused.get_height()//2:
						Game.__init__(self)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.paused = not self.paused
			Game.drawScore(self)
			Game.drawMisses(self)
			Game.drawCombos(self)
			pygame.display.update()

Game().__init__()