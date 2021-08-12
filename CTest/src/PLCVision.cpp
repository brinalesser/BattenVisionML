/**
 * This is the c++ version of the PLCTest.py program. It is a 
 * proof of concept test doing vision processing merged with 
 * PLC communication. It uses the raspberry pi + camera
 * in the lab trained on a sheet of white paper with colored paper
 * shapes on it. The location of the colored papers on the white
 * paper is translated to a 2x8 grid and sent to the PLC which
 * lights up leds corresponding to the grid locations of the papers.
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/12/2021
 **/

#include "PLCVision.h"

/**
 * Main method to parse command line arguments and process video.
 * For a list of command line arguments, see the usage function.
 **/
int main(int argc, char* argv[]){
    
    //initialise variables that can be effected by command line arguments
    std::string tag_attr_str[10] = {"protocol=", "ab_eip", "&cpu=","controllogix",
        "&gateway=","10.1.8.15", "&path=","1,2", "&name=","OUTPUT_LEDS"};
    bool use_camera = true;
    bool use_plc = true;
    std::string vid_file = "";
    
    //parse command line arguments
    std::string opt;
    for(int i = 1; i < argc; i++){
        //get next arg
        opt = std::string(argv[i]);
        //v: video file
        if(opt.compare("-v") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            vid_file = argv[i]; 
            use_camera = false; 
        }
        //p: don't communicate with plc
        else if(opt.compare("-p") == 0){
            use_plc = false;
        }
        //i: ip address for plc
        else if(opt.compare("-i") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[5] = argv[i];
        }
        //r: path to PLC
        else if(opt.compare("-r") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[7] = argv[i];
        }
        //t: tag name to write to
        else if(opt.compare("-t") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[9] = argv[i];
        }
        //show usage
        else{
            usage(argv[0], opt);
            exit(EXIT_FAILURE);
        }
    }
    
    //open video
    cv::VideoCapture cap;
    if(use_camera){
        cap = cv::VideoCapture(0);
    } 
    else{
        cap = cv::VideoCapture(vid_file);
    }
    
	//camera frame is captured
	if(cap.isOpened()){
        
        //initialise variables
        bool pause = false, ret = false;
        int count = 0, rc = 0;
        cv::Mat frame;
        int32_t tag = 0, write_val = 0;
        
        //set up plc communication
        if(use_plc){
            //put attribute string together
            std::string attr_str = "";
            for(int i = 0; i < 10; i++){
                attr_str += tag_attr_str[i];
            }
            //try to setup
            rc = plc_setup(tag,attr_str.c_str());    
            if(rc != 0){ //check status
                use_plc = false;
            }
        }
            
		//continue reading frames while the video is open
		while(cap.isOpened()){
			
			//if not paused, get new frame
			if(!pause){
				ret = cap.read(frame);
			}
			
			//check return value
			if(ret){
				//show original frame
				cv::imshow("Original",frame);
                //get roi (white paper)
                cv::Rect bounds = detect_background(frame);
                cv::Mat bounded_frame = frame(bounds);
                //get bounding rectangles around objects (colored papers)
				std::vector<cv::Rect> objects = detect_objects(bounded_frame);
                //draw the bounds and label the objects
                cv::Scalar color(255,0,0);
                draw_bounds(frame, bounds, color);
                color = cv::Scalar(0,0,255);
                write_val = label_objects(frame, bounds, objects, color);
                //write to PLC
                if(use_plc){
                    plc_tag_set_int32(tag,TAG_OFFSET,write_val);
                    rc = plc_tag_write(tag,DATA_TIMEOUT);
                    
                    if(rc != PLCTAG_STATUS_OK) {
                        std::cerr << "ERROR: Unable to write to tag. Error code " << rc << ": " << plc_tag_decode_error(rc);
                        plc_tag_destroy(tag);
                        use_plc = false;
                    }
                }
                //show processed frame
				cv::imshow("Processed Frame", frame);
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
        //free tag
        plc_tag_destroy(tag);
		return 0;
	}
	
	//camera frame not captured
	else{
		std::cout << "Cannot get video file" << std::endl;
		return -1;
	}
}

/**
 * Print help message for command line arguments
 * 
 * @param prog the name of the program
 * @param opt the option that caused the error
**/
static void usage(std::string prog, std::string opt){
    std::cerr << "Usage: " << prog << " with option " << opt << std::endl;
    std::cerr << "Options: " << std::endl;
    std::cerr << "\t-h\t\t show this help message" << std::endl;
    std::cerr << "\t-v\t\t video file name - default is pi USB camera" << std::endl;
    std::cerr << "\t-i\t\t ip address of PLC" << std::endl;
    std::cerr << "\t-r\t\t route to PLC" << std::endl;
    std::cerr << "\t-t\t\t PLC output tag name" << std::endl;
    std::cerr << "\t-p\t\t don't use PLC" << std::endl;
}

/**
 * Setup to communicate with plc
 * 
 * @param tag the tag handle
 * @param attr_str the attribute string for the PLC tag: see libplctag 
 * documentation for more info: https://github.com/libplctag/libplctag
 * @return error code: 0 for success, -1 for incompatible library version,
 * -2 for tag creation error, -3 for tag status error after creation
**/
int plc_setup(int32_t &tag, const char * attr_str) {
    if(plc_tag_check_lib_version(REQUIRED_VERSION) != PLCTAG_STATUS_OK) {
        std::cerr << "Required compatible libplctag library version: 2.1.0" << std::endl;
        return -1;
    }
    
    tag = plc_tag_create(attr_str, DATA_TIMEOUT);
    
    if(tag < 0) {
        std::cerr << "ERROR" << plc_tag_decode_error(tag) << ": Could not create tag" << std::endl;
        return -2;
    }
    if(plc_tag_status(tag) != PLCTAG_STATUS_OK) {
        std::cerr << "Error setting up tag internal state. Error "<< plc_tag_decode_error(plc_tag_status(tag)) << std::endl;
        plc_tag_destroy(tag);
        return -3;
    }
    
    return 0;
}

/**
 * Find the dimensions and location of the background
 * 
 * @param im the video frame
 * @return the bounding rectangle for the white sheet of paper
 * or an empty rectangle if no contours were found
**/
cv::Rect detect_background(cv::Mat im){
    cv::Mat gray, blur, thresh, edges;
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    
    //blur and convert to grayscale
    cv::cvtColor(im, gray, cv::COLOR_BGR2GRAY);
    cv::medianBlur(gray, blur, 5);
    //use a binary threshold to make everything that is not white black
    cv::threshold(blur, thresh, 230, 255, cv::THRESH_BINARY);
    //edge detection
    cv::Canny(thresh, edges, 0, 255);
    //find largest contour which should be the paper
    cv::findContours(edges, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    int idx = get_largest_contour(contours);
    if(idx < 0){ //no contours -> return empty rectangle
        return cv::Rect();
    }
    
    return cv::boundingRect(contours[idx]);
}

/**
 * Detect objects that are within a certain color range
 * which is defined in the PLCVision.h header file
 * 
 * @param im the video frame
 * @return a vector of rectangles. each of the rectangles is a bounding
 * rectangle for a contour.
**/
std::vector<cv::Rect> detect_objects(cv::Mat im){
    std::vector<cv::Rect> locations;
    cv::Mat hsv, gray, mask, masked;
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    
    //convert to HSV
    cv::cvtColor(im, hsv, cv::COLOR_BGR2HSV);
    //find the pixels in the color range to create a bit mask
    cv::inRange(hsv, cv::Scalar(MIN_HUE, MIN_SATURATION, MIN_VALUE), cv::Scalar(MAX_HUE, MAX_SATURATION, MAX_VALUE), mask);
    //use the bit mask to ignore objects that are not in the color range in the original image
    cv::bitwise_and(im, im, masked, mask);
    //convert the masked image to grayscale
    cv::cvtColor(masked, gray, cv::COLOR_BGR2GRAY);
    //find the contours of the masked image
    cv::findContours(gray, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    //add the bounding rectangles for the contours to the return vector
    for(int i = 0; i < contours.size(); i++){
        //make sure contours are large enough so noise is not included
        double area = cv::contourArea(contours[i]);
        if(area > MIN_AREA){ 
            //add bounding rectangle to vector
            locations.push_back(cv::boundingRect(contours[i]));
        }
    }
    
    return locations;
}

/**
 * Get the index of the largest contour in a vector of contours
 * 
 * @param contours a vector of contours
 * @return the index of the largest contour, or -1 if the vector is empty
**/
int get_largest_contour(std::vector<std::vector<cv::Point>> contours){
    double max_area = 0;
    int idx = -1;
    
    //go through contours to find largest
    for(int i = 0; i < contours.size(); i++){
        //calculate area
        double area = cv::contourArea(contours[i]);
        //if area is larger than previous max, make it the new max and update the index
        if(area > max_area){
            max_area = area;
            idx = i;
        }
    }
    
    return idx;
}

/**
 * Draw the bounds of the paper and the 2x8 grid on the video frame
 * 
 * @param frame the video frame
 * @param bounds the bounding rectangle around the paper
 * @param color the color to make the grid and rectangle
**/
void draw_bounds(cv::Mat frame, cv::Rect bounds, cv::Scalar color){
    
    //draw rectangle around paper
    cv::rectangle(frame, bounds, color);
    //draw 2x8 grid
    cv::Point p1(bounds.x+int(bounds.width*0.5), bounds.y);
    cv::Point p2(bounds.x+int(bounds.width*0.5), bounds.y+bounds.height);
    cv::line(frame, p1, p2, color);
    for(int i = 0; i < 8; i++){
        p1 = cv::Point(bounds.x, bounds.y+int(bounds.height*i*0.125));
        p2 = cv::Point(bounds.x+bounds.width, bounds.y+int(bounds.height*i*0.125));
        cv::line(frame, p1, p2, color);
    }  
}

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
int32_t label_objects(cv::Mat frame, cv::Rect bounds, std::vector<cv::Rect> objects, cv::Scalar color){
    int32_t write_val = 0;
    cv::Point p;
    cv::Rect r;
    grid_point_t g;

    //iterate through the objects
    for(auto it = objects.begin(); it != objects.end(); ++it){
        //find the center point
        p = cv::Point((it->x * 2 + it->width) / 2, (it->y * 2 + it->height) / 2);
        //find the grid index
        g = grid_point_t(p, bounds.width, bounds.height);
        //offset the center point
        p.x += bounds.x;
        p.y += bounds.y;
        //draw a rectangle around the object
        r = cv::Rect(it->x + bounds.x, it->y + bounds.y, it->width, it->height);
        cv::rectangle(frame, r, color);
        //draw a circle at the center point of the object
        cv::circle(frame , p, 2, color);
        //label the location of the object at the center point
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2) << "(" << g.x << ", " << g.y << ")";
        cv::putText(frame, ss.str(), p, cv::FONT_HERSHEY_SIMPLEX, 0.5, color);
        //add grid location to write value
        write_val |= (1 << g.grid_idx);
    }
    return write_val;
}
