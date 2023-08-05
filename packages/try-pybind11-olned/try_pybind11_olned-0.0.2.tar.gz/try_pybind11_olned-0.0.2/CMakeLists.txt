cmake_minimum_required(VERSION 3.16.3)
project(try_pybind11_olned VERSION 0.1.0 DESCRIPTION "pybind11 example")

SET(PYBIND11_PYTHON_VERSION 3.8)

include(CTest)
enable_testing()

add_subdirectory(pybind11)
pybind11_add_module(${PROJECT_NAME} src/example.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
