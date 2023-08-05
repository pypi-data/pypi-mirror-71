add_executable(
    my_test
    main_test.cpp
    arithmetic_test.cpp)
               
target_link_libraries(
    my_test
    my_lib)

add_test(NAME cpp_test COMMAND my_test)
