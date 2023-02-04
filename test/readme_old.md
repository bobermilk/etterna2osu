# This project is more of a playground for investigating the following issue

> There is a random offset that comes from audio playback between etterna and osu due to differing audio libraries, that makes the osu songs come about 30-60ms earlier

This is confirmed to be because of etterna and osu decoding the audio files with different libraries as quaver and osu are compatible with one another (they both use bass) while etterna uses libmad and does not use bass.


# Current progress
Managed to generate two raw audio files from libmad (sox) and bass (the program in `OffsetCalculator/` folder) and compare them in audacity or writing to .wav files and comparing them with audio-offset-finder but the offset seems constant, it does not reflect the offset seen in-game. Further investigation is needed please help me gdmeme xD

The problem is probably not from the decoding, rather its the playback that adds latency. etterna uses pulseaudio/jack/alsa its all native. osu use bass i thinks. the best case is, the playback waveforms for both match, we just need a way to do a virtual recording, then compare the first non zero sample
use the osu framework code for reference on how bass is used for audio playback, etterna should be about accurate here for playback offset? 

# Playground structure
- OffsetCalculator/ is the c# code used for bass to decode the audio and write to a raw audio file (unadulterated pcm samples)
- py/etterna2osu.py is the main interface of the project
- py/audio-offset-finder is https://github.com/bbc/audio-offset-finder but with some minor fixes. you can cd into it and run `pip install .` it is a library for calculating offset between .wav files, and it can be used here i guess? maybe not though.
- py/raindrop is the converter used to do the real .sm to .osu, the python wrapper just does it in bulk and edits the timing to fit the offsets, but the offset part of the program is still broken


# Dependencies
- python 3.9, other versions should not exist https://www.python.org/downloads/release/python-390/ scroll down, amd64, needed to run the waveform comparison code
- sox with libmad https://stackoverflow.com/a/23939403
- audacity for comparing the raw waveforms, or aligning video recordings of both games on the same chart with hitsounds so you can tell if the tool works
- c# ide like visual studio, but you can just use msbuild or whatever you want
