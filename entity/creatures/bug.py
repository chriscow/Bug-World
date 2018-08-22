import random
import pygame
import numpy as np

from entity.creatures import senses
from entity import BWObject
from helpers import Color, get_pos_transform



class Bug ( BWObject ):

	DEFAULT_TURN_AMT = np.deg2rad(30) # turns are in radians
	DEFAULT_MOVE_AMT = 5

	def __init__( self, initial_pos, name = "Bug" ):
		super().__init__( None, initial_pos, name )
		self.size = 10 #override default and set the intial radius of bug
		self.color = Color.PINK #override default and set the initial color of a default bug
		self.energy = 100 #default...needs to be overridden
		self.score = 0 #used to reinforce behaviour.  Add to the score when does a "good" thing

		self.senses = []

		#add the eyes for a default bug
		#put eye center on circumference, rotate then translate.

		rT = get_pos_transform( 0, 0, 0, np.deg2rad(-30) )
		tT = get_pos_transform( self.size, 0, 0, 0 )
		self.RIGHT_EYE_LOC = np.matmul(rT,tT)

		rT = get_pos_transform( 0, 0, 0, np.deg2rad(30) )
		self.LEFT_EYE_LOC = np.matmul(rT,tT)

		eye_size = int(self.size * 0.50) #set a percentage the size of the bug
		
		#instantiate the eyes
		# parent, name, pos, size, range=10, acuity=3
		#self.senses.append( senses.Vision(self, self.RIGHT_EYE_LOC, 'left eye', self.EYE_SIZE, range=10*self.size, acuity=3*self.size) )
		#self.senses.append( senses.Vision(self, self.LEFT_EYE_LOC, 'right eye', self.EYE_SIZE, range=10*self.size, acuity=3*self.size) )
		left_eye  = self._create_sensor(senses.Vision, 
			name='left eye', 
			size=eye_size, 
			pos=(eye_size,-eye_size,0), 
			deg=-30,
			range=eye_size*10, 
			acuity=eye_size*3)

		right_eye = self._create_sensor(senses.Vision, 
			name='right eye', 
			size=eye_size, 
			pos=(eye_size,eye_size,0), 
			deg=0,
			range=eye_size*10, 
			acuity=eye_size*3)

		self.senses.append(left_eye)
		self.senses.append(right_eye)


	def _create_sensor(self, clsdef, name, size, pos, deg, **kwargs):
		"""
		Sensor creation helper

		:param clsdef: Class definition deriving from Sensor
		:param name: String description of sensor
		:param size: Phisical size for display purposes
		:param pos: Relative position 
		:param rad: Sensor rotation
		:returns: Instance of clsdef sensor
		"""
		x,y,z = pos
		tx = get_pos_transform(x,y,z,np.deg2rad(deg))
		return clsdef(self, tx, name, size, **kwargs)


	def detect(self):
		#
		# Detect threats and obsticles within field of sensory range
		#
		for sense in self.senses:
			sense.detect()

	def think(self):
		# 
		# Do something with information from senses
		#
		pass

	def move(self, base):
		self.kinematic_wander()
		self.set_abs_position( base )	
		for sense in self.senses:
			sense.move(self.abs_position)

	def update( self, base ):
		self.detect()
		self.think()
		self.move(base)

	def draw( self, surface ):
		super().draw(surface) #inherited from BWObject
		for sense in self.senses:
			sense.draw(surface)

	def move_forward( self, amount_to_move = DEFAULT_MOVE_AMT ):
		#assume bug's 'forward' is along the x direction in local coord frame
		tM = get_pos_transform( x=amount_to_move, y=0, z=0, theta=0 ) #create an incremental translation
		self.set_rel_position ( np.matmul(self.rel_position, tM)) #update the new position

	def turn_left( self, theta = DEFAULT_TURN_AMT ):
		rM = get_pos_transform( x=0, y=0, z=0, theta=theta ) #create an incremental rotation
		self.set_rel_position (np.matmul(self.rel_position, rM )) #update the new position

	def turn_right( self, theta  = DEFAULT_TURN_AMT ):
		#'turning right is just a negative angle passed to turn left'
		self.turn_left( -theta )

	def wander( self ):
		rand_x = random.randint( 0, Bug.DEFAULT_MOVE_AMT )
		rand_theta = random.uniform( -Bug.DEFAULT_TURN_AMT, Bug.DEFAULT_TURN_AMT )
		wM = get_pos_transform( x=rand_x, y=0, z=0, theta=rand_theta ) #create an incremental movement
		self.set_rel_position(np.matmul(self.rel_position, wM )) #update the new relative position

	def kinematic_wander(self):

		rand_vr = random.uniform( -.5, 1 ) #random right wheel velocity normalized
		rand_vl = random.uniform( -.5, 1 ) #biased to move forward though
										   #eventually will be driven by a neuron

		delta_x, delta_y, delta_theta = self.kinematic_move( rand_vr, rand_vl )
		wM = get_pos_transform( x=delta_x, y=delta_y, z=0, theta=delta_theta ) #create an incremental movement
		self.set_rel_position(np.matmul(self.rel_position, wM )) #update the new relative position		
		

	def kinematic_move( self, vel_r, vel_l ): #assume bugbot with two wheels on each side of it.
										      #taken from GRIT robotics course
		wheel_radius = self.size * 0.5 #wheel radius is some proportion of the radius of the body
		wheel_separation = self.size * 2 #wheels are separated by the size of the bug
		delta_theta = ( wheel_radius/wheel_separation)*(vel_r - vel_l )
		temp_vect = (wheel_radius/2)*(vel_r + vel_l)
		delta_x = temp_vect * np.cos( delta_theta )
		delta_y = temp_vect * np.sin( delta_theta )
		return delta_x, delta_y, delta_theta

