#ifndef VECTOR_H
#define VECTOR_H

#include <iostream>
#include <vector>
#include <stdexcept>

template<typename T>
class Vector {
private:
    std::vector<T> data;

public:
    Vector() {}
    explicit Vector(int size) : data(size) {}
    Vector(const Vector& other) : data(other.data) {}
    virtual ~Vector() {}

    Vector& operator=(const Vector& other) {
        if (this != &other) {
            data = other.data;
        }
        return *this;
    }

    int getSize() const {
        return data.size();
    }

    T& operator[](int index) {
        if (index < 0 || index >= data.size()) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    const T& operator[](int index) const {
        if (index < 0 || index >= data.size()) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    Vector operator+(const Vector& other) const {
        if (data.size() != other.data.size()) {
            throw std::invalid_argument("Vectors must be of the same size");
        }
        Vector result(data.size());
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] + other.data[i];
        }
        return result;
    }

    Vector operator-(const Vector& other) const {
        if (data.size() != other.data.size()) {
            throw std::invalid_argument("Vectors must be of the same size");
        }
        Vector result(data.size());
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] - other.data[i];
        }
        return result;
    }

    T operator*(const Vector& other) const {
        if (data.size() != other.data.size()) {
            throw std::invalid_argument("Vectors must be of the same size");
        }
        T result = 0;
        for (size_t i = 0; i < data.size(); ++i) {
            result += data[i] * other.data[i];
        }
        return result;
    }

    friend std::istream& operator>>(std::istream& is, Vector& vec) {
        for (auto& element : vec.data) {
            is >> element;
        }
        return is;
    }

    friend std::ostream& operator<<(std::ostream& os, const Vector& vec) {
        for (const auto& element : vec.data) {
            os << element << " ";
        }
        return os;
    }
};

#endif // VECTOR_H