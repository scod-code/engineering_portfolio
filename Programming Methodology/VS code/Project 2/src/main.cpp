#include <iostream>
#include <string>
//#include <filesystem>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize.h"

#include "Image.h"
#include <iostream>

int main() {
    try {
        Image img("path_to_input_image.png");
        Image scaledImg = img * 0.5; // Scale by a factor of 0.5
        Image addedImg = img + img; // Add image to itself
        Image subtractedImg = img - img; // Subtract image from itself
        Image multipliedImg = img * img; // Multiply image by itself

        scaledImg.save("path_to_output_scaled_image.png");
        addedImg.save("path_to_output_added_image.png");
        subtractedImg.save("path_to_output_subtracted_image.png");
        multipliedImg.save("path_to_output_multiplied_image.png");
    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}