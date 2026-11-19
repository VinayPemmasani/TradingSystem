# Aeron (https://github.com/real-logic/aeron): the C client and the C media
# driver, fetched at configure time and built as static libraries. Point
# FETCHCONTENT_SOURCE_DIR_AERON at a local checkout to build offline.
include(FetchContent)

# 1.47.x is the newest line that configures with CMake 3.26+ (Ubuntu 24.04 ships 3.28);
# 1.48 and later need CMake 3.30.
set(LAB_AERON_VERSION 1.47.7 CACHE STRING "Aeron release tag to build")

set(BUILD_AERON_DRIVER ON CACHE BOOL "" FORCE)
set(BUILD_AERON_ARCHIVE_API OFF CACHE BOOL "" FORCE)
set(AERON_TESTS OFF CACHE BOOL "" FORCE)
set(AERON_UNIT_TESTS OFF CACHE BOOL "" FORCE)
set(AERON_SYSTEM_TESTS OFF CACHE BOOL "" FORCE)
set(AERON_BUILD_SAMPLES OFF CACHE BOOL "" FORCE)
set(AERON_BUILD_DOCUMENTATION OFF CACHE BOOL "" FORCE)
set(AERON_INSTALL_TARGETS OFF CACHE BOOL "" FORCE)

FetchContent_Declare(aeron
  GIT_REPOSITORY https://github.com/real-logic/aeron.git
  GIT_TAG ${LAB_AERON_VERSION}
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL)
FetchContent_MakeAvailable(aeron)
