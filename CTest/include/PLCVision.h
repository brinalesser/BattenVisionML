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

static void usage(std::string str, std::string opt);
int plc_setup(int32_t &tag, const char * attr_str);
cv::Rect detect_background(cv::Mat im);
std::vector<cv::Rect> detect_objects(cv::Mat im);
int get_largest_contour(std::vector<std::vector<cv::Point>> contours);

#ifdef __cplusplus
extern "C" {
#endif

#ifdef __cplusplus
}
#endif

#endif
