add_executable(
    cpp_tests
    main_test.cpp
    arithmetic_test.cpp
    pet_test.cpp
)
               
target_link_libraries(
    cpp_tests
    my_lib)

add_test(NAME cpp_my_lib_test COMMAND cpp_tests)
