from entity import BWOType, BWObject, Color

class Meat( BWObject ): #brown
	def __init__ (self, starting_pos, name = "MEAT" ):
		super().__init__( None, starting_pos, name )
		self.color = Color.BROWN
		self.type = BWOType.MEAT
		self.size = 10

class Plant( BWObject ): #dark green
	def __init__ (self, starting_pos, name = "PLANT" ):
		super().__init__( None, starting_pos, name )
		self.color = Color.DARK_GREEN
		self.type = BWOType.PLANT
		self.size = 5