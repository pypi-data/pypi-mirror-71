cmake_minimum_required(VERSION 3.16.3)
SET(PROJECT_VER "0.0.2")
project(try_pybind11_olned VERSION ${PROJECT_VER} DESCRIPTION "pybind11 example")

include(CTest)
enable_testing()

SET(SYSTEM PYBIND11_PYTHON_VERSION 3.8)
include_directories(SYSTEM ${CMAKE_SOURCE_DIR}/include)

add_subdirectory(src)
add_subdirectory(pybind11)
add_subdirectory(bindings)
add_subdirectory(tests)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
