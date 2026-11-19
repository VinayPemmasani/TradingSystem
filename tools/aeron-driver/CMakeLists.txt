add_executable(aeron-driver main.cpp)
target_link_libraries(aeron-driver PRIVATE lab::aeron lab::core)
