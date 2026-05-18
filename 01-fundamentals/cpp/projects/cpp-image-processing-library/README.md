# C++ Image-Processing Library

Object-oriented C++ refactor of the image-processing library using explicit
`Image`, `Matrix`, and `Vector` abstractions.

## Structure

| Path | Purpose |
| --- | --- |
| `src/main.cpp` | Program entry point and demonstration workflow |
| `src/Image.cpp`, `src/Image.h` | Image-specific operations and file handling |
| `src/Matrix.cpp`, `src/Matrix.h`, `src/Matrix.tpp` | Matrix abstraction and templated implementation |
| `src/Vector.h` | Reusable vector abstraction |
| `stb_image/` | Third-party image read/write/resize headers |
| `project-brief.pdf` | Original coursework brief |

## Skills Demonstrated

C++ OOP, templates, operator overloading, constructors/destructors, composition,
Makefiles, image-processing operations, modular architecture.
