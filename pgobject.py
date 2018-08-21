import pygame

#assume 2D graphics and using Pygame to render.
class PGObject():

	def draw( self, surface ):
		x = int(self.get_abs_x())
		y = int(self.get_abs_y())


		r,g,b = self.color #unpack the tuple
#modulate color based on health
		# hp = self.health/100 #what is the healt percentage
		# r *= hp
		# g *= hp
		# b *= hp


		pygame.draw.circle(surface, (int(r),int(g),int(b)), (x, y), self.size, 0) 
	
	def get_abs_x():
		pass

	def get_abs_y():
		pass