from BotTracker import BotTracker
import time

if __name__ == '__main__':
	try:
		tracker = BotTracker()
		# tracker.set_grid_edges(0,100,0,100)
		# tracker.display_grid_image()
		for i in range(0,100000):
			# start = time.clock()
			coord = tracker.get_bot_location()
			end = time.clock()
			# print end-start
			direction = tracker.get_bot_direction()
			time.sleep(.1)
			print coord
	except Exception, e:
		print e
		print "Exiting with error"