# BattenVisionML
Test repo using vision processing on battens

## Description
Various vision processing programs using OpenCV and python3 on a Raspberry Pi with a USB camera. 

## File Structure

```
.
├── CTest                       # C++ code for vision processing
│   ├── build   
│   │   ├── bin                 # Folder containing the binary executables for the c++ programs
│   ├── include
│   │   ├── ImageFilter.h       # Header file for image filtering program
│   │   ├── PLCCommTest.h       # Header file for PLC communication program
│   ├── src
│   │   ├── ImageFilter.cpp     # C++ program to process an image from the raspberry pi usb camera pixel by pixel
│   │   ├── PLCCommTest.cpp     # C++ program to communicate with the PLC

│   ├── CMakeLists.txt          # CMake file for creating executables
│   ├── README.md               # Details on using the libplctag library

├── Images                      # Images of battens to test code with
├── Old                         # Previous versions or quick tests left for reference
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
├── ImageFilter                 # An attempt to process frames pixel by pixel
                                  - too slow using python: see CTest code instead
├── LineMergeTest.py            # An attempt to make edge lines steadier
                                  - slow: see LineTest.py instead
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
