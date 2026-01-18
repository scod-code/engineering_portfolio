#ifndef MATRIX_H
#define MATRIX_H

#include "Vector.h"
#include <iostream>
#include <cstdint>

template <typename T>
class Matrix {
protected:
    Vector<Vector<T>> data;
    int numRows;
    int numCols;

public:
    // Default constructor
    Matrix() : numRows(0), numCols(0), data() {}

    // Constructor with rows and columns
    Matrix(int rows, int cols) : numRows(rows), numCols(cols), data(rows, Vector<T>(cols)) {}

    // Copy constructor
    Matrix(const Matrix& other) : numRows(other.numRows), numCols(other.numCols), data(other.data) {}

    // Destructor
    virtual ~Matrix() {}

    // Assignment operator
    Matrix& operator=(const Matrix& other) {
        if (this != &other) {
            numRows = other.numRows;
            numCols = other.numCols;
            data = other.data;
        }
        return *this;
    }

    // Subscript operator for non-const objects
    Vector<T>& operator[](int index) {
        if (index < 0 || index >= numRows) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    // Subscript operator for const objects
    const Vector<T>& operator[](int index) const {
        if (index < 0 || index >= numRows) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    // Get number of rows
    int getRows() const {
        return numRows;
    }

    // Get number of columns
    int getCols() const {
        return numCols;
    }

    // Matrix addition
    Matrix operator+(const Matrix& other) const {
        if (numRows != other.numRows || numCols != other.numCols) {
            throw std::invalid_argument("Matrices must have the same dimensions");
        }
        Matrix result(numRows, numCols);
        for (int i = 0; i < numRows; ++i) {
            for (int j = 0; j < numCols; ++j) {
                result[i][j] = data[i][j] + other[i][j];
            }
        }
        return result;
    }

    // Matrix subtraction
    Matrix operator-(const Matrix& other) const {
        if (numRows != other.numRows || numCols != other.numCols) {
            throw std::invalid_argument("Matrices must have the same dimensions");
        }
        Matrix result(numRows, numCols);
        for (int i = 0; i < numRows; ++i) {
            for (int j = 0; j < numCols; ++j) {
                result[i][j] = data[i][j] - other[i][j];
            }
        }
        return result;
    }

    // Matrix multiplication
    Matrix operator*(const Matrix& other) const {
        if (numCols != other.numRows) {
            throw std::invalid_argument("Matrices dimensions do not allow multiplication");
        }
        Matrix result(numRows, other.numCols);
        for (int i = 0; i < numRows; ++i) {
            for (int j = 0; j < other.numCols; ++j) {
                for (int k = 0; k < numCols; ++k) {
                    result[i][j] += data[i][k] * other[k][j];
                }
            }
        }
        return result;
    }

    // Input stream operator
    friend std::istream& operator>>(std::istream& in, Matrix& mat) {
        for (int i = 0; i < mat.numRows; ++i) {
            for (int j = 0; j < mat.numCols; ++j) {
                in >> mat[i][j];
            }
        }
        return in;
    }

    // Output stream operator
    friend std::ostream& operator<<(std::ostream& out, const Matrix& mat) {
        for (int i = 0; i < mat.numRows; ++i) {
            for (int j = 0; j < mat.numCols; ++j) {
                out << mat[i][j] << ' ';
            }
            out << std::endl;
        }
        return out;
    }
};
#include "Matrix.tpp"
#endif // MATRIX_H