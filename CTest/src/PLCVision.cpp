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
    
    while(opt = getopt(argc, argv, "hv:pi:r:t:") != -1){
        switch(opt){
            case 'v': vid_file = optarg; use_camera = false; break;
            case 'p': use_plc = false; break;
            case 'i': tag_attr_str[5] = std::to_string(optarg); break;
            case 'r': tag_attr_str[7] = std::to_string(optarg); break;
            case 't': tag_attr_str[9] = std::to_string(optarg); break;
            case 'h':
            case '?':
            default : usage(argv[0]); exit(EXIT_FAILURE);
        }
    }



    
    cv::VideoCapture cap;
    if(use_camera){
         cap = cv::VideoCapture(0);
    else{
        cap cv::VideoCapture(vid_file);
    }
    
	//camera frame is captured
	if(cap.isOpened()){
        
        bool pause = false;
        bool ret = false;
        int count = 0;
        int rc = 0;
        rectangle_t bounds;
        std::vector<rectangle_t> objects;
        cv::Mat frame, bounded_frame;
        int32_t tag = 0;
        
        //set up plc communication
        if(use_plc){
            //put attribute string together
            std::string attr_str = tag_attr_str[0];
            for(int i = 1; i < 10; i++){ attr_str += tag_attr_str[i]; }
            //try to setup
            rc = plc_setup(&tag,attr_str);    
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
                bounded_frame = frame[];//TODO
				objects = detect_objects(bounded_frame);
                
                //draw bounds around frame
                cv::rectangle();
                //draw grid
                cv::line();
                for(int i = 0; i < 8; i++){ cv::line(); }
                //draw object locations
                int32_t write_val = 0;
                for(auto it = objects.begin(); it != objects.end(); ++it){
                    grid_point_t grid_pt();
                    cv::rectangle(); //object bounds
                    cv::circle(); //object midpoint
                    cv::puText(); //object location
                    write_val |= (1 << grid_pt.grid_idx);
                }
                //write to PLC
                if(use_plc){
                    plc_tag_set_int32(tag,TAG_OFFSET,write_val);
                    rc = plc_tag_write(tag,DATA_TIMEOUT);
                    
                    if(rc != PLCTAG_STATUS_OK) {
                        std::cerr << "ERROR: Unable to write to tag. Error code " << rc << ": " << plc_tag_decode_error(rc));
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

static void usage(std::string str){
    std::cerr << "Usage: " << str << std::endl;
    std::cerr << "Options: " << std::endl;
    std::cerr << "\t-h\t\t show this help message\n" << std::endl;
    std::cerr << "\t-v\t\t video file name. default is pi USB camera\n" << std::endl;
    std::cerr << "\t-i\t\t ip address of PLC\n" << std::endl;
    std::cerr << "\t-r\t\t route to PLC\n" << std::endl;
    std::cerr << "\t-t\t\t PLC output tag name\n" << std::endl;
    std::cerr << "\t-p\t\t don't use PLC\n" << std::endl;
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
