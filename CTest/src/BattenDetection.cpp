/**
 * This program detects the gap between battens and draws a line there.
 * It works best on a close up view of a stack of battens.
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/9/2021
 **/
 
#include "BattenDetection.h"

/**
 * Get video and process it frame by frame
 **/
int main(int argc, char* argv[]){
	//capture video frame
	cv::VideoCapture cap("/home/pi/Desktop/PythonProjects/BattenVisionML/Videos/test.mp4"); 
	
	bool pause = false;
	bool ret = false;
	int count = 0;
	
	//camera frame is captured
	if(cap.isOpened()){
		cv::Mat frame, new_frame;
		std::vector<cv::Vec4i> lines, merged_lines;
		
		//continue reading frames from the camera
		while(cap.isOpened()){
			
			//while not paused, keep getting new frame
			if(!pause){
				ret = cap.read(frame);
			}
			
			//check return value
			if(ret){
				//process frame
				lines = get_lines(frame);
				merged_lines = merge_lines(lines, frame.size().width, frame.size().height);
				new_frame = draw_lines(frame, merged_lines);
				cv::imshow("Battens", new_frame);
			}
			else{
				std::cout << "End of video" << std::endl;
				break;
			}

			/** 
				keypress:
				q: quit program
				esc: quit program
				s: take screenshot of current frame
				p: pause on the current frame 
			**/
			int key = cv::waitKey(1) & 255;
			if(key == 27 || key == 113){ //esc or q
				std::cout << "Video ended by user" << std::endl;
				break;
			}
			else if (key == 115){ //s
				std::string filename = "Screenshot";
				filename.append(std::to_string(count));
				filename.append(".jpg");
				cv::imwrite(filename, frame);
				count ++;
			}
			else if(key == 112){ //p
				pause = !pause;
			}
			
		}
		//close all OpenCV windows
		cv::destroyAllWindows();
		return 0;
	}
	
	//camera frame not captured
	else{
		std::cout << "Cannot get video file" << std::endl;
		return -1;
	}
}

/**
 * Do edge detection and get the lines along the edges for an image
 * 
 * @param im an image
 * @return a vector holding lines represented as a Vec4i
 **/
std::vector<cv::Vec4i> get_lines(cv::Mat im){
	cv::Mat edges, blur1, blur2, gray;
	std::vector<cv::Vec4i> lines;
	//convert to grayscale and blur
    cv::cvtColor(im, gray, cv::COLOR_BGR2GRAY);
    cv::medianBlur(gray, blur1, 5);
    cv::bilateralFilter(blur1, blur2, 7, 75.0, 75.0);
    //find the edges
    cv::Canny(blur2, edges, 0, 255, 3);
    //find the lines
    cv::HoughLinesP(edges, lines, 1, CV_PI/180, 1, 10, 1);
    return lines;
}

/**
 * Merge lines together to get one line that spans the frame where the gap in the battens is
 * 
 * @param lines a vector holding lines represented as a Vec4i
 * @param frame_width the width of the frame
 * @param frame_height the height of the frame
 * @return the merged lines as a vector holding lines represented as a Vec4i
 * 			-if the lines cannot be merged, return the original vector of lines
 **/
std::vector<cv::Vec4i> merge_lines(std::vector<cv::Vec4i> lines, int frame_width, int frame_height){
	if(lines.size() < 2){
		return lines;
	}
	
	//each index of this will hold a group of lines to merge:
	std::vector<std::vector<line_t>> points; 
	//this will be a vector of indices of groups to merge:
	std::vector<int> groups;

	line_t l;
	//iterate through the lines to merge lines that are close together
	for(int line_idx = 0; line_idx < lines.size(); line_idx++){
		//get midpoint and make line_t
		l.x_1 = lines[line_idx][0];
		l.y_1 = lines[line_idx][1];
		l.x_2 = lines[line_idx][2];
		l.y_2 = lines[line_idx][3];
		l.x_m = (l.x_1 + l.x_2)/2;
		l.y_m = (l.y_1 + l.y_2)/2;
		
		//check which indices in the points vector have points that are 
		//close to the midpoint
		for(int i= 0; i < points.size(); i++){
			for(int j = 0; j < points[i].size(); j++){
				//check if points are close
				if(l.isNear(points[i][j])){
					//indicate that the groups should be merged
					groups.push_back(i);
					break;
				}
			}
		}
		
		//point should not be added to a group - make a new group
		if(groups.size() < 1){
			std::vector<line_t> new_group;
			new_group.push_back(l);
			points.push_back(new_group);
		}
		//add point to group, then merge with other groups
		else{
			int idx = groups.back();
			points[idx].push_back(l);
			groups.pop_back();
			while(groups.size() > 0){
				//Add group to first group
				int group_idx = groups.back();
				for(int i = 0; i < points[group_idx].size(); i++){
					points[idx].push_back(points[group_idx][i]);
				}
				//remove group from points
				points.erase(points.begin()+group_idx);
				groups.pop_back();
			}
		}
		
	}
	
	//calculate lines of best fit for each group using simple linear regression
	//(reference: https://en.wikipedia.org/wiki/Simple_linear_regression#Fitting_the_regression_line)
	std::vector<cv::Vec4i> merged;
	for(int i = 0; i < points.size(); i++){
		int n = points[i].size(); //number of points to make the line with
		
		if(n < 1){ //empty group
			std::cout << "Error: wrong number of points to make line" << std::endl;
		}
		else if(n == 1){ //only one line in group
			merged.push_back(cv::Vec4i(points[i][0].x_1, points[i][0].y_1, points[i][0].x_2, points[i][0].y_2));
		}
		else{ //find line of best fit
			
			// calculate summations and means
			double x_sum=0, y_sum=0, xy_sum=0, xx_sum=0;
			double x, y, x_mean, y_mean;
			for(int j = 0; j < n; j++) {
				x = points[i][j].x_m;
				y = points[i][j].y_m;
				x_sum += x;
				y_sum += y;
				xy_sum += x * y;
				xx_sum += x * x;
			}
			x_mean = x_sum / n;
			y_mean = y_sum / n;
			
			// calculate slope and intercept, then stretch line across frame
			double denom = xx_sum - x_sum * x_mean;
			double m, b;
			int x1, x2, y1, y2;
			if( std::fabs(denom) > 1e-7 ) { //defined slope
				m = (xy_sum - x_sum * y_mean) / denom;
				b = y_mean - m * x_mean;
				x1 = 0;
				y1 = b;
				x2 = frame_width;
				y2 = (m * x2) + b;
			}
			else { //undefined slope
				x1 = x_mean;
				y1 = 0;
				x2 = x_mean;
				y2 = frame_height;
			}
			merged.push_back(cv::Vec4i(x1, y1, x2, y2));
		}
	}
	return merged;

}

/**
 * Draw lines on an image
 * 
 * @param im an image
 * @param lines the lines to draw on the image
 * @return the image with the lines drawn on it
 **/
cv::Mat draw_lines(cv::Mat im, std::vector<cv::Vec4i> lines){
	for( int i = 0; i < lines.size(); i++ ) {
		cv::Vec4i l = lines[i];
        cv::line( im, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, cv::LINE_AA);
    }
	return im;
}

