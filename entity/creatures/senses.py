import random
import pygame
import numpy as np

from entity import BWObject
from helpers import Color, get_pos_transform

class Sensor( BWObject ):
	"""
	Base class for bug senses.  Senses take input from the world and fire events
	via callbacks.
	"""

	def __init__(self, parent, pos, name, range, acuity, visible=True, alpha=32):
    	
		super().__init__(parent, pos, name)
		self.color = Color.GREY

		assert(acuity <= range) # acuity must be less than range
		self.range = range			# How far can anything be detected (corner of your eye)
		self.acuity = acuity		# How far is detection enhanced (center of eye)

		# Determines if the range and acuity is drawn for debugging
		self.visible = visible	
		self.alpha = alpha

	def move(self, base):
		self.set_abs_position( base )
		super().update(base)

	def draw(self, surface):

		# If the sense itself is visible, draw it transparently
		# TODO: This is just mostly copied from PGObject::draw() -- need to refactor
		if self.visible:
			x = int(self.get_abs_x())
			y = int(self.get_abs_y())
			r,g,b = self.color

			dia = self.range * 2
			surface2 = pygame.Surface((dia, self.range))
			surface2.set_colorkey((0,0,0))
			surface2.set_alpha(self.alpha)
			
			pygame.draw.circle(surface2, 
				(int(r), int(g), int(b)), 	# color
				(self.range, self.range), 	# position int(self.range)
				self.range)					# radius

			surface.blit(surface2, (x - self.range,y - self.range))
		
		# Now draw the physical representation of the sensory object on top
		super().draw(surface)

	def detect( self ):
		pass

class Vision(BWObject):
	"""
	Physical representation of an eye
	"""
	def __init__(self, parent, pos, name, size, range=100, acuity=3):
		super().__init__(parent, pos, name)
		self.size = size
		self.color = Color.GREY
		self.sensor = Sensor(self, pos, name + ' sensor', range=range, acuity=acuity)
	
	def draw(self, surface):
		self.sensor.draw(surface)
		super().draw(surface)

	def detect(self):
		return self.sensor.detect()
		
	def move( self, base ):
		self.set_abs_position( base )
		super().update(base)
		self.sensor.move(base)

class Antennae(Sensor):
	def __init__(self, parent, pos, name, size=1, range=20, acuity=3):
		super().__init__(parent, pos, name)
		self.size = size
		self.color = Color.BLACK
		self.sensor = Sensor(self, pos, name + ' sensor', range, acuity)
	
	def draw(self, surface):
		self.sensor.draw(surface)
		super().draw(surface)

	def detect(self):
		return self.sensor.detect()
		
	def move( self, base ):
		self.set_abs_position( base )
		super().move(base)
		self.sensor.move(base)