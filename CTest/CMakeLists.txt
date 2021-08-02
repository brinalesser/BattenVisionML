cmake_minimum_required(VERSION 2.8)

PROJECT(image_filter)
find_package(OpenCV REQUIRED)

set(IMAGE_FILTER_SRC src/ImageFilter.cpp)
set(IMAGE_FILTER_HEADERS include/ImageFilter.h)

INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/include )
link_directories( ${CMAKE_BINARY_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

add_executable( image_filter ${IMAGE_FILTER_SRC} ${IMAGE_FILTER_HEADERS} )

target_link_libraries( image_filter ${OpenCV_LIBS} )