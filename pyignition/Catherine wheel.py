# Catherine wheel

import pyignition.PyIgnition as PyIgnition, pygame, sys


screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("PyIgnition demo: catherine wheel")
clock = pygame.time.Clock()

wheel = PyIgnition.ParticleEffect(screen, (0, 0), (600, 600))
flame = wheel.CreateSource((300, 300), initspeed = 20.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.5, particlesperframe = 3, particlelife = 50, drawtype = PyIgnition.DRAWTYPE_SCALELINE, colour = (255, 200, 200), length = 20.0)
sparks = wheel.CreateSource((300, 300), initspeed = 1.0, initdirection = 0.0, initspeedrandrange = 0.9, initdirectionrandrange = 3.141592653, particlesperframe = 1, particlelife = 300, genspacing = 3, drawtype = PyIgnition.DRAWTYPE_IMAGE, imagepath = "spark.png")
wheel.CreateDirectedGravity(strength = 0.05, direction = [0, 1])

velocity = 0.1
maxvelocity = 0.5
acceleration = 0.001


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				wheel.SaveToFile("Test.xml")
	
	flame.SetInitDirection(flame.initdirection + velocity)
	if flame.curframe % 30 == 0:
		flame.ConsolidateKeyframes()
	
	if velocity <= maxvelocity:
		velocity += acceleration
	
	screen.fill((10, 0, 50))
	wheel.Update()
	wheel.Redraw()
	pygame.display.update()
	clock.tick(30)
