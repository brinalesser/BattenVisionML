
# Cascade Classifiers
---------------------------------------------------------------------------------
## About

---------------------------------------------------------------------------------
## How to create a Cascade Classifier Model

### 1. Get the OpenCV Applications

First you will need the following applications and their dependencies from the OpenCV library.

    opencv_annotation
    opencv_createsamples
    opencv_traincascade
    
They can be found on GitHub here: github.com/opencv/opencv/tree/master/apps
    
### 2. Get Samples

Put negative samples (images that don't include the object) in one folder and positive samples (images that include one or more of the object) in another

For example:

    /neg_img
        img1.jpg
        img2.jpg
    /pos_img
        img1.jpg
        img2.jpg

Then make a text file that lists the negative samples like so:
    
    neg_img/img1.jpg
    neg_img/img2.jpg
    
You will also need to make a text file that lists the positive samples including:

        - the number of objects in each image
        - the location of each object as a bounding rectangle
        
    pos_img/img1.jpg 1 42 42 142 142
    pos_img/img2.jpg 2 24 27 256 311  18 54 92 66
    
I would recommend using the opencv_annotation for this. 

In the command line, you can run the executable with the following command line prompts to create the file pos.txt with the images in a folde named pos_img

    opencv_annotation --annotations=/path/pos.txt --images=/path/pos_img/
    
It will create a pop up where you will have to draw bounding rectangles aroung every object that you are looking for in the image. When in the pop up:
    
        - click two points to indicate the corners of the bounding rectangle (it should draw the rectangle on the image)
        - press c to confirm the annotation
        - press d to delete the last annotation
        - press n to go to the next image
        - press esc to exit
        
### 3. Create Samples

Using the opencv_createsamples application, create a .vec file from your positive sample file.

For example, if your positive sample file is called pos.txt, you want your .vec file to be pos.vec, you want the width and height of the training samples to be 24 pixels by 24 pixels, and you have fewer than 250 positive samples, you can run the application in the command line like so: 

    opencv_createsamples -info pos.txt -w 24 -h 24 -num 250 -vec pos.vec
    
    
### 4. Train the Model

Using the opencv_traincascade application, create the model to use in your program.

For example, if you want the model stored in a folder called cascade, your .vec file is called pos.vec, your negative sample list is called neg.txt, the width and height of the training samples is 24 pixels by 24 pixels, you have more than 200 positive samples, and you want to train 10 stages, you can run the application from the command line like so:

    opencv_traincascade -data ./cascade -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 200 -numNeg 100 -numStages 10
    
Training a lot of stages can lead to "overtraining" and if you don't train the model enough, you will get a lot of false positives.
If you start with a lower number of stages, you can run the app multiple times, increaing the number of stages until your model works as intended.
It will build off the stages previously trained (so it won't take as much time as retraining it completely) as long as you do not delete those stages from the folder.
You can also run the program again with a reduced number of stages if you accidentally overtrain the model.
    
More information can be found here: docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html
