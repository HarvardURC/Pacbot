import numpy as np
import cv2

# Tune constants for grid
LEFT_EDGE = 267
RIGHT_EDGE = 1103
TOP_EDGE = -17
BOTTOM_EDGE = 735

#28 grid spaces across
class BotTracker:

	def __capture_image(self, cap):
		ret, frame = cap.read()
		return frame

	# Takes RGB image
	def __process_image(self, image):

		# Our operations on the frame come here
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		hsv = cv2.medianBlur(hsv, 5)

		draw_col = (0,0,255)

		p1 = (LEFT_EDGE, BOTTOM_EDGE)
		p2 = (RIGHT_EDGE, TOP_EDGE)
		cv2.rectangle(hsv, p1, p2, draw_col) #bounding rectangle

		vert_spacing = (RIGHT_EDGE - LEFT_EDGE)/31. # vertical lines
		for i in range(1, 31): 
			x_pos = int(LEFT_EDGE + i*vert_spacing)
			p1 = (x_pos, BOTTOM_EDGE)
			p2 = (x_pos, TOP_EDGE)
			cv2.line(hsv, p1, p2, draw_col)

		horiz_spacing = (BOTTOM_EDGE - TOP_EDGE)/28. # horizontal lines
		for i in range(1, 28): 
			y_pos = int(TOP_EDGE + i*horiz_spacing)
			p1 = (LEFT_EDGE, y_pos)
			p2 = (RIGHT_EDGE, y_pos)
			cv2.line(hsv, p1, p2, draw_col)

		## box around target pixel for testing
		# pt = (600, 350)
		# cv2.circle(hsv, pt, 3, draw_col, thickness =1)


		return hsv

	def __detect_bot(self, hsv_image):

		# Experimentally determined LED thresholds
		BOT_MIN = np.array([28,25,100], np.uint8)
		BOT_MAX = np.array([32,255,255], np.uint8)

		thresholded_image = cv2.inRange(hsv_image, BOT_MIN, BOT_MAX)
		thresholded_image = cv2.medianBlur(thresholded_image, 11)

		contours, hierarchy = cv2.findContours(thresholded_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		if not contours:
			(bot_x, bot_y) = (-1000,-1000)
		else:		
			bot = contours[0]
			M = cv2.moments(bot)
			if len(bot) > 2:
				bot_x = int(M['m10']/M['m00'])
				bot_y = int(M['m01']/M['m00'])
			else:
				bot_x = self.current_location[0]
				bot_y = self.current_location[1]

		return thresholded_image, (bot_x, bot_y)
		

	def __cam2game(self, coord):
		# account for board rotation here
		cam_x = coord[0]
		cam_y = coord[1]
		if cam_x < LEFT_EDGE or cam_x > RIGHT_EDGE or cam_y < TOP_EDGE or cam_y > BOTTOM_EDGE:
			return (-1,-1) # return this if coordinate isn't on arena (or no yellow in frame)
		else:
			# print "check 1"
			x = int((BOTTOM_EDGE-cam_y)/((BOTTOM_EDGE-TOP_EDGE)/28.0))
			y = int((cam_x-LEFT_EDGE)/((RIGHT_EDGE-LEFT_EDGE)/31.0))
			# print "check 2"
			return (x, y)


	def __init__(self, cam_number=0):
		self.cap = cv2.VideoCapture(cam_number) # set camera
		self.cap.set(3, 1280) # set frame width
		self.cap.set(4, 720) # set frame height
		self.previous_location = (-1, -1)
		self.current_location = (-1, -2)

		# cap.release()
		# cv2.destroyAllWindows()

	def get_bot_location(self):
		image = self.__capture_image(self.cap)
		image = self.__process_image(image)
		#cv2.imshow('Grid Reference', image)
		thresh_image, location = self.__detect_bot(image)
		# cv2.waitKey(1)
		game_loc = self.__cam2game(location)
		if self.current_location != game_loc:
			self.previous_location = self.current_location
			self.current_location = game_loc
		self.current_location = game_loc
		return game_loc
		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 		break

	def get_bot_direction(self):
		new_x = self.current_location[0]
		new_y = self.current_location[1]
		last_x = self.previous_location[0]
		last_y = self.previous_location[1]
		if new_x > last_x:
			return "EAST"
		elif new_x < last_x:
			return "WEST"
		elif new_y > last_y:
			return "NORTH"
		elif new_y < last_y:
			return "SOUTH"
		else:
			return "NO DIRECTION"

	def display_grid_image(self):
		while(True):
			image = self.__capture_image(self.cap)
			image = self.__process_image(image)
			cv2.imshow('Grid Reference', image)
			if cv2.waitKey(1) & 0xFF == ord('q'):
		 		break

		cap.release()
		cv2.destroyAllWindows()

	def set_grid_edges(self, l, r, t, b):
		global LEFT_EDGE
		global RIGHT_EDGE
		global TOP_EDGE
		global BOTTOM_EDGE
		LEFT_EDGE = l
		RIGHT_EDGE = r
		TOP_EDGE = t
		BOTTOM_EDGE = b
