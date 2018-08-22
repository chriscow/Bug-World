
import random
import numpy as np

import config
import helpers
from entity.creatures import *
from entity.obsticles import *
from entity.food import *


import collision

class BugWorld(): #defines the world, holds the objects, defines the rules of interaction

#--- Class Constants

	IDENTITY = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]] #equates to x=0, y=0, z=0, rotation = 0

	WorldObjects = []
	BWD = collision.BWCollision_Dict() #instantiate a dictionary to handle collisions

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
		for i in range(0, config.NUM_HERBIVORE_BUGS): #instantiate all of the Herbivores with a default name
			start_pos = helpers.get_random_location_in_world()
			self.WorldObjects.append( Herbivore( start_pos, "H"+ str(i) ))

		for i in range(0, config.NUM_CARNIVORE_BUGS):
			start_pos = helpers.get_random_location_in_world()
			self.WorldObjects.append( Carnivore( start_pos, "C"+ str(i) ))

		for i in range(0, config.NUM_OMNIVORE_BUGS ):
 			start_pos = helpers.get_random_location_in_world()
 			self.WorldObjects.append( Omnivore( start_pos, "O"+ str(i) ))

		for i in range(0, config.NUM_OBSTACLES ):
 			start_pos = helpers.get_random_location_in_world()
 			self.WorldObjects.append( Obstacle( start_pos, "B"+ str(i) ))

		for i in range(0, config.NUM_PLANT_FOOD ):
 			start_pos = helpers.get_random_location_in_world()
 			self.WorldObjects.append( Plant( start_pos, "P"+ str(i) ))

		for i in range(0, config.NUM_MEAT_FOOD ):
 			start_pos = helpers.get_random_location_in_world()
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

