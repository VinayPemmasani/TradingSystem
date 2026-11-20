// packet-life-gl: the packet-life scene in native OpenGL 3.3 with GLFW. It reads the same
// order-trace output and scene.json as ../index.html and plays the same timeline: one
// order's messages moving between the lab's threads, switches and firms, each drawn as a
// strip of boxes, one per field, sized by the field's bytes.
//
//   packet-life-gl                                  trace.json and scene.json from ..
//   packet-life-gl --trace t.json --scene scene.json
//   packet-life-gl --t 40 --screenshot shot.png --size 1500x900    one frame to a PNG
//
// Keys: Space play/pause, Left/Right previous/next stage, F follow the packet,
// +/- speed, L light/dark, Esc quit. Mouse: drag to orbit, right-drag to pan, scroll to
// zoom, click the progress bar to seek.

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include "gl.hpp"
#include "json.hpp"
#include "stb_easy_font.h"

namespace {

// ---- Timeline rules, shared with ../index.html (keep the two in step) ---------------------
constexpr float kTravel = 10.0f;    // scene units per second at 1x
constexpr float kMinLeg = 1.4f;     // seconds for a leg that stays at one station
constexpr float kWaveGap = 0.5f;    // pause after each wave
constexpr float kStageGap = 1.8f;   // pause after each stage
constexpr const char* kFieldColors[] = {"#ff6b6b", "#ffd166", "#06d6a0", "#4cc9f0",
                                        "#b388ff", "#f78c6b", "#9ef01a", "#f15bb5"};
constexpr const char* kHeaderColor = "#7f8ea3";
constexpr float kPi = 3.14159265358979f;

// ---- Small math ----------------------------------------------------------------------------
struct V3 {
  float x = 0, y = 0, z = 0;
};
V3 operator+(V3 a, V3 b) { return {a.x + b.x, a.y + b.y, a.z + b.z}; }
V3 operator-(V3 a, V3 b) { return {a.x - b.x, a.y - b.y, a.z - b.z}; }
V3 operator*(V3 a, float s) { return {a.x * s, a.y * s, a.z * s}; }
float dot(V3 a, V3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
V3 cross(V3 a, V3 b) { return {a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x}; }
float length(V3 a) { return std::sqrt(dot(a, a)); }
V3 normalize(V3 a) { return a * (1.0f / std::max(1e-6f, length(a))); }
V3 lerp(V3 a, V3 b, float t) { return a + (b - a) * t; }

struct Color {
  float r = 1, g = 1, b = 1, a = 1;
};
Color hex_color(const std::string& h, float alpha = 1) {
  const unsigned v = static_cast<unsigned>(std::strtoul(h.c_str() + (h[0] == '#'), nullptr, 16));
  return {((v >> 16) & 255) / 255.0f, ((v >> 8) & 255) / 255.0f, (v & 255) / 255.0f, alpha};
}
Color with_alpha(Color c, float a) { return {c.r, c.g, c.b, a}; }

// Column-major 4x4, as GL expects.
struct M4 {
  std::array<float, 16> m{1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
};
M4 operator*(const M4& a, const M4& b) {
  M4 r;
  for (int c = 0; c < 4; ++c)
    for (int row = 0; row < 4; ++row) {
      float s = 0;
      for (int k = 0; k < 4; ++k) s += a.m[k * 4 + row] * b.m[c * 4 + k];
      r.m[c * 4 + row] = s;
    }
  return r;
}
M4 translate(V3 t) {
  M4 r;
  r.m[12] = t.x, r.m[13] = t.y, r.m[14] = t.z;
  return r;
}
M4 scale(V3 s) {
  M4 r;
  r.m[0] = s.x, r.m[5] = s.y, r.m[10] = s.z;
  return r;
}
// Same sense as three.js rotation.y: local +x turns toward -z for positive angles.
M4 rot_y(float a) {
  M4 r;
  const float c = std::cos(a), s = std::sin(a);
  r.m[0] = c, r.m[2] = -s, r.m[8] = s, r.m[10] = c;
  return r;
}
M4 perspective(float fovy, float aspect, float n, float f) {
  M4 r;
  const float t = 1.0f / std::tan(fovy / 2);
  r.m = {t / aspect, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) / (n - f), -1, 0, 0, 2 * f * n / (n - f), 0};
  return r;
}
M4 look_at(V3 eye, V3 target, V3 up) {
  const V3 f = normalize(target - eye), s = normalize(cross(f, up)), u = cross(s, f);
  M4 r;
  r.m = {s.x, u.x, -f.x, 0, s.y, u.y, -f.y, 0, s.z, u.z, -f.z, 0,
         -dot(s, eye), -dot(u, eye), dot(f, eye), 1};
  return r;
}
std::array<float, 4> apply(const M4& a, std::array<float, 4> v) {
  std::array<float, 4> r{};
  for (int row = 0; row < 4; ++row)
    for (int k = 0; k < 4; ++k) r[row] += a.m[k * 4 + row] * v[k];
  return r;
}

// stb_easy_font draws ASCII only.
std::string ascii(const std::string& s) {
  std::string o;
  for (std::size_t i = 0; i < s.size(); ++i) {
    const auto c = static_cast<unsigned char>(s[i]);
    if (c < 0x80) {
      o += c == '\t' ? ' ' : static_cast<char>(c);
      continue;
    }
    if (s.compare(i, 2, "\xC2\xB7") == 0) o += '-', i += 1;            // middle dot
    else if (s.compare(i, 3, "\xE2\x86\x92") == 0) o += "->", i += 2;  // right arrow
    else if (s.compare(i, 2, "\xC2\xB5") == 0) o += 'u', i += 1;       // micro
    else {
      o += '?';
      while (i + 1 < s.size() && (static_cast<unsigned char>(s[i + 1]) & 0xC0) == 0x80) ++i;
    }
  }
  return o;
}

// ---- Data ----------------------------------------------------------------------------------
struct Field {
  int off = 0, len = 0;
  std::string name, value;
};
struct Msg {
  std::string name, proto, link, note, hex, text;
  int size = 0;
  std::vector<Field> fields;
};
struct Stage {
  std::string id, where, title, body;
  std::vector<std::pair<std::string, std::array<float, 2>>> timing;
  std::vector<Msg> msgs;
};
struct Group {
  std::string id, label;
  Color color;
};
struct Station {
  std::string id, group, label;
  float x = 0, z = 0;
};
struct Leg {
  int stage = 0, wave = 0;
  const Msg* msg = nullptr;
  std::string label;
  std::vector<std::string> path;
  std::vector<V3> pts;
  float len = 0, dur = 0, t0 = 0;
};
struct Wave {
  int stage = 0;
  float t0 = 0, t1 = 0;
  std::vector<int> legs;
};

struct Model {
  std::vector<Stage> stages;
  std::vector<Group> groups;
  std::vector<Station> stations;
  std::vector<Leg> legs;
  std::vector<Wave> waves;
  std::vector<float> stage_start;
  float total = 0;

  const Station* station(const std::string& id) const {
    for (const auto& s : stations)
      if (s.id == id) return &s;
    return nullptr;
  }
  const Group* group(const std::string& id) const {
    for (const auto& g : groups)
      if (g.id == id) return &g;
    return nullptr;
  }
};

std::string read_file(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw std::runtime_error("cannot read " + path);
  std::stringstream ss;
  ss << f.rdbuf();
  return ss.str();
}

Model load(const std::string& trace_path, const std::string& scene_path) {
  const json::Value trace = json::parse(read_file(trace_path));
  const json::Value scene = json::parse(read_file(scene_path));
  Model m;
  m.stages.reserve(trace["stages"].arr.size());  // legs point into msgs; no reallocation
  for (const auto& s : trace["stages"].arr) {
    Stage st{s["id"].str, s["where"].str, s["title"].str, s["body"].str, {}, {}};
    for (const auto& [k, v] : s["timing"].obj)
      st.timing.push_back({k, {static_cast<float>(v[0].num), static_cast<float>(v[1].num)}});
    for (const auto& mj : s["msgs"].arr) {
      Msg msg{mj["name"].str, mj["proto"].str, mj["link"].str, mj["note"].str, mj["hex"].str,
              mj["text"].str, static_cast<int>(mj["size"].num), {}};
      for (const auto& f : mj["fields"].arr)
        msg.fields.push_back({static_cast<int>(f[0].num), static_cast<int>(f[1].num), f[2].str,
                              f[3].str});
      st.msgs.push_back(std::move(msg));
    }
    m.stages.push_back(std::move(st));
  }
  for (const auto& g : scene["groups"].arr)
    m.groups.push_back({g["id"].str, g["label"].str, hex_color(g["color"].str)});
  for (const auto& s : scene["stations"].arr)
    m.stations.push_back({s["id"].str, s["group"].str, s["label"].str,
                          static_cast<float>(s["x"].num), static_cast<float>(s["z"].num)});

  auto stage_index = [&](const std::string& id) {
    for (std::size_t i = 0; i < m.stages.size(); ++i)
      if (m.stages[i].id == id) return static_cast<int>(i);
    return -1;
  };
  for (const auto& l : scene["legs"].arr) {
    Leg leg;
    leg.stage = stage_index(l["stage"].str);
    if (leg.stage < 0) continue;
    leg.wave = static_cast<int>(l["wave"].num);
    const int src = l.find("from") ? stage_index(l["from"].str) : leg.stage;
    const int mi = static_cast<int>(l["msg"].number(-1));
    if (src >= 0 && mi >= 0 && mi < static_cast<int>(m.stages[src].msgs.size()))
      leg.msg = &m.stages[src].msgs[mi];
    leg.label = l["label"].str;
    for (const auto& p : l["path"].arr) {
      const Station* s = m.station(p.str);
      if (s == nullptr) throw std::runtime_error("scene.json: unknown station " + p.str);
      leg.path.push_back(p.str);
      leg.pts.push_back({s->x, 0, s->z});
    }
    for (std::size_t i = 1; i < leg.pts.size(); ++i) leg.len += length(leg.pts[i] - leg.pts[i - 1]);
    leg.dur = leg.pts.size() > 1 ? std::max(0.6f, leg.len / kTravel) : kMinLeg;
    m.legs.push_back(std::move(leg));
  }

  float t = 0;
  for (int si = 0; si < static_cast<int>(m.stages.size()); ++si) {
    m.stage_start.push_back(t);
    std::set<int> waves;
    for (const auto& l : m.legs)
      if (l.stage == si) waves.insert(l.wave);
    for (int w : waves) {
      Wave wave{si, t, t, {}};
      float dur = 0;
      for (int li = 0; li < static_cast<int>(m.legs.size()); ++li) {
        Leg& l = m.legs[li];
        if (l.stage != si || l.wave != w) continue;
        l.t0 = t;
        dur = std::max(dur, l.dur);
        wave.legs.push_back(li);
      }
      wave.t1 = t + dur;
      m.waves.push_back(wave);
      t += dur + kWaveGap;
    }
    t += kStageGap;
  }
  m.total = t;
  return m;
}

V3 point_at(const Leg& l, float p) {
  if (l.pts.size() == 1) return l.pts[0];
  float d = p * l.len;
  for (std::size_t i = 1; i < l.pts.size(); ++i) {
    const float seg = length(l.pts[i] - l.pts[i - 1]);
    if (d <= seg || i == l.pts.size() - 1)
      return lerp(l.pts[i - 1], l.pts[i], std::min(1.0f, seg > 0 ? d / seg : 1.0f));
    d -= seg;
  }
  return l.pts.back();
}

// Framing fields are grey; payload fields take the palette in order (as in index.html).
bool is_header(const std::string& n) {
  for (const char* p : {"Soup", "Message Type", "Message Length"})
    if (n.rfind(p, 0) == 0) return true;
  for (const char* e : {"Session", "Sequence Number", "Message Count", "8", "9", "10"})
    if (n == e) return true;
  return false;
}
Color field_color(std::size_t i, const std::string& name) {
  return hex_color(is_header(name) ? kHeaderColor : kFieldColors[i % std::size(kFieldColors)]);
}

std::string fmt_ns(float ns) {
  char b[32];
  if (ns >= 1000)
    std::snprintf(b, sizeof b, "%.2f us", ns / 1000);
  else
    std::snprintf(b, sizeof b, "%.1f ns", ns);
  return b;
}

// ---- GL helpers ----------------------------------------------------------------------------
gl::GLuint compile(gl::GLenum type, const char* src) {
  const gl::GLuint s = gl::CreateShader(type);
  gl::ShaderSource(s, 1, &src, nullptr);
  gl::CompileShader(s);
  gl::GLint ok = 0;
  gl::GetShaderiv(s, gl::COMPILE_STATUS, &ok);
  if (!ok) {
    char log[2048];
    gl::GetShaderInfoLog(s, sizeof log, nullptr, log);
    throw std::runtime_error(std::string("shader: ") + log);
  }
  return s;
}
gl::GLuint program(const char* vs, const char* fs) {
  const gl::GLuint p = gl::CreateProgram();
  const gl::GLuint v = compile(gl::VERTEX_SHADER, vs), f = compile(gl::FRAGMENT_SHADER, fs);
  gl::AttachShader(p, v);
  gl::AttachShader(p, f);
  gl::LinkProgram(p);
  gl::GLint ok = 0;
  gl::GetProgramiv(p, gl::LINK_STATUS, &ok);
  if (!ok) {
    char log[2048];
    gl::GetProgramInfoLog(p, sizeof log, nullptr, log);
    throw std::runtime_error(std::string("link: ") + log);
  }
  gl::DeleteShader(v);
  gl::DeleteShader(f);
  return p;
}

const char* kLitVs = R"(#version 330 core
layout(location = 0) in vec3 aPos;
uniform mat4 uVP, uModel;
out vec3 vWorld;
void main() {
  vec4 w = uModel * vec4(aPos, 1.0);
  vWorld = w.xyz;
  gl_Position = uVP * w;
})";

// Flat shading from screen-space derivatives: every mesh here is faceted, so no normals.
const char* kLitFs = R"(#version 330 core
in vec3 vWorld;
uniform vec4 uColor;
uniform float uEmissive, uUnlit;
uniform vec3 uEye, uBg;
out vec4 frag;
void main() {
  vec3 c = uColor.rgb;
  if (uUnlit < 0.5) {
    vec3 n = normalize(cross(dFdx(vWorld), dFdy(vWorld)));
    vec3 hemi = mix(vec3(0.10, 0.13, 0.19), vec3(0.90, 0.93, 1.0), n.y * 0.5 + 0.5);
    float sun = max(dot(n, normalize(vec3(-20.0, 50.0, 30.0))), 0.0);
    c = uColor.rgb * (hemi * 0.6 + sun * 0.7) + uColor.rgb * uEmissive;
  }
  float fog = smoothstep(70.0, 140.0, distance(vWorld, uEye));
  frag = vec4(mix(c, uBg, fog), uColor.a);
})";

const char* kUiVs = R"(#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec4 aColor;
uniform vec2 uScreen;
out vec4 vColor;
void main() {
  vColor = aColor;
  gl_Position = vec4(aPos.x / uScreen.x * 2.0 - 1.0, 1.0 - aPos.y / uScreen.y * 2.0, 0.0, 1.0);
})";

const char* kUiFs = R"(#version 330 core
in vec4 vColor;
out vec4 frag;
void main() { frag = vColor; })";

struct Mesh {
  gl::GLuint vao = 0, vbo = 0;
  int count = 0;
  gl::GLenum mode = gl::TRIANGLES;
};

Mesh make_mesh(const std::vector<float>& xyz, gl::GLenum mode = gl::TRIANGLES) {
  Mesh m;
  m.mode = mode;
  m.count = static_cast<int>(xyz.size() / 3);
  gl::GenVertexArrays(1, &m.vao);
  gl::BindVertexArray(m.vao);
  gl::GenBuffers(1, &m.vbo);
  gl::BindBuffer(gl::ARRAY_BUFFER, m.vbo);
  gl::BufferData(gl::ARRAY_BUFFER, static_cast<gl::GLsizeiptr>(xyz.size() * sizeof(float)),
                 xyz.data(), gl::STATIC_DRAW);
  gl::VertexAttribPointer(0, 3, gl::FLOAT, gl::kFalse, 3 * sizeof(float), nullptr);
  gl::EnableVertexAttribArray(0);
  return m;
}

void push_tri(std::vector<float>& v, V3 a, V3 b, V3 c) {
  for (V3 p : {a, b, c}) v.insert(v.end(), {p.x, p.y, p.z});
}

// Unit cube centred on the origin.
std::vector<float> cube() {
  std::vector<float> v;
  const V3 p[8] = {{-.5f, -.5f, -.5f}, {.5f, -.5f, -.5f}, {.5f, .5f, -.5f}, {-.5f, .5f, -.5f},
                   {-.5f, -.5f, .5f},  {.5f, -.5f, .5f},  {.5f, .5f, .5f},  {-.5f, .5f, .5f}};
  const int f[6][4] = {{4, 5, 6, 7}, {1, 0, 3, 2}, {5, 1, 2, 6}, {0, 4, 7, 3}, {7, 6, 2, 3}, {0, 1, 5, 4}};
  for (const auto& q : f) {
    push_tri(v, p[q[0]], p[q[1]], p[q[2]]);
    push_tri(v, p[q[0]], p[q[2]], p[q[3]]);
  }
  return v;
}

// Hexagonal prism, radius 1, height 1, centred.
std::vector<float> hex_prism() {
  std::vector<float> v;
  for (int i = 0; i < 6; ++i) {
    const float a0 = i * kPi / 3, a1 = (i + 1) * kPi / 3;
    const V3 b0{std::sin(a0), -.5f, std::cos(a0)}, b1{std::sin(a1), -.5f, std::cos(a1)};
    const V3 t0{b0.x, .5f, b0.z}, t1{b1.x, .5f, b1.z};
    push_tri(v, b0, b1, t1);
    push_tri(v, b0, t1, t0);
    push_tri(v, {0, .5f, 0}, t0, t1);
    push_tri(v, {0, -.5f, 0}, b1, b0);
  }
  return v;
}

// Icosphere, one subdivision, radius 1.
std::vector<float> sphere() {
  const float t = (1 + std::sqrt(5.0f)) / 2;
  std::vector<V3> p = {{-1, t, 0}, {1, t, 0}, {-1, -t, 0}, {1, -t, 0}, {0, -1, t}, {0, 1, t},
                       {0, -1, -t}, {0, 1, -t}, {t, 0, -1}, {t, 0, 1}, {-t, 0, -1}, {-t, 0, 1}};
  const int f[20][3] = {{0, 11, 5}, {0, 5, 1},  {0, 1, 7},   {0, 7, 10}, {0, 10, 11},
                        {1, 5, 9},  {5, 11, 4}, {11, 10, 2}, {10, 7, 6}, {7, 1, 8},
                        {3, 9, 4},  {3, 4, 2},  {3, 2, 6},   {3, 6, 8},  {3, 8, 9},
                        {4, 9, 5},  {2, 4, 11}, {6, 2, 10},  {8, 6, 7},  {9, 8, 1}};
  std::vector<float> v;
  for (const auto& tri : f) {
    const V3 a = normalize(p[tri[0]]), b = normalize(p[tri[1]]), c = normalize(p[tri[2]]);
    const V3 ab = normalize((a + b) * .5f), bc = normalize((b + c) * .5f), ca = normalize((c + a) * .5f);
    push_tri(v, a, ab, ca);
    push_tri(v, b, bc, ab);
    push_tri(v, c, ca, bc);
    push_tri(v, ab, bc, ca);
  }
  return v;
}

// ---- 2D overlay: triangles in pixels, one colour per vertex --------------------------------
class Ui {
 public:
  void clear() { v_.clear(); }
  void rect(float x, float y, float w, float h, Color c) {
    quad({x, y}, {x + w, y}, {x + w, y + h}, {x, y + h}, c);
  }
  // Returns the text's width in pixels.
  float text(float x, float y, const std::string& s, Color c, float scale, bool bold = false) {
    std::string a = ascii(s);
    static std::vector<char> buf(1 << 18);
    const int quads = stb_easy_font_print(0, 0, a.data(), nullptr, buf.data(), static_cast<int>(buf.size()));
    for (float dx : {0.0f, bold ? scale * 0.6f : -1.0f}) {
      if (dx < 0) break;
      for (int q = 0; q < quads; ++q) {
        const float* p = reinterpret_cast<const float*>(buf.data() + q * 64);
        auto at = [&](int k) {
          return std::array<float, 2>{x + dx + p[k * 4] * scale, y + p[k * 4 + 1] * scale};
        };
        quad(at(0), at(1), at(2), at(3), c);
      }
    }
    return width(s, scale);
  }
  static float width(const std::string& s, float scale) {
    std::string a = ascii(s);
    return static_cast<float>(stb_easy_font_width(a.data())) * scale;
  }
  const std::vector<float>& data() const { return v_; }

 private:
  void vert(std::array<float, 2> p, Color c) { v_.insert(v_.end(), {p[0], p[1], c.r, c.g, c.b, c.a}); }
  void quad(std::array<float, 2> a, std::array<float, 2> b, std::array<float, 2> c,
            std::array<float, 2> d, Color col) {
    vert(a, col), vert(b, col), vert(c, col);
    vert(a, col), vert(c, col), vert(d, col);
  }
  std::vector<float> v_;
};

// Greedy word wrap to a pixel width.
std::vector<std::string> wrap(const std::string& s, float max_w, float scale) {
  std::vector<std::string> lines;
  std::string line, word;
  std::istringstream in(ascii(s));
  while (in >> word) {
    const std::string next = line.empty() ? word : line + " " + word;
    if (!line.empty() && Ui::width(next, scale) > max_w) {
      lines.push_back(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (!line.empty()) lines.push_back(line);
  return lines;
}

// Hard wrap (for hex and FIX text, which have no useful spaces).
std::vector<std::string> chunk(const std::string& s, float max_w, float scale) {
  std::vector<std::string> out;
  std::string cur;
  for (char c : s) {
    if (!cur.empty() && Ui::width(cur + c, scale) > max_w) out.push_back(cur), cur.clear();
    cur += c;
  }
  if (!cur.empty()) out.push_back(cur);
  return out;
}

// ---- PNG writer (stored deflate blocks; small and dependency-free) -------------------------
std::uint32_t crc32(const unsigned char* p, std::size_t n, std::uint32_t c = 0xFFFFFFFFu) {
  for (std::size_t i = 0; i < n; ++i) {
    c ^= p[i];
    for (int k = 0; k < 8; ++k) c = (c >> 1) ^ (0xEDB88320u & (0u - (c & 1u)));
  }
  return c;
}
bool write_png(const std::string& path, int w, int h, const std::vector<unsigned char>& rgb) {
  std::vector<unsigned char> raw;
  for (int y = 0; y < h; ++y) {
    raw.push_back(0);
    const unsigned char* row = rgb.data() + static_cast<std::size_t>(h - 1 - y) * w * 3;  // GL is bottom-up
    raw.insert(raw.end(), row, row + static_cast<std::size_t>(w) * 3);
  }
  std::vector<unsigned char> z = {0x78, 0x01};
  std::uint32_t a = 1, b = 0;
  for (unsigned char c : raw) a = (a + c) % 65521, b = (b + a) % 65521;
  for (std::size_t i = 0; i < raw.size(); i += 65535) {
    const std::size_t n = std::min<std::size_t>(65535, raw.size() - i);
    z.push_back(i + n == raw.size());
    z.push_back(n & 255), z.push_back(n >> 8), z.push_back(~n & 255), z.push_back((~n >> 8) & 255);
    z.insert(z.end(), raw.begin() + static_cast<std::ptrdiff_t>(i), raw.begin() + static_cast<std::ptrdiff_t>(i + n));
  }
  const std::uint32_t adler = (b << 16) | a;
  for (int s = 24; s >= 0; s -= 8) z.push_back((adler >> s) & 255);

  std::FILE* f = std::fopen(path.c_str(), "wb");
  if (!f) return false;
  auto be32 = [&](std::uint32_t v) {
    const unsigned char o[4] = {static_cast<unsigned char>(v >> 24), static_cast<unsigned char>(v >> 16),
                                static_cast<unsigned char>(v >> 8), static_cast<unsigned char>(v)};
    std::fwrite(o, 1, 4, f);
  };
  auto chunk_out = [&](const char* type, const std::vector<unsigned char>& data) {
    be32(static_cast<std::uint32_t>(data.size()));
    std::vector<unsigned char> td(type, type + 4);
    td.insert(td.end(), data.begin(), data.end());
    std::fwrite(td.data(), 1, td.size(), f);
    be32(crc32(td.data(), td.size()) ^ 0xFFFFFFFFu);
  };
  const unsigned char sig[8] = {137, 80, 78, 71, 13, 10, 26, 10};
  std::fwrite(sig, 1, 8, f);
  std::vector<unsigned char> ihdr = {static_cast<unsigned char>(w >> 24), static_cast<unsigned char>(w >> 16),
                                     static_cast<unsigned char>(w >> 8), static_cast<unsigned char>(w),
                                     static_cast<unsigned char>(h >> 24), static_cast<unsigned char>(h >> 16),
                                     static_cast<unsigned char>(h >> 8), static_cast<unsigned char>(h),
                                     8, 2, 0, 0, 0};
  chunk_out("IHDR", ihdr);
  chunk_out("IDAT", z);
  chunk_out("IEND", {});
  return std::fclose(f) == 0;
}

// ---- Viewer --------------------------------------------------------------------------------
struct Theme {
  Color bg, floor, grid, tube, panel, line, text, muted, accent;
};
const Theme kDark{hex_color("#0a0e13"), hex_color("#0f151d"), hex_color("#1b2532"),
                  hex_color("#3a4a5e"), hex_color("#0f141c", 0.92f), hex_color("#243041"),
                  hex_color("#dbe3ec"), hex_color("#8a99ab"), hex_color("#5ab0ff")};
const Theme kLight{hex_color("#f3f5f8"), hex_color("#e7ecf2"), hex_color("#d2dae4"),
                   hex_color("#a9b6c6"), hex_color("#ffffff", 0.94f), hex_color("#d4dbe4"),
                   hex_color("#18212d"), hex_color("#5b6a7c"), hex_color("#2f7fd6")};

struct Viewer {
  Model model;
  GLFWwindow* win = nullptr;
  const Theme* theme = &kDark;
  gl::GLuint lit = 0, ui_prog = 0, ui_vao = 0, ui_vbo = 0;
  Mesh box, hex, ball, grid;
  Ui ui;

  float T = 0, speed = 1, spin = 0;
  bool playing = true, follow = false;
  // Orbit camera, starting where index.html does: eye (-8, 46, 54) looking at (-3, 0, 5).
  V3 target{-3, 0, 5};
  float yaw = std::atan2(-5.0f, 49.0f), pitch = std::asin(46.0f / std::sqrt(25.0f + 2116 + 2401));
  float dist = std::sqrt(25.0f + 2116 + 2401);
  double mx = 0, my = 0;
  bool drag_l = false, drag_r = false;
  float ui_scale = 1;
  struct Rect {
    float x = 0, y = 0, w = 0, h = 0;
  } rail;

  V3 eye() const {
    return target + V3{std::cos(pitch) * std::sin(yaw), std::sin(pitch), std::cos(pitch) * std::cos(yaw)} * dist;
  }

  void init() {
    lit = program(kLitVs, kLitFs);
    ui_prog = program(kUiVs, kUiFs);
    box = make_mesh(cube());
    hex = make_mesh(hex_prism());
    ball = make_mesh(sphere());
    std::vector<float> g;
    for (int i = -45; i <= 45; i += 2) {
      g.insert(g.end(), {static_cast<float>(i) - 3, 0.01f, -30, static_cast<float>(i) - 3, 0.01f, 40});
      if (i >= -35 && i <= 35)
        g.insert(g.end(), {-48, 0.01f, static_cast<float>(i) + 5, 42, 0.01f, static_cast<float>(i) + 5});
    }
    grid = make_mesh(g, gl::LINES);
    gl::GenVertexArrays(1, &ui_vao);
    gl::BindVertexArray(ui_vao);
    gl::GenBuffers(1, &ui_vbo);
    gl::BindBuffer(gl::ARRAY_BUFFER, ui_vbo);
    gl::VertexAttribPointer(0, 2, gl::FLOAT, gl::kFalse, 6 * sizeof(float), nullptr);
    gl::EnableVertexAttribArray(0);
    gl::VertexAttribPointer(1, 4, gl::FLOAT, gl::kFalse, 6 * sizeof(float),
                            reinterpret_cast<const void*>(2 * sizeof(float)));
    gl::EnableVertexAttribArray(1);
  }

  int stage_at() const {
    int s = 0;
    for (std::size_t i = 0; i < model.stage_start.size(); ++i)
      if (model.stage_start[i] <= T + 1e-4f) s = static_cast<int>(i);
    return s;
  }
  int wave_at() const {
    int w = -1;
    for (std::size_t i = 0; i < model.waves.size(); ++i)
      if (model.waves[i].t0 <= T) w = static_cast<int>(i);
    return w;
  }
  void next_stage() {
    const int s = stage_at();
    T = s + 1 < static_cast<int>(model.stages.size()) ? model.stage_start[s + 1] : 0;
  }
  void prev_stage() {
    const int s = stage_at();
    T = model.stage_start[T - model.stage_start[s] > 1 ? s : std::max(0, s - 1)];
  }

  // Packets in the current wave: position, heading and leg.
  struct Live {
    const Leg* leg;
    V3 pos;
    float heading;
  };
  std::vector<Live> live() const {
    std::vector<Live> out;
    const int wi = wave_at();
    if (wi < 0) return out;
    for (int li : model.waves[wi].legs) {
      const Leg& l = model.legs[li];
      const float prog = std::min(1.0f, (T - l.t0) / l.dur);
      V3 at = point_at(l, prog);
      const V3 ahead = point_at(l, std::min(1.0f, prog + 0.02f));
      float heading = spin;
      if (length(ahead - at) > 1e-3f) heading = std::atan2(-(ahead.z - at.z), ahead.x - at.x);
      at.y = 3.4f + 0.25f * std::sin(T * 6);
      out.push_back({&l, at, heading});
    }
    return out;
  }

  void draw_mesh(const Mesh& m, const M4& model_m, Color c, float emissive = 0, bool unlit = false) {
    gl::UniformMatrix4fv(gl::GetUniformLocation(lit, "uModel"), 1, gl::kFalse, model_m.m.data());
    gl::Uniform4f(gl::GetUniformLocation(lit, "uColor"), c.r, c.g, c.b, c.a);
    gl::Uniform1f(gl::GetUniformLocation(lit, "uEmissive"), emissive);
    gl::Uniform1f(gl::GetUniformLocation(lit, "uUnlit"), unlit ? 1.0f : 0.0f);
    gl::BindVertexArray(m.vao);
    gl::DrawArrays(m.mode, 0, m.count);
  }

  void frame(int fb_w, int fb_h, float dt) {
    if (playing) {
      T += dt * speed;
      if (T >= model.total) T = model.total, playing = false;
    }
    spin += dt * 1.8f;
    const auto packets = live();
    if (follow && !packets.empty()) {
      const V3 p = packets[0].pos;
      target = lerp(target, {p.x, 1, p.z}, 0.08f);
      dist += (25 - dist) * 0.05f;
    }

    const Theme& th = *theme;
    gl::Viewport(0, 0, fb_w, fb_h);
    gl::ClearColor(th.bg.r, th.bg.g, th.bg.b, 1);
    gl::Clear(gl::COLOR_BUFFER_BIT | gl::DEPTH_BUFFER_BIT);
    gl::Enable(gl::DEPTH_TEST);
    gl::Enable(gl::MULTISAMPLE);
    gl::Disable(gl::CULL_FACE);

    // Projection like index.html: 40 degree fov, zoomed out on narrow windows, and the scene
    // nudged left of centre so the story panel on the right does not cover it.
    const float aspect = static_cast<float>(fb_w) / std::max(1, fb_h);
    const float zoom = std::min(1.0f, aspect / 1.6f + 0.3f);
    const float fov = 2 * std::atan(std::tan(40 * kPi / 360) / zoom);
    M4 shift;
    shift.m[12] = -2.0f * 190 * ui_scale / static_cast<float>(fb_w) * (fb_w > 820 * ui_scale ? 1.0f : 0.0f);
    const V3 e = eye();
    const M4 vp = shift * perspective(fov, aspect, 0.1f, 400) * look_at(e, target, {0, 1, 0});

    gl::UseProgram(lit);
    gl::UniformMatrix4fv(gl::GetUniformLocation(lit, "uVP"), 1, gl::kFalse, vp.m.data());
    gl::Uniform3f(gl::GetUniformLocation(lit, "uEye"), e.x, e.y, e.z);
    gl::Uniform3f(gl::GetUniformLocation(lit, "uBg"), th.bg.r, th.bg.g, th.bg.b);

    // Floor and grid.
    draw_mesh(box, translate({-3, -0.05f, 5}) * scale({90, 0.04f, 70}), th.floor, 0, true);
    draw_mesh(grid, M4{}, th.grid, 0, true);

    // Links: every hop any leg uses, once.
    std::set<std::string> seen;
    for (const Leg& l : model.legs)
      for (std::size_t i = 1; i < l.pts.size(); ++i) {
        const std::string k = std::min(l.path[i - 1], l.path[i]) + "|" + std::max(l.path[i - 1], l.path[i]);
        if (!seen.insert(k).second) continue;
        const V3 a = l.pts[i - 1], b = l.pts[i], d = b - a;
        const V3 mid = (a + b) * 0.5f;
        draw_mesh(box, translate({mid.x, 0.5f, mid.z}) * rot_y(std::atan2(-d.z, d.x)) * scale({length(d), 0.22f, 0.22f}),
                  th.tube);
      }

    // Stations, glowing while a packet is on one.
    for (const Station& s : model.stations) {
      const Group* g = model.group(s.group);
      float glow = 0;
      for (const Live& p : packets)
        for (const auto& id : p.leg->path)
          if (id == s.id) {
            const float d = std::hypot(p.pos.x - s.x, p.pos.z - s.z);
            if (d < 3) glow = std::max(glow, 1 - d / 3);
          }
      const Color c = g ? g->color : Color{};
      if (s.group == "net")
        draw_mesh(hex, translate({s.x, 0.9f, s.z}) * scale({1.6f, 1.2f, 1.6f}), c, 0.6f * glow);
      else
        draw_mesh(box, translate({s.x, 1.1f, s.z}) * scale({3.2f, 1.6f, 3.2f}), c, 0.6f * glow);
    }

    // Packets: a strip of boxes, one per field, sized by bytes.
    for (const Live& p : packets) {
      const M4 base = translate(p.pos) * rot_y(p.heading);
      if (p.leg->msg == nullptr) {
        draw_mesh(ball, base * scale({1, 1, 1}), {1, 1, 1, 1}, 0.4f);
        continue;
      }
      const Msg& m = *p.leg->msg;
      const float size = static_cast<float>(std::max(1, m.size));
      const float len = 2 + 6 * std::sqrt(size / 172);
      float x = -len / 2;
      for (std::size_t i = 0; i < m.fields.size(); ++i) {
        const float w = std::max(0.04f, m.fields[i].len / size * len);
        draw_mesh(box, base * translate({x + w / 2, 0, 0}) * scale({w * 0.94f, 1.1f, 1.4f}),
                  field_color(i, m.fields[i].name), 0.35f);
        x += w;
      }
    }

    // Translucent pads under each group, after the opaque pass.
    gl::Enable(gl::BLEND);
    gl::BlendFunc(gl::SRC_ALPHA, gl::ONE_MINUS_SRC_ALPHA);
    gl::DepthMask(gl::kFalse);
    std::vector<std::array<float, 4>> pads;
    for (const Group& g : model.groups) {
      float x0 = 1e9f, x1 = -1e9f, z0 = 1e9f, z1 = -1e9f;
      for (const Station& s : model.stations)
        if (s.group == g.id)
          x0 = std::min(x0, s.x), x1 = std::max(x1, s.x), z0 = std::min(z0, s.z), z1 = std::max(z1, s.z);
      if (x0 > x1) {
        pads.push_back({0, 0, 0, 0});
        continue;
      }
      x0 -= 3.5f, x1 += 3.5f, z0 -= 3.5f, z1 += 3.5f;
      pads.push_back({x0, x1, z0, z1});
      draw_mesh(box, translate({(x0 + x1) / 2, 0.15f, (z0 + z1) / 2}) * scale({x1 - x0, 0.3f, z1 - z0}),
                with_alpha(g.color, 0.16f), 0, true);
    }
    gl::DepthMask(gl::kTrue);

    // ---- Overlay ----
    ui.clear();
    const float s = ui_scale;
    auto project = [&](V3 p, float& sx, float& sy) {
      const auto c = apply(vp, {p.x, p.y, p.z, 1});
      if (c[3] <= 0) return false;
      sx = (c[0] / c[3] * 0.5f + 0.5f) * fb_w;
      sy = (1 - (c[1] / c[3] * 0.5f + 0.5f)) * fb_h;
      return true;
    };
    auto tag = [&](V3 p, const std::string& text, Color bg, Color fg) {
      float x, y;
      if (!project(p, x, y)) return;
      const float ts = 1.6f * s, w = Ui::width(text, ts);
      ui.rect(x - w / 2 - 5 * s, y - 8 * s, w + 10 * s, 16 * s, bg);
      ui.text(x - w / 2, y - 5 * s, text, fg, ts);
    };
    for (std::size_t i = 0; i < model.groups.size(); ++i) {
      const auto& b = pads[i];
      if (b[1] <= b[0]) continue;
      float x, y;
      if (project({(b[0] + b[1]) / 2, 0.4f, b[3] + 0.9f}, x, y)) {
        const float w = Ui::width(model.groups[i].label, 1.8f * s);
        ui.text(x - w / 2, y, model.groups[i].label, th.text, 1.8f * s, true);
      }
    }
    for (const Station& st : model.stations) tag({st.x, 2.6f, st.z}, st.label, th.panel, th.text);
    for (const Live& p : packets) {
      std::string label = p.leg->label;
      if (p.leg->msg) {
        label = p.leg->msg->name;
        if (auto k = label.find(" ("); k != std::string::npos) label.resize(k);
        label += " - " + std::to_string(p.leg->msg->size) + " B";
      }
      if (!label.empty()) tag(p.pos + V3{0, 1.6f, 0}, label, {0.08f, 0.12f, 0.18f, 0.85f}, {1, 1, 1, 1});
    }
    draw_panels(fb_w, fb_h, packets);

    gl::Disable(gl::DEPTH_TEST);
    gl::UseProgram(ui_prog);
    gl::Uniform2f(gl::GetUniformLocation(ui_prog, "uScreen"), static_cast<float>(fb_w), static_cast<float>(fb_h));
    gl::BindVertexArray(ui_vao);
    gl::BindBuffer(gl::ARRAY_BUFFER, ui_vbo);
    gl::BufferData(gl::ARRAY_BUFFER, static_cast<gl::GLsizeiptr>(ui.data().size() * sizeof(float)),
                   ui.data().data(), gl::STREAM_DRAW);
    gl::DrawArrays(gl::TRIANGLES, 0, static_cast<gl::GLsizei>(ui.data().size() / 6));
    gl::Disable(gl::BLEND);

    const int si = stage_at();
    const std::string title = "Packet life - stage " + std::to_string(si + 1) + "/" +
                              std::to_string(model.stages.size()) + ": " + ascii(model.stages[si].title);
    glfwSetWindowTitle(win, title.c_str());
  }

  void panel_box(float x, float y, float w, float h) {
    const float b = 1 * ui_scale;
    ui.rect(x - b, y - b, w + 2 * b, h + 2 * b, theme->line);
    ui.rect(x, y, w, h, with_alpha(theme->panel, 1.0f));
  }

  void draw_panels(int fb_w, int fb_h, const std::vector<Live>& packets) {
    const Theme& th = *theme;
    const float s = ui_scale, ts = 1.6f * s, lh = 16 * s, pad = 14 * s;
    const int si = stage_at();
    const Stage& st = model.stages[si];

    // Legend, top left.
    {
      const float x = 12 * s, y = 12 * s, w = 300 * s;
      const float h = pad * 2 + lh * (4 + model.groups.size()) + 10 * s;
      panel_box(x, y, w, h);
      float cy = y + pad;
      ui.text(x + pad, cy, "One order's packet life", th.text, 1.9f * s, true);
      cy += lh * 1.3f;
      ui.text(x + pad, cy, "Data: tools/order-trace", th.muted, ts);
      cy += lh * 1.2f;
      for (const Group& g : model.groups) {
        ui.rect(x + pad, cy, 9 * s, 9 * s, g.color);
        ui.text(x + pad + 15 * s, cy, g.label, th.text, ts);
        cy += lh;
      }
      float sum = 0;
      for (int i = 0; i <= si; ++i)
        for (const auto& t : model.stages[i].timing) sum += t.second[0];
      cy += 4 * s;
      ui.text(x + pad, cy, "In-process work so far (p50 sum)", th.muted, ts);
      cy += lh;
      ui.text(x + pad, cy, fmt_ns(sum) + " over " + std::to_string(si + 1) + " stage" + (si ? "s" : ""),
              th.text, 1.9f * s, true);
    }

    // Story, right.
    const float bar_h = 50 * s;
    const float w = 420 * s, x = fb_w - w - 12 * s, y = 12 * s, h = fb_h - bar_h - 36 * s;
    panel_box(x, y, w, h);
    const float inner = w - 2 * pad, bottom = y + h - pad;
    float cy = y + pad;
    auto line = [&](const std::string& t, Color c, float scale = 0, bool bold = false) {
      if (cy + lh > bottom) return;
      const float sc = scale > 0 ? scale : ts;
      std::string fit = ascii(t);
      while (fit.size() > 3 && Ui::width(fit, sc) > inner) fit.resize(fit.size() - 4), fit += "...";
      ui.text(x + pad, cy, fit, c, sc, bold);
      cy += scale > ts ? lh * 1.3f : lh;
    };
    line("Stage " + std::to_string(si + 1) + " of " + std::to_string(model.stages.size()) + " - " + st.where,
         th.muted);
    for (const auto& l : wrap(st.title, inner, 2.1f * s)) line(l, th.text, 2.1f * s, true);
    cy += 3 * s;
    for (const auto& l : wrap(st.body, inner, ts)) line(l, th.text);
    if (!st.timing.empty()) {
      cy += 6 * s;
      line("MEASURED ON THIS MACHINE (P50 / P99)", th.muted);
      float max99 = 1;
      for (const auto& t : st.timing) max99 = std::max(max99, t.second[1]);
      for (const auto& t : st.timing) {
        if (cy + lh * 1.6f > bottom) break;
        const std::string v = fmt_ns(t.second[0]) + "  /  " + fmt_ns(t.second[1]);
        ui.text(x + pad, cy, t.first, th.text, ts);
        if (Ui::width(t.first, ts) + Ui::width(v, ts) + 12 * s > inner) cy += lh;  // no room: next line
        ui.text(x + w - pad - Ui::width(v, ts), cy, v, th.muted, ts);
        cy += lh;
        ui.rect(x + pad, cy, inner * t.second[0] / max99, 4 * s, with_alpha(th.accent, 0.8f));
        cy += 8 * s;
      }
    }
    if (!st.msgs.empty()) {
      cy += 6 * s;
      line("MESSAGES", th.muted);
    }
    for (const Msg& m : st.msgs) {
      bool is_live = false;
      for (const Live& p : packets) is_live |= p.leg->msg == &m;
      if (cy + lh * 2 > bottom) break;
      line(m.name, is_live ? th.accent : th.text, 0, true);
      line(m.proto + " - " + std::to_string(m.size) + " bytes - " + m.link, th.muted);
      if (!is_live) {
        cy += 4 * s;
        continue;
      }
      // Bytes, coloured by field, wrapped to the panel.
      const float bs = 1.5f * s;
      float bx = x + pad;
      for (std::size_t i = 0; i < m.fields.size(); ++i) {
        const Field& f = m.fields[i];
        std::string piece;
        if (!m.hex.empty()) {
          for (int k = 0; k < f.len; ++k) {
            const std::size_t at = static_cast<std::size_t>(f.off + k) * 2;
            if (at + 2 <= m.hex.size()) piece += m.hex.substr(at, 2) + " ";
          }
        } else if (!m.text.empty() && static_cast<std::size_t>(f.off) < m.text.size()) {
          piece = m.text.substr(f.off, f.len);
        }
        const Color c = field_color(i, f.name);
        for (const auto& part : chunk(piece, inner, bs)) {
          const float pw = Ui::width(part, bs);
          if (bx + pw > x + w - pad) bx = x + pad, cy += lh;
          if (cy + lh > bottom) break;
          ui.text(bx, cy, part, c, bs);
          bx += pw + (m.hex.empty() ? 0 : 2 * s);
        }
      }
      cy += lh * 1.4f;
      float name_w = 0;
      for (const Field& f : m.fields) name_w = std::max(name_w, Ui::width(f.name, ts));
      const float vx = x + pad + std::min(name_w + 26 * s, inner * 0.55f);
      for (std::size_t i = 0; i < m.fields.size(); ++i) {
        const Field& f = m.fields[i];
        if (cy + lh > bottom) break;
        ui.rect(x + pad, cy + 1 * s, 8 * s, 8 * s, field_color(i, f.name));
        ui.text(x + pad + 14 * s, cy, f.name, th.text, ts);
        std::string v = f.value;
        while (!v.empty() && Ui::width(v, ts) > x + w - pad - vx) v.pop_back();
        ui.text(vx, cy, v, th.muted, ts);
        cy += lh;
      }
      cy += 6 * s;
    }

    // Progress bar and keys, bottom.
    const float bx = 12 * s, by = fb_h - bar_h - 12 * s, bw = fb_w - 24 * s;
    panel_box(bx, by, bw, bar_h);
    const std::string state = std::string(playing ? "Playing" : "Paused") + "  " +
                              (speed == 0.5f ? "0.5x" : speed == 1 ? "1x" : "2x");
    ui.text(bx + pad, by + 10 * s, state, th.text, ts, true);
    const std::string keys = "Space play  <- -> stage  F follow  +/- speed  L theme  drag orbit, right-drag pan, scroll zoom";
    ui.text(bx + pad, by + 30 * s, keys, th.muted, 1.4f * s);
    rail = {bx + 110 * s, by + 12 * s, bw - 125 * s, 6 * s};
    ui.rect(rail.x, rail.y, rail.w, rail.h, th.line);
    ui.rect(rail.x, rail.y, rail.w * T / model.total, rail.h, th.accent);
    for (std::size_t i = 0; i < model.stage_start.size(); ++i) {
      const float tx = rail.x + rail.w * model.stage_start[i] / model.total;
      ui.rect(tx, rail.y - 4 * s, 2 * s, rail.h + 8 * s, th.muted);
      ui.text(tx + 4 * s, rail.y - 8 * s, std::to_string(i + 1), th.muted, 1.2f * s);
    }
  }
};

Viewer* g_viewer = nullptr;

void on_key(GLFWwindow* w, int key, int, int action, int) {
  if (action == GLFW_RELEASE) return;
  Viewer& v = *g_viewer;
  switch (key) {
    case GLFW_KEY_ESCAPE: glfwSetWindowShouldClose(w, 1); break;
    case GLFW_KEY_SPACE:
      if (!v.playing && v.T >= v.model.total - 0.01f) v.T = 0;
      v.playing = !v.playing;
      break;
    case GLFW_KEY_RIGHT: v.next_stage(); break;
    case GLFW_KEY_LEFT: v.prev_stage(); break;
    case GLFW_KEY_F:
      v.follow = !v.follow;
      if (!v.follow) v.target = {-3, 0, 5}, v.dist = std::sqrt(25.0f + 2116 + 2401);
      break;
    case GLFW_KEY_EQUAL:
    case GLFW_KEY_KP_ADD: v.speed = std::min(2.0f, v.speed * 2); break;
    case GLFW_KEY_MINUS:
    case GLFW_KEY_KP_SUBTRACT: v.speed = std::max(0.5f, v.speed / 2); break;
    case GLFW_KEY_L: v.theme = v.theme == &kDark ? &kLight : &kDark; break;
    default: break;
  }
}

void on_button(GLFWwindow* w, int button, int action, int) {
  Viewer& v = *g_viewer;
  double x, y;
  glfwGetCursorPos(w, &x, &y);
  int ww, wh, fw, fh;
  glfwGetWindowSize(w, &ww, &wh);
  glfwGetFramebufferSize(w, &fw, &fh);
  const float fx = static_cast<float>(x) * fw / std::max(1, ww), fy = static_cast<float>(y) * fh / std::max(1, wh);
  if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS && fx >= v.rail.x && fx <= v.rail.x + v.rail.w &&
      fy >= v.rail.y - 10 * v.ui_scale && fy <= v.rail.y + v.rail.h + 10 * v.ui_scale) {
    v.T = v.model.total * (fx - v.rail.x) / v.rail.w;
    return;
  }
  if (button == GLFW_MOUSE_BUTTON_LEFT) v.drag_l = action == GLFW_PRESS;
  if (button == GLFW_MOUSE_BUTTON_RIGHT) v.drag_r = action == GLFW_PRESS;
  v.mx = x, v.my = y;
}

void on_move(GLFWwindow*, double x, double y) {
  Viewer& v = *g_viewer;
  const float dx = static_cast<float>(x - v.mx), dy = static_cast<float>(y - v.my);
  v.mx = x, v.my = y;
  if (v.drag_l) {
    v.yaw -= dx * 0.006f;
    v.pitch = std::clamp(v.pitch + dy * 0.006f, 0.12f, kPi * 0.47f);
  } else if (v.drag_r) {
    const V3 right{std::cos(v.yaw), 0, -std::sin(v.yaw)}, fwd{-std::sin(v.yaw), 0, -std::cos(v.yaw)};
    const float k = v.dist * 0.0018f;
    v.target = v.target - right * (dx * k) + fwd * (dy * k);
  }
}

void on_scroll(GLFWwindow*, double, double dy) {
  Viewer& v = *g_viewer;
  v.dist = std::clamp(v.dist * std::pow(0.9f, static_cast<float>(dy)), 8.0f, 160.0f);
}

std::string default_path(const char* name) {
  for (const std::string& dir : {std::string("."), std::string(".."), std::string(PACKET_LIFE_DATA_DIR)}) {
    const std::string p = dir + "/" + name;
    if (std::ifstream(p)) return p;
  }
  return name;
}

}  // namespace

int main(int argc, char** argv) {
  std::string trace = default_path("trace.json"), scene = default_path("scene.json"), shot;
  float start_t = 0;
  int width = 1500, height = 900;
  bool light = false, start_t_set = false;
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    const char* v = i + 1 < argc ? argv[i + 1] : nullptr;
    if (a == "--trace" && v) trace = v, ++i;
    else if (a == "--scene" && v) scene = v, ++i;
    else if (a == "--screenshot" && v) shot = v, ++i;
    else if (a == "--t" && v) start_t = std::strtof(v, nullptr), start_t_set = true, ++i;
    else if (a == "--size" && v) std::sscanf(v, "%dx%d", &width, &height), ++i;
    else if (a == "--light") light = true;
    else {
      std::fprintf(stderr,
                   "usage: packet-life-gl [--trace FILE] [--scene FILE] [--t SECONDS] [--light]\n"
                   "                      [--screenshot OUT.png] [--size WxH]\n");
      return 2;
    }
  }

  Viewer v;
  try {
    v.model = load(trace, scene);
  } catch (const std::exception& e) {
    std::fprintf(stderr, "packet-life-gl: %s\n", e.what());
    return 2;
  }
  if (v.model.stages.empty() || v.model.waves.empty()) {
    std::fprintf(stderr, "packet-life-gl: nothing to play in %s\n", trace.c_str());
    return 2;
  }
  if (!glfwInit()) {
    std::fprintf(stderr, "packet-life-gl: glfwInit failed (no display?)\n");
    return 1;
  }
  glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
  glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
  glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
  glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);  // macOS needs it for 3.3 core
  glfwWindowHint(GLFW_SAMPLES, 4);
  if (!shot.empty()) glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);
  v.win = glfwCreateWindow(width, height, "Packet life", nullptr, nullptr);
  if (v.win == nullptr) {
    std::fprintf(stderr, "packet-life-gl: cannot create an OpenGL 3.3 core window\n");
    glfwTerminate();
    return 1;
  }
  glfwMakeContextCurrent(v.win);
  glfwSwapInterval(1);
  if (const char* missing = gl::load()) {
    std::fprintf(stderr, "packet-life-gl: OpenGL function %s not available\n", missing);
    return 1;
  }
  g_viewer = &v;
  glfwSetKeyCallback(v.win, on_key);
  glfwSetMouseButtonCallback(v.win, on_button);
  glfwSetCursorPosCallback(v.win, on_move);
  glfwSetScrollCallback(v.win, on_scroll);
  try {
    v.init();
  } catch (const std::exception& e) {
    std::fprintf(stderr, "packet-life-gl: %s\n", e.what());
    return 1;
  }
  if (light) v.theme = &kLight;
  if (start_t_set) v.T = start_t, v.playing = false;

  int rc = 0;
  double last = glfwGetTime();
  while (!glfwWindowShouldClose(v.win)) {
    int fw, fh, ww, wh;
    glfwGetFramebufferSize(v.win, &fw, &fh);
    glfwGetWindowSize(v.win, &ww, &wh);
    // Text and panels scale with the display (Retina, Windows scaling) and with big windows.
    v.ui_scale = (ww > 0 ? static_cast<float>(fw) / ww : 1.0f) * std::clamp(wh / 900.0f, 0.8f, 1.6f);
    const double now = glfwGetTime();
    v.frame(fw, fh, static_cast<float>(std::min(0.1, now - last)));
    last = now;
    if (!shot.empty()) {
      std::vector<unsigned char> px(static_cast<std::size_t>(fw) * fh * 3);
      gl::PixelStorei(gl::PACK_ALIGNMENT, 1);
      gl::ReadPixels(0, 0, fw, fh, gl::RGB, gl::UNSIGNED_BYTE, px.data());
      rc = write_png(shot, fw, fh, px) ? 0 : 1;
      std::printf("Wrote %s (%dx%d) at t=%.1f s, stage %d\n", shot.c_str(), fw, fh, v.T, v.stage_at() + 1);
      break;
    }
    glfwSwapBuffers(v.win);
    glfwPollEvents();
  }
  glfwDestroyWindow(v.win);
  glfwTerminate();
  return rc;
}
