# BattenVisionML
Test repo using vision processing on battens

## Description
Various vision processing programs using OpenCV and python3 or C++ on a Raspberry Pi
with a USB camera. For the purpose of detecting battens to pick up with a robotic arm.

## File Structure

```
.
├── CTest                       # C++ code for vision processing
│   ├── build   
│   │   ├── bin                 # Folder containing the binary executables for the c++ programs
│   ├── include
│   │   ├── ImageFilter.h       # Header file for image filtering program
│   │   ├── PLCCommTest.h       # Header file for PLC communication program
│   │   ├── BattenDetection.h   # Header file for baten detection program
│   ├── src
│   │   ├── ImageFilter.cpp     # C++ program to process an image from the raspberry pi usb camera pixel by pixel
│   │   ├── PLCCommTest.cpp     # C++ program to communicate with the PLC
│   │   ├── BattenDetection.cpp # C++ program for batten detection (use close-up view)
│   ├── CMakeLists.txt          # CMake file for creating executables
│   ├── README.md               # Details on using the libplctag library and the C++ code in the CTest folder

├── Images                      # Images of battens to test code with
├── Old                         # Previous versions and quick tests left for reference
├── Videos                      # Videos of battens to test code with

├── BackgroundRemovalTest.py    # Removes a settable background from a video 
                                  - good for stationary camera with unchanging background, changing foreground
├── BattenTest.py               # Attempts to use color filtering + Canny edge detection + contours to detect a stack of battens then identify edges of individual battens
                                  - has trouble finding the stack with a noisy background
├── ColorTest.py                # Attempts to use color filtering to detect a stack of battens, then identify edges of individual battens
                                  - dependent on lighting
├── ColorTuneBGR.py             # Used to find the BGR color values for an object
├── ColorTuneHSV.py             # Used to find the HSV color values in a frame
├── DetectionMethodsTest.py     # Tests different OpenCV library feature and edge detection methods
├── ImageFilter.py              # An attempt to process frames pixel by pixel
                                  - too slow using python: see CTest instead
├── LineMergeTest.py            # An attempt to make edge lines steadier
                                  - slow: see LineTest.py instead
├── LineTest.py                 # Identifies the location of the gap between battens on close up frames
├── ObjectDetectTest.py         # Object detection using Cascade Classifier
                                  - was unable to create a good enough model for the the battens to be accurately identified
├── PLCTest.py                  # Tests communication with PLC merged with vision processing
├── PencilTest.py               # Detects a stack of pencils on a white sheet of paper, then marks the edges of individual pencils
                                  - proof of concept test
├── README.md
├── TrackbarTest.py             # Shows the effects of different values on edge detection
└── mp4Tojpg.py                 # Used to save screenshots from video as jpgs
```
