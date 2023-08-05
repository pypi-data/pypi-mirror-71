cmake_minimum_required(VERSION 3.16.3)
# project(try_pybind11_olned VERSION 0.1.0 DESCRIPTION "pybind11 example")


SET(PYBIND11_PYTHON_VERSION 3.8)
# include_directories(${CMAKE_SOURCE_DIR}/include)


pybind11_add_module( 
    try_pybind11_olned 
    try_pypind11_olned.cpp 
    ${CMAKE_SOURCE_DIR}/src/arithmetic.cpp
)