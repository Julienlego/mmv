### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle and ParticleSource objects


from src.pyignition import keyframes, interpolate
import random, math, pygame
from src.pyignition.constants import *


class Particle:
	def __init__(self, parent, initpos, velocity, life, drawtype = DRAWTYPE_POINT, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None, keyframes = []):
		self.parent = parent
		self.pos = initpos
		self.velocity = velocity
		self.life = life
		self.drawtype = drawtype
		self.colour = colour
		self.radius = radius
		self.length = length
		self.image = image
		
		self.keyframes = []
		self.keyframes.extend(keyframes[:])
		self.curframe = 0
		
		self.alive = True
	
	def Update(self):
		self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
		
		if self.life != -1 and self.curframe > self.life:
			self.alive = False
		else:
			if self.life == -1 and self.curframe >= len(self.parent.particlecache):  # If the particle has infinite life and has passed the last cached frame
				self.colour = (self.parent.particlecache[len(self.parent.particlecache) - 1]['colour_r'], self.parent.particlecache[len(self.parent.particlecache) - 1]['colour_g'], self.parent.particlecache[len(self.parent.particlecache) - 1]['colour_b'])
				self.radius = self.parent.particlecache[len(self.parent.particlecache) - 1]['radius']
				self.length = self.parent.particlecache[len(self.parent.particlecache) - 1]['length']
			else:  # Otherwise, get the values for the current frame
				self.colour = (self.parent.particlecache[self.curframe]['colour_r'], self.parent.particlecache[self.curframe]['colour_g'], self.parent.particlecache[self.curframe]['colour_b'])
				self.radius = self.parent.particlecache[self.curframe]['radius']
				self.length = self.parent.particlecache[self.curframe]['length']
			
			self.curframe = self.curframe + 1
	
	def Draw(self, display):
		offset = self.parent.parenteffect.pos
		
		if (self.pos[0] > 10000) or (self.pos[1] > 10000) or (self.pos[0] < -10000) or (self.pos[1] < -10000):
			return
		
		if self.drawtype == DRAWTYPE_POINT:  # Point
			pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), 0)
			
		elif self.drawtype == DRAWTYPE_CIRCLE:  # Circle
			pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), int(self.radius))
		
		elif self.drawtype == DRAWTYPE_LINE:
			if self.length == 0.0:
				pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), 0)
			
			else:
				# Vector = (velocity / mag(velocity)) * length (a line of magnitude 'length' in
				# direction of velocity); this is calculated as velocity / (mag(velocity) / length)
				# so that parts consistent for both components in the final calculation are only calculated once
				velocitymagoverlength = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2) / self.length
				
				if velocitymagoverlength > 0.0:  # Avoid division-by-zero errors by handling lines with zero velocity separately
					linevec = [(self.velocity[0] / velocitymagoverlength), (self.velocity[1] / velocitymagoverlength)]
				else:
					linevec = [self.length, 0.0]  # Draw a line pointing to the right
				
				endpoint = [offset[0] + int(self.pos[0] + linevec[0]), offset[1] + int(self.pos[1] + linevec[1])]
				pygame.draw.aaline(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), endpoint)
			
		elif self.drawtype == DRAWTYPE_SCALELINE:  # Scaling line (scales with velocity)
			endpoint = [offset[0] + int(self.pos[0] + self.velocity[0]), offset[1] + int(self.pos[1] + self.velocity[1])]
			pygame.draw.aaline(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), endpoint)
			
		elif self.drawtype == DRAWTYPE_BUBBLE:  # Bubble
			if self.radius >= 1.0:
				pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), int(self.radius), 1)
			else:  # Pygame won't draw circles with thickness < radius, so if radius is smaller than one don't bother trying to set thickness
				pygame.draw.circle(display, self.colour, (offset[0] + int(self.pos[0]), offset[1] + int(self.pos[1])), int(self.radius))
		
		elif self.drawtype == DRAWTYPE_IMAGE:  # Image
			size = self.image.get_size()
			display.blit(self.image, (offset[0] + int(self.pos[0] - size[1]), offset[1] + int(self.pos[1] - size[1])))

	def CreateKeyframe(self, frame, colour = (None, None, None), radius = None, length = None):
		keyframes.CreateKeyframe(self.keyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length})


class ParticleSource:
	def __init__(self, parenteffect, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, imagepath = None):
		self.parenteffect = parenteffect
		self.pos = pos
		self.initspeed = initspeed
		self.initdirection = initdirection
		self.initspeedrandrange = initspeedrandrange
		self.initdirectionrandrange = initdirectionrandrange
		self.particlesperframe = particlesperframe
		self.particlelife = particlelife
		self.genspacing = genspacing
		self.colour = colour
		self.drawtype = drawtype
		self.radius = radius
		self.length = length
		self.imagepath = imagepath
		if self.imagepath == None:
			self.image = None
		else:
			self.image = pygame.image.load(self.imagepath).convert_alpha()
		self.drawtype = drawtype
		
		self.keyframes = []
		self.CreateKeyframe(0, self.pos, self.initspeed, self.initdirection, self.initspeedrandrange, self.initdirectionrandrange, self.particlesperframe, self.genspacing)
		self.particlekeyframes = []
		self.particlecache = []
		self.CreateParticleKeyframe(0, colour = self.colour, radius = self.radius, length = self.length)
		self.curframe = 0
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing}, self.keyframes)
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		self.initspeed = newvars['initspeed']
		self.initdirection = newvars['initdirection']
		self.initspeedrandrange = newvars['initspeedrandrange']
		self.initdirectionrandrange = newvars['initdirectionrandrange']
		self.particlesperframe = newvars['particlesperframe']
		self.genspacing = newvars['genspacing']
		
		particlesperframe = self.particlesperframe
		
		if (self.genspacing == 0) or ((self.curframe % self.genspacing) == 0):
			for i in range(0, int(particlesperframe)):
				self.CreateParticle()
		
		self.curframe = self.curframe + 1
	
	def CreateParticle(self):
		if self.initspeedrandrange != 0.0:
			speed = self.initspeed + (float(random.randrange(int(-self.initspeedrandrange * 100.0), int(self.initspeedrandrange * 100.0))) / 100.0)
		else:
			speed = self.initspeed
		if self.initdirectionrandrange != 0.0:
			direction = self.initdirection + (float(random.randrange(int(-self.initdirectionrandrange * 100.0), int(self.initdirectionrandrange * 100.0))) / 100.0)
		else:
			direction = self.initdirection
		velocity = [speed * math.sin(direction), -speed * math.cos(direction)]
		newparticle = Particle(self, initpos = self.pos, velocity = velocity, life = self.particlelife, drawtype = self.drawtype, colour = self.colour, radius = self.radius, length = self.length, image = self.image, keyframes = self.particlekeyframes)
		self.parenteffect.AddParticle(newparticle)

	def CreateKeyframe(self, frame, pos = (None, None), initspeed = None, initdirection = None, initspeedrandrange = None, initdirectionrandrange = None, particlesperframe = None, genspacing = None, interpolationtype = INTERPOLATIONTYPE_LINEAR):
		return keyframes.CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'initspeed':initspeed, 'initdirection':initdirection, 'initspeedrandrange':initspeedrandrange, 'initdirectionrandrange':initdirectionrandrange, 'particlesperframe':particlesperframe, 'genspacing':genspacing, 'interpolationtype':interpolationtype})
	
	def CreateParticleKeyframe(self, frame, colour = (None, None, None), radius = None, length = None, interpolationtype = INTERPOLATIONTYPE_LINEAR):
		newframe = keyframes.CreateKeyframe(self.particlekeyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length, 'interpolationtype':interpolationtype})
		self.PreCalculateParticles()
		return newframe
	
	def GetKeyframeValue(self, keyframe):
		return keyframe.frame
	
	def PreCalculateParticles(self):
		self.particlecache = []  # Clear the cache
		
		# If the particle has infinite life, interpolate for each frame up until its last keyframe
		if self.particlelife == -1:
			particlelife = max(self.particlekeyframes, key = self.GetKeyframeValue).frame
		else:  # Otherwise, interpolate the particle variables for each frame of its life
			particlelife = self.particlelife
		
		for i in range(0, particlelife + 1):
			vars = interpolate.InterpolateKeyframes(i, {'colour_r':0, 'colour_g':0, 'colour_b':0, 'radius':0, 'length':0}, self.particlekeyframes)
			self.particlecache.append(vars)
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing})
	
	def SetPos(self, newpos):
		self.CreateKeyframe(self.curframe, pos = newpos)
	
	def SetInitSpeed(self, newinitspeed):
		self.CreateKeyframe(self.curframe, initspeed = newinitspeed)
	
	def SetInitDirection(self, newinitdirection):
		self.CreateKeyframe(self.curframe, initdirection = newinitdirection)
	
	def SetInitSpeedRandRange(self, newinitspeedrandrange):
		self.CreateKeyframe(self.curframe, initspeedrandrange = newinitspeedrandrange)
	
	def SetInitDirectionRandRange(self, newinitdirectionrandrange):
		self.CreateKeyframe(self.curframe, initdirectionrandrange = newinitdirectionrandrange)
	
	def SetParticlesPerFrame(self, newparticlesperframe):
		self.CreateKeyframe(self.curframe, particlesperframe = newparticlesperframe)
	
	def SetGenSpacing(self, newgenspacing):
		self.CreateKeyframe(self.curframe, genspacing = newgenspacing)
