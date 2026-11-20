# Native OpenGL 3.3 version of the packet-life scene. A standalone project, not part of
# the lab's main build, so the lab itself never needs a window system:
#
#   cmake -S viz/packet-life/opengl -B build/packet-life -DCMAKE_BUILD_TYPE=Release
#   cmake --build build/packet-life --config Release
#   build/packet-life/packet-life-gl
#
# Dependencies: OpenGL and GLFW (an installed GLFW 3.3+ if found, otherwise GLFW 3.4 is
# fetched), plus stb_easy_font for on-screen text, downloaded at configure time. GL entry
# points are loaded by hand in gl.hpp, so no GLAD or GLEW.
cmake_minimum_required(VERSION 3.20)
project(packet_life_gl LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(OpenGL REQUIRED)
find_package(glfw3 3.3 QUIET)
include(FetchContent)
if(NOT glfw3_FOUND)
  set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
  set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
  set(GLFW_INSTALL OFF CACHE BOOL "" FORCE)
  # X11 only on Linux: works on desktops and under WSLg, and needs no wayland-scanner.
  set(GLFW_BUILD_WAYLAND OFF CACHE BOOL "" FORCE)
  FetchContent_Declare(glfw
    URL https://github.com/glfw/glfw/releases/download/3.4/glfw-3.4.zip
    URL_HASH SHA256=b5ec004b2712fd08e8861dc271428f048775200a2df719ccf575143ba749a3e9)
  FetchContent_MakeAvailable(glfw)
endif()

# stb_easy_font (public domain), pinned to one commit.
set(STB_DIR ${CMAKE_BINARY_DIR}/stb)
if(NOT EXISTS ${STB_DIR}/stb_easy_font.h)
  file(DOWNLOAD
    https://raw.githubusercontent.com/nothings/stb/6b5799bae8a1fe3792691ef4b72ae26434c3e799/stb_easy_font.h
    ${STB_DIR}/stb_easy_font.h
    EXPECTED_HASH SHA256=f26a20fbbf1aee3e270a83d1e69ecc2a66eb9415aee718f2b7f58da5d6704848
    TLS_VERIFY ON)
endif()

add_executable(packet-life-gl main.cpp)
target_include_directories(packet-life-gl SYSTEM PRIVATE ${STB_DIR})
target_link_libraries(packet-life-gl PRIVATE glfw OpenGL::GL)
# Default data: trace.json and scene.json one directory up.
target_compile_definitions(packet-life-gl PRIVATE
  PACKET_LIFE_DATA_DIR="${CMAKE_CURRENT_SOURCE_DIR}/.." GLFW_INCLUDE_NONE)
if(MSVC)
  target_compile_options(packet-life-gl PRIVATE /W4 /utf-8)
  target_compile_definitions(packet-life-gl PRIVATE _CRT_SECURE_NO_WARNINGS)
else()
  target_compile_options(packet-life-gl PRIVATE -Wall -Wextra)
endif()
