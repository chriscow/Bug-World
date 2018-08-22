
import numpy as np

import random
import config

#Going to use 3D matrices even if in 2d
#See http://matthew-brett.github.io/transforms3d/ for details on the lib used
#Object's local coord frame is in the x,y plane and faces in the x direction.  
#Positive rotation follow RHR, x-axis into the y-axis...so z is up.
import transforms3d.affines as AFF 
import transforms3d.euler as E


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


#----- Utility Class Methods ----------------

def adjust_for_boundary( wT ): #adjust an inputed transform to account for world boundaries and wrap
	if config.BOUNDARY_WRAP:
		if wT[0][3] < 0:  wT[0][3] = config.BOUNDARY_WIDTH 
		elif wT[0][3] > config.BOUNDARY_WIDTH: wT[0][3] = 0

		if wT[1][3] < 0: wT[1][3] = config.BOUNDARY_HEIGHT
		elif wT[1][3] > config.BOUNDARY_HEIGHT: wT[1][3] = 0
	else:
		if wT[0][3] < 0:  wT[0][3] = 0 
		elif wT[0][3] > config.BOUNDARY_WIDTH: wT[0][3] = config.BOUNDARY_WIDTH

		if wT[1][3] < 0: wT[1][3] = 0
		elif wT[1][3] > config.BOUNDARY_HEIGHT: wT[1][3] = config.BOUNDARY_HEIGHT

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
	x = random.randint(0, config.BOUNDARY_WIDTH )
	y = random.randint(0, config.BOUNDARY_HEIGHT)
	z = 0
	theta = random.uniform(0, 2*np.pi) #orientation in radians
	return get_pos_transform( x, y, z, theta )