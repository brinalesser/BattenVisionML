/**
 * Header file for c++ vision program that processes each frame 
 * of a video pixel by pixel
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#ifndef BATTEN_DETECTION
#define BATTEN_DETECTION

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <math.h>

#define MAX_DIST 100

/**
 * Do edge detection and get the lines along the edges of an image
 * 
 * @param im an image
 * @return a vector holding lines represented as a Vec4i
 **/
std::vector<cv::Vec4i> get_lines(cv::Mat im);

/**
 * Merge lines together to get one line where the gap in the battens is
 * 
 * @param lines a vector holding lines represented as a Vec4i
 * @return the merged lines as a vector holding lines represented as a Vec4i
 **/
std::vector<cv::Vec4i> merge_lines(std::vector<cv::Vec4i> lines, int frame_width, int frame_height);

/**
 * Draw lines on an image
 * 
 * @param im an image
 * @param lines the lines to draw on the image
 * @return the image with the lines drawn on it
 **/
cv::Mat draw_lines(cv::Mat im, std::vector<cv::Vec4i> lines);

struct line_t {
	int x_1;
	int x_2;
	int y_1;
	int y_2;
	int x_m;
	int y_m;
	
	bool isNear(const line_t& other){
		return sqrt(pow(x_m - other.x_m, 2) + pow(y_m - other.y_m, 2)) < MAX_DIST;
	}
};

#endif
