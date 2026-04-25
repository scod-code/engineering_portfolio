// Matrix.tpp - Implementation of the Matrix class template

template <typename T>
Matrix<T>::Matrix() : numRows(0), numCols(0), data() {}

template <typename T>
Matrix<T>::Matrix(int rows, int cols) : numRows(rows), numCols(cols), data(rows, Vector<T>(cols)) {}

template <typename T>
Matrix<T>::Matrix(const Matrix& other) : numRows(other.numRows), numCols(other.numCols), data(other.data) {}

template <typename T>
Matrix<T>::~Matrix() {}

template <typename T>
Matrix<T>& Matrix<T>::operator=(const Matrix& other) {
    if (this != &other) {
        numRows = other.numRows;
        numCols = other.numCols;
        data = other.data;
    }
    return *this;
}

template <typename T>
Vector<T>& Matrix<T>::operator[](int index) {
    return data[index];
}

template <typename T>
const Vector<T>& Matrix<T>::operator[](int index) const {
    return data[index];
}

template <typename T>
int Matrix<T>::getRows() const {
    return numRows;
}

template <typename T>
int Matrix<T>::getCols() const {
    return numCols;
}

template <typename T>
Matrix<T> Matrix<T>::operator+(const Matrix& other) const {
    // Implement matrix addition
}

template <typename T>
Matrix<T> Matrix<T>::operator-(const Matrix& other) const {
    // Implement matrix subtraction
}

template <typename T>
Matrix<T> Matrix<T>::operator*(const Matrix& other) const {
    // Implement matrix multiplication
}

template <typename T>
std::istream& operator>>(std::istream& in, Matrix<T>& mat) {
    // Implement input stream operator
}

template <typename T>
std::ostream& operator<<(std::ostream& out, const Matrix<T>& mat) {
    // Implement output stream operator
}