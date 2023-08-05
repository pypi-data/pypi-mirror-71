cmake_minimum_required(VERSION 3.16.3)
project(my_lib VERSION 0.1.0 DESCRIPTION "lib example")

add_library (${PROJECT_NAME} 
    arithmetic.cpp 
    pet/animal.cpp
    pet/dog.cpp
)
# add_executable (demo src/main.cpp)
# target_link_libraries (demo ${PROJECT_NAME})
