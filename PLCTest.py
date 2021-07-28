'''

This is a program to test interacting with a PLC using python

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified:7/27/21

'''
from pylogix import PLC
from struct import pack, unpack_from
import cv2 as cv
import argparse


#adapted from pylogix documentation:
#get the bit from a binary number
def get_bit(value, bit_number):
    mask = 1 << bit_number
    return (value & mask)
#adapted from pylogix documentation:
#class to facilitate reading timers
class Timer(object):
    def __init__(self,data):
        self.PRE = unpack_from('<i', data, 4)[0]
        self.ACC = unpack_from('<i', data, 8)[0]
        bits = unpack_from('<i', data, 0)[0]
        self.EN = get_bit(bits, 31)
        self.TT = get_bit(bits, 30)
        self.DN = get_bit(bits, 29)

'''

Main

'''
if __name__=='__main__':
    
    
    #command line arguments
    parser = argparse.ArgumentParser(description='Vision test with PLC communications')
    parser.add_argument('-v', help='Video file name. Default is usb camera.', default=0, type=str)
    parser.add_argument('-i', help='IP address of PLC', default='1.1.1.1', type=str)
    parser.add_argument('-s', help='Processor Slot of PLC', default=0, type=int)
    parser.add_argument('-r', help='Route to PLC', default=None, type=str)
    parser.add_argument('-c', help='Connection Size for PLC', default=4002, type=int)
    args = parser.parse_args()

    #open video
    cap = cv.VideoCapture(args.v)
    if(cap.isOpened() == False):
        print("Video failed to open")
        
    #connect to PLC
    comm = PLC()
    comm.IPAddress = args.i
    comm.ProcessorSlot = args.s
    comm.Route = args.r
    comm.ConnectionSize = args.c
    '''
    tag_list = comm.GetTagList()
    for val in tag_list.Value:
    print(val)
    '''
    
    count = 0
    pause = False
    #process video frame by frame
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if not ret:
            print("failed to read frame")
            break
        else:
            #do stuff
            cv.imshow("Frame", frame)
            key = cv.waitKey(1)
            if(key == 27 or key == 113): #esc or q
                break
            elif(key == 115): #s
                cv.imwrite("Screenshot"+str(count)+".jpg", frame)
                count += 1
            elif(key == 112): #p
                pause = not pause
            elif(key != -1):
                print(key)

    cap.release()
    cv.destroyAllWindows()
    
    #From the API: If the PLC no longer sees a request,
    #it will eventually flush the connection, after about 90 seconds
    comm.Close()
    

