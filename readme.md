[![logo](https://github.com/bobermilk/etterna2osu/blob/master/icon.ico?raw=true)]()
# etterna2osu 
Advanced converter for etterna charts to osu beatmaps

# Features

## General
- Pretty Terminal GUI
- Bulk pack conversion
- Single chart conversion
- Accurate conversion timings
- Notes are aligned to snaps in editor

## Chart attributes
- Change OD/HP
- Change mapper name
- Change global offset
- Add custom tags to conversions
- Change shlongs to normal notes (short LNs with hold duration not exceeding 1/8 snap)

## Conversion MSD
- Use minacalc v472 as msd calculator (used in etterna 0.72.1)
- Overall MSD in conversion diff names
- Customize specific skillset MSD in conversion difficulty names

## Conversion rates
- Base rate is always converted
- Custom increment for rates
- Filter rates by msd
- Option for audio pitch rates for conversion on rates

# How to run?
## Option 1: Run from prebuild
1. Download etterna2osu.zip from [github releases](https://github.com/bobermilk/etterna2osu/releases)
2. Unzip the contents into a folder
3. Double click on etterna2osu.exe

## Option 2: Run from source
1. Install latest python from [python releases](https://www.python.org/downloads/)
2. Open command prompt
3. Run these commands:
```
git clone https://github.com/bobermilk/etterna2osu/
cd etterna2osu
pip install -r requirements.txt
cd src
python etterna2osu.py
```
# Demo
[![asciicast](https://asciinema.org/a/559338.svg)](https://asciinema.org/a/559338)
# Credits
### DemiFiendSMT, nakadashi, marcino, guilhermeziat, chxu, senya, gonx and messica for feedback
### kangalioo for minacalc C api
### Trippin for beatmap rate changer