### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
# 
# Obstacle objects

import pygame
from math import sqrt, pow
from pyignition.gravity import UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL
from pyignition import keyframes, interpolate
from pyignition.constants import *


MAXDIST = 20.0


def dotproduct2d(v1, v2):
	return ((v1[0] * v2[0]) + (v1[1] * v2[1]))

def magnitude(vec):
	try:
		return sqrt(vec[0] ** 2 + vec[1] ** 2)
	except:
		return 1.0

def magnitudesquared(vec):
	try:
		return (vec[0] ** 2 + vec[1] ** 2)
	except:
		return 1.0

def normalise(vec):
	mag = magnitude(vec)
	return [vec[0] / mag, vec[1] / mag]


class Obstacle:
	def __init__(self, parenteffect, pos, colour, bounce):
		self.parenteffect = parenteffect
		self.pos = pos
		self.colour = colour
		self.bounce = bounce
		self.maxdist = MAXDIST  # The maximum (square-based, not circle-based) distance away for which forces will still be calculated
		self.curframe = 0
		self.keyframes = []
	
	def Draw(self, display):
		pass
	
	def Update(self):
		self.curframe = self.curframe + 1
	
	def OutOfRange(self, pos):
		return (abs(pos[0] - self.pos[0]) > self.maxdist) or (abs(pos[1] - self.pos[1]) > self.maxdist)
	
	def InsideObject(self, pos, pradius):
		pass
	
	def GetResolved(self, pos, pradius):  # Get a resolved position for a particle located inside the object
		pass
	
	def GetDist(self, pos):
		return magnitude([pos[0] - self.pos[0], pos[1] - self.pos[1]])
	
	def GetNormal(self, pos):  # Gets the normal relevant to a particle at the supplied potision (for example, that of the appropriate side of a squre)
		pass
	
	def GetForceFactor(self, pos, pradius):  # Gets the force as a factor of maximum available force (0.0 - 1.0), determined by an inverse cube distance law
		pass
	
	def GetForce(self, pos, velocity, pradius = 0.0):  # Gets the final (vector) force
		if self.OutOfRange(pos) or self.bounce == 0.0:
			return [0.0, 0.0]
		
		if (pos[0] == self.pos[0]) and (pos[1] == self.pos[1]):
			return [0.0, 0.0]
		
		normal = self.GetNormal(pos)
		scalingfactor = -dotproduct2d(normal, velocity)  # An integer between 0.0 and 1.0 used to ensure force is maximised for head-on collisions and minimised for scrapes
		
		if scalingfactor <= 0.0:  # The force should never be attractive, so take any negative value of the scaling factor to be zero
			return [0.0, 0.0]  # A scaling factor of zero always results in zero force
		
		forcefactor = (self.GetForceFactor(pos, pradius))
		velmag = magnitude(velocity)  # Magnitude of the velocity - multiplied in the force equation
		
		# Force = bounce factor * velocity * distance force factor (0.0 - 1.0) * angle force factor (0.0 - 1.0), along the direction of the normal pointing away from the obstacle
		return [normal[0] * forcefactor * velmag * scalingfactor * self.bounce, normal[1] * forcefactor * velmag * scalingfactor * self.bounce]
	
	def CreateKeyframe(self):
		pass
	
	def SetPos(self, newpos):
		self.CreateKeyframe(self.curframe, pos = newpos)
	
	def SetColour(self, newcolour):
		self.CreateKeyframe(self.curframe, colour = newcolour)
	
	def SetBounce(self, newbounce):
		self.CreateKeyframe(self.curframe, bounce = newbounce)


class Circle(Obstacle):
	def __init__(self, parenteffect, pos, colour, bounce, radius):
		Obstacle.__init__(self, parenteffect, pos, colour, bounce)
		self.type = "circle"
		self.radius = radius
		self.radiussquared = self.radius ** 2
		self.maxdist = MAXDIST + self.radius
		self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.radius)
	
	def Draw(self, display):
		offset = self.parenteffect.pos
		pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), int(self.radius))
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'radius':self.radius}, self.keyframes)
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
		self.bounce = newvars['bounce']
		self.radius = newvars['radius']
		
		Obstacle.Update(self)
	
	def InsideObject(self, pos, pradius = 0.0):
		mag = magnitude([pos[0] - self.pos[0], pos[1] - self.pos[1]])
		return (((mag - pradius) ** 2) < self.radiussquared)
	
	def GetResolved(self, pos, pradius = 0.0):
		if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
			return self.GetResolved([pos[0], pos[1] - 1])
			
		vec = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
		mag = magnitude(vec)
		nor = [vec[0] / mag, vec[1] / mag]
		
		# Split the pradius into appropriate components by multiplying the normal vector by pradius
		pradiusvec = [(nor[0] * pradius), (nor[1] * pradius)]
		
		correctedvec = [nor[0] * (self.radius), nor[1] * (self.radius)]
		
		return [self.pos[0] + correctedvec[0] + pradiusvec[0], self.pos[1] + correctedvec[1] + pradiusvec[1]]
	
	def GetNormal(self, pos):
		vec = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
		mag = magnitude(vec)
		
		return [vec[0] / mag, vec[1] / mag]
	
	def GetForceFactor(self, pos, pradius = 0.0):
		nvec = self.GetNormal(pos)
		tempradius = self.radius
		vec = [tempradius * nvec[0], tempradius * nvec[1]]
		newpos = [pos[0] - vec[0], pos[1] - vec[1]]
		
		distcubed = (abs(pow(float(newpos[0] - self.pos[0]), 3.0)) + abs(pow(float(newpos[1] - self.pos[1]), 3.0))) - (pradius * pradius * pradius)
		if distcubed <= 1.0:
			return 1.0
		
		force = (1.0 / distcubed)
		
		return force
	
	def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, radius = None, interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'radius':radius, 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'radius':self.radius})
	
	def SetRadius(self, newradius):
		self.CreateKeyframe(self.curframe, radius = newradius)


class Rectangle(Obstacle):
	def __init__(self, parenteffect, pos, colour, bounce, width, height):
		Obstacle.__init__(self, parenteffect, pos, colour, bounce)
		self.type = "rectangle"
		self.width = width
		self.halfwidth = self.width / 2.0
		self.height = height
		self.halfheight = height / 2.0
		self.maxdist = max(self.halfwidth, self.halfheight) + MAXDIST
		self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.width, self.height)
	
	def Draw(self, display):
		offset = self.parenteffect.pos
		pygame.draw.rect(display, self.colour, pygame.Rect(offset[0] + (self.pos[0] - self.halfwidth), offset[1] + (self.pos[1] - self.halfheight), self.width, self.height))
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'width':self.width, 'height':self.height}, self.keyframes)
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
		self.bounce = newvars['bounce']
		self.width = newvars['width']
		self.halfwidth = self.width / 2.0
		self.height = newvars['height']
		self.halfheight = self.height / 2.0
		self.maxdist = max(self.halfwidth, self.halfheight) + MAXDIST
		
		Obstacle.Update(self)
	
	def InsideObject(self, pos, pradius = 0.0):
		return (((pos[0] + pradius) > (self.pos[0] - self.halfwidth)) and ((pos[0] - pradius) < (self.pos[0] + self.halfwidth)) and ((pos[1] + pradius) > (self.pos[1] - self.halfheight)) and ((pos[1] - pradius) < self.pos[1] + self.halfheight))
	
	def GetResolved(self, pos, pradius = 0.0):
		if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
			return self.GetResolved([pos[0], pos[1] - 1])
		
		# Where 'triangles' within the rectangle are referred to, imagine a rectangle with diagonals drawn between its vertices. The four triangles formed by this process are the ones referred to
		if pos[0] == self.pos[0]:  # If it's directly above the centre of the rectangle
			if pos[1] > self.pos[1]:
				return [pos[0], self.pos[1] + self.halfheight + pradius]
			else:
				return [pos[0], self.pos[1] - (self.halfheight + pradius)]
		elif pos[1] == self.pos[1]:  # If it's directly to one side of the centre of the rectangle
			if pos[0] > self.pos[0]:
				return [self.pos[0] + self.halfwidth + pradius, pos[1]]
			else:
				return [self.pos[0] - (self.halfwidth + pradius), pos[1]]
		elif abs(float(pos[1] - self.pos[1]) / float(pos[0] - self.pos[0])) > (float(self.height) / float(self.width)):  # If it's in the upper or lower triangle of the rectangle
			return [pos[0], self.pos[1] + ((self.halfheight + pradius) * ((pos[1] - self.pos[1]) / abs(pos[1] - self.pos[1])))]  # Halfheight is multiplied by a normalised version of (pos[1] - self.pos[1]) - thus if (pos[1] - self.pos[1]) is negative, it should be subtracted as the point is in the upper triangle
		else:  # If it's in the left or right triangle of the rectangle
			return [self.pos[0] + ((self.halfwidth + pradius) * ((pos[0] - self.pos[0]) / abs(pos[0] - self.pos[0]))), pos[1]]
	
	def GetNormal(self, pos):
		if pos[1] < (self.pos[1] - self.halfheight):
			return [0, -1]
		elif pos[1] > (self.pos[1] + self.halfheight):
			return [0, 1]
		elif pos[0] < (self.pos[0] - self.halfwidth):
			return [-1, 0]
		elif pos[0] > (self.pos[0] + self.halfwidth):
			return [1, 0]
		else:
			vect = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
			mag = magnitude(vect)
			return [vect[0] / mag, vect[1] / mag]
	
	def GetForceFactor(self, pos, pradius = 0.0):
		nor = self.GetNormal(pos)
		
		if nor[0] == 0:
			if (pos[0] > (self.pos[0] - self.halfwidth)) and (pos[0] < (self.pos[0] + self.halfwidth)):
				r = (abs(pos[1] - self.pos[1]) - self.halfheight) - pradius
			else:
				return 0.0
		elif nor[1] == 0:
			if (pos[1] > (self.pos[1] - self.halfheight)) and (pos[1] < (self.pos[1] + self.halfheight)):
				r = (abs(pos[0] - self.pos[0]) - self.halfwidth) - pradius
			else:
				return 0.0
		else:
			return 1.0
		
		if r <= 1.0:
			return 1.0
		
		return (1.0 / pow(float(r), 3.0))
	
	def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, width = None, height = None, interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'width':width, 'height':height, 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'width':self.width, 'height':self.height})
	
	def SetWidth(self, newwidth):
		self.CreateKeyframe(self.curframe, width = newwidth)
	
	def SetHeight(self, newheight):
		self.CreateKeyframe(self.curframe, height = newheight)


class BoundaryLine(Obstacle):
	def __init__(self, parenteffect, pos, colour, bounce, normal):
		Obstacle.__init__(self, parenteffect, pos, colour, bounce)
		self.type = "boundaryline"
		self.normal = normalise(normal)
		self.edgecontacts = []
		self.hascontacts = False
		self.storedw, self.storedh = None, None
		self.curframe = 0
		self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.normal)
	
	def Draw(self, display):
		offset = self.parenteffect.pos
		
		W = display.get_width()
		H = display.get_height()
		
		if (W != self.storedw) or (H != self.storedh):
			self.hascontacts = False
		
		if not self.hascontacts:
			self.storedw, self.storedh = W, H
			
			edgecontacts = []  # Where the line touches the screen edges
			
			if self.normal[0] == 0.0:
				edgecontacts = [[0, self.pos[1]], [W, self.pos[1]]]
			
			elif self.normal[1] == 0.0:
				edgecontacts = [[self.pos[0], 0], [self.pos[0], H]]
			
			else:
				pdotn = (self.pos[0] * self.normal[0]) + (self.pos[1] * self.normal[1])
				reciprocaln0 = (1.0 / self.normal[0])
				reciprocaln1 = (1.0 / self.normal[1])
				
				# Left-hand side of the screen
				pointl = [0, 0]
				pointl[1] = pdotn * reciprocaln1
				if (pointl[1] >= 0) and (pointl[1] <= H):
					edgecontacts.append(pointl)
				
				# Top of the screen
				pointt = [0, 0]
				pointt[0] = pdotn * reciprocaln0
				if (pointt[0] >= 0) and (pointt[0] <= W):
					edgecontacts.append(pointt)
				
				# Right-hand side of the screen
				pointr = [W, 0]
				pointr[1] = (pdotn - (W * self.normal[0])) * reciprocaln1
				if (pointr[1] >= 0) and (pointr[1] <= H):
					edgecontacts.append(pointr)
				
				# Bottom of the screen
				pointb = [0, H]
				pointb[0] = (pdotn - (H * self.normal[1])) * reciprocaln0
				if (pointb[0] >= 0) and (pointb[0] <= W):
					edgecontacts.append(pointb)

			self.edgecontacts = edgecontacts
			self.hascontacts = True
		
		tempedgecontacts = []
		
		for contact in self.edgecontacts:
			tempedgecontacts.append([offset[0] + contact[0], offset[1] + contact[1]])
		
		if len(tempedgecontacts) >= 2:
			pygame.draw.aalines(display, self.colour, True, tempedgecontacts)
		else:
			pass  # The line must be completely outwith the boundaries of the display
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'normal_x':self.normal[0], 'normal_y':self.normal[1]}, self.keyframes)
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
		self.bounce = newvars['bounce']
		oldnormal = self.normal[:]
		self.normal = [newvars['normal_x'], newvars['normal_y']]
		if self.normal != oldnormal:
			self.hascontacts = False
		
		Obstacle.Update(self)
	
	def OutOfRange(self, pos):
		return (self.GetDist(pos) > MAXDIST)
	
	def InsideObject(self, pos, pradius = 0.0):
		if pradius == 0.0:  # If the particle has no radius, just test whether its centre position has crossed the line
			return (((float(pos[0] - self.pos[0]) * self.normal[0]) + (float(pos[1] - self.pos[1]) * self.normal[1])) <= 0.0)
		
		radialnormal = [self.normal[0] * pradius, self.normal[1] * pradius]
		leftside = [pos[0] + radialnormal[0], pos[1] + radialnormal[1]]
		rightside = [pos[0] - radialnormal[0], pos[1] - radialnormal[1]]
		
		return ((((float(leftside[0] - self.pos[0]) * self.normal[0]) + (float(leftside[1] - self.pos[1]) * self.normal[1])) <= 0.0)
			or (((float(rightside[0] - self.pos[0]) * self.normal[0]) + (float(rightside[1] - self.pos[1]) * self.normal[1])) <= 0.0))
	
	def GetResolved(self, pos, pradius = 0.0):
		if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
			return self.GetResolved([pos[0], pos[1] - 1])
		
		dist = abs(self.GetDist(pos, pradius))
		vec = [dist * self.normal[0], dist * self.normal[1]]
		
		return [pos[0] + vec[0], pos[1] + vec[1]]
	
	def GetNormal(self, pos):
		return self.normal
	
	def GetDist(self, pos, pradius = 0.0):
		v = [float(pos[0] - self.pos[0]), float(pos[1] - self.pos[1])]
		return (v[0] * self.normal[0]) + (v[1] * self.normal[1]) - pradius
	
	def GetForceFactor(self, pos, pradius = 0.0):
		r = self.GetDist(pos) - pradius
		
		if r <= 1.0:
			return 1.0
		
		return (1.0 / pow(r, 3.0))
	
	def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, normal = [None, None], interpolationtype = INTERPOLATIONTYPE_LINEAR):
		if (normal != [None, None]) and (abs(magnitudesquared(normal) - 1.0) >= 0.3):
			normal = normalise(normal)
		return keyframes.CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'normal_x':normal[0], 'normal_y':normal[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'normal_x':self.normal[0], 'normal_y':self.normal[1]})
	
	def SetNormal(self, newnormal):
		self.CreateKeyframe(self.curframe, normal = newnormal)
