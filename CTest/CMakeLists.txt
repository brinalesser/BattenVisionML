cmake_minimum_required(VERSION 2.8)

PROJECT(cpp_test)

find_package(OpenCV REQUIRED)

INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/include )
link_directories( ${CMAKE_BINARY_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set(IMAGE_FILTER_SRC src/ImageFilter.cpp)
set(SIMPLE_IMAGE_FILTER_SRC src/SimpleImageFilter.cpp)
set(PLC_COMM_SRC src/PLCCommTest.cpp)
set(BATTEN_DETECT_SRC src/BattenDetection.cpp)
set(PLC_VISION_SRC src/PLCVision.cpp)

set(IMAGE_FILTER_HEADERS include/ImageFilter.h)
set(SIMPLE_IMAGE_FILTER_HEADERS include/SimpleImageFilter.h)
set(PLC_COMM_HEADERS include/PLCCommTest.h)
set(BATTEN_DETECT_HEADERS include/BattenDetection.h)
set(PLC_VISION_HEADERS include/PLCVision.h)

set(THREAD_LIB_LINK pthread)
set(PLC_LIB_LINK libplctag.a)

add_executable( image_filter ${IMAGE_FILTER_SRC} ${IMAGE_FILTER_HEADERS})
target_link_libraries( image_filter ${OpenCV_LIBS} )

add_executable( simple_image_filter ${SIMPLE_IMAGE_FILTER_SRC} ${SIMPLE_IMAGE_FILTER_HEADERS})
target_link_libraries( simple_image_filter ${OpenCV_LIBS} )

add_executable( plc_comm_test ${PLC_COMM_SRC} ${PLC_COMM_HEADERS})
target_link_libraries(plc_comm_test ${PLC_LIB_LINK} ${THREAD_LIB_LINK})

add_executable( batten_detect ${BATTEN_DETECT_SRC} ${BATTEN_DETECT_HEADERS})
target_link_libraries( batten_detect ${OpenCV_LIBS} )

add_executable( plc_vision ${PLC_VISION_SRC} ${PLC_VISION_HEADERS})
target_link_libraries( plc_vision ${OpenCV_LIBS} ${PLC_LIB_LINK} ${THREAD_LIB_LINK})
