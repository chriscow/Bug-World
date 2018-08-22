
# pygamehelper.py -- written by Andrej Karpathy

import pygame
from pygame.locals import *

from display import AbstractDisplay, DisplayEvents

#helper that draws an array arr on screen in steps of step pixels
def drawGraph(screen, arr, step=5):
	maxy = screen.get_height()
	for i in range(len(arr)-1):
		x = i*step
		p1 = (i*step, maxy-arr[i])
		p2 = ((i+1)*step, maxy-arr[i+1])
		pygame.draw.line(screen, (0,0,0), p1, p2)


class PygameHelper(AbstractDisplay):

	def __init__(self, size=(640,480), fill=(255,255,255)):
		super().__init__()
		pygame.init()
		self.screen = pygame.display.set_mode(size)
		self.screen.fill(fill)
		pygame.display.flip()
		self.running = False
		self.clock = pygame.time.Clock() #to track FPS
		self.size = size

	#
	# Publisher Implementation
	#
	def register(self, event, who, callback=None):
		super().register(event, who, callback)

	def unregister(self, event, who):
		super().unregister(event, who)

	def handleEvents(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False

			elif event.type == KEYDOWN:
				self.publisher.dispatch(DisplayEvents.KEYDOWN, source=self, key=event.key)

			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					self.running = False
				self.publisher.dispatch(DisplayEvents.KEYUP, source=self, key=event.key)

			elif event.type == MOUSEBUTTONUP:
				self.publisher.dispatch(DisplayEvents.MOUSEUP, source=self, button=event.button, pos=event.pos)


	#wait until a key is pressed, then return
	def waitForKey(self):
		press=False
		while not press:
			for event in pygame.event.get():
				if event.type == KEYUP:
					press = True

	#enter the main loop, possibly setting max FPS
	def run(self, fps=60):
		self.running = True

		while self.running:
			pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
			self.handleEvents()
			self.publisher.dispatch(DisplayEvents.UPDATE, self, self.screen)
			self.clock.tick(fps)
