
#include "PLCCommTest.h"

#include <libplctag.h>

int main()
{
    int32_t tag = 0;
    int32_t sw_tag = 0;
    int rc;

    /* check the library version. */
    if(plc_tag_check_lib_version(REQUIRED_VERSION) != PLCTAG_STATUS_OK) {
        fprintf(stderr, "Required compatible library version %d.%d.%d not available!", REQUIRED_VERSION);
        exit(1);
    }

    /* create the tag */
    tag = plc_tag_create(LED_TAG_PATH, DATA_TIMEOUT);
    sw_tag = plc_tag_create(SW_TAG_PATH, DATA_TIMEOUT);

    /* everything OK? */
    if(tag < 0) {
        fprintf(stderr,"ERROR %s: Could not create led tag!\n", plc_tag_decode_error(tag));
        return 0;
    }

    if((rc = plc_tag_status(tag)) != PLCTAG_STATUS_OK) {
        fprintf(stderr,"Error setting up led tag internal state. Error %s\n", plc_tag_decode_error(rc));
        plc_tag_destroy(tag);
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

    int32_t data;
    while(true){
        /* get the data */
        rc = plc_tag_read(sw_tag, DATA_TIMEOUT);
        data = plc_tag_get_int32(sw_tag,0);
        if(rc != PLCTAG_STATUS_OK) {
            fprintf(stderr,"ERROR: Unable to read the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
            plc_tag_destroy(sw_tag);
            return 0;
        }

        /* print out the data */
        //fprintf(stderr,"data=%d\n",plc_tag_get_int32(tag,0));

        /* now test a write */
        //fprintf(stderr,"Setting element to data just read\n");
        plc_tag_set_int32(tag,0,data);
        rc = plc_tag_write(tag,DATA_TIMEOUT);

        if(rc != PLCTAG_STATUS_OK) {
            fprintf(stderr,"ERROR: Unable to write the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
            plc_tag_destroy(tag);
            return 0;
        }
        
        if(data == 1){
            break;
        }
        
        for(int i = 0; i < 1000; i++){
        }
    }
    
    /* we are done */
    plc_tag_destroy(tag);
    plc_tag_destroy(sw_tag);

    return 0;
}
