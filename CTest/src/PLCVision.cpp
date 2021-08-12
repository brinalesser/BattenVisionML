/**
 * This is the c++ version of the PLCTest.py program
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/11/2021
 **/

#include "PLCVision.h"

int main(int argc, char* argv[]){
    std::string tag_attr_str[10] = {"protocol=", "ab_eip", 
                                        "&cpu=","controllogix",
                                        "&gateway=","10.1.8.15",
                                        "&path=","1,2",
                                        "&name=","OUTPUT_LEDS"};
    bool use_camera = true;
    bool use_plc = true;
    std::string vid_file = "";
    std::string opt;
    for(int i = 1; i < argc; i++){
        opt = std::string(argv[i]);
        if(opt.compare("-v") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            vid_file = argv[i]; 
            use_camera = false; 
        }
        else if(opt.compare("-p") == 0){
            use_plc = false;
        }
        else if(opt.compare("-i") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[5] = argv[i];
        }
        else if(opt.compare("-r") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[7] = argv[i];
        }
        else if(opt.compare("-t") == 0){
            i++;
            if( i >= argc ){
                usage(argv[0], opt);
                exit(EXIT_FAILURE);
            }
            tag_attr_str[9] = argv[i];
        }
        else{
            usage(argv[0], opt);
            exit(EXIT_FAILURE);
        }
    }
    
    cv::VideoCapture cap;
    if(use_camera){
        cap = cv::VideoCapture(0);
    } 
    else{
        cap = cv::VideoCapture(vid_file);
    }
    
	//camera frame is captured
	if(cap.isOpened()){
        
        bool pause = false;
        bool ret = false;
        int count = 0;
        int rc = 0;
        cv::Rect bounds;
        std::vector<cv::Rect> objects;
        cv::Mat frame, bounded_frame;
        int32_t tag = 0;
        
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
            
		//continue reading frames from the camera
		while(cap.isOpened()){
			
			//while not paused, keep getting new frame
			if(!pause){
				ret = cap.read(frame);
			}
			
			//check return value
			if(ret){
				//process frame
				cv::imshow("Original",frame);
                bounds = detect_background(frame);
                bounded_frame = frame(bounds);
				objects = detect_objects(bounded_frame);
                //draw bounds around frame
                cv::Scalar colour(255,0,0);
                cv::rectangle(frame, bounds, colour);
                //draw grid
                cv::line(frame, cv::Point(bounds.x+int(bounds.width*0.5), bounds.y), cv::Point(bounds.x+int(bounds.width*0.5), bounds.y+bounds.height), colour);
                for(int i = 0; i < 8; i++){
                    cv::line(frame, cv::Point(bounds.x, bounds.y+int(bounds.height*i*0.125)), cv::Point(bounds.x+bounds.width, bounds.y+int(bounds.height*i*0.125)), colour);
                }
                //draw object locations
                int32_t write_val = 0;
                cv::Point p;
                cv::Rect r;
                grid_point_t g;
                colour = cv::Scalar(0,0,255);
                for(auto it = objects.begin(); it != objects.end(); ++it){
                    p = cv::Point(bounds.x + ((it->x * 2 + it->width) / 2), bounds.y + ((it->y * 2 + it->height) / 2));
                    g = grid_point_t(p, bounds.width, bounds.height);//get grid index
                    r = cv::Rect(it->x + bounds.x, it->y + bounds.y, it->width, it->height);
                    cv::rectangle(frame, r, colour); //object bounds
                    cv::circle(frame , p, 2, colour); //object midpoint
                    std::stringstream ss;
                    ss << std::fixed << std::setprecision(2) << "(" << g.x << ", " << g.y << ")";
                    cv::putText(frame, ss.str(), p, cv::FONT_HERSHEY_SIMPLEX, 0.5, colour); //object location
                    write_val |= (1 << g.grid_idx);
                }
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

static void usage(std::string str, std::string opt){
    std::cerr << "Usage: " << str << " with option " << opt << std::endl;
    std::cerr << "Options: " << std::endl;
    std::cerr << "\t-h\t\t show this help message" << std::endl;
    std::cerr << "\t-v\t\t video file name - default is pi USB camera" << std::endl;
    std::cerr << "\t-i\t\t ip address of PLC" << std::endl;
    std::cerr << "\t-r\t\t route to PLC" << std::endl;
    std::cerr << "\t-t\t\t PLC output tag name" << std::endl;
    std::cerr << "\t-p\t\t don't use PLC" << std::endl;
}

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

cv::Rect detect_background(cv::Mat im){
    cv::Mat gray, blur, thresh, edges;
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    //blur and convert to grayscale
    cv::cvtColor(im, gray, cv::COLOR_BGR2GRAY);
    cv::medianBlur(gray, blur, 5);
    cv::threshold(blur, thresh, 230, 255, cv::THRESH_BINARY);
    cv::Canny(thresh, edges, 0, 255);
    cv::findContours(edges, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    int idx = get_largest_contour(contours);
    if(idx < 0){
        return cv::Rect();
    }
    return cv::boundingRect(contours[idx]);
}

std::vector<cv::Rect> detect_objects(cv::Mat im){
    std::vector<cv::Rect> locations;
    cv::Mat hsv, gray, mask, masked;
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    
    cv::cvtColor(im, hsv, cv::COLOR_BGR2HSV);
    cv::inRange(hsv, cv::Scalar(MIN_HUE, MIN_SATURATION, MIN_VALUE), cv::Scalar(MAX_HUE, MAX_SATURATION, MAX_VALUE), mask);
    cv::bitwise_and(im, im, masked, mask);
    cv::cvtColor(masked, gray, cv::COLOR_BGR2GRAY);
    
    cv::findContours(gray, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    for(int i = 0; i < contours.size(); i++){
        double area = cv::contourArea(contours[i]);
        if(area > MIN_AREA){
            locations.push_back(cv::boundingRect(contours[i]));
        }
    }
    return locations;
}

int get_largest_contour(std::vector<std::vector<cv::Point>> contours){
    double max_area = 0;
    int idx = -1;
    for(int i = 0; i < contours.size(); i++){
        double area = cv::contourArea(contours[i]);
        if(area > max_area){
            max_area = area;
            idx = i;
        }
    }
    return idx;
}
