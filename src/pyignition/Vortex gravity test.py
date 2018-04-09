import pygame, PyIgnition, sys


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

effect = PyIgnition.ParticleEffect(screen)
gravity = effect.CreateVortexGravity(pos = (400, 300), strength = 1.0, strengthrandrange = 0.0)
particles = effect.CreateSource(pos = (0, 0), initspeed = 5.0, initdirectionrandrange = 0.5, particlesperframe = 5, particlelife = 200, drawtype = PyIgnition.DRAWTYPE_LINE, length = 5.0, radius = 5.0)


def Draw():    
    screen.fill((255, 255, 255))
    
    effect.Update()
    effect.Redraw()
    
    pygame.draw.circle(screen, (255, 0, 100), (400, 300), 3)
    
    mpos = pygame.mouse.get_pos()
    #f = gravity.GetForce(mpos)
    #endpos = [mpos[0] + f[0], mpos[1] + f[1]]
    
    #pygame.draw.aaline(screen, (0, 0, 0), mpos, endpos)
    particles.SetPos(mpos)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    Draw()
    pygame.display.update()
    clock.tick(30)
