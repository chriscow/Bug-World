from entity import BWOType

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



