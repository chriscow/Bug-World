import pygame 
import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'

from pygame.locals import *

#Helper class that controls interaction loop in Pygame
from pygamehelper import *

#Get the definition of the World
from BugWorld import *

#main control loop of the pygame
class BugSim( PygameHelper ):
	
	def __init__(self):
		self.BW = BugWorld() #instantiate the world and its objects
		super(BugSim,self).__init__( (self.BW.BOUNDARY_WIDTH, self.BW.BOUNDARY_HEIGHT), Color.WHITE )

	def update(self): #update everything in the world
		self.BW.update()


	def draw( self ): #draw the resulting world
		self.screen.fill(Color.WHITE)
		self.BW.draw(self.screen)
		pygame.display.update()

	def keyDown(self, key):
		
		if key == K_SPACE:
			pass
		elif key == K_LEFT:
			pass
		elif key == K_RIGHT:
			pass
		else:
			print(key)

		
if __name__ == "__main__":
	g = BugSim()
	g.mainLoop(60)
    
