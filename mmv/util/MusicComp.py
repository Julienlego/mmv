#!/usr/bin/env python
#############################################################
#                                                           #
#         !!! FOR COMPUTATIONAL MUSIC ANALYSIS!!!           #
#                                                           #
#############################################################
import music21
import math
import mmv.core.VizNote as vn


def get_chord(notes):
    note_names = []
    for note in notes:
        if isinstance(note, music21.note.Note):
            note_names.append(note.name)
        elif isinstance(note, vn.VizNote):
            note_names.append(note.note.name)

    if len(note_names) > 0:
        chord = music21.chord.Chord(note_names)
        return chord
    return None


def get_recent_notes(notes, num=5):
    index = abs(num) * -1
    previous_notes = notes[index:]
    return previous_notes


def get_average_note(track):
    """
    Returns average note in a given track. Track must be a part from a score.
    """
    midi_sum = 0
    num_notes = 0
    for note in track.notes:
        # if not isinstance(n, music21.note.Rest):
        #     num_notes += 1
        if not isinstance(note, music21.note.Rest):
            midi = 0
            if isinstance(note, music21.chord.Chord):
                s = 0
                for p in note.pitches:
                    s += p.midi
                midi = s // len(note.pitches)
            if isinstance(note, music21.note.Note):
                midi = note.pitch.midi
            midi_sum += midi
            num_notes += 1

    new_p = midi_sum // num_notes
    return music21.note.Note(new_p)


def get_pos_on_circle_of_fifths(note, origin, radius, key, quality=None):

    if isinstance(note, vn.VizNote):
        pitch = note.note.pitch.midi
    elif isinstance(note, music21.note.Note):
        pitch = note.pitch.midi
    else:
        pitch = note

    pitch = pitch % 12

    # have the tonic of the key on top of the circle
    if key is not None:
        tonic_pitch = key.tonic.pitchClass
        relative_pitch = (pitch - tonic_pitch) % 12
        relative_position = convert_pitch_to_circle_position(relative_pitch, quality)

        if quality == 'major':
            radius *= 0.82
        elif quality == 'minor':
            radius *= 0.5
        elif quality == 'diminished':
            radius *= 0.3
        else:
            radius *= 0.0

        x = origin[0] + (radius * math.cos(math.radians(-90 + (30 * relative_position))))
        y = origin[1] + (radius * math.sin(math.radians(-90 + (30 * relative_position))))

        x = int(x)
        y = int(y)

        return x, y

    # if there is no specified key, just go by the pitch itself, meaning C is on top
    else:
        x = origin[0] + (radius * math.cos(math.radians(-90 + (30 * pitch))))
        y = origin[1] + (radius * math.sin(math.radians(-90 + (30 * pitch))))

        x = int(x)
        y = int(y)

        return x, y


def get_diatonic_circle_level(note=None):
    """
    Returns the diatonic circle level of the given music21 note.
    """
    name = note.name
    val = 0     # start at C = 0
    if name is 'G':
        val = 1
    elif name is 'D':
        val = 2
    elif name is 'A':
        val = 3
    elif name is 'E':
        val = 4
    elif name is 'B':
        val = 5
    elif name is ('G-' or 'F#'):
        val = 6
    elif name is 'D-':
        val = 7
    elif name is 'A-':
        val = 8
    elif name is 'E-':
        val = 9
    elif name is 'B-':
        val = 10
    elif name is 'F':
        val = 11

    return val


def convert_pitch_to_circle_position(pitch, quality=None):
    """
    Converts a pitch (assumes already normalized to key) to a position on the circle of fifths.
    """
    if pitch % 2 == 0:
        absolute_pitch = pitch
    else:
        absolute_pitch = (pitch - 6) % 12

    if quality == 'major':
        # print("QUALITY: major--------------------------------")
        pass

    if quality == 'minor':
        absolute_pitch -= 3
        # print("QUALITY: minor--------------------------------")

    elif quality == 'diminished':
        absolute_pitch -= 5
        # print("QUALITY: diminished--------------------------------")

    elif quality != 'major':
        # print("QUALITY: other--------------------------------")
        pass

    return absolute_pitch


def get_dissonance_of_note(note, viz_manager, notes=None):
    if isinstance(note, vn.VizNote):
        pitch = note.note.pitch.midi % 12
    elif isinstance(note, music21.note.Note):
        pitch = note.pitch.midi % 12
    else:
        pitch = note % 12

    key_num = viz_manager.key.tonic.pitchClass

    distance_from_key = abs(convert_pitch_to_circle_position(pitch) - convert_pitch_to_circle_position(key_num))
    if distance_from_key > 6:
        distance_from_key = 12 - distance_from_key

    recent_notes = get_recent_notes(notes)
    chord = get_chord(recent_notes)
    root = chord.root()
    root_note = music21.note.Note(root)
    root_pitch = root_note.pitch.midi % 12

    dissonance = (convert_pitch_to_circle_position(pitch) - convert_pitch_to_circle_position(root_pitch)) % 12

    return distance_from_key + dissonance


def get_chromatic_circle_level(note=None):
    """

    """
    name = note.name
    val = 0  # start at C = 0
    if name is ('C#' or 'D-'):
        val = 1
    elif name is 'D':
        val = 2
    elif name is ('D#' or 'E-'):
        val = 3
    elif name is 'E':
        val = 4
    elif name is 'F':
        val = 5
    elif name is ('G-' or 'F#'):
        val = 6
    elif name is 'G':
        val = 7
    elif name is ('A-' or 'G#'):
        val = 8
    elif name is 'A':
        val = 9
    elif name is ('B-' or 'A-'):
        val = 10
    elif name is 'B':
        val = 11

    return val


def get_pitch_distance(pitch1=None, pitch2=None):
    """
    Sums up the number of moves on the diatonic and chromatic circle of fifths between the two music21 pitches.
    """
    note1_dia_lvl = get_diatonic_circle_level(pitch1)
    note2_dia_lvl = get_diatonic_circle_level(pitch2)
    dia_dist = abs(note1_dia_lvl - note2_dia_lvl)

    note1_chr_lvl = get_chromatic_circle_level(pitch1)
    note2_chr_lvl = get_chromatic_circle_level(pitch2)
    chr_dist = abs(note1_chr_lvl - note2_chr_lvl)

    return dia_dist + chr_dist


def get_note_distance(note1=None, note2=None):
    """
    Calculates the distance between two notes.
    """
    return get_pitch_distance(note1, note2)


def get_chord_distance(chord=None, chord2=None):
    """
    Attempted implementation of the chord distance rule from the Cornell paper.

    Calculates distance between notes using the Diatonic chord istance rule from the Cornell paper. The rule is a
    stated: F(x, y) = i + j + k, where
        - i = the number of moves on the circle of fifths at the diatonic level
        - j = the number of moves on the cycle of fifths at the chromatic level
        - k = the number of non-common pitch classes in the basic space of y compared to the basic space of x
    """
    # Find root of each chord
    root_chord1 = chord.root()
    root_chord2 = chord2.root()

    # Sum of moves on both circles
    circle_sum = get_pitch_distance(root_chord1, root_chord2)

    # Count non-common pitch classes in both y and x
    num_noncom_pitch = 0
    for p in chord.pitches:
        if p not in chord2.pitches:
            num_noncom_pitch += 1
    for p in chord2.pitches:
        if p not in chord.pitches:
            num_noncom_pitch += 1

    return circle_sum + (num_noncom_pitch // 2)


def get_surface_tension(viz_note=None, prev_notes_played=None, scorekey=None):
    """
    Calculates the surface tension of a note using the Surface tension rule from the Cornell paper, which states:

    F(x) = scale degree + inversion + non-harmonic tones summed over all pitch classes in x, where
        - scale degree = 1 if scale degree is 3 or 5 in the melodic voice, 0 otherwise
        - inversion = 2 if 3rd of 5th inversion, 0 otherwise
        - non-harmonic tone = 3 if pitch class is a diatonic non-chord tone, 4 if it is a chromatic non-chord tone,
          0 otherwise

    Parts of the rule are improvised due to lack of musical and technical expertise.
    """
    # First, figure out if we're dealing with a chord
    chord = find_chord_from_viznote(viz_note, prev_notes_played)
    scale = music21.scale.ConcreteScale(scorekey)   # scale the song is in

    score = 0
    sd = 0

    if chord is None:      # It's a single note that doesn't belong to any chord in the track
        note = viz_note.note
        # pc = note.pitch.pitchClass

        # Determine scale degree
        sd = scale.getScaleDegreeFromPitch(note.pitch)

        # Since we can't inverse a note, just add 1 because the note stands out
        score += 1

        # Determine if the note is a diatonic or chromatic non-chord tone, or not
        if note.pitch.accidental:     # note has accidental, meaning it's chromatic
            score += 3
        else:                           # note is diatonic
            score += 2

    elif chord.pitches is not None:                   # note belongs to a chord, so use the chord
        root_pitch = chord.root()
        root_pc = root_pitch.pitchClass

        # Determine the scale degree of the chord's melodic note/voice
        # Using highest pitch in chord as melodic note
        chord = chord.sortAscending()
        if scale._abstract is not None:
            sd = scale.getScaleDegreeFromPitch(chord.pitches[-1])

        # Determine the chord's inversion
        inv = chord.inversion()
        if inv is (3 or 5):
            score += 2

        # Determine if a pitch class in the chord is a diatonic or chromatic non-chord tone or neither
        pc = chord.pitchClasses
        ideal_chord = music21.chord.Chord([root_pc, root_pc+2, root_pc+4])
        # Is any pitch class in the ideal
        for x in pc:
            is_non_chord = True
            for y in ideal_chord.pitchClasses:
                if x is y:
                    is_non_chord = False
            if is_non_chord is True:
                # Determine if non-chord pitch is diatonic or chromatic
                index = pc.index(x)
                pitch = chord.pitches[index]       # get pitch in chord from pitch class
                if pitch.accidental:  # note has accidental, meaning it's chromatic
                    score += 4
                else:  # note is diatonic
                    score += 3

    if sd is (3 or 5):
        score += 1

    return score


def find_chord_from_viznote(viz_note, prev_notes_played):
    """
    Sees if the note belongs to a chord by looking for other notes played that have
    the same offset and are from the same track.

    Returns a chord object containing the notes that are in the chord. Returns Nonte
    if the note doesn't belong to a chord.
    """
    offset = viz_note.note.offset
    track = viz_note.track
    notes = []

    for vn in prev_notes_played:
        if (vn.track == track) and (vn.note.offset == offset):
            notes.append(vn.note)

    if not notes:
        return None
    else:
        return music21.chord.Chord(notes)


def get_melodic_attraction(pitch1=None, pitch2=None):
    """
    Attempted implementation of the melodic attraction rule from the Cornell paper.

    F(p1, p2) = (s1 / s2) x (1 / n^2), where
        - p1 /= p2
        - s1 = anchoring strength of p1
        - s2 = anchoring strength of p2
        - n = number of semitone intervals between p1 and p2

    The anchoring strength of a pitch is relative to its pitch class.

    This function might be biased towards major scales (assume everything is in major)
    """
    if pitch1 == pitch2:
        return None

    tension_sequence = [4, 1, 2, 1, 3, 2, 1, 3, 1, 2, 1, 2, 4]         # For all major scales in I/C
    p1 = tension_sequence[pitch1.pitchClass]
    p2 = tension_sequence[pitch2.pitchClass]
    n = abs(pitch1.midi - pitch2.midi)

    return (p1 / p2) * (1 / n ^ 2)


def get_harmonic_attraction(pitch1=None, pitch2=None):
    """
    Attempted implementation of the harmonic attraction rule from the Cornell paper.

    F(p1, p2) = 10 x [a(p1, p2) / o(p1, p2)], where
        - a = sum of realized voice-leading attractions for all voices in p1
        - o = distance from p1 to p2
    """
    # Calculate sum of melodic attraction between all pitches between pitch1 and pitch2
    sum = 0
    for x in range(pitch1.midi, pitch2.midi, 1):
        a = music21.pitch.Pitch(x)
        b = music21.pitch.Pitch(x+1)
        val = get_melodic_attraction(a, b)
        if val is not None:
            sum += val

    c = music21.note.Note(pitch1)
    d = music21.note.Note(pitch2)
    result = sum / get_note_distance(c, d)
    return 10 * result


def get_local_hierarchical_tension(viz_note=None, prev_notes_played=None):
    """
    Calculates the local tension of the note hierrarchicaly using the hierarchical tension rule from the Cornell paper.

    F(x) = d(x2, x) + s(x), where
        - x = the target note
        - d = the distance between x and x2
        - x2 = the chord that directly dominates x in the prolongational tree
        - s = tje surface tension associated with x
    """
    pass


def get_global_hierarchical_tension(viz_note=None, prev_notes_played=None):
    """
    Calculates the local tension of the note hierrarchicaly using the hierarchical tension rule from the Cornell paper.

    F(x) = l(x) + u(x), where
        - x = the target note
        - l = the local tension associated with x
        - u = the sum of distance values inherited by x from chords that dominate x2
        - x2 = the chord that directly dominates x in the prolongational tree
    """
    pass


def get_sequential_tension(target_viz_note=None, prev_notes_played=None, key=None):
    """
    Calculates the tension of a note sequentially using the sequential tension rule from the Cornell paper.

    F(x) = d(x2, x) + s(x), where
        - x = the target chord
        - d = the distance between x and x2
        - x2 = the chord that immediately precedes y in the sequence
        - s = the surface tension associated with x

    First, we need to determine if the target is a note or belongs to a chord since the Cornell paper mainly deals
    with chords and our program iterates through a flat list of all the notes in the track, striped from their chord.
    If the target note doesn't belong to a chord at all, then we need to improvise so a note's pitch can be used.
    """
    temp = find_chord_from_viznote(target_viz_note, prev_notes_played)
    dist = 0
    if temp is None:        # standalone note
        prec_note = prev_notes_played[:1]
        dist = get_note_distance(prec_note.note, target_viz_note.note) + \
               get_surface_tension(target_viz_note, prev_notes_played)
        return dist
    else:                   # chord
        # get preceding note or chord
        i = 1
        temp2 = find_chord_from_viznote(prev_notes_played[len(prev_notes_played) - i], prev_notes_played)
        while (temp == temp2) and (temp2 is not None):
            temp2 = find_chord_from_viznote(prev_notes_played[len(prev_notes_played) - i], prev_notes_played)
        if temp2 is None:       # what precedes the target is a note!
            prec_note = prev_notes_played[len(prev_notes_played) - i]
            pc = prec_note.pitchClass
            ideal_chord = music21.chord.Chord([pc, pc + 2, pc + 4])
            return get_chord_distance(temp, ideal_chord) + get_surface_tension(target_viz_note, prev_notes_played, key)
        else:                   # what precedes the target is another chord!
            return get_chord_distance(temp, temp2) + get_surface_tension(target_viz_note, prev_notes_played, key)


def create_chord_from_note(root_note=None):
    """
    Creates and returns a normal chord with the given note as its root.
    """
    pass


def analyze_key(score):
    if isinstance(score, music21.stream.Score):
        key = score.analyze('key')
        return key
