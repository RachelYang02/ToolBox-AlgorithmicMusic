""" Synthesizes a blues solo algorithmically """

from Nsound import *
import numpy as np
from random import choice

def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

        out: the stream to add the note to
        instr: the instrument that should play the note
        key_num: the piano key number (A 440Hzz is 49)
        duration: the duration of the note in beats
        bpm: the tempo of the music
        volume: the volume of the note
    """
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream

# this controls the sample rate for the sound file you will generate
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 16)

bass = GuitarBass(sampling_rate)    # use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
    See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 45               # Let's make a slow blues solo
time = [0.5, 0.8, 0.9, 1.2, 1.5]    # add random swing
volume = [0.5, 0.8, 1.0, 2.0, 2.5, 3.0, 5.0]    # add random dynamics

""" initial conditions """
curr_note = 12 
roots = [0,6,12,18]
add_note(solo, bass, blues_scale[curr_note], 1.0, beats_per_minute, 1.0)

licks = [ [ [3,choice(time)], [-2,choice(time)], [-4,choice(time)], [2,choice(time)], [3,choice(time)] ],
          [ [1,choice(time)], [4,choice(time)], [-2,choice(time)], [1,choice(time)], [1,choice(time)] ],
          [ [-1,choice(time)], [2,choice(time)], [-1,choice(time)], [2,choice(time)], [-1,choice(time)] ],
          [ [2,choice(time)], [-1,choice(time)], [-1,choice(time)],[-1,choice(time)], [2,choice(time)] ] ]

for i in range(20):
    lick = choice(licks)
    for note in lick:
        curr_note += note[0]
        if curr_note < 0 or curr_note > len(blues_scale) - 1:   # keep in index of blues_scale
            curr_note = choice(roots)
        add_note(solo, bass, blues_scale[curr_note], note[1], beats_per_minute, choice(volume))

""" Make it cooler-- adding a backing track and mixing various audio streams """
backing_track = AudioStream(sampling_rate, 1)
Wavefile.read('backing.wav', backing_track)

m = Mixer()

solo *= 0.4     # adjust volumes

m.add(2.25, 0, solo)    # delay solo to sync with backing track
m.add(0, 0, backing_track)

m.getStream(500.0) >> "slow_blues.wav"      # change from blues_solo.wav to slow_blues.wav

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 45				# Let's make a slow blues solo

add_note(solo, bass, blues_scale[0], 1.0, beats_per_minute, 1.0)

solo >> "blues_solo.wav"

