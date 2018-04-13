# Wind - randomised gravity

import PyIgnition, pygame, sys


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: wind")
clock = pygame.time.Clock()

effect = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
source = effect.CreateSource((400, 600), initspeed = 5.0, initdirection = 0.0, initspeedrandrange = 2.0, initdirectionrandrange = 0.2, particlesperframe = 10, particlelife = 200, drawtype = PyIgnition.DRAWTYPE_POINT, colour = (255, 255, 200))
grav = effect.CreateDirectedGravity(0.0, 0.2, [1, 0])
#othergrav = effect.CreateDirectedGravity(0.05, 0.0, [0, 1])
circle = effect.CreateCircle((0, 0), (0, 0, 0), bounce = 0.4, radius = 30.0)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				effect.SaveToFile("Test.xml")
	
	screen.fill((100, 125, 200))
	circle.SetPos(pygame.mouse.get_pos())
	if circle.curframe % 30 == 0:
		circle.ConsolidateKeyframes()
	effect.Update()
	effect.Redraw()
	pygame.display.update()
	clock.tick(30)
