These are the steps I followed to download and use the libplctag library
which allows tags to be read from and written to a PLC using c++ code:
---------------------------------------------------------------------------------

Part 1 - Downloading and Installing the Library

1. Get the library from git here: https://github.com/libplctag/libplctag

    1a. on line 535 of the CMakeLists.txt file, I changed the DESTINATION of 
    the installation from lib${LIB_SUFFIX} to /usr/lib to change where
    the static library was installed

2. Do the following commands in the top level of the libplctag folder:

    cmake .
    sudo make install

This should put the static library (.a file) in the DESTINATION folder

---------------------------------------------------------------------------------

Part 2 - Using Library Functions That Read and Write PLC Tags

1. To use the library functions, #include <libplctag.h> in the .c/cpp/h file

2. To create a tag handle to a PLC tag, use the following function:
    
    int32_t plc_tag_create(const char *attrib_str, int timeout);

    2a. An example of an attribute string is this:

        "protocol=ab_eip&gateway=[IP address]&path=1,2&cpu=controllogix&name=TAG_NAME"

    2b. A list of the different attributes that can be specified such as the size of 
    the tag and the number of tags to read/write can be found here:
        https://github.com/libplctag/libplctag/wiki/Tag-String-Attributes
        
    2c. An example for how to determine the path attribute can be found here:
        https://docs.inductiveautomation.com/pages/viewpage.action?pageId=1704045

3. To free a tag, use the following function:

    int plc_tag_destroy(int32_t tag);
    
4. To read a tag, use the following functions:
    
    int plc_tag_read(int32_t tag, int timeout);
    size_t plc_tag_get_size_t(int32_t tag, int offset);
    
5. To write to a tag, use the following funtions:

    int plc_tag_set_size_t(int32_t tag, int offset, size_t new_value);
    int plc_tag_write(int32_t tag, int timeout);
        
6. For additional functions see the API here:
    
    https://github.com/libplctag/libplctag/wiki/API
---------------------------------------------------------------------------------

Part 3 - Writing a CMakeList File to Create an Executable

1. Make an executable with the source and header files like so:

    add_executable (executable_name ${SRC_FILES} ${HEADER_FILES})
    
2. Link the libplctag AND pthread libraries to the executable to use the functions 
from the library mentioned in Part 2. This can be done thusly:

    target_link_libraries (executable_name ${tool_lib} pthread libplctag.a)
    
---------------------------------------------------------------------------------

To download OpenCV, run the following command in the terminal on the Raspberry Pi:

    pip3 install opencv-python
    
---------------------------------------------------------------------------------

Once all the libraries have been installed, the executables can be rebuilt and 
run using the following commands in the terminal on the Raspberry Pi starting in 
the CTest folder using the CMakeLists file in this repository.

    cd build
    cmake ..
    make
    ./bin/name_of_executable_to_run

