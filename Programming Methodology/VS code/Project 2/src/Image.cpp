// Image.cpp

#include "Image.h"
#include "stb_image.h"
#include "stb_image_write.h"
#include "stb_image_resize.h"
#include <algorithm>
#include <stdexcept>
#include <vector>

// Default constructor
Image::Image() : Matrix<uint8_t>(), filePath(""), numChannels(0), width(0), height(0) {}

// Constructor with file path
Image::Image(const std::string& filePath) : Matrix<uint8_t>() {
    // Load the image using stb_image
    int w, h, channels;
    uint8_t* imageData = stbi_load(filePath.c_str(), &w, &h, &channels, 0);
    if (!imageData) {
        throw std::runtime_error("Failed to load image");
    }

    // Initialize the Matrix base class with the image data
    // Assuming Matrix has a constructor that takes dimensions and data
    *this = Image(filePath, channels, w, h);

    // Free the loaded image data
    stbi_image_free(imageData);
}

// Constructor with file path, channels, width, and height
Image::Image(const std::string& filePath, int numChannels, int width, int height)
    : Matrix<uint8_t>(height, width * numChannels), filePath(filePath), numChannels(numChannels), width(width), height(height) {
    // Initialize the matrix data with zeros or actual image data if provided
}

// Copy constructor
Image::Image(const Image& other)
    : Matrix<uint8_t>(other), filePath(other.filePath), numChannels(other.numChannels), width(other.width), height(other.height) {}

// Assignment operator
Image& Image::operator=(const Image& other) {
    if (this != &other) {
        Matrix<uint8_t>::operator=(other);
        filePath = other.filePath;
        numChannels = other.numChannels;
        width = other.width;
        height = other.height;
    }
    return *this;
}

// Implement the resize function using stb_image_resize
void Image::resize(int newWidth, int newHeight) {
    // Create a new vector of vectors with the new dimensions
    Vector<Vector<uint8_t>> newData(newHeight, Vector<uint8_t>(newWidth * numChannels));

    // Prepare a flat array to use with stb_image_resize
    std::vector<uint8_t> flatData(newWidth * newHeight * numChannels);
    for (int i = 0; i < newHeight; ++i) {
        for (int j = 0; j < newWidth * numChannels; ++j) {
            flatData[i * newWidth * numChannels + j] = newData[i][j];
        }
    }

    // Resize the image
    stbir_resize_uint8(&data[0][0], width, height, 0, &flatData[0], newWidth, newHeight, 0, numChannels);

    // Update the Image object's properties
    width = newWidth;
    height = newHeight;
    for (int i = 0; i < newHeight; ++i) {
        for (int j = 0; j < newWidth * numChannels; ++j) {
            newData[i][j] = flatData[i * newWidth * numChannels + j];
        }
    }
    data = newData;
}

// Implement the save function using stb_image_write
void Image::save(const std::string& filePath) const {
    // Prepare a flat array to use with stb_image_write
    std::vector<uint8_t> flatData(width * height * numChannels);
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width * numChannels; ++j) {
            flatData[i * width * numChannels + j] = data[i][j];
        }
    }

    // Save the image to a file
    stbi_write_png(filePath.c_str(), width, height, numChannels, &flatData[0], width * numChannels);
}

// Destructor
Image::~Image() {
    // No dynamic memory to free, but if there were, it would be done here
}

// Scaling an image
Image Image::operator*(double scalar) const {
    // Implement image scaling logic here
    // This will likely involve creating a new Image object with scaled dimensions
    // and using stb_image_resize to resize the current image data into it
}

// Adding two images
Image Image::operator+(const Image& other) const {
    // Implement image addition logic here
    // Ensure both images have the same dimensions and number of channels
}

// Subtracting two images
Image Image::operator-(const Image& other) const {
    // Implement image subtraction logic here
    // Ensure both images have the same dimensions and number of channels
}

// Multiplying two images
Image Image::operator*(const Image& other) const {
    // Implement image multiplication logic here
    // Ensure both images have the same dimensions and number of channels
}

// Resize function
void Image::resize(int newWidth, int newHeight) {
    // Implement image resizing logic here using stb_image_resize
    // You will need to allocate a new buffer for the resized image,
    // call the appropriate stb_image_resize function, and then update
    // the Image object's properties and data to reflect the new size
}

// getWidth and getHeight are already implemented correctly

// Save function is implemented correctly, assuming the data layout in Matrix is row-major
