### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Gravity objects


from math import sqrt
from src.pyignition import keyframes, interpolate
import random
from src.pyignition.constants import *


def RandomiseStrength(base, range):
	return base + (float(random.randrange(int(-range * 100), int(range * 100))) / 100.0)


class DirectedGravity:
	def __init__(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
		self.type = "directed"
		self.initstrength = strength
		self.strength = strength
		self.strengthrandrange = strengthrandrange
		directionmag = sqrt(direction[0]**2 + direction[1]**2)
		self.direction = [direction[0] / directionmag, direction[1] / directionmag]
		
		self.keyframes = []
		self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.direction)
		self.curframe = 0
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]}, self.keyframes)
		self.initstrength = newvars['strength']
		self.strengthrandrange = newvars['strengthrandrange']
		self.direction = [newvars['direction_x'], newvars['direction_y']]
		
		if self.strengthrandrange != 0.0:
			self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
		
		self.curframe = self.curframe + 1
	
	def GetForce(self, pos):
		force = [self.strength * self.direction[0], self.strength * self.direction[1]]
		
		return force
	
	def GetForceOnParticle(self, particle):
		return self.GetForce(particle.pos)
	
	def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, direction = [None, None], interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'direction_x':direction[0], 'direction_y':direction[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]})
	
	def SetStrength(self, newstrength):
		self.CreateKeyframe(self.curframe, strength = newstrength)
	
	def SetStrengthRandRange(self, newstrengthrandrange):
		self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
	
	def SetDirection(self, newdirection):
		self.CreateKeyframe(self.curframe, direction = newdirection)


class PointGravity:
	def __init__(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		self.type = "point"
		self.initstrength = strength
		self.strength = strength
		self.strengthrandrange = strengthrandrange
		self.pos = pos
		
		self.keyframes = []
		self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
		self.curframe = 0
	
	def Update(self):			
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]}, self.keyframes)
		self.initstrength = newvars['strength']
		self.strengthrandrange = newvars['strengthrandrange']
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		
		if self.strengthrandrange != 0.0:
			self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
		else:
			self.strength = self.initstrength
		
		self.curframe = self.curframe + 1
	
	def GetForce(self, pos):
		distsquared = (pow(float(pos[0] - self.pos[0]), 2.0) + pow(float(pos[1] - self.pos[1]), 2.0))
		if distsquared == 0.0:
			return [0.0, 0.0]
		
		forcemag = (self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL) / (distsquared)
		
		# Calculate normal vector from pos to the gravity point and multiply by force magnitude to find force vector
		dist = sqrt(distsquared)
		dx = float(self.pos[0] - pos[0]) / dist
		dy = float(self.pos[1] - pos[1]) / dist
		
		force = [forcemag * dx, forcemag * dy]
		
		return force
	
	def GetForceOnParticle(self, particle):
		return self.GetForce(particle.pos)
	
	def GetMaxForce(self):
		return self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL
	
	def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, pos = (None, None), interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'pos_x':pos[0], 'pos_y':pos[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]})
	
	def SetStrength(self, newstrength):
		self.CreateKeyframe(self.curframe, strength = newstrength)
	
	def SetStrengthRandRange(self, newstrengthrandrange):
		self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
	
	def SetPos(self, newpos):
		self.CreateKeyframe(self.curframe, pos = newpos)


class VortexGravity(PointGravity):
	def __init__(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		PointGravity.__init__(self, strength, strengthrandrange, pos)
		self.type = "vortex"
		
		self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
	
	def Update(self):			
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]}, self.keyframes)
		self.initstrength = newvars['strength']
		self.strengthrandrange = newvars['strengthrandrange']
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		
		if self.strengthrandrange != 0.0:
			self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
		else:
			self.strength = self.initstrength
		
		self.curframe = self.curframe + 1
	
	def GetForce(self, pos):
		try:
			self.alreadyshownerror
		except:
			print("WARNING: VortexGravity relies upon particle velocities as well as positions, and so its \
				force can only be obtained using GetForceOnParticle([PyIgnition particle object]).".replace("\t", ""))
			self.alreadyshownerror = True
		
		return [0.0, 0.0]
	
	def GetForceOnParticle(self, particle):
		# This uses F = m(v^2 / r) (the formula for centripetal force on an object moving in a circle)
		# to determine what force should be applied to keep an object circling the gravity. A small extra
		# force (self.strength * VORTEX_ACCELERATION) is added in order to accelerate objects inward as
		# well, thus creating a spiralling effect. Note that unit mass is assumed throughout.
		
		distvector = [self.pos[0] - particle.pos[0], self.pos[1] - particle.pos[1]]  # Vector from the particle to this gravity
		try:
			distmag = sqrt(float(distvector[0] ** 2) + float(distvector[1] ** 2))  # Distance from the particle to this gravity
		except:
			return [0.0, 0.0]  # This prevents OverflowErrors
		
		if distmag == 0.0:
			return [0.0, 0.0]
		
		if distmag <= VORTEX_SWALLOWDIST:
			particle.alive = False
		
		normal = [float(distvector[0]) / distmag, float(distvector[1]) / distmag]  # Normal from particle to this gravity
		
		velocitymagsquared = (particle.velocity[0] ** 2) + (particle.velocity[1] ** 2)  # Velocity magnitude squared
		forcemag = (velocitymagsquared / distmag) + (self.strength * VORTEX_ACCELERATION)  # Force magnitude = (v^2 / r) + radial acceleration
		
		#velparmag = (particle.velocity[0] * normal[0]) + (particle.velocity[1] * normal[1])  # Magnitude of velocity parallel to normal
		#velpar = [normal[0] * velparmag, normal[1] * velparmag]  # Vector of velocity parallel to normal
		#velperp = [particle.velocity[0] - velpar[0], particle.velocity[1] - velpar[1]]  # Vector of velocity perpendicular to normal
		#
		#fnpar = [-velperp[1], velperp[0]]  # Force normal parallel to normal
		#fnperp = [velpar[1], -velpar[0]]  # Force normal perpendicular to normal
		#
		#force = [(fnpar[0] + fnperp[0]) * forcemag, (fnpar[1] + fnperp[1]) * forcemag]
		
		force = [normal[0] * forcemag, normal[1] * forcemag]  # Works, but sometimes goes straight to the gravity w/ little spiraling
		
		return force
	
	def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, pos = (None, None), interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'pos_x':pos[0], 'pos_y':pos[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]})
