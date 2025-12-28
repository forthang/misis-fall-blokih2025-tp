cmake_minimum_required(VERSION 3.10)

project(type_list_element_extraction)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(GTest REQUIRED)

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Test executable
ADD_EXECUTABLE(${PROJECT_NAME}_test tests/sample_test.cpp include/base_interface.hpp)
target_link_libraries(${PROJECT_NAME}_test GTest::gtest_main)

# Demo executable
ADD_EXECUTABLE(${PROJECT_NAME}_demo src/demo.cpp include/base_interface.hpp)
