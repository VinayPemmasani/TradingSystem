# Shared warning, tuning and sanitizer flags. Every lab target links lab_options.
add_library(lab_options INTERFACE)
add_library(lab::options ALIAS lab_options)

target_compile_options(lab_options INTERFACE
  -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor -Wold-style-cast
  -Wcast-align -Woverloaded-virtual -Wnull-dereference -Wdouble-promotion
  -Wformat=2 -Wimplicit-fallthrough -Wsign-compare)

if(LAB_WERROR)
  target_compile_options(lab_options INTERFACE -Werror)
endif()

if(LAB_NATIVE)
  target_compile_options(lab_options INTERFACE -march=native)
  # On CPUs with AVX10 (e.g. some CI runners), clang 18 warns that -march=native
  # enables avx10.1-256 and promotes it to avx10.1-512. That warning says nothing
  # about lab code, so keep it from failing -Werror builds.
  # GCC accepts any -Wno-* silently, so limit this to Clang.
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    include(CheckCXXCompilerFlag)
    check_cxx_compiler_flag(-Wno-invalid-feature-combination LAB_HAS_WNO_INVALID_FEATURE_COMBINATION)
    if(LAB_HAS_WNO_INVALID_FEATURE_COMBINATION)
      target_compile_options(lab_options INTERFACE -Wno-invalid-feature-combination)
    endif()
  endif()
endif()

if(LAB_SANITIZE)
  target_compile_options(lab_options INTERFACE -fsanitize=${LAB_SANITIZE} -fno-omit-frame-pointer)
  target_link_options(lab_options INTERFACE -fsanitize=${LAB_SANITIZE})
  target_compile_definitions(lab_options INTERFACE LAB_SANITIZED=1)
endif()
