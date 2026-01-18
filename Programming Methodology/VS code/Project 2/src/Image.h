#ifndef IMAGE_H
#define IMAGE_H

#include "Matrix.h"
#include <string>

class Image : public Matrix<uint8_t> {
private:
    std::string filePath;
    int numChannels;
    int width;
    int height;

public:
    Image();
    explicit Image(const std::string& filePath);
    Image(const std::string& filePath, int numChannels, int width, int height);
    Image(const Image& other);
    Image& operator=(const Image& other);
    virtual ~Image();

    void resize(int newWidth, int newHeight);
    void save(const std::string& filePath) const;

    int getWidth() const { return width; }
    int getHeight() const { return height; }

    Image operator*(double scalar) const;
    Image operator+(const Image& other) const;
    Image operator-(const Image& other) const;
    Image operator*(const Image& other) const;
};

#endif // IMAGE_H