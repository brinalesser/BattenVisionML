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
    bool use_plc = false;
    std::string vid_file = "";
    
    while(opt = getopt(argc, argv, "hv:pi:r:t:") != -1){
        switch(opt){
            case 'v': vid_file = optarg; use_camera = false; break;
            case 'i': tag_attr_str[5] = std::to_string(optarg); break;
            case 'r': tag_attr_str[7] = std::to_string(optarg); break;
            case 't': tag_attr_str[9] = std::to_string(optarg); break;
            case 'h':
            case '?':
            default : usage(argv[0]); exit(EXIT_FAILURE);
        }
    }


    //set up plc tag handle
    int32_t tag = 0;
    std::string attr_str = tag_attr_str[0];
    for(int i = 1; i < 10; i++){ attr_str += tag_attr_str[i]; }
    int rc = plc_setup(&tag,attr_str);
    
    if(rc != 0){
        exit(EXIT_FAILURE);
    }
    
    cv::VideoCapture cap;
    if(use_camera){
         cap = cv::VideoCapture(0);
    else{
        cap cv::VideoCapture(vid_file);
    }
    
	bool pause = false;
	bool ret = false;
	int count = 0;
	cv::Mat frame, new_frame;
	
	//camera frame is captured
	if(cap.isOpened()){
		//create trackbar window
		setup_trackbars();
		
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
				new_frame = process_frame(frame);
				cv::imshow("Processed Frame", new_frame);
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

static void usage(std::string str){
    std::cerr << "Usage: " << str << std::endl;
    std::cerr << "Options: " << std::endl;
    std::cerr << "\t-h\t\t show this help message\n" << std::endl;
    std::cerr << "\t-v\t\t video file name. default is pi USB camera\n" << std::endl;
    std::cerr << "\t-i\t\t ip address of PLC\n" << std::endl;
    std::cerr << "\t-r\t\t route to PLC\n" << std::endl;
    std::cerr << "\t-t\t\t PLC output tag name\n" << std::endl;
}
int plc_setup(int32_t &tag, std::string attr_str) {
    if(plc_tag_check_lib_version(REQUIRED_VERSION) != PLCTAG_STATUS_OK) {
        std::cerr << "Required compatible libplctag library version: " << REQUIRED_VERSION << std::endl;
        return -1;
    }
    
    tag = plc_tag_create(attr_str, DATA_TIMEOUT);
    
    if(tag < 0) {
        std::cerr << "ERROR" << plc_tag_decode_error(led_tag) << ": Could not create tag" << std::endl;
        return -2;
    }
    if(plc_tag_status(tag) != PLCTAG_STATUS_OK) {
        std::cerr << "Error setting up tag internal state. Error "<< plc_tag_decode_error(plc_tag_status(tag)) << std::endl;
        plc_tag_destroy(tag);
        return -3;
    }
    
    return 0;
}
cv::Mat process_frame(cv::Mat im){
    return im;
}
rectangle_t detect_background(cv::Mat im){
    return rectangle_t();
}
std::vector<rectangle_t> detect_objects(cv::Mat im){
    return rectangle_t();
}
