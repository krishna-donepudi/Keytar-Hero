#contains the objects in the game

import pygame

#class for the buttons in the game
class Button(object):
	def __init__(self, num, bgWidth, bgHeight, image):
		self.num = num
		self.image = pygame.image.load('images/button%d.png' % \
			num).convert_alpha()
		border = (bgWidth  - self.image.get_width() * 4)//2
		self.x, self.y = self.image.get_width() * num + border,\
			bgHeight - bgHeight/4
	#draws the button on the window
	def draw(self, window):
		window.blit(self.image, (self.x, self.y))

#class for the targets that fall as notes
class Target(object):
	def __init__(self, num, speed, bgWidth, bgHeight, image):
		self.num = num
		self.image = image
		border = (bgWidth  - self.image.get_width() * 4)//2
		self.x, self.y = self.image.get_width() * num + border, 0
		self.move = speed
		self.seen = False
	#draws the target on the window
	def draw(self, window):
		window.blit(self.image, (self.x, self.y))
	#drops the target down
	def drop(self,timeStep):
#Logic implemented from:
#https://gamedev.stackexchange.com/questions/48227/smooth-movement-pygame
		self.y += self.move*timeStep