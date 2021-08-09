/**
 * Header file for the c++ program thhat tests reading from and writing to PLC tags using the libplctag library
 * 
 * @author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
 * @date 8/5/2021
 **/

#ifndef PLC_COMM_TEST
#define PLC_COMM_TEST

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <strings.h>
#include <stdint.h>
#include <iostream>

//PLC communications library
#include <libplctag.h>

#define snprintf_platform snprintf
#define sscanf_platform sscanf
	
//paramaters for creating plc tag handles
#define REQUIRED_VERSION 2,1,0
#define LED_TAG_PATH "protocol=ab_eip&gateway=10.1.8.15&path=1,2&debug=1&cpu=controllogix&name=OUTPUT_LEDS"
#define SW_TAG_PATH "protocol=ab_eip&gateway=10.1.8.15&path=1,2&debug=1&cpu=controllogix&name=INPUT_SWITCHES"
#define DATA_TIMEOUT 5000

#ifdef __cplusplus
extern "C" {
#endif

extern int util_sleep_ms(int ms);
extern int64_t util_time_ms(void);

#ifdef __cplusplus
}
#endif

#endif
