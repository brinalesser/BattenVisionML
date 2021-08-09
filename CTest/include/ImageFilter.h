/**
 * Header file for c++ vision program that processes each frame 
 * of a video pixel by pixel
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#ifndef IMAGE_FILTER
#define IMAGE_FILTER

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <string>

#define MAX_COLOR 255
#define MIN_COLOR 0

/**
 * Process a single frame pixel by pixel
 * 
 * @param im the original frame as a cv::Mat object
 * @return the processed frame as a cv::Mat object
 **/
cv::Mat process_image(cv::Mat im);

/**
 * Trackbar callback function
 **/
static void tb_cb(int, void*);

/**
 * Setup trackbar window
 **/
void setup_trackbars();

#endif
