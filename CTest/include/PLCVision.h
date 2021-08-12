/**
 * Header file for the c++ program that 
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#ifndef PLC_VISION
#define PLC_VISION

//Vision Processing Library
#include <opencv2/opencv.hpp>

//PLC Communication Library
#include <libplctag.h>

//Standard Libraries
//#include <stdio.h>
//#include <stdlib.h>
#include <unistd.h>
//#include <stdint.h>
#include <iostream>
#include <string>
//#include <vector>
//#include <math.h>

//plc params
#define REQUIRED_VERSION		2,1,0
#define DATA_TIMEOUT			5000
#define TAG_OFFSET				0

//frame params
#define PAGE_WIDTH				11
#define PAGE_HEIGHT				17
#define PIXEL_WIDTH_PER_PAGE	200
#define PIXEL_HEIGHT_PER_PAGE	275
#define X_OFFSET				0
#define Y_OFFSET				0
#define X_INCREMENT				(PIXEL_WIDTH_PER_PAGE / PAGE_WIDTH)
#define Y_INCREMENT				(PIXEL_HEIGHT_PER_PAGE / PAGE_HEIGHT)
#define MIN_AREA				20

//color params (bgr)
#define MIN_BLUE				252
#define MAX_BLUE				256
#define MIN_GREEN				252
#define MAX_GREEN				256
#define MIN_RED					205
#define MAX_RED					220

//color params (hsv)
#define MIN_HUE					70
#define MAX_HUE					90
#define MIN_SATURATION			15
#define MAX_SATURATION			60
#define MIN_VALUE				245
#define MAX_VALUE				255

/**
 * A struct that holds the a coordinate point relative to the corner
 * of a pice of paper in inches and the grid index for a 2x8 grid
 * oriented in the manner shown here:
 * 
 * 				+-------+-------+
 * 				+   0   +   8   +
 * 				+-------+-------+
 *	 			+   1   +   9   +
 * 				+-------+-------+
 * 				+   2   +   10  +
 * 				+-------+-------+
 * 				+   3   +   11  +
 * 				+-------+-------+
 * 				+   4   +   12  +
 * 				+-------+-------+
 * 				+   5   +   13  +
 * 				+-------+-------+
 * 				+   6   +   14  +
 * 				+-------+-------+
 * 				+   7   +   15  +
 * 				+-------+-------+
 * 
**/
struct grid_point_t {
	double x;
	double y;
	int grid_idx;
	grid_point_t() : x(0), y(0), grid_idx(0) {
	}
	grid_point_t(cv::Point point, int width, int height) {
		//round x and y to 2 decimal places
		x = X_OFFSET + ((double)point.x / X_INCREMENT);
		y = Y_OFFSET + ((double)point.y / Y_INCREMENT);
		//calculate grid position for 2x8 grid
		if(point.x < (width/2)){
			if(point.y < (height*0.125))		{ grid_idx = 0; }
			else if(point.y < (height*0.25))	{ grid_idx = 1; }
			else if(point.y < (height*0.375))	{ grid_idx = 2; }
			else if(point.y < (height*0.5))		{ grid_idx = 3; }
			else if(point.y < (height*0.625))	{ grid_idx = 4; }
			else if(point.y < (height*0.75))	{ grid_idx = 5; }
			else if(point.y < (height*0.875))	{ grid_idx = 6; }
			else 								{ grid_idx = 7; }
		}
		else{
			if(point.y < (height*0.125))		{ grid_idx = 8; }
			else if(point.y < (height*0.25))	{ grid_idx = 9; }
			else if(point.y < (height*0.375))	{ grid_idx = 10; }
			else if(point.y < (height*0.5))		{ grid_idx = 11; }
			else if(point.y < (height*0.625))	{ grid_idx = 12; }
			else if(point.y < (height*0.75))	{ grid_idx = 13; }
			else if(point.y < (height*0.875))	{ grid_idx = 14; }
			else 								{ grid_idx = 15; }
		}
	}
};

/**
 * Print help message for command line arguments
 * 
 * @param prog the name of the program
 * @param opt the option that caused the error
**/
static void usage(std::string str, std::string opt);

/**
 * Setup to communicate with plc
 * 
 * @param tag the tag handle
 * @param attr_str the attribute string for the PLC tag: see libplctag 
 * documentation for more info: https://github.com/libplctag/libplctag
 * @return error code: 0 for success, -1 for incompatible library version,
 * -2 for tag creation error, -3 for tag status error after creation
**/
int plc_setup(int32_t &tag, const char * attr_str);

/**
 * Find the dimensions and location of the background
 * 
 * @param im the video frame
 * @return the bounding rectangle for the white sheet of paper
 * or an empty rectangle if no contours were found
**/
cv::Rect detect_background(cv::Mat im);

/**
 * Detect objects that are within a certain color range
 * which is defined in the PLCVision.h header file
 * 
 * @param im the video frame
 * @return a vector of rectangles. each of the rectangles is a bounding
 * rectangle for a contour.
**/
std::vector<cv::Rect> detect_objects(cv::Mat im);

/**
 * Get the index of the largest contour in a vector of contours
 * 
 * @param contours a vector of contours
 * @return the index of the largest contour, or -1 if the vector is empty
**/
int get_largest_contour(std::vector<std::vector<cv::Point>> contours);

/**
 * Draw the bounds of the paper and the 2x8 grid on the video frame
 * 
 * @param frame the video frame
 * @param bounds the bounding rectangle around the paper
 * @param color the color to make the grid and rectangle
**/
void draw_bounds(cv::Mat frame, cv::Rect bounds, cv::Scalar color);

/**
 * Draw and label the bounds of the objects on the paper in the 2x8 grid
 * 
 * @param frame the video frame
 * @param bounds the bounding rectangle around the paper
 * @param objects the bounding rectangles of the objects
 * @param color the color to make the grid and rectangle
 * @return the value to write to a plc tag to light up leds in a 2x8 grid
 * that correspond to the objects
**/
int32_t label_objects(cv::Mat frame, cv::Rect bounds, std::vector<cv::Rect> objects, cv::Scalar color);

#ifdef __cplusplus
extern "C" {
#endif

#ifdef __cplusplus
}
#endif

#endif
