# BattenVisionML
Test repo for using vision processing on battens

## Description
Various vision processing programs using OpenCV and python3 or C++ on a Raspberry Pi
with a USB camera. For the purpose of detecting battens to pick up with a robotic arm.

## File Structure

```
.
├── CTest                       # C++ code for vision processing
│   ├── build                   # Folder containing CMake files made by CMakeLists.txt
│   │   ├── bin                 # Folder containing the binary executables for the C++ programs
│   ├── include                 # Folder containing header files for the C++ programs
│   │   ├── ImageFilter.h       # Header file for image filtering program
│   │   ├── PLCCommTest.h       # Header file for PLC communication program
│   │   ├── BattenDetection.h   # Header file for baten detection program
│   ├── src                     # Folder containing source code for the C++ programs
│   │   ├── ImageFilter.cpp     # program to process an image from the raspberry pi usb camera pixel by pixel
│   │   ├── PLCCommTest.cpp     # program to communicate with the PLC
│   │   ├── BattenDetection.cpp # program for batten detection (use close-up view)
│   ├── CMakeLists.txt          # CMake file for creating executables
│   ├── README.md               # Details on using the libplctag library and the C++ code in the CTest folder
├── Images                      # Folder containing images of battens to test code with
├── Old                         # Folder containing previous versions and quick tests left for reference
├── Videos                      # Folder containing videos of battens to test code with
├── BackgroundRemovalTest.py    # Removes a settable background from a video (useful for stationary camera and unchanging background)
├── BattenTest.py               # Attempt to use color filtering + Canny edge detection + contours to detect a stack of battens then identify edges of individual battens
├── ColorTest.py                # Attempt to use color filtering to detect a stack of battens, then identify edges of individual battens
├── ColorTuneBGR.py             # Used to find the BGR color values in a frame
├── ColorTuneHSV.py             # Used to find the HSV color values in a frame
├── DetectionMethodsTest.py     # Tests and displays different OpenCV library feature and edge detection methods
├── ImageFilter.py              # Attempt to process frames pixel by pixel (too slow using python: see CTest instead)
├── LineTest.py                 # Identifies the location of the gap between battens in close up frames
├── ObjectDetectTest.py         # Object detection using Cascade Classifier (was unable to create a good enough model for the the battens to be accurately identified)
├── PLCTest.py                  # Tests communication with PLC merged with vision processing
├── PencilTest.py               # Detects a stack of pencils on a white sheet of paper, then marks the edges of individual pencils (proof of concept test)
├── README.md                   # This
├── TrackbarTest.py             # Shows the effects of different values on edge detection
└── mp4Tojpg.py                 # Used to save screenshots from video as jpgs
```
