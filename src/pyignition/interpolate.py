### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
# 
# Utility module for interpolating between keyframed values


import math
from src.pyignition.constants import *


def LinearInterpolate(val1, val2, t):
    diff = val2 - val1
    dist = float(diff) * t

    return val1 + dist


def CosineInterpolate(val1, val2, t):
    amplitude = float(val2 - val1) / 2.0
    midpoint = float(val1 + val2) / 2.0

    return (amplitude * math.cos(math.pi * (1.0 - t))) + midpoint


def LinearInterpolateKeyframes(curframe, key1, key2, val1, val2):
    if key1 == key2:
        return val2

    factor = float(curframe - key1) / float(key2 - key1)

    return LinearInterpolate(val1, val2, factor)


def CosineInterpolateKeyframes(curframe, key1, key2, val1, val2):
    if key1 == key2:
        return val2

    factor = float(curframe - key1) / float(key2 - key1)

    return CosineInterpolate(val1, val2, factor)


def InterpolateKeyframes(curframe, variables, keyframes):
    if len(keyframes) == 1:
        return keyframes[0].variables

    finalvariables = {}

    if not ('interpolationtype' in variables):
        variables['interpolationtype'] = INTERPOLATIONTYPE_LINEAR

    keys = variables.keys()

    for key in keys:  # Determine current keyframe and next one for this variable
        curkeyframe = None
        nextkeyframe = None

        for i in range(len(keyframes)):
            try:
                frame = keyframes[i]
                if (frame.variables[key] != None):  # If the current keyframe has a keyed value for the current variable
                    if frame.frame <= curframe:  # If its frame is below or equal to the current, it is the current keyframe
                        curkeyframe = i
                    if (nextkeyframe == None) and (
                        frame.frame > curframe):  # If this is the first keyframe with a frame higher than the current, it is the next keyframe
                        nextkeyframe = i
            except KeyError:
                pass

        if nextkeyframe == None or key == "interpolationtype":  # If there is no next key frame, maintain the value specified by the current one
            finalvariables[key] = keyframes[curkeyframe].variables[
                key]  # (Also do this if it is an interpolation type variable; they should only change once their next keyframe has been reached

        else:  # Interpolate between the current and next keyframes
            if keyframes[nextkeyframe].variables['interpolationtype'] == INTERPOLATIONTYPE_LINEAR:
                finalvariables[key] = LinearInterpolateKeyframes(curframe, keyframes[curkeyframe].frame,
                                                                 keyframes[nextkeyframe].frame,
                                                                 keyframes[curkeyframe].variables[key],
                                                                 keyframes[nextkeyframe].variables[key])
            elif keyframes[nextkeyframe].variables['interpolationtype'] == INTERPOLATIONTYPE_COSINE:
                finalvariables[key] = CosineInterpolateKeyframes(curframe, keyframes[curkeyframe].frame,
                                                                 keyframes[nextkeyframe].frame,
                                                                 keyframes[curkeyframe].variables[key],
                                                                 keyframes[nextkeyframe].variables[key])

    return finalvariables
