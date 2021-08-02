#include "PLCCommTest.h"

int main()
{
    int32_t tag = 0;
    int rc;

    /* check the library version. */
    if(plc_tag_check_lib_version(REQUIRED_VERSION) != PLCTAG_STATUS_OK) {
        fprintf(stderr, "Required compatible library version %d.%d.%d not available!", REQUIRED_VERSION);
        exit(1);
    }

    /* create the tag */
    tag = plc_tag_create(TAG_PATH, DATA_TIMEOUT);

    /* everything OK? */
    if(tag < 0) {
        fprintf(stderr,"ERROR %s: Could not create tag!\n", plc_tag_decode_error(tag));
        return 0;
    }

    if((rc = plc_tag_status(tag)) != PLCTAG_STATUS_OK) {
        fprintf(stderr,"Error setting up tag internal state. Error %s\n", plc_tag_decode_error(rc));
        plc_tag_destroy(tag);
        return 0;
    }

    /* get the data */
    rc = plc_tag_read(tag, DATA_TIMEOUT);
    if(rc != PLCTAG_STATUS_OK) {
        fprintf(stderr,"ERROR: Unable to read the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
        plc_tag_destroy(tag);
        return 0;
    }

    /* print out the data */
    fprintf(stderr,"data=%d\n",plc_tag_get_int32(tag,0));

    /* now test a write */
    fprintf(stderr,"Setting element to 1\n");
    plc_tag_set_int32(tag,0,2);
    rc = plc_tag_write(tag, DATA_TIMEOUT);

    if(rc != PLCTAG_STATUS_OK) {
        fprintf(stderr,"ERROR: Unable to write the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
        plc_tag_destroy(tag);
        return 0;
    }


    /* get the data again*/
    rc = plc_tag_read(tag, DATA_TIMEOUT);

    if(rc != PLCTAG_STATUS_OK) {
        fprintf(stderr,"ERROR: Unable to read the data! Got error code %d: %s\n",rc, plc_tag_decode_error(rc));
        plc_tag_destroy(tag);
        return 0;
    }

    /* print out the data */
    fprintf(stderr,"data=%d\n",plc_tag_get_int32(tag,0));

    /* we are done */
    plc_tag_destroy(tag);

    return 0;
}
