# Controlled Eruption - PyIgnition beta 1 demo
# Copyright David Barker 2010
#
# Be forewarned - this is quite possibly the messiest code you will see all year.
# Let this mess be a lesson to those who try tostart coding without deciding
# what they're going to code beforehand...

import pyignition.PyIgnition as PyIgnition, pygame, sys, math, random


pygame.font.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition 'Controlled Eruption' demo")
clock = pygame.time.Clock()

curframe = 0
started = False

# 'Press space to start' text
starttextfont = pygame.font.Font("courbd.ttf", 50)
starttext = starttextfont.render("Press space to start", True, (255, 255, 255), (0, 0, 0))
starttextpos = ((400 - (starttext.get_width() / 2)), (300 - (starttext.get_height() / 2)))

# Background
background = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
backgroundsource = background.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = PyIgnition.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
backgroundsource.CreateParticleKeyframe(50, colour = (0, 255, 0), length = 10.0)
backgroundsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
backgroundsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
backgroundsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)
backgroundsource2 = background.CreateSource((790, 10), initspeed = 5.0, initdirection = -2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 0, particlelife = 125, drawtype = PyIgnition.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
backgroundsource2.CreateParticleKeyframe(50, colour = (0, 255, 0), length = 10.0)
backgroundsource2.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
backgroundsource2.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
backgroundsource2.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

# Periodic firework
fireworkcounter = 0.0
fireworkdist = 200.0
firework = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
firework.CreateDirectedGravity(strength = 0.2, direction = [0, 1])
fireworksource = firework.CreateSource((10, 10), initspeed = 8.0, initdirection = 0.0, initspeedrandrange = 2.0, initdirectionrandrange = math.pi, particlesperframe = 0, particlelife = 150, drawtype = PyIgnition.DRAWTYPE_IMAGE, imagepath = "Spark.png")
fireworkblast = background.CreateCircle(pos = (1000, 1000), colour = (0, 0, 0), bounce = 1.5, radius = 100.0)

# Ground-level bubbles
bubbles = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
bubblesource = bubbles.CreateSource(initspeed = 1.0, initdirection = 0.0, initspeedrandrange = 0.5, initdirectionrandrange = math.pi, particlesperframe = 0, particlelife = 200, colour = (200, 255, 200), drawtype = PyIgnition.DRAWTYPE_BUBBLE, radius = 5.0, genspacing = 5)
bubblesource.CreateParticleKeyframe(500, colour = (250, 100, 250))
bubblesource.CreateParticleKeyframe(75, colour = (190, 190, 200))
bubblesource.CreateParticleKeyframe(100, colour = (50, 250, 252))
bubblesource.CreateParticleKeyframe(125, colour = (250, 250, 255))
bubbles.CreateDirectedGravity(strength = 0.04, direction = [0, -1])

# Fire, just for laughs
fire = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
gravity = fire.CreateDirectedGravity(strength = 0.07, direction = [0, -1])
wind = fire.CreateDirectedGravity(strength = 0.05, direction = [1, 0])
source = fire.CreateSource((150, 500), initspeed = 2.0, initdirection = 0.0, initspeedrandrange = 1.0, initdirectionrandrange = 0.5, particlesperframe = 10, particlelife = 100, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100), radius = 3.0)
source.CreateParticleKeyframe(10, colour = (200, 50, 20), radius = 4.0)
source.CreateParticleKeyframe(30, colour = (150, 0, 0), radius = 6.0)
source.CreateParticleKeyframe(60, colour = (50, 20, 20), radius = 20.0)
source.CreateParticleKeyframe(80, colour = (0, 0, 0), radius = 50.0)

# Text
font = pygame.font.Font("euphemia.ttf", 70)
font2 = pygame.font.Font("euphemia.ttf", 40)
text = font.render("PyIgnition", True, (255, 255, 255), (0, 0, 0))
text2 = font2.render("ExeSoft", True, (200, 200, 200), (0, 0, 0))
textalpha = font.render("PyIgnition", True, (255, 255, 255))
text2alpha = font2.render("ExeSoft", True, (200, 200, 200))
temptext = text.copy()
temptext2 = text2.copy()
temptext.set_alpha(0)
temptext2.set_alpha(0)
textpos = ((400 - (text.get_width() / 2)), 250)
textpos2 = (textpos[0] + 110, textpos[1] - 30)
font3 = pygame.font.Font("courbd.ttf", 20)
text3 = font3.render("Version 1.0", True, (200, 200, 255), (0, 0, 0))
textpos3 = ((800 - text3.get_width()) - 5, (600 - text3.get_height()))


def Update():
    global curframe, fireworkcounter, temptext, temptext2
    
    background.Update()

    if curframe == 100:
        backgroundsource2.SetParticlesPerFrame(5)

    fireworksource.SetPos((400 + fireworkdist * math.cos(fireworkcounter), 300 + fireworkdist * math.sin(fireworkcounter)))
    if (curframe > 200) and (curframe % 50 == 0):
        fireworksource.CreateKeyframe(fireworksource.curframe, particlesperframe = 10)
        fireworksource.CreateKeyframe(fireworksource.curframe + 4, particlesperframe = 0)
        firework.Update()
        fireworkblast.SetPos(fireworksource.pos)
        fireworksource.ConsolidateKeyframes()
        #fireworkblast.ConsolidateKeyframes()
    else:
        if curframe % 30 == 0:
            fireworkblast.ConsolidateKeyframes()
        firework.Update()
        fireworkblast.SetPos((1000, 1000))
    fireworkcounter = fireworkcounter + 0.1

    random.seed()
    if curframe == 400:
        bubblesource.SetParticlesPerFrame(1)
    bubbles.Update()
    bubblesource.SetPos((random.randint(0, 800), 600))
    if curframe % 30 == 0:
        bubblesource.ConsolidateKeyframes()

    if curframe > 500:
        fire.Update()
        source.SetPos(pygame.mouse.get_pos())
        if curframe % 30 == 0:
            source.ConsolidateKeyframes()

    if curframe > 400:
        if curframe > 500:
            temptext = textalpha.copy()
            temptext2 = text2alpha.copy()
        else:
            factor = (float(curframe) - 400.0) / 100.0
            if factor > 1.0:
                factor = 1.0
            alpha = int(factor * 255.0)
            temptext = text.copy()
            temptext.set_alpha(alpha)
            temptext2 = text2.copy()
            temptext2.set_alpha(alpha)

    curframe = curframe + 1

def Redraw():
    if curframe > 500:
        screen.blit(text3, textpos3)
    fire.Redraw()
    screen.blit(temptext, textpos)
    screen.blit(temptext2, textpos2)
    background.Redraw()
    firework.Redraw()
    bubbles.Redraw()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                started = True

    screen.fill((0, 0, 0))

    if started:
        Update()
        Redraw()
    else:
        screen.blit(starttext, starttextpos)

    pygame.display.update()
    clock.tick(30)
