### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle effect manager


from src.pyignition import particles, gravity, obstacles, constants
import sys, pygame, xml
from src.pyignition.constants import *


class ParticleEffect:
    def __init__(self, display, pos=(0, 0), size=(0, 0)):
        self.display = display
        self.pos = pos
        self.size = size

        self.left = pos[0]
        self.top = pos[1]
        self.right = pos[0] + size[0]
        self.bottom = pos[1] + size[1]

        self.particles = []
        self.sources = []
        self.gravities = []
        self.obstacles = []

    def Update(self):
        for source in self.sources:
            source.Update()

        for gravity in self.gravities:
            gravity.Update()

        for obstacle in self.obstacles:
            obstacle.Update()

        for particle in self.particles:
            radius = 0.0  # Used for making sure radii don't overlap objects...

            if particle.drawtype == DRAWTYPE_CIRCLE or particle.drawtype == DRAWTYPE_BUBBLE:
                radius = particle.radius * (
                1.0 - RADIUS_PERMITTIVITY)  # ...But only set if the particle is actually circular

            # First calculate the forces acting on the particle
            totalforce = [0.0, 0.0]

            for gravity in self.gravities:
                force = gravity.GetForceOnParticle(particle)
                totalforce[0] += force[0]
                totalforce[1] += force[1]

            for obstacle in self.obstacles:
                force = obstacle.GetForce(particle.pos, particle.velocity, radius)
                totalforce[0] += force[0]
                totalforce[1] += force[1]

            # Apply the forces to the velocity and update the particle
            particle.velocity = [particle.velocity[0] + totalforce[0], particle.velocity[1] + totalforce[1]]

            particle.Update()

            # Resolve collisions
            for obstacle in self.obstacles:
                if (not obstacle.OutOfRange(particle.pos)) and (obstacle.InsideObject(particle.pos, radius)):
                    particle.pos = obstacle.GetResolved(particle.pos, radius)

        # Delete dead particles
        for particle in self.particles:
            if not particle.alive:
                self.particles.remove(particle)

    def Redraw(self):
        for particle in self.particles:
            particle.Draw(self.display)

        for obstacle in self.obstacles:
            obstacle.Draw(self.display)

    def CreateSource(self, pos: object = (0, 0), initspeed: object = 0.0, initdirection: object = 0.0,
                     initspeedrandrange: object = 0.0,
                     initdirectionrandrange: object = 0.0,
                     particlesperframe: object = 0,
                     particlelife: object = -1,
                     genspacing: object = 0,
                     drawtype: object = 0,
                     colour: object = (0, 0, 0),
                     radius: object = 0.0,
                     length: object = 0.0,
                     imagepath: object = None) -> object:
        newsource = particles.ParticleSource(self, pos, initspeed, initdirection, initspeedrandrange,
                                             initdirectionrandrange, particlesperframe, particlelife, genspacing,
                                             drawtype, colour, radius, length, imagepath)
        self.sources.append(newsource)
        return newsource  # Effectively a reference

    def CreatePointGravity(self, strength=0.0, strengthrandrange=0.0, pos=(0, 0)):
        newgrav = gravity.PointGravity(strength, strengthrandrange, pos)
        self.gravities.append(newgrav)
        return newgrav

    def CreateDirectedGravity(self, strength=0.0, strengthrandrange=0.0, direction=[0, 1]):
        newgrav = gravity.DirectedGravity(strength, strengthrandrange, direction)
        self.gravities.append(newgrav)
        return newgrav

    def CreateVortexGravity(self, strength=0.0, strengthrandrange=0.0, pos=(0, 0)):
        newgrav = gravity.VortexGravity(strength, strengthrandrange, pos)
        self.gravities.append(newgrav)
        return newgrav

    def CreateCircle(self, pos=(0, 0), colour=(0, 0, 0), bounce=1.0, radius=0.0):
        newcircle = obstacles.Circle(self, pos, colour, bounce, radius)
        self.obstacles.append(newcircle)
        return newcircle

    def CreateRectangle(self, pos=(0, 0), colour=(0, 0, 0), bounce=1.0, width=0.0, height=0.0):
        newrect = obstacles.Rectangle(self, pos, colour, bounce, width, height)
        self.obstacles.append(newrect)
        return newrect

    def CreateBoundaryLine(self, pos=(0, 0), colour=(0, 0, 0), bounce=1.0, normal=[0, 1]):
        newline = obstacles.BoundaryLine(self, pos, colour, bounce, normal)
        self.obstacles.append(newline)
        return newline

    def AddParticle(self, particle):
        self.particles.append(particle)

    def GetDrawtypeAsString(self, drawtype):
        if drawtype == DRAWTYPE_POINT:
            return "point"
        elif drawtype == DRAWTYPE_CIRCLE:
            return "circle"
        elif drawtype == DRAWTYPE_LINE:
            return "line"
        elif drawtype == DRAWTYPE_SCALELINE:
            return "scaleline"
        elif drawtype == DRAWTYPE_BUBBLE:
            return "bubble"
        elif drawtype == DRAWTYPE_IMAGE:
            return "image"
        else:
            return "ERROR: Invalid drawtype"

    def GetStringAsDrawtype(self, string):
        if string == "point":
            return DRAWTYPE_POINT
        elif string == "circle":
            return DRAWTYPE_CIRCLE
        elif string == "line":
            return DRAWTYPE_LINE
        elif string == "scaleline":
            return DRAWTYPE_SCALELINE
        elif string == "bubble":
            return DRAWTYPE_BUBBLE
        elif string == "image":
            return DRAWTYPE_IMAGE
        else:
            return DRAWTYPE_POINT

    def GetInterpolationtypeAsString(self, interpolationtype):
        if interpolationtype == INTERPOLATIONTYPE_LINEAR:
            return "linear"
        elif interpolationtype == INTERPOLATIONTYPE_COSINE:
            return "cosine"

    def GetStringAsInterpolationtype(self, string):
        if string == "linear":
            return INTERPOLATIONTYPE_LINEAR
        elif string == "cosine":
            return INTERPOLATIONTYPE_COSINE
        else:
            return INTERPOLATIONTYPE_LINEAR

    def TranslatePos(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])

    def ConvertXMLTuple(self, string):
        # 'string' must be of the form "(value, value, value, [...])"
        bracketless = string.replace("(", "").replace(")", "")
        strings = bracketless.split(", ")
        finaltuple = []
        for string in strings:
            temp = string.split(".")
            if len(temp) > 1:
                finaltuple.append(float(string))
            else:
                finaltuple.append(int(string))

        return tuple(finaltuple)

    def SaveToFile(self, outfilename):
        outfile = open(outfilename, 'w')

        outfile.write("<?xml version = \"1.0\"?>\n<?pyignition version = \"%f\"?>\n\n" % PYIGNITION_VERSION)
        outfile.write("<effect>\n")

        # Write out sources
        for source in self.sources:
            outfile.write("\t<source>\n")

            # Write out source variables
            outfile.write("\t\t<pos>(%i, %i)</pos>\n" % source.pos)
            outfile.write("\t\t<initspeed>%f</initspeed>\n" % source.initspeed)
            outfile.write("\t\t<initdirection>%f</initdirection>\n" % source.initdirection)
            outfile.write("\t\t<initspeedrandrange>%f</initspeedrandrange>\n" % source.initspeedrandrange)
            outfile.write("\t\t<initdirectionrandrange>%f</initdirectionrandrange>\n" % source.initdirectionrandrange)
            outfile.write("\t\t<particlesperframe>%i</particlesperframe>\n" % source.particlesperframe)
            outfile.write("\t\t<particlelife>%i</particlelife>\n" % source.particlelife)
            outfile.write("\t\t<genspacing>%i</genspacing>\n" % source.genspacing)
            outfile.write("\t\t<drawtype>%s</drawtype>\n" % self.GetDrawtypeAsString(source.drawtype))
            outfile.write("\t\t<colour>(%i, %i, %i)</colour>\n" % source.colour)
            outfile.write("\t\t<radius>%f</radius>\n" % source.radius)
            outfile.write("\t\t<length>%f</length>\n" % source.length)
            outfile.write("\t\t<imagepath>%s</imagepath>\n" % source.imagepath)

            # Write out source keyframes
            outfile.write("\t\t<keyframes>\n")

            for keyframe in source.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue

                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)

                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (
                        variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))

                outfile.write("\t\t\t</keyframe>\n")

            outfile.write("\t\t</keyframes>\n")

            # Write out source particle keyframes
            outfile.write("\t\t<particlekeyframes>\n")

            for keyframe in source.particlekeyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue

                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)

                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (
                        variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))

                outfile.write("\t\t\t</keyframe>\n")

            outfile.write("\t\t</particlekeyframes>\n")

            outfile.write("\t</source>\n\n")

        # Write out gravities
        for gravity in self.gravities:
            # Identify type
            gtype = gravity.type

            outfile.write("\t<%sgravity>\n" % gtype)

            # Write out gravity variables
            outfile.write("\t\t<strength>%f</strength>\n" % gravity.initstrength)
            outfile.write("\t\t<strengthrandrange>%f</strengthrandrange>\n" % gravity.strengthrandrange)
            if gtype == "directed":
                outfile.write("\t\t<direction>(%f, %f)</direction>\n" % tuple(gravity.direction))
            elif gtype == "point" or gtype == "vortex":
                outfile.write("\t\t<pos>(%i, %i)</pos>\n" % gravity.pos)

            # Write out gravity keyframes
            outfile.write("\t\t<keyframes>\n")

            for keyframe in gravity.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue

                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)

                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (
                        variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))

                outfile.write("\t\t\t</keyframe>\n")

            outfile.write("\t\t</keyframes>\n")

            outfile.write("\t</%sgravity>\n\n" % gtype)

        # Write out obstacles
        for obstacle in self.obstacles:
            # Identify type
            otype = obstacle.type

            outfile.write("\t<%s>\n" % otype)

            # Write out obstacle variables
            outfile.write("\t\t<pos>(%i, %i)</pos>\n" % obstacle.pos)
            outfile.write("\t\t<colour>(%i, %i, %i)</colour>\n" % obstacle.colour)
            outfile.write("\t\t<bounce>%f</bounce>\n" % obstacle.bounce)
            if otype == "circle":
                outfile.write("\t\t<radius>%f</radius>\n" % obstacle.radius)
            elif otype == "rectangle":
                outfile.write("\t\t<width>%i</width>\n" % obstacle.width)
                outfile.write("\t\t<height>%i</height>\n" % obstacle.height)
            elif otype == "boundaryline":
                outfile.write("\t\t<normal>(%f, %f)</normal>\n" % tuple(obstacle.normal))

            # Write out obstacle keyframes
            outfile.write("\t\t<keyframes>\n")

            for keyframe in obstacle.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue

                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)

                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (
                        variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))

                outfile.write("\t\t\t</keyframe>\n")

            outfile.write("\t\t</keyframes>\n")

            outfile.write("\t</%s>\n\n" % otype)

        outfile.write("</effect>")
        outfile.close()

    def LoadFromFile(self, infilename):
        infile = open(infilename, "r")

        data = xml.XMLParser(infile.read()).Parse()
        infile.close()

        for child in data.children:
            if child.tag == "source":  # Source object
                pos = (0, 0)
                initspeed = 0.0
                initdirection = 0.0
                initspeedrandrange = 0.0
                initdirectionrandrange = 0.0
                particlesperframe = 0
                particlelife = 0
                genspacing = 0
                drawtype = DRAWTYPE_POINT
                colour = (0, 0, 0)
                radius = 0.0
                length = 0.0
                imagepath = None

                keyframes = None
                particlekeyframes = None

                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "initspeed":
                        initspeed = float(parameter.inside)
                    elif parameter.tag == "initdirection":
                        initdirection = float(parameter.inside)
                    elif parameter.tag == "initspeedrandrange":
                        initspeedrandrange = float(parameter.inside)
                    elif parameter.tag == "initdirectionrandrange":
                        initdirectionrandrange = float(parameter.inside)
                    elif parameter.tag == "particlesperframe":
                        particlesperframe = int(parameter.inside)
                    elif parameter.tag == "particlelife":
                        particlelife = int(parameter.inside)
                    elif parameter.tag == "genspacing":
                        genspacing = int(parameter.inside)
                    elif parameter.tag == "drawtype":
                        drawtype = self.GetStringAsDrawtype(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "radius":
                        radius = float(parameter.inside)
                    elif parameter.tag == "length":
                        length = float(parameter.inside)
                    elif parameter.tag == "image":
                        imagepath = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                    elif parameter.tag == "particlekeyframes":
                        particlekeyframes = parameter.children

                newsource = self.CreateSource(pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange,
                                              particlesperframe, particlelife, genspacing, drawtype, colour, radius,
                                              length, imagepath)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "initspeed" and variable.inside != "None":
                            variables['initspeed'] = float(variable.inside)
                        elif variable.tag == "initdirection" and variable.inside != "None":
                            variables['initdirection'] = float(variable.inside)
                        elif variable.tag == "initspeedrandrange" and variable.inside != "None":
                            variables['initspeedrandrange'] = float(variable.inside)
                        elif variable.tag == "initdirectionrandrange" and variable.inside != "None":
                            variables['initdirectionrandrange'] = float(variable.inside)
                        elif variable.tag == "particlesperframe" and variable.inside != "None":
                            variables['particlesperframe'] = int(variable.inside)
                        elif variable.tag == "genspacing" and variable.inside != "None":
                            variables['genspacing'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newsource.CreateKeyframe(frame=frame)
                    newframe.variables = variables

                for keyframe in particlekeyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "radius" and variable.inside != "None":
                            variables['radius'] = float(variable.inside)
                        elif variable.tag == "length" and variable.inside != "None":
                            variables['length'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newsource.CreateParticleKeyframe(frame=frame)
                    newframe.variables = variables
                    newsource.PreCalculateParticles()

            elif child.tag == "directedgravity":
                strength = 0.0
                strengthrandrange = 0.0
                direction = [0, 0]

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "direction":
                        direction = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newgrav = self.CreateDirectedGravity(strength, strengthrandrange, direction)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif variable.tag == "direction_x" and variable.inside != "None":
                            variables['direction_x'] = float(variable.inside)
                        elif variable.tag == "direction_y" and variable.inside != "None":
                            variables['direction_y'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newgrav.CreateKeyframe(frame=frame)
                    newframe.variables = variables

            elif child.tag == "pointgravity":
                strength = 0.0
                strengthrandrange = 0.0
                pos = (0, 0)

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newgrav = self.CreatePointGravity(strength, strengthrandrange, pos)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newgrav.CreateKeyframe(frame=frame)
                    newframe.variables = variables

            elif child.tag == "vortexgravity":
                strength = 0.0
                strengthrandrange = 0.0
                pos = (0, 0)

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "pos":
                        direction = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newgrav = self.CreateVortexGravity(strength, strengthrandrange, pos)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newgrav.CreateKeyframe(frame=frame)
                    newframe.variables = variables

            elif child.tag == "circle":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                radius = 0.0

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "radius":
                        radius = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newobstacle = self.CreateCircle(pos, colour, bounce, radius)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "radius" and variable.inside != "None":
                            variables['radius'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newobstacle.CreateKeyframe(frame=frame)
                    newframe.variables = variables

            elif child.tag == "rectangle":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                width = 0.0
                height = 0.0

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "width":
                        width = float(parameter.inside)
                    elif parameter.tag == "height":
                        height = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newobstacle = self.CreateRectangle(pos, colour, bounce, width, height)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "width" and variable.inside != "None":
                            variables['width'] = float(variable.inside)
                        elif variable.tag == "height" and variable.inside != "None":
                            variables['height'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newobstacle.CreateKeyframe(frame=frame)
                    newframe.variables = variables

            elif child.tag == "boundaryline":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                direction = [0.0, 0.0]

                keyframes = None

                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "normal":
                        normal = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children

                newobstacle = self.CreateBoundaryLine(pos, colour, bounce, normal)

                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}

                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "normal_x" and variable.inside != "None":
                            variables['normal_x'] = float(variable.inside)
                        elif variable.tag == "normal_y" and variable.inside != "None":
                            variables['normal_y'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)

                    newframe = newobstacle.CreateKeyframe(frame=frame)
                    newframe.variables = variables


## Begin testing code
if __name__ == '__main__':
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyIgnition demo")
    clock = pygame.time.Clock()
    test = ParticleEffect(screen, (0, 0), (800, 600))
    testgrav = test.CreatePointGravity(strength=1.0, pos=(500, 380))
    testgrav.CreateKeyframe(300, strength=10.0, pos=(0, 0))
    testgrav.CreateKeyframe(450, strength=10.0, pos=(40, 40))
    testgrav.CreateKeyframe(550, strength=-2.0, pos=(600, 480))
    testgrav.CreateKeyframe(600, strength=-20.0, pos=(600, 0))
    testgrav.CreateKeyframe(650, strength=1.0, pos=(500, 380))
    anothertestgrav = test.CreateDirectedGravity(strength=0.04, direction=[1, 0])
    anothertestgrav.CreateKeyframe(300, strength=1.0, direction=[-0.5, 1])
    anothertestgrav.CreateKeyframe(600, strength=1.0, direction=[1.0, -0.1])
    anothertestgrav.CreateKeyframe(650, strength=0.04, direction=[1, 0])
    testsource = test.CreateSource((10, 10), initspeed=5.0, initdirection=2.35619449, initspeedrandrange=2.0,
                                   initdirectionrandrange=1.0, particlesperframe=5, particlelife=125,
                                   drawtype=DRAWTYPE_SCALELINE, colour=(255, 255, 255), length=10.0)
    testsource.CreateParticleKeyframe(50, colour=(0, 255, 0), length=10.0)
    testsource.CreateParticleKeyframe(75, colour=(255, 255, 0), length=10.0)
    testsource.CreateParticleKeyframe(100, colour=(0, 255, 255), length=10.0)
    testsource.CreateParticleKeyframe(125, colour=(0, 0, 0), length=10.0)

    test.SaveToFile("PyIgnition test.ppe")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        test.Update()
        test.Redraw()
        pygame.display.update()
        clock.tick(20)
