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
#include <iostream>
#include <string>

/**
 * Process a single frame pixel by pixel
 * 
 * @param im the original frame as a cv::Mat object
 * @return the processed frame as a cv::Mat object
 **/
cv::Mat process_image(cv::Mat im);

#endif
