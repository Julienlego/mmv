### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
# 
# Global constants module


# Which version is this?
PYIGNITION_VERSION = 1.0

# Drawtype constants
DRAWTYPE_POINT = 100
DRAWTYPE_CIRCLE = 101
DRAWTYPE_LINE = 102
DRAWTYPE_SCALELINE = 103
DRAWTYPE_BUBBLE = 104
DRAWTYPE_IMAGE = 105

# Interpolation type constants
INTERPOLATIONTYPE_LINEAR = 200
INTERPOLATIONTYPE_COSINE = 201

# Gravity constants
UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL = 1000.0  # Well, Newton got one to make it less stupidly large.
VORTEX_ACCELERATION = 0.01  # A tiny value added to the centripetal force exerted by vortex gravities to draw in particles
VORTEX_SWALLOWDIST = 20.0  # Particles closer than this will be swallowed up and regurgitated in the bit bucket

# Fraction of radius which can go inside an object
RADIUS_PERMITTIVITY = 0.3