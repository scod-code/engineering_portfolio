// helpers.c

// Include necessary headers
#include <stdlib.h>
#include "helpers.h"

// Define the missing functions
imatrix* resize_image_to_imatrix(imatrix* img, int new_width, int new_height) {
    // Allocate memory for the resized image matrices
    unsigned char* resized_r = malloc(new_width * new_height * sizeof(unsigned char));
    unsigned char* resized_g = malloc(new_width * new_height * sizeof(unsigned char));
    unsigned char* resized_b = malloc(new_width * new_height * sizeof(unsigned char));

    // Resize each color channel matrix
    stbir_resize_uint8(img->r, img->width, img->height, 0, resized_r, new_width, new_height, 0, 1);
    stbir_resize_uint8(img->g, img->width, img->height, 0, resized_g, new_width, new_height, 0, 1);
    stbir_resize_uint8(img->b, img->width, img->height, 0, resized_b, new_width, new_height, 0, 1);

    // Allocate memory for the resized image
    imatrix* resized_img = (imatrix*)malloc(sizeof(imatrix));
    resized_img->r = resized_r;
    resized_img->g = resized_g;
    resized_img->b = resized_b;
    resized_img->width = new_width;
    resized_img->height = new_height;
    
    // Free the original image
    free_imatrix(img);
    
    return resized_img;
}

imatrix* transpose(imatrix* img) {
    // Allocate memory for the transposed image matrices
    unsigned char* transposed_r = malloc(img->width * img->height * sizeof(unsigned char));
    unsigned char* transposed_g = malloc(img->width * img->height * sizeof(unsigned char));
    unsigned char* transposed_b = malloc(img->width * img->height * sizeof(unsigned char));

    // Transpose each color channel matrix
    for (int i = 0; i < img->height; i++) {
        for (int j = 0; j < img->width; j++) {
            transposed_r[j * img->height + i] = img->r[i * img->width + j];
            transposed_g[j * img->height + i] = img->g[i * img->width + j];
            transposed_b[j * img->height + i] = img->b[i * img->width + j];
        }
    }

    // Allocate memory for the transposed image
    imatrix* transposed_img = (imatrix*)malloc(sizeof(imatrix));
    transposed_img->r = transposed_r;
    transposed_img->g = transposed_g;
    transposed_img->b = transposed_b;
    transposed_img->width = img->height;
    transposed_img->height = img->width;
    
    // Free the original image
    free_imatrix(img);
    
    return transposed_img;
}

