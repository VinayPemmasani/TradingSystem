#pragma once

// The OpenGL 3.3 core entry points this viewer uses, loaded through GLFW, so the build
// needs no GLAD or GLEW. Enum values are from the Khronos registry (gl.xml).

#include <GLFW/glfw3.h>

#include <cstddef>
#include <cstdint>

#if defined(_WIN32) && !defined(APIENTRY)
#define APIENTRY __stdcall
#elif !defined(APIENTRY)
#define APIENTRY
#endif

namespace gl {

using GLenum = unsigned int;
using GLuint = unsigned int;
using GLint = int;
using GLsizei = int;
using GLboolean = unsigned char;
using GLbitfield = unsigned int;
using GLfloat = float;
using GLchar = char;
using GLsizeiptr = std::ptrdiff_t;
using GLintptr = std::ptrdiff_t;

constexpr GLenum LINES = 0x0001;
constexpr GLenum TRIANGLES = 0x0004;
constexpr GLenum DEPTH_BUFFER_BIT = 0x0100;
constexpr GLenum COLOR_BUFFER_BIT = 0x4000;
constexpr GLenum SRC_ALPHA = 0x0302;
constexpr GLenum ONE_MINUS_SRC_ALPHA = 0x0303;
constexpr GLenum CULL_FACE = 0x0B44;
constexpr GLenum DEPTH_TEST = 0x0B71;
constexpr GLenum BLEND = 0x0BE2;
constexpr GLenum PACK_ALIGNMENT = 0x0D05;
constexpr GLenum UNSIGNED_BYTE = 0x1401;
constexpr GLenum FLOAT = 0x1406;
constexpr GLenum RGB = 0x1907;
constexpr GLenum MULTISAMPLE = 0x809D;
constexpr GLenum ARRAY_BUFFER = 0x8892;
constexpr GLenum STATIC_DRAW = 0x88E4;
constexpr GLenum STREAM_DRAW = 0x88E0;
constexpr GLenum FRAGMENT_SHADER = 0x8B30;
constexpr GLenum VERTEX_SHADER = 0x8B31;
constexpr GLenum COMPILE_STATUS = 0x8B81;
constexpr GLenum LINK_STATUS = 0x8B82;
constexpr GLboolean kFalse = 0;
constexpr GLboolean kTrue = 1;

#define PL_GL_FUNCS(X)                                                                     \
  X(void, Clear, GLbitfield)                                                               \
  X(void, ClearColor, GLfloat, GLfloat, GLfloat, GLfloat)                                  \
  X(void, Viewport, GLint, GLint, GLsizei, GLsizei)                                        \
  X(void, Enable, GLenum)                                                                  \
  X(void, Disable, GLenum)                                                                 \
  X(void, BlendFunc, GLenum, GLenum)                                                       \
  X(void, DepthMask, GLboolean)                                                            \
  X(void, DrawArrays, GLenum, GLint, GLsizei)                                              \
  X(void, PixelStorei, GLenum, GLint)                                                      \
  X(void, ReadPixels, GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, void*)               \
  X(void, GenBuffers, GLsizei, GLuint*)                                                    \
  X(void, BindBuffer, GLenum, GLuint)                                                      \
  X(void, BufferData, GLenum, GLsizeiptr, const void*, GLenum)                             \
  X(void, GenVertexArrays, GLsizei, GLuint*)                                               \
  X(void, BindVertexArray, GLuint)                                                         \
  X(void, VertexAttribPointer, GLuint, GLint, GLenum, GLboolean, GLsizei, const void*)     \
  X(void, EnableVertexAttribArray, GLuint)                                                 \
  X(GLuint, CreateShader, GLenum)                                                          \
  X(void, ShaderSource, GLuint, GLsizei, const GLchar* const*, const GLint*)               \
  X(void, CompileShader, GLuint)                                                           \
  X(void, GetShaderiv, GLuint, GLenum, GLint*)                                             \
  X(void, GetShaderInfoLog, GLuint, GLsizei, GLsizei*, GLchar*)                            \
  X(GLuint, CreateProgram)                                                                 \
  X(void, AttachShader, GLuint, GLuint)                                                    \
  X(void, LinkProgram, GLuint)                                                             \
  X(void, GetProgramiv, GLuint, GLenum, GLint*)                                            \
  X(void, GetProgramInfoLog, GLuint, GLsizei, GLsizei*, GLchar*)                           \
  X(void, DeleteShader, GLuint)                                                            \
  X(void, UseProgram, GLuint)                                                              \
  X(GLint, GetUniformLocation, GLuint, const GLchar*)                                      \
  X(void, UniformMatrix4fv, GLint, GLsizei, GLboolean, const GLfloat*)                     \
  X(void, Uniform4f, GLint, GLfloat, GLfloat, GLfloat, GLfloat)                            \
  X(void, Uniform3f, GLint, GLfloat, GLfloat, GLfloat)                                     \
  X(void, Uniform2f, GLint, GLfloat, GLfloat)                                              \
  X(void, Uniform1f, GLint, GLfloat)

#define PL_GL_DECLARE(ret, name, ...) inline ret(APIENTRY* name)(__VA_ARGS__) = nullptr;
PL_GL_FUNCS(PL_GL_DECLARE)
#undef PL_GL_DECLARE

// Call after glfwMakeContextCurrent. Returns the first missing function, or nullptr.
inline const char* load() {
#define PL_GL_LOAD(ret, name, ...)                                                         \
  name = reinterpret_cast<ret(APIENTRY*)(__VA_ARGS__)>(glfwGetProcAddress("gl" #name)); \
  if (name == nullptr) return "gl" #name;
  PL_GL_FUNCS(PL_GL_LOAD)
#undef PL_GL_LOAD
  return nullptr;
}

}  // namespace gl
