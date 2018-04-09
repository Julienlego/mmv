# Water - collisions demo

import PyIgnition, pygame, sys, math


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: collisions")
clock = pygame.time.Clock()


effect = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
source = effect.CreateSource((0, 0), initspeed = 2.0, initdirection = math.pi, initspeedrandrange = 1.0, initdirectionrandrange = math.pi, particlesperframe = 20, particlelife = 80, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (100, 100, 250), radius = 10.0)
grav = effect.CreateDirectedGravity(0.2, 0.0, [0, 1])
circle1 = effect.CreateCircle((100, 200), (0, 0, 0), bounce = 0.1, radius = 50.0)
circle2 = effect.CreateCircle((400, 100), (0, 0, 0), bounce = 0.1, radius = 50.0)
circle3 = effect.CreateCircle((300, 300), (0, 0, 0), bounce = 0.1, radius = 50.0)
circle4 = effect.CreateCircle((500, 250), (0, 0, 0), bounce = 0.1, radius = 50.0)
circle5 = effect.CreateCircle((150, 400), (0, 0, 0), bounce = 0.1, radius = 50.0)
rect1 = effect.CreateRectangle((500, 450), colour = (100, 200, 200), width = 250.0, height = 100.0, bounce = 0.2)
rect1.CreateKeyframe(200, pos = (400, 100), width = 400.0, interpolationtype = PyIgnition.INTERPOLATIONTYPE_COSINE)
rect1.CreateKeyframe(300, colour = (255, 0, 0))
circle2.CreateKeyframe(250, pos = (400, 500), interpolationtype = PyIgnition.INTERPOLATIONTYPE_COSINE)
circle2.CreateKeyframe(300, colour = (0, 255, 50))
circle4.CreateKeyframe(200, pos = circle4.pos)
circle4.CreateKeyframe(230, pos = (100, 300), interpolationtype = PyIgnition.INTERPOLATIONTYPE_COSINE)
source.CreateParticleKeyframe(60, colour = (100, 100, 250), radius = 10.0)
source.CreateParticleKeyframe(80, colour = (255, 255, 255), radius = 20.0)
line = effect.CreateBoundaryLine((700, 500), colour = (0, 0, 0), bounce = 0.1, normal = [-1.4142, -1.4142])
line.CreateKeyframe(300, normal = [-2, -1])
line.CreateKeyframe(500, normal = [-1, 0])
line2 = effect.CreateBoundaryLine((0, 600), colour = (0, 0, 0), bounce = 0.1, normal = [0, -1])
line3 = effect.CreateBoundaryLine((0, 600), colour = (0, 0, 0), bounce = 0.1, normal = [1, 0])

effect.SaveToFile("Water.ppe")
#effect.LoadFromFile("Water.ppe")


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill((255, 255, 255))
	
	source.SetPos(pygame.mouse.get_pos())
	if source.curframe % 30 == 0:
		source.ConsolidateKeyframes()
        
	effect.Update()
	effect.Redraw()
	pygame.display.update()
	clock.tick(30)
