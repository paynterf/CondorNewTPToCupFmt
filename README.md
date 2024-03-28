# CondorNewTPToCupFmt
Python script that converts Condor 'custom' Turnpoints to XCSoar-compatible CUP Format

Many Condor contest tasks utilize custom turnpoints in addition to turnpoints defined in the associated [landscape-name].cup file. These custom turnpoints are typically defined by text blocks provided by the contest organizer like the following:

TP 2 (955 m.)
Heading: 93° for 65.1 km,
Coords: 49.8.359N / 20.14.201E
Classic turnpoint,
min. height: 0 m., max.: 10,000 m.
angle: 360°, radius: 1,000 m.

This script assumes the above block(s) are located in a text file selected by the user, and writes an XCSoar-compatible .CUP formatted line to the user-selected output file, which should have a .CUP extension. The resulting output file can then be used in XCSoar by selecting it as the 'Additional Waypoints' file.
