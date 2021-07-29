# BattenVisionML
Test repo using vision processing on battens

## Description
Various vision processing programs using OpenCV and python3 on a Raspberry Pi with a USB camera. 

## File Structure

### Top Level
```
.
├── Images                      # Images of battens to test code with
├── Old                         # Badly documented older code used for quick tests
                                  - left for reference
├── Videos                      # Videos of battens to test code with

├── BackgroundRemovalTest.py    # Removes a settable background from a video 
                                  - good for stationary camera with unchanging background, changing foreground
├── BattenTest.py               # Attempts to use color filtering + Canny edge detection + contours to detect a stack of battens then identify edges of individual battens
                                  - has trouble finding the stack with a noisy background
├── ColorTest.py                # Attempts to use color filtering to detect a stack of battens, then identify edges of individual battens
                                  - very dependent on lighting
├── ColorTuneBGR.py             # Used to find the BGR color values for an object
├── ColorTuneHSV.py             # Used to find the HSV color values in a frame
├── DetectionMethodsTest.py     # Tests different OpenCV feature and edge detection methods
├── LineMergeTest.py            # An attempt to make edge lines steadier
├── LineTest.py                 # Identifies the location of the gap between battens on close up frames
├── ObjectDetectTest.py         # Object detection using Cascade Classifier
                                  - was unable to create a good enough model for the the battens to be accurately identified
├── PLCTest.py                  # Lights up LEDs on a PLC depending on the location of blue pieces of paper on a white piece of paper (2x8 grid)
├── PencilTest.py               # Detects a stack of pencils on a white sheet of paper, then marks the edges of individual pencils
                                  - proof of concept test
├── README.md
├── TrackbarTest.py             # Show the effect of different values on edge detection
└── mp4Tojpg.py                 # Used to save screenshots from video as jpgs
```
