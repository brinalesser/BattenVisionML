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
//#include <unistd.h>
//#include <stdint.h>
#include <iostream>
#include <string>
//#include <vector>
//#include <math.h>

//paramaters for creating plc tag handles
#define REQUIRED_VERSION 2,1,0
#define DATA_TIMEOUT 5000

//vision params
#define PAGE_WIDTH 11
#define PAGE_HEIGHT 17
#define PIXEL_WIDTH_PER_PAGE 200
#define PIXEL_HEIGHT_PER_PAGE 275
#define X_OFFSET 0
#define Y_OFFSET 0
#define X_INCREMENT (PIXEL_WIDTH_PER_PAGE / PAGE_WIDTH)
#define Y_INCREMENT (PIXEL_HEIGHT_PER_PAGE / PAGE_HEIGHT)

struct line_t {
	int x_1;
	int x_2;
	int y_1;
	int y_2;
	int x_m;//midpoint
	int y_m;//midpoint
	
	bool isNear(const line_t& other){
		return sqrt(pow(x_m - other.x_m, 2) + pow(y_m - other.y_m, 2)) < MAX_DIST;
	}
};

struct point_t {
	int x;
	int y;
}

struct rectangle_t {
	int x;
	int y;
	int w;
	int h;
	rectangle_t() : x(0), y(0), w(0), h(0) {}
	rectangle_t(int px, int py, int pw, int ph) : x(px), y(py), w(pw), h(ph) {}
}

struct grid_point_t {
	point_t p;
	int grid_idx;
	grid_point_t(point_t point, int height, int width) {
		p.x = X_OFFSET + (point.x / X_INCREMENT);
		p.y = Y_OFFSET + (point.y / Y_INCREMENT);
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
	
}

static void usage(std::string str);
int plc_setup(int32_t &tag, std::string attr_str);
cv::Mat process_frame(cv::Mat im);
rectangle_t detect_background(cv::Mat im);
std::vector<rectangle_t> detect_objects(cv::Mat im);


#ifdef __cplusplus
extern "C" {
#endif

#ifdef __cplusplus
}
#endif

#endif
