# MMV : Midi Music Visualizer
Originally inspired by Stephen Malinowski's Music Animation Machine
http://www.musanim.com/

`MMV` (name pending..) is a MIDI music visualization software that provides meaningful
visualizations based off of musical data contained within MIDI files.

We find there is a general lack of music visualizer programs that
utilize multi-track MIDI files to generate visuals. There is also a
lack of audio visualizers that display meaningful interpretive
information regarding the song being played. `MMV` aims to remedy this.

We hope that using `MMV` will not only be entertaining to watch but also
provide useful visual interpretations of songs for musical analysis.

# Features
**(EVERYTHING IS WIP)**
+ Easy-to-use GUI to select and load preset visualizations and MIDI
(*.mid) files
+ Real-time video and sound playback
+ Audio playback playback powered by soundfounts (*.sf2)
+ Many color options
+ API for making custom visualizations
+ Visualizations included out-of-box:
    + Piano Roll (and variations)
    + Colored Circles which convert note frequency to light
    + Tension and Pitch Space

# License
`MMV` is under the MIT License. (https://opensource.org/licenses/MIT)

# How-To
`MMV` is powered by `Python 3.X` and thus requires the subsequent libraries to operate:
+ Pygame - (for graphics display)
+ wxPython - (for GUI)
+ music21 - (for computational music analysis)
+ fluidsynth - (for audio playback)

