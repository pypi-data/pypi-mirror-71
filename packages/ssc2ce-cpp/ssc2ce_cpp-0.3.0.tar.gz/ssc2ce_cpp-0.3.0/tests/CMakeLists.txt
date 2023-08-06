include_directories(SYSTEM ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(
    cpp_tests
    main_test.cpp
    cex_parser_test.cpp
    coinbase_parser_test.cpp
    deribit_parser_test.cpp
)
               
target_link_libraries(
    cpp_tests
    ssc2ce)

add_test(NAME ssc2ce_cpp_lib_test COMMAND cpp_tests)

