/**
 * Header file for c++ vision program that processes each frame 
 * of a video pixel by pixel
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#ifndef SIMPLE_IMAGE_FILTER
#define SIMPLE_IMAGE_FILTER

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

#define MAX_COLOR 255
#define MIN_COLOR 0

#define BLUE_MIN 0
#define BLUE_MAX 255
#define GREEN_MIN 0
#define GREEN_MAX 255
#define RED_MIN 0
#define RED_MAX 200

/**
 * Process a single frame pixel by pixel
 * 
 * @param im the original frame as a cv::Mat object
 * @return the processed frame as a cv::Mat object
 **/
cv::Mat process_image(cv::Mat im);


#endif
