#!/usr/bin/env python

import math
import pygame
pygame.init()

# Set the height and width of the screen
size = [512, 768]
screen = pygame.display.set_mode(size)

red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)
white=(255,255,255)
yellow=(255,255,0)
pink=(255,0,255)
cyan=(0,255,255)
gray=(128,128,128)
colors = [red, green, blue, yellow, pink, cyan, white, gray]

gravity = 1
fps = 30 # frames per second
tps = 3 # throws per second

fpt = fps/tps # frames per throw

class Pattern:
	def __init__(self, pattern_ = "3"):
		self.pattern = []
		for n in pattern_:
			self.pattern += [int(n)]
		
		self.pattern_index = 0

	def numberOfBalls(self):
		return sum(self.pattern) / len(self.pattern)

	def next(self):
		self.pattern_index = (self.pattern_index + 1) % len(self.pattern)
		ret = self.pattern[self.pattern_index] 
		return ret

def distance(a,b):
	return ((a[0]-b[0])**2 + (a[1]+b[1])**2)**0.5

class Ball:
	def __init__(self, index):
		self.v = (0.0, 0.0) # velocity
		self.p = (100.0,100.0) # position
		self.r = 25 # radius
		self.nextActionIn = 0

		self.color = colors[index]
		
		if i % 2:
			self.p = clown.righthand
		else:
			self.p = clown.lefthand
		self.throw(index)
		self.flying = False

	def current_hand(self):
		if distance(self.p, clown.righthand) > distance(self.p, clown.lefthand):
			return clown.lefthand
		else:
			return clown.righthand
			
	def other_hand(self):
		if distance(self.p, clown.righthand) > distance(self.p, clown.lefthand):
			return clown.righthand
		else:
			return clown.lefthand
	
	def draw(self):
		pygame.draw.ellipse(screen, self.color, (self.p[0], self.p[1], self.r, self.r))
		
	def tick(self):
		if self.flying:
			self.v = (self.v[0], self.v[1] + gravity)
			self.p = (self.p[0] + self.v[0], self.p[1] + self.v[1])
		else:
			self.p = self.current_hand()
			
		if self.nextActionIn > 0:
			self.nextActionIn -= 1
		else:
			self.p = self.current_hand()
			n = pattern.next()
			self.throw(n)
		self.draw()
		
	def throw(self, nr): # juggling order, destination
		if nr % 2:
			dst = self.other_hand()
		else:
			dst = self.current_hand()

		vx = 1.0 * (dst[0] - self.p[0]) / (fpt*nr - 1)
			
		vy = -0.5 * nr * fpt * gravity
		self.v = (vx, vy)
		self.nextActionIn = nr * fpt - 1
		if nr == 2:
			self.flying = False
		else:
			self.flying = True
		self.nr = nr

class Clown:
	def __init__(self):
		self.hand_radius = 50
		self.righthand_center = (250, 500)
		self.lefthand_center = (50, 500)
		self.righthand = (self.righthand_center[0], self.righthand_center[1])
		self.lefthand = (self.lefthand_center[0], self.lefthand_center[1])
		#~ self.righthand_current = (self.righthand_center[0] - self.hand_radius, self.righthand_center[1])
		#~ self.lefthand_current = (self.lefthand_center[0] + self.hand_radius, self.lefthand_center[1])
		self.angle = 0
		
	def draw(self):
		col = (160,128,148)
		pygame.draw.ellipse(screen, col,  (105,150,90,110)) # head
		pygame.draw.circle(screen, black, (125, 190),  5) # eyes
		pygame.draw.circle(screen, black, (175, 190),  5) # eyes
		pygame.draw.line(screen, black,   (135, 230), (165, 230), 5) # mouth
		pygame.draw.rect(screen, col, (130,243,40,100)) # neck
		pygame.draw.rect(screen, col, (75,300,150,400)) # body
		pygame.draw.line(screen, col,   (75,300), (50, 500), 15) # arm
		pygame.draw.line(screen, col,   (225,300), (250, 500), 15) # arm
		
		#~ pygame.draw.line(screen, col,   (50,500), self.lefthand_current, 15) # moving arm
		#~ pygame.draw.line(screen, col,   (250, 500), self.righthand_current, 15) # moving arm
		
	def tick(self):
		self.angle += 2 * math.pi / fpt
		#~ self.righthand_current = (self.righthand_center[0] + self.hand_radius * math.cos(self.angle), self.righthand_center[1] + self.hand_radius * math.sin(self.angle))
		#~ self.lefthand_current = (self.lefthand_center[0] + self.hand_radius * math.cos(-self.angle), self.lefthand_center[1] + self.hand_radius * math.sin(-self.angle))
		self.draw()

clown = Clown()
pattern = Pattern("3")
balls = []
print "number of Balls:", pattern.numberOfBalls()
for i in range(pattern.numberOfBalls()):
	balls += [Ball(i)]

clock = pygame.time.Clock()

# first draw everything for initial view:
clown.draw()
for b in balls:
	b.draw()
pygame.display.flip()
clock.tick(2)

done = False
while not done:

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
	
	# Clear the screen and set the screen background
	screen.fill(black)
	clown.tick()
	
	for b in balls:
		b.tick()
	
	# print stuff on screen and wait
	pygame.display.flip()
	clock.tick(fps)
