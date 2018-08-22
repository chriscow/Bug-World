from observer import Publisher

class DisplayEvents:
	UPDATE = 'update'
	KEYDOWN = 'key_down'	# callback(source, key)
	KEYUP   = 'key_up'		# callback(source, key)
	MOUSEUP = 'mouse_up'	# callback(source, button, pos)

class AbstractDisplay:
	def __init__(self):
		self.publisher = Publisher([DisplayEvents.UPDATE, 
			DisplayEvents.KEYDOWN, 
			DisplayEvents.KEYUP, 
			DisplayEvents.MOUSEUP])

	#
	# Publisher Implementation
	#
	def register(self, event, who, callback=None):
		self.publisher.register(event, who, callback)

	def unregister(self, event, who):
		self.publisher.unregister(event, who)

	# Overridden by concrete display class
	def run(self):
		pass
