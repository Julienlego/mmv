### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Keyframe object and generic keyframe creation function


from src.pyignition.constants import *


def CreateKeyframe(parentframes, frame, variables):
    newframe = Keyframe(frame, variables)

    # Look for duplicate keyframes and copy other defined variables
    try:
        oldkey = (keyframe for keyframe in parentframes if keyframe.frame == frame).__next__()
    except StopIteration:
        oldkey = None

    if oldkey != None:
        for var in oldkey.variables.keys():  # For every variable defined by the old keyframe
            if (var not in newframe.variables or newframe.variables[var] == None) and (
                oldkey.variables[var] != None):  # If a variable is undefined, copy its value to the new keyframe
                newframe.variables[var] = oldkey.variables[var]

    # Remove the duplicate keyframe, if it existed
    for duplicate in (keyframe for keyframe in parentframes if keyframe.frame == frame):
        parentframes.remove(duplicate)
        break

    # Append the new keyframe then sort them all by frame
    parentframes.append(newframe)
    sortedframes = sorted(parentframes, key=lambda keyframe: keyframe.frame)
    parentframes[:] = sortedframes

    return newframe  # Return a reference to the new keyframe, in case it's needed


def ConsolidateKeyframes(parentframes, frame, variables):
    newframe = Keyframe(frame, variables)
    parentframes.append(newframe)

    finallist = []  # A truncated list of keyframes

    # Append all the frames which come after the current one to the final list
    for keyframe in parentframes:
        if keyframe.frame >= frame:
            finallist.append(keyframe)

    # Sort the keyframes and give them to the parent object
    sortedframes = sorted(finallist, key=lambda keyframe: keyframe.frame)
    parentframes[:] = sortedframes


class Keyframe:
    def __init__(self, frame=0, variables={}):
        self.frame = frame
        self.variables = variables

        if not ('interpolationtype' in self.variables):
            self.variables['interpolationtype'] = INTERPOLATIONTYPE_LINEAR
