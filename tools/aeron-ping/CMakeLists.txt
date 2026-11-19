add_executable(aeron-ping main.cpp)
target_link_libraries(aeron-ping PRIVATE lab::aeron lab::core)
