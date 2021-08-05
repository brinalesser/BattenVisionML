/**
 * This program that processes each frame of a video pixel by pixel
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/2/2021
 **/
 
#include "ImageFilter.h"

/**
 * Get video from pi camera and process it frame by frame
 **/
int main(int argc, char* argv[]){
	//init values
	cv::VideoCapture cap(0); //change 0 to filename for video file
	bool pause = false;
	bool ret = false;
	int count = 0;
	cv::Mat frame, new_frame;
	std::string title = "Frame";
	
	//camera frame is captured
	if(cap.isOpened()){
		//create main window
		cv::namedWindow(title, cv::WINDOW_NORMAL);
		
		//continue reading frames from the camera
		while(cap.isOpened()){
			
			//while not paused, keep getting new frame
			if(!pause){
				ret = cap.read(frame);
			}
			
			//check return value
			if(ret){
				//process frame
				cv::imshow(title,frame);
				new_frame = process_image(frame);
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


/**
 * Process a single frame
 * 
 * @param im the original frame as a cv::Mat object
 * @return the processed frame as a cv::Mat object
 **/
cv::Mat process_image(cv::Mat im){
	//init vars
	int h = im.rows; //height
	int w = im.cols; //width
	cv::Vec3b intensity; //pixel color
	
	//iterate through pixels
	for(int y = 0; y < h; y++){
		for(int x = 0; x < w; x++){
			//get pixel color
			intensity = im.at<cv::Vec3b>(y, x);
            uchar blue = intensity.val[0];
            uchar green = intensity.val[1];
            uchar red = intensity.val[2];
            //color threshold
            if(blue < 200){
				//change pixel to black if not within threshold
				uchar avg = (blue + green + red) / 3;
				im.at<cv::Vec3b>(y, x) = {0, 0, 0};
			}
		}
	}
	
	return im;
}
