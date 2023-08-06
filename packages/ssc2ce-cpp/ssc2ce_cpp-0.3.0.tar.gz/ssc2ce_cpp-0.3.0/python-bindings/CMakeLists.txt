pybind11_add_module( 
    ssc2ce_cpp 
    ssc2ce_cpp.cpp 
    ${CMAKE_SOURCE_DIR}/src/cex/parser.cpp
    ${CMAKE_SOURCE_DIR}/src/coinbase_pro/parser.cpp
    ${CMAKE_SOURCE_DIR}/src/deribit/parser.cpp
)
