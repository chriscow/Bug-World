from entity import BWOType, BWObject, Color


class Obstacle( BWObject ): #yellow
	def __init__ (self, starting_pos, name = "OBST" ):
		super().__init__( None, starting_pos, name )
		self.color = Color.YELLOW
		self.type = BWOType.OBST
		self.size = 7