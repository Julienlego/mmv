# Bubbles!

import src.pyignition.PyIgnition as PyIgnition, pygame, sys, math


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: bubbles")
clock = pygame.time.Clock()

effect = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
source = effect.CreateSource(initspeed = 1.0, initdirection = 0.0, initspeedrandrange = 0.5, initdirectionrandrange = math.pi, particlelife = 1000, colour = (200, 255, 200), drawtype = PyIgnition.DRAWTYPE_BUBBLE, radius = 4.0)
source.CreateParticleKeyframe(500, colour = (250, 100, 250))
source.CreateParticleKeyframe(75, colour = (190, 190, 200))
source.CreateParticleKeyframe(100, colour = (50, 250, 252))
source.CreateParticleKeyframe(125, colour = (250, 250, 255))
effect.CreateDirectedGravity(strength = 0.04, direction = [0, -1])


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			source.CreateKeyframe(source.curframe + 1, pos = pygame.mouse.get_pos(), particlesperframe = 1)
			source.CreateKeyframe(source.curframe + 2, pos = pygame.mouse.get_pos(), particlesperframe = 0)
	
	screen.fill((100, 150, 255))
	effect.Update()
	effect.Redraw()
	pygame.display.update()
	clock.tick(30)
