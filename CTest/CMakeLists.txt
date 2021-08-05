cmake_minimum_required(VERSION 2.8)

PROJECT(cpp_test)

find_package(OpenCV REQUIRED)
include_directories(include)

INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/include )
link_directories( ${CMAKE_BINARY_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set(IMAGE_FILTER_SRC src/ImageFilter.cpp)
set(PLC_COMM_SRC src/PLCCommTest.cpp)
set(IMAGE_FILTER_HEADERS include/ImageFilter.h)
set(PLC_COMM_HEADERS include/PLCCommTest.h)
set(THREAD_LIB_LINK ${tool_lib} pthread)
set(PLC_LIB_LINK libplctag.a)

add_executable( image_filter ${IMAGE_FILTER_SRC} ${IMAGE_FILTER_HEADERS})
target_link_libraries( image_filter ${OpenCV_LIBS} )

add_executable( plc_comm_test ${PLC_COMM_SRC} ${PLC_COMM_HEADERS})
target_link_libraries(plc_comm_test ${PLC_LIB_LINK} ${THREAD_LIB_LINK})
