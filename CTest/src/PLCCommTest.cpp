/**
 * This program tests reading from and writing to PLC tags using the libplctag library
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#include "PLCCommTest.h"

int main()
{
     /* initialize variables */
    int32_t led_tag = 0;
    int32_t sw_tag = 0;
    int32_t value = 0;
    int offset = 0;
    int rc = 0;

    /* check the library version. */
    if(plc_tag_check_lib_version(REQUIRED_VERSION) != PLCTAG_STATUS_OK) {
        fprintf(stderr, "Required compatible library version %d.%d.%d not available!", REQUIRED_VERSION);
        exit(1);
    }

    /* create the tag handles */
    led_tag = plc_tag_create(LED_TAG_PATH, DATA_TIMEOUT);
    sw_tag = plc_tag_create(SW_TAG_PATH, DATA_TIMEOUT);

    /* status check */
    if(led_tag < 0) {
        fprintf(stderr,"ERROR %s: Could not create led tag!\n", plc_tag_decode_error(led_tag));
        return 0;
    }
    if((rc = plc_tag_status(led_tag)) != PLCTAG_STATUS_OK) {
        fprintf(stderr,"Error setting up led tag internal state. Error %s\n", plc_tag_decode_error(rc));
        plc_tag_destroy(led_tag);
        return 0;
    }
    if(sw_tag < 0) {
        fprintf(stderr,"ERROR %s: Could not create switches tag!\n", plc_tag_decode_error(sw_tag));
        return 0;
    }
    if((rc = plc_tag_status(sw_tag)) != PLCTAG_STATUS_OK) {
        fprintf(stderr,"Error setting up switches tag internal state. Error %s\n", plc_tag_decode_error(rc));
        plc_tag_destroy(sw_tag);
        return 0;
    }
    
    /* continuously write the value of the switches tag to the LEDs tag */
    std::cout << "\nwriting switch values to LEDs" << std::endl;
    std::cout << "set first switch to ON position or type ctrl+c to stop" << std::endl;
    while(true){
        
        /* get the switches tag value */
        rc = plc_tag_read(sw_tag, DATA_TIMEOUT);
        value = plc_tag_get_int32(sw_tag,offset);
        
        /* status check */
        if(rc != PLCTAG_STATUS_OK) {
            fprintf(stderr,"ERROR: Unable to read the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
            plc_tag_destroy(sw_tag);
            return 0;
        }
        //fprintf(stderr,"value read =%d\n",plc_tag_get_int32(sw_tag,offset)); //print switch values

        /* write to the LEDs tag */
        plc_tag_set_int32(led_tag,offset,value);
        rc = plc_tag_write(led_tag,DATA_TIMEOUT);
        
        /* status check */
        if(rc != PLCTAG_STATUS_OK) {
            fprintf(stderr,"ERROR: Unable to write the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
            plc_tag_destroy(led_tag);
            return 0;
        }
        //fprintf(stderr,"value written =%d\n",plc_tag_get_int32(led_tag,offset)); //print LED values
        
        /* way of exiting the loop */
        if(value == 1){
            break;
        }
        
        /* pause between iterations */
        for(int i = 0; i < 10000; i++){
        }
    }
    
    /* free the tags */
    plc_tag_destroy(led_tag);
    plc_tag_destroy(sw_tag);

    return 0;
}
