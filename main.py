import pygame 
import os 
import pygame
import world
import display
import config
from helpers import Color
from pygame.locals import K_SPACE, K_LEFT, K_RIGHT
from pygamehelper import PygameHelper

os.environ['SDL_VIDEO_CENTERED'] = '1'


class BugSim():
	
	def __init__(self, DisplayCls):
		self.world = world.BugWorld() #instantiate the world and its objects
		self.display = DisplayCls((config.BOUNDARY_WIDTH, config.BOUNDARY_HEIGHT), Color.WHITE)
		self.display.register(display.DisplayEvents.UPDATE, self, self.update)

	def run(self):
		self.display.run()

	def update(self, source, screen):
		# Update
		self.world.update()

		# Draw
		screen.fill(Color.WHITE)
		self.world.draw(screen)
		pygame.display.update()


		
if __name__ == "__main__":
	g = BugSim(PygameHelper)
	g.run()
    
