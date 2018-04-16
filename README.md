## MMV : Midi Music Visualizer

This project was initially by Julien G. and Daniel K. for their
Comp. Sci. & Innov. Major at
[Champlain College](https://www.champlain.edu/).
Originally inspired by Stephen Malinowski's Music Animation Machine
http://www.musanim.com/.

`MMV` is a MIDI music visualization software that provides meaningful
visualizations based off of musical data contained within MIDI files.

We find there is a general lack of music visualizer programs that
utilize multi-track MIDI files to generate visuals. There is also a
lack of audio visualizers that display meaningful interpretive
information regarding the song being played. `MMV` aims to remedy this.

We hope that using `MMV` will not only be entertaining to watch but also
provide useful visual interpretations of songs for musical analysis.

### Features
+ Easy-to-use GUI to select and load preset visualizations and MIDI
(*.mid) files.
+ Real-time visual and audio playback.
+ Visualizations that provide meaningful visualizations of what you are
hearing.

### Upcoming Features
+ Use [pyfluidsynth](https://pypi.python.org/pypi/pyFluidSynth) with soundfonts (*.sf2) files for much better audio playback.
+ Awesome particle effects in visualizations.

### Quick Start
For now if you want to work with `MMV`, you need to have `Python 3.X` installed,
 an IDE (we recommend pycharm), and the subsequent libraries to operate:
+ [Pygame](https://www.pygame.org/news) - for graphics display and audio playback
+ [wxPython](https://www.wxpython.org/) - for user interface (GUI)
+ [music21](http://web.mit.edu/music21/) - for computational music analysis

### License
[LGPL](https://www.gnu.org/licenses/lgpl-3.0)