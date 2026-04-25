// Your name here: Somtochukwu C Osigwe-Daniel
// Your NetID here: sco46
//
// IMPORTANT NOTE:
// In your submission, you are only allowed to make modifications where it is indicated, 
// and you must provide your implementation in those designated areas. 
// You are not permitted to make changes to the code in any other location.
//
#ifndef HW2B_H
#define HW2B_H

#include <vector>
#include <stdexcept>

class Event {
public:
    int location_id;
    int event_id;
    int timestamp;
    std::string detail;

    Event(int location_id, int event_id, int timestamp, const std::string& text)
        : location_id(location_id), event_id(event_id), timestamp(timestamp), detail(text) {}

    bool operator<(const Event& other) const {
        return timestamp < other.timestamp; 
    }
    
    bool operator>(const Event& other) const {
        return timestamp > other.timestamp; 
    }
    
    friend std::ostream& operator<< (std::ostream& out, const Event& e) ;
};

std::ostream& operator<< (std::ostream& out, const Event& e) {
    out << e.location_id << "," << e.event_id << "," << e.timestamp << "," << e.detail ;
    return out;
}


template <typename T>
class MinHeap {
public:
    std::vector<T> heap;

    void minHeapify(int i) {
        // Provide your implementation here
    int smallest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < heap.size() && heap[left] < heap[smallest]) {
        smallest = left;
    }
    if (right < heap.size() && heap[right] < heap[smallest]) {
        smallest = right;
    }
    if (smallest != i) {
        std::swap(heap[i], heap[smallest]);
        minHeapify(smallest);
    }
    // End of your implementation
    }
public:
    MinHeap() {}

    MinHeap(const std::vector<T>& arr) {
        heap = arr;
        int n = heap.size();
        for (int i =n / 2 - 1; i >= 0; i--) {
            minHeapify(i);
        }
    }

    void insert(const T& value) {
        // Provide your implementation here
        heap.push_back(value);
        int i = heap.size() - 1;
        while (i != 0 && heap[(i - 1) / 2] > heap[i]) {
        std::swap(heap[i], heap[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
        // End of your implementation
    }

    T getMin() {
        if (!isEmpty()) {
            return heap[0];
        }
        throw std::runtime_error("Heap is empty.");
    }

    T extractMin() {
        if (isEmpty()) {
            throw std::runtime_error("Heap is empty.");
        }

        // Provide your implementation here
        T min = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        minHeapify(0);

    return min;
        // Don't forget to return the extracted Min item
        // End of your implementation
    }

    bool isEmpty() {
        return heap.empty();
    }
};

std::vector<Event> getFirstNEvents(std::vector<std::vector<Event>>& all_events, int n) {
    std::vector<Event> first_n_events;
    MinHeap<Event> min_heap;

    // Provide your implementation here
    
    std::vector<int> indices(all_events.size(), 0);

    // Insert the first event from each location
    for (int i = 0; i < all_events.size(); ++i) {
        if (!all_events[i].empty()) {
            min_heap.insert(all_events[i][0]);
            indices[i]++;
        }
    }

    // Extract the first N events
    while (first_n_events.size() < n && !min_heap.isEmpty()) {
        Event current = min_heap.extractMin();
        first_n_events.push_back(current);

        int loc_id = current.location_id;
        if (indices[loc_id] < all_events[loc_id].size()) {
            min_heap.insert(all_events[loc_id][indices[loc_id]]);
            indices[loc_id]++;
        }
    }

    // End of your implementation
    
    return first_n_events;
}

#endif // HW2B_H
