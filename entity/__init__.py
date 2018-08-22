import pygame
import numpy as np

import world
from helpers import Color, adjust_for_boundary, get_x, get_y

class BWOType():
	
	#use integers so it is faster for dict lookups
	HERB = int(1) # Herbivore
	OMN = int(2)  # Omnivore
	CARN = int(3) # Carnivore 
	OBST = int(4) # Obstacle
	MEAT = int(5) # Food for Carnivore and Omnivore
	PLANT = int(6)# Food for Herbivore and Omnivore
	OBJ = int(7)  #catch all for the base class.  Shouldn't ever show up


IDENTITY = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]


class BWObject( ): #Bug World Object

	#Everything is a BWObject including bug body parts (e.g., eyes, ears, noses).
	#has a position and orientation relative to the container, which could be the world.  But it could be the body, the eye
	#has a color
	#has a size
	#has a name
	#stores an absolute position to prevent recalculating it when passing to contained objects.
	#BWO's should have a draw method that includes itself, hitboxes (based on global var)
	#stub methods for what collisions to register for

	def __init__(self, parent, starting_pos = IDENTITY, name = "BWOBject"):

		self.parent = parent
		self.rel_position = starting_pos
		self.abs_position = starting_pos
		self.name = name
		self.size = 1 				#default...needs to be overridden
		self.color = Color.BLACK	#default...needs to be overridden
		self.alpha = 255
		self.type = BWOType.OBJ		#default...needs to be overridden
		self.health = 100			#default...needs to be overridden


	def __repr__(self):
  		return ( self.name + ": abs position={}".format(self.abs_position) ) #print its name and transform

	def set_rel_position(self, pos_transform = IDENTITY): # position relative to its container
		self.rel_position = adjust_for_boundary( pos_transform ) #class method handles boundary adjustment
		return self.rel_position			

	def set_abs_position(self, base_transform = IDENTITY):
		self.abs_position = np.matmul( base_transform, self.rel_position )
		return self.abs_position

	def get_abs_position(self):
		return self.abs_position

	def get_abs_x( self ):
		return( get_x( self.abs_position ) )

	def get_abs_y( self ):
		return( get_y( self.abs_position ) )

	def update( self, base ): #stub method. Override to move this object each sample period
		pass	

	def draw(self, surface):
		# TODO: This will get abstracted out to run headless in the cloud
		x = int(self.get_abs_x())
		y = int(self.get_abs_y())

		r,g,b = self.color 

		# TODO: Abstract drawing out for headless simulation
		pygame.draw.circle(surface, (int(r),int(g),int(b)), (x, y), self.size, 0) 
