include_directories(SYSTEM ${CMAKE_CURRENT_SOURCE_DIR})

# add_executable(
#     cpp_tests
#     main_test.cpp
#     deribit_parser_test.cpp
# )
               
# target_link_libraries(
#     cpp_tests
#     ssc2ce)

# add_test(NAME ssc2ce_cpp_lib_test COMMAND cpp_tests)

add_executable(
    deribit_parser_test
    main_test.cpp
    deribit_parser_test.cpp
)


target_link_libraries(
    deribit_parser_test
    ssc2ce
)

add_test(NAME deribit_parser_test COMMAND deribit_parser_test)
