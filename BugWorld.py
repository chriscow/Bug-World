import pygame
import numpy as np
import random

#Going to use 3D matrices even if in 2d
#See http://matthew-brett.github.io/transforms3d/ for details on the lib used
#Object's local coord frame is in the x,y plane and faces in the x direction.  
#Positive rotation follow RHR, x-axis into the y-axis...so z is up.
import transforms3d.affines as AFF 
import transforms3d.euler as E

from pgobject import *


#Color class so can separate out code from PG specific stuff.
#http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/
class Color(): #RGB values
	BLACK = (0,0,0)
	WHITE = (255,255,255)
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	YELLOW = (255,255,0)
	PINK = (255,192,203)
	BROWN = (160,82,45)
	ORANGE = (255, 165, 0)
	DARK_GREEN = (34,139,34)
	GREY = (190,190,190)


class BWOType():

	#use integers so it is faster for dict lookups
	HERB = int(1) # Herbivore
	OMN = int(2)  # Omnivore
	CARN = int(3) # Carnivore 
	OBST = int(4) # Obstacle
	MEAT = int(5) # Food for Carnivore and Omnivore
	PLANT = int(6)# Food for Herbivore and Omnivore
	OBJ = int(7)  #catch all for the base class.  Shouldn't ever show up

	
class BWCollision_Dict():	#Dictionary: two types as the keys, function as the item 
							#passes pointers into each object

	def print_collision( OB1, OB2 ):
		# print(OB1.name + 'T: ' + str(OB1.type) + ' H: ' + str(OB1.health) + ', ' 
			# + OB2.name + 'T: ' + str(OB2.type) + ' H: ' + str(OB2.health))
		pass

#Bug to Bug interactions
	def herb_omn( herb, omn ): #handle herbivore an omnivore collision
		BWCollision_Dict.print_collision( herb, omn )
		#do damage to herbivore
		herb.health -= 1

	def herb_carn( herb, carn):
		BWCollision_Dict.print_collision( herb, carn )
		#do damage to herbivore
		herb.health -= 20

	def herb_herb( herb1, herb2 ):
		BWCollision_Dict.print_collision( herb1, herb2 )
		#certain probability of mating?

	def omn_omn( omn1, omn2 ): 
		BWCollision_Dict.print_collision( omn1, omn2 )
		#certain probability of mating?

	def omn_carn( omn, carn ):
		BWCollision_Dict.print_collision( omn, carn )
		#do damage to omn
		omn.health -= 20
		carn.health -= 5

	def carn_carn( carn1, carn2 ):
		BWCollision_Dict.print_collision( carn1, carn2 )
		#certain probability of mating or fighting?
		carn1.health -= 5
		carn2.health -= 5

#Bug to food interactions
	def herb_plant( herb, plant ):
		BWCollision_Dict.print_collision( herb, plant )		
		herb.energy += 10
		plant.health -= 10
		if ( plant.size > 1 ): plant.size -= 1

	def omn_plant( omn, plant ):
		BWCollision_Dict.print_collision( omn, plant )		
		omn.energy += 10
		plant.health -= 10
		if ( plant.size > 1 ): plant.size -= 1

	def omn_meat( omn, meat ):
		BWCollision_Dict.print_collision( omn, meat )		
		omn.energy += 10
		meat.health -= 10
		if ( meat.size > 1 ): meat.size -= 1

	def carn_meat( carn, meat ):
		BWCollision_Dict.print_collision( carn, meat )		
		carn.energy += 10
		meat.health -= 10
		if ( meat.size > 1 ): meat.size -= 1

#Bug obstacle interactions
	def herb_obst( herb, obst ):
		BWCollision_Dict.print_collision( herb, obst )		
		herb.health -= 1 #ouch obstacles hurt

	def omn_obst( omn, obst ):
		BWCollision_Dict.print_collision( omn, obst )		
		omn.health -= 1 #ouch obstacles hurt

	def carn_obst( carn, obst ):
		BWCollision_Dict.print_collision( carn, obst )		
		carn.health -= 1 #ouch obstacles hurt

	CollisionDict={ # look up which function to call when two objects of certain types collide
		(BWOType.HERB, BWOType.OMN): herb_omn,
		(BWOType.HERB, BWOType.CARN ): herb_carn,
		(BWOType.HERB, BWOType.HERB): herb_herb,
		(BWOType.OMN, BWOType.OMN ): omn_omn,
		(BWOType.OMN, BWOType.CARN): omn_carn,
		(BWOType.CARN, BWOType.CARN ): carn_carn,
		(BWOType.HERB, BWOType.PLANT ): herb_plant,
		(BWOType.OMN, BWOType.PLANT ): omn_plant,
		(BWOType.OMN, BWOType.MEAT ): omn_meat,
		(BWOType.CARN, BWOType.MEAT ): carn_meat,
		(BWOType.HERB, BWOType.OBST ): herb_obst,
		(BWOType.OMN, BWOType.OBST ): omn_obst,
		(BWOType.CARN, BWOType.OBST ): carn_obst

		}

	def handle_collision( self, OB1, OB2):
		if (OB1.type > OB2.type ): self.handle_dict(OB2, OB1) #order the keys for dict lookup
		else: self.handle_dict(OB1, OB2)

	def handle_dict( self, OB1, OB2 ):
		try:
			self.CollisionDict[(OB1.type,OB2.type)]( OB1, OB2 ) #use types to lookup function to call and then call it
		except KeyError:
			pass #ignore it if isn't in dictionary

			# for debugging
			# if not (OB1.type == BWOType.OBST or OB2.type == BWOType.OBST ): #ignore if something dies on an obstacle
			# 	print('No handler for: ' + OB1.name + ' T:' + str(OB1.type)	+ ", " +
			# 							OB2.name + ' T:' + str(OB2.type))



class BugWorld(): #defines the world, holds the objects, defines the rules of interaction

#--- Class Constants
	BOUNDARY_WIDTH = 800
	BOUNDARY_HEIGHT = 600
	BOUNDARY_WRAP = True

	NUM_CARNIVORE_BUGS = 5
	NUM_OMNIVORE_BUGS = 3
	NUM_HERBIVORE_BUGS = 10
	NUM_PLANT_FOOD = 20
	NUM_MEAT_FOOD = 1
	NUM_OBSTACLES = 5
	IDENTITY = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]] #equates to x=0, y=0, z=0, rotation = 0

	WorldObjects = []
	BWD = BWCollision_Dict() #instantiate a dictionary to handle collisions

#used for collisions
	#SolidObjects = [] #bugbodies, food, obstacles add themselves to this list
	#LightEmittingObjects = [] #bugbodies, food, obstacles add themselves to this list
	#LightDetectingObjects = [] #add eye hit boxes themselves to this list
	#OdorEmittingObjects 
	#OdorDetectingObjects
	#SoundEmittingObjects
	#SoundDetectingObjects

#--- Instance Methods	
	def __init__(self):
		self.rel_position = BugWorld.IDENTITY #sets the world as the root equates to x=0, y=0, z=0, rotation = 0
		for i in range(0, BugWorld.NUM_HERBIVORE_BUGS): #instantiate all of the Herbivores with a default name
			start_pos = BugWorld.get_random_location_in_world()
			self.WorldObjects.append( Herbivore( start_pos, "H"+ str(i) ))

		for i in range(0, BugWorld.NUM_CARNIVORE_BUGS):
			start_pos = BugWorld.get_random_location_in_world()
			self.WorldObjects.append( Carnivore( start_pos, "C"+ str(i) ))

		for i in range(0, BugWorld.NUM_OMNIVORE_BUGS ):
 			start_pos = BugWorld.get_random_location_in_world()
 			self.WorldObjects.append( Omnivore( start_pos, "O"+ str(i) ))

		for i in range(0, BugWorld.NUM_OBSTACLES ):
 			start_pos = BugWorld.get_random_location_in_world()
 			self.WorldObjects.append( Obstacle( start_pos, "B"+ str(i) ))

		for i in range(0, BugWorld.NUM_PLANT_FOOD ):
 			start_pos = BugWorld.get_random_location_in_world()
 			self.WorldObjects.append( Plant( start_pos, "P"+ str(i) ))

		for i in range(0, BugWorld.NUM_MEAT_FOOD ):
 			start_pos = BugWorld.get_random_location_in_world()
 			self.WorldObjects.append( Meat( start_pos, "M"+ str(i) ))

	def update(self):
		for BWO in self.WorldObjects:
			BWO.update(self.rel_position)

		self.detect_collisions()
		self.post_collision_processing()

	def draw( self, surface ):
		for BWO in self.WorldObjects:
			BWO.draw( surface )
	
	def detect_collisions( self ):
		self.detect_light_collisions()
		self.detect_physical_collisions()

		#detect odor collisions
		#detect sound collisions

	def post_collision_processing ( self ):
		#loop through objects and delete them, convert them etc.
		#if health < 0, delete.
		#if was a bug, convert it to meat
		#if it was a plant, just delete it

		#need to keep track of where in list when deleting so that when an item is deleted, the range is shortened.
		list_len = len( self.WorldObjects ) #starting lenght of the list of objects
		i = 0 #index as to where we are in the list

		#loop through every object in the list
		while ( i < list_len ):
			if ( self.WorldObjects[i].health <= 0 ): #if the objects health is gone, deal with it.
				co = self.WorldObjects[i] #get the current object

				#if it is a bug, then convert it to meat
				if( co.type in { BWOType.HERB, BWOType.OMN, BWOType.CARN } ):
			   		start_pos = co.get_abs_position() #get location of the dead bug
			   		self.WorldObjects.append( Meat( start_pos, "M"+ str(i) )) #create a meat object at same location
			   		#list length hasn't changed because we are going to delete and add one
				else:
					list_len -= 1	#reduce the length of the list 

				del self.WorldObjects[i] #get rid of the object
				#'i' should now point to the next one in the list because an item was removed so shouldn't have to increment
			else:
				i += 1 #manually increment index pointer because didn't delete the object


	def detect_light_collisions( self ):
		#loop through light emitting objects and see if they collide with light detecting
		#make sure doesn't collide with self
		#need to differientiate between RGB detection/emission
		#need to differentiate intensities so objects further away stimulate less
		pass

	def detect_physical_collisions( self ):
		#loop through solid bodies
		#call collision handlers on each object
		for BWO1 in self.WorldObjects:
			for BWO2 in self.WorldObjects:
				if BWO1 == BWO2: continue
				elif self.circle_collision(BWO1, BWO2):
					# print("Hit " + BWO1.name + " and " + BWO2.name )
					self.BWD.handle_collision(BWO1, BWO2)

	def circle_collision( self, BWO1, BWO2 ):	#takes two BugWorld Objects in.
		dx = BWO1.abs_position[0][3] - BWO2.abs_position[0][3]
		dy = BWO1.abs_position[1][3] - BWO2.abs_position[1][3]

		dist_sqrd = ( dx * dx ) + ( dy * dy )
		#size is radius of objections circle hit box
		if (dist_sqrd < (BWO1.size + BWO2.size)**2) : return True
		else: return False

#----- Utility Class Methods ----------------

	def adjust_for_boundary( wT ): #adjust an inputed transform to account for world boundaries and wrap
		if BugWorld.BOUNDARY_WRAP:
			if wT[0][3] < 0:  wT[0][3] = BugWorld.BOUNDARY_WIDTH 
			elif wT[0][3] > BugWorld.BOUNDARY_WIDTH: wT[0][3] = 0

			if wT[1][3] < 0: wT[1][3] = BugWorld.BOUNDARY_HEIGHT
			elif wT[1][3] > BugWorld.BOUNDARY_HEIGHT: wT[1][3] = 0
		else:
			if wT[0][3] < 0:  wT[0][3] = 0 
			elif wT[0][3] > BugWorld.BOUNDARY_WIDTH: wT[0][3] = BugWorld.BOUNDARY_WIDTH

			if wT[1][3] < 0: wT[1][3] = 0
			elif wT[1][3] > BugWorld.BOUNDARY_HEIGHT: wT[1][3] = BugWorld.BOUNDARY_HEIGHT

		return wT #return the updated transform

	def get_pos_transform( x=0, y=0, z=0, theta=0 ): #utility function to encapsulate translation and rotation
		#use this anytime a transform is needed in the world.  
		#assume the angle is measured in the x,y plane around z axis
		#it will be an absolute transform in the local x, y, theta space
		T = [x, y, z] #create a translation matrix
		R = E.euler2mat( 0, 0, theta ) #create a rotation matrix around Z axis.
		Z = [1, 1, 1] # zooms...only included because API required it... will ignore the skew
		return AFF.compose(T, R, Z)

	def get_x( position ):
		return position[0][3] 

	def get_y( position ):
		return position[1][3] 

	def get_random_location_in_world():
		x = random.randint(0, BugWorld.BOUNDARY_WIDTH )
		y = random.randint(0, BugWorld.BOUNDARY_HEIGHT)
		z = 0
		theta = random.uniform(0, 2*np.pi) #orientation in radians
		return BugWorld.get_pos_transform( x, y, z, theta )
	

class BWObject( PGObject ): #Bug World Object

	#Everything is a BWObject including bug body parts (e.g., eyes, ears, noses).
	#has a position and orientation relative to the container, which could be the world.  But it could be the body, the eye
	#has a color
	#has a size
	#has a name
	#stores an absolute position to prevent recalculating it when passing to contained objects.
	#BWO's should have a draw method that includes itself, hitboxes (based on global var)
	#stub methods for what collisions to register for

	def __init__(self, parent, starting_pos = BugWorld.IDENTITY, name = "BWOBject"):

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

	def set_rel_position(self, pos_transform = BugWorld.IDENTITY): # position relative to its container
		self.rel_position = BugWorld.adjust_for_boundary( pos_transform ) #class method handles boundary adjustment
		return self.rel_position			

	def set_abs_position(self, base_transform = BugWorld.IDENTITY):
		self.abs_position = np.matmul( base_transform, self.rel_position )
		return self.abs_position

	def get_abs_position(self):
		return self.abs_position

	def get_abs_x( self ):
		return( BugWorld.get_x( self.abs_position ) )

	def get_abs_y( self ):
		return( BugWorld.get_y( self.abs_position ) )

	def update( self, base ): #stub method. Override to move this object each sample period
		pass	


#Things to do
#import logging
#fix z axis flip from pygame to local coord system
#have a scale for drawing in pygame that is independent of bug kinematics


#have a sample period so can do velocity
#simulate collision dynamics to mimic accelerometer
#kinematics for zumo
#kinematics for gopigo

#range
#collisions could do damage
#minimize energy spent
#maximize health


#Bug
#knows how to move
#holds attributes
#has a brain
#has sensors
#has outputs

#Bug parts
#has a shape, size, color, location(relative to base), hitbox(relative to location)
#knows how to draw itself
#knows what type of collisions to register for

class BugSense( BWObject ):
	"""
	Base class for bug senses.  Senses take input from the world and fire events
	via callbacks.
	"""

	def __init__(self, parent, pos, name, range, acuity, visible=True, alpha=128):
    	
		super().__init__(parent, pos, name)
		self.color = Color.GREY

		assert(acuity <= range) # acuity must be less than range
		self.range = range			# How far can anything be detected (corner of your eye)
		self.acuity = acuity		# How far is detection enhanced (center of eye)

		# Determines if the range and acuity is drawn for debugging
		self.visible = visible	
		self.alpha = alpha

	def draw(self, surface):

		# If the sense itself is visible, draw it transparently
		# TODO: This is just mostly copied from PGObject::draw() -- need to refactor
		if self.visible:
			x = int(self.get_abs_x())
			y = int(self.get_abs_y())
			r,g,b = self.color
			surface2 = pygame.Surface((self.range,self.range))
			surface2.set_colorkey((0,0,0))
			surface2.set_alpha(self.alpha)
			pygame.draw.circle(surface2, (int(r), int(g), int(b)), (0,0), self.range)
			surface.blit(surface2, (x,y))
		
		# Now draw the physical representation of the sensory object on top
		super().draw(surface)

	def detect( self ):
		pass

class BugEye( BugSense ):
	"""
	Physical representation of an eye
	"""
	def __init__(self, parent, pos, name, size, range=100, acuity=3):
		super().__init__(parent, pos, name, range, acuity)
		self.size = size
		self.color = Color.GREY
	
	def draw(self, surface):
		super().draw(surface)

	def detect(self):
		super().detect()
		
	def move( self, base ):
		self.set_abs_position( base )
		super().update(base)

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

		rT = BugWorld.get_pos_transform( 0, 0, 0, np.deg2rad(-30) )
		tT = BugWorld.get_pos_transform( self.size, 0, 0, 0 )
		self.RIGHT_EYE_LOC = np.matmul(rT,tT)

		rT = BugWorld.get_pos_transform( 0, 0, 0, np.deg2rad(30) )
		self.LEFT_EYE_LOC = np.matmul(rT,tT)

		self.EYE_SIZE = int(self.size * 0.50) #set a percentage the size of the bug
		
		#instantiate the eyes
		# parent, name, pos, size, range=10, acuity=3
		self.senses.append( BugEye(self, self.RIGHT_EYE_LOC, 'left eye', self.EYE_SIZE, range=10*self.size, acuity=3*self.size) )
		self.senses.append( BugEye(self, self.LEFT_EYE_LOC, 'right eye', self.EYE_SIZE, range=10*self.size, acuity=3*self.size) )

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
		tM = BugWorld.get_pos_transform( x=amount_to_move, y=0, z=0, theta=0 ) #create an incremental translation
		self.set_rel_position ( np.matmul(self.rel_position, tM)) #update the new position

	def turn_left( self, theta = DEFAULT_TURN_AMT ):
		rM = BugWorld.get_pos_transform( x=0, y=0, z=0, theta=theta ) #create an incremental rotation
		self.set_rel_position (np.matmul(self.rel_position, rM )) #update the new position

	def turn_right( self, theta  = DEFAULT_TURN_AMT ):
		#'turning right is just a negative angle passed to turn left'
		self.turn_left( -theta )

	def wander( self ):
		rand_x = random.randint( 0, Bug.DEFAULT_MOVE_AMT )
		rand_theta = random.uniform( -Bug.DEFAULT_TURN_AMT, Bug.DEFAULT_TURN_AMT )
		wM = BugWorld.get_pos_transform( x=rand_x, y=0, z=0, theta=rand_theta ) #create an incremental movement
		self.set_rel_position(np.matmul(self.rel_position, wM )) #update the new relative position

	def kinematic_wander(self):

		rand_vr = random.uniform( -.5, 1 ) #random right wheel velocity normalized
		rand_vl = random.uniform( -.5, 1 ) #biased to move forward though
										   #eventually will be driven by a neuron

		delta_x, delta_y, delta_theta = self.kinematic_move( rand_vr, rand_vl )
		wM = BugWorld.get_pos_transform( x=delta_x, y=delta_y, z=0, theta=delta_theta ) #create an incremental movement
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

class Obstacle( BWObject ): #yellow
	def __init__ (self, starting_pos, name = "OBST" ):
		super().__init__( None, starting_pos, name )
		self.color = Color.YELLOW
		self.type = BWOType.OBST
		self.size = 7

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



