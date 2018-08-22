from entity import BWOType
from entity.creatures.bug import Bug
from helpers import Color

class Herbivore( Bug ): 
	def __init__ (self, starting_pos, name = "Herb" ):
		super().__init__( starting_pos, name )
		self.color = Color.GREEN
		self.type = BWOType.HERB

class Omnivore( Bug ): #Orange
	def __init__ (self, starting_pos, name = "OMN" ):
		super().__init__( starting_pos, name )
		self.color = Color.ORANGE
		self.type = BWOType.OMN

class Carnivore( Bug ): #Red
	def __init__ (self, starting_pos, name = "CARN" ):
		super().__init__( starting_pos, name )
		self.color = Color.RED
		self.type = BWOType.CARN

