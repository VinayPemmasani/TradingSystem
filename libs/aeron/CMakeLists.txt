include(${PROJECT_SOURCE_DIR}/cmake/Aeron.cmake)

add_library(lab_aeron src/aeron.cpp)
add_library(lab::aeron ALIAS lab_aeron)

target_include_directories(lab_aeron PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
# Aeron's own headers are third-party: include them as system headers so the
# lab's warning flags do not apply to them.
target_include_directories(lab_aeron SYSTEM PUBLIC
  ${aeron_SOURCE_DIR}/aeron-client/src/main/c
  ${aeron_SOURCE_DIR}/aeron-driver/src/main/c)
target_link_libraries(lab_aeron PUBLIC lab::options aeron_static PRIVATE aeron_driver_static)
