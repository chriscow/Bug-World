# Bug-World



#PGBugWorld where pygame dependent code goes
#contains draw code
#toggle display of light, smell, sound

#----------------- START PYGAME SPECIFIC CODE ---------------------------------------


#world for simulations to happen 
#has boundaries
#has objects
#	- determines which type
#	- determines where and when
#	- kills objects
#	- determines rules for affecting object attributes (health, mutating, mating)


#objects register for different types of collisions (physical, sound, smell, light(RGB))
#objects have hitboxes for each sensor.


#objects emit light at 1/r^2 three different colors
#how do you keep senses from sensing itself
#objects emit sound (varies on speed)
#objects emit smell
#objects have physical collision
#objects have smell collision
#objects have sound collision
#eyes collide with objects and extracts RGB values from the target object .color tuple
#eye collision also gives distance
#bodies collide with other solid bodies

# has the sample time which is the update loop time...used for velocity and accleration

#detects collisions
#	- different hitbox shapes.  Hitbox needed for eyes so that collisions can be detected
#		in field of vision (use circles to start for everything.  Could use cones for vision eventually)
#	- should return "distance" so can be used for intensity
#	- returns an intensity of collision (for eye interaction with light, sound, smell)


#contains rules of interactions
#how do bugs die
#have a score that indicates successfulness (distance travelled, area covered, energy amount (expended moving, gained eating) )
#how do bugs reproduce (should we use the "weakest 500" to avoid extinction events)

#need global counters so can do rates to keep populations stable.
#timer
	#controls rates like food introduction, mating
	#creates extinction events

#Iterations/generations/epoch:
	#can be used to create extinction events in so many cycles

#Need a point system to keep track of goal reinforcement
	#points for distance travelled (would incent to move.  otherwise would just sit still to max energy/health)
	#points for time alive
	#points for food eaten
	#could use energy and health

#Need an energy system
	#controls whether starves
	#consume energy based on speed
	#speed driven by amount of energy