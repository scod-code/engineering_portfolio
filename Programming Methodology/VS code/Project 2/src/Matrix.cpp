// Matrix.cpp

#include "Matrix.h"
#include <stdexcept>

// Default constructor
template <typename T>
Matrix<T>::Matrix() : numRows(0), numCols(0), data() {}

// Constructor with rows and columns
template <typename T>
Matrix<T>::Matrix(int rows, int cols) : numRows(rows), numCols(cols), data(rows, Vector<T>(cols)) {}

// Copy constructor
template <typename T>
Matrix<T>::Matrix(const Matrix& other) : numRows(other.numRows), numCols(other.numCols), data(other.data) {}

// Assignment operator
template <typename T>
Matrix<T>& Matrix<T>::operator=(const Matrix& other) {
    if (this != &other) {
        numRows = other.numRows;
        numCols = other.numCols;
        data = other.data;
    }
    return *this;
}

// Destructor
template <typename T>
Matrix<T>::~Matrix() {
    // No need for explicit cleanup since we're using std::vector in Vector
}

// Number of rows
template <typename T>
int Matrix<T>::getRows() const {
    return numRows;
}

// Number of columns
template <typename T>
int Matrix<T>::getCols() const {
    return numCols;
}

// Input stream operator
template <typename T>
std::istream& operator>>(std::istream& in, Matrix<T>& mat) {
    for (int i = 0; i < mat.numRows; ++i) {
        for (int j = 0; j < mat.numCols; ++j) {
            in >> mat.data[i][j];
        }
    }
    return in;
}

// Output stream operator
template <typename T>
std::ostream& operator<<(std::ostream& out, const Matrix<T>& mat) {
    for (int i = 0; i < mat.numRows; ++i) {
        for (int j = 0; j < mat.numCols; ++j) {
            out << mat.data[i][j] << ' ';
        }
        out << std::endl;
    }
    return out;
}

// Arithmetic operators
template <typename T>
Matrix<T> Matrix<T>::operator+(const Matrix<T>& other) const {
    if (numRows != other.numRows || numCols != other.numCols) {
        throw std::invalid_argument("Matrices must have the same dimensions to be added");
    }
    Matrix<T> result(numRows, numCols);
    for (int i = 0; i < numRows; ++i) {
        for (int j = 0; j < numCols; ++j) {
            result.data[i][j] = data[i][j] + other.data[i][j];
        }
    }
    return result;
}

template <typename T>
Matrix<T> Matrix<T>::operator-(const Matrix<T>& other) const {
    if (numRows != other.numRows || numCols != other.numCols) {
        throw std::invalid_argument("Matrices must have the same dimensions to be subtracted");
    }
    Matrix<T> result(numRows, numCols);
    for (int i = 0; i < numRows; ++i) {
        for (int j = 0; j < numCols; ++j) {
            result.data[i][j] = data[i][j] - other.data[i][j];
        }
    }
    return result;
}

template <typename T>
Matrix<T> Matrix<T>::operator*(const Matrix<T>& other) const {
    if (numCols != other.numRows) {
        throw std::invalid_argument("Matrices dimensions do not allow multiplication");
    }
    Matrix<T> result(numRows, other.numCols);
    for (int i = 0; i < numRows; ++i) {
        for (int j = 0; j < other.numCols; ++j) {
            for (int k = 0; k < numCols; ++k) {
                result.data[i][j] += data[i][k] * other.data[k][j];
            }
        }
    }
    return result;
}

// Subscript operator
template <typename T>
Vector<T>& Matrix<T>::operator[](int index) {
    if (index < 0 || index >= numRows) {
        throw std::out_of_range("Index out of range");
    }
    return data[index];
}

template <typename T>
const Vector<T>& Matrix<T>::operator[](int index) const {
    if (index < 0 || index >= numRows) {
        throw std::out_of_range("Index out of range");
    }
    return data[index];
}

// Transpose function (in-place)
template <typename T>
void Matrix<T>::transpose() {
    Matrix<T> transposed(numCols, numRows);
    for (int i = 0; i < numRows; ++i) {
        for (int j = 0; j < numCols; ++j) {
            transposed[j][i] = data[i][j];
        }
    }
    *this = std::move(transposed);
}

// Explicit template instantiation
template class Matrix<uint8_t>;

// Other explicit instantiations may be added as needed
// template class Matrix<int>;
// template class Matrix<float>;
// template class Matrix<double>;