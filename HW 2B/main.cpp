#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include "hw2b.h"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " num_locations num_events" << std::endl;
        return 1; 
    }

    int num_locations = std::atoi(argv[1]); // Number of locations to consider
    int num_events = std::atoi(argv[2]); // Number of events to include in the "timeline"
    
    std::vector<std::vector<Event>> all_events(num_locations); 

    for (int location_id = 0; location_id < num_locations; location_id++) {
        std::string filename = "location" + std::to_string(location_id);
        std::ifstream input_file(filename);

        if (input_file.is_open()) {
            std::string line;

            while (std::getline(input_file, line)) {
                std::istringstream iss(line);
                std::string token;
                int event_id;
                int timestamp;
                std::string detail;

                std::getline(iss, token, ','); // location_id
                std::getline(iss, token, ','); // event_id
                event_id = std::stoi(token);
                std::getline(iss, token, ','); // event_timestamp
                timestamp = std::stoi(token);
                std::getline(iss, detail); // event_detail

                all_events[location_id].push_back(Event(location_id, event_id, timestamp, detail));
            }

            input_file.close();
        } else {
            std::cerr << "Error: Unable to open " << filename << std::endl;
            return 1;
        }
    }

    std::vector<Event> first_n_events = getFirstNEvents(all_events, num_events); 

    std::cout << "Beginning of the events:" << std::endl;

    if (first_n_events.size() == 0) {
        std::cout << "There are no events." << std::endl;
    }
    else {
        for (const Event& e : first_n_events) {
            std::cout << e << std::endl;
        }
    }

    std::cout << "End of the events." << std::endl;

    return 0;
}

// Example tests
/*
Test 1 
Command line input: 1 5
Expected output:
Beginning of the events:
0,1,1727312949,Event 1 at Location 0
0,2,1727313916,Event 2 at Location 0
0,3,1727316969,Event 3 at Location 0
0,4,1727319335,Event 4 at Location 0
0,5,1727320188,Event 5 at Location 0
End of the events.

Test 2
Command line input: 2 10
Expected output:
Beginning of the events:
1,1,1727311391,Event 1 at Location 1
1,2,1727312196,Event 2 at Location 1
0,1,1727312949,Event 1 at Location 0
0,2,1727313916,Event 2 at Location 0
1,3,1727314923,Event 3 at Location 1
1,4,1727316217,Event 4 at Location 1
1,5,1727316475,Event 5 at Location 1
0,3,1727316969,Event 3 at Location 0
1,6,1727317120,Event 6 at Location 1
1,7,1727318419,Event 7 at Location 1
End of the events.

Test 3
Command line input: 3 10
Expected output:
Beginning of the events:
1,1,1727311391,Event 1 at Location 1
1,2,1727312196,Event 2 at Location 1
0,1,1727312949,Event 1 at Location 0
0,2,1727313916,Event 2 at Location 0
2,1,1727314210,Event 1 at Location 2
2,2,1727314385,Event 2 at Location 2
1,3,1727314923,Event 3 at Location 1
2,3,1727315721,Event 3 at Location 2
1,4,1727316217,Event 4 at Location 1
1,5,1727316475,Event 5 at Location 1
End of the events.

Test 4
Command line input: 5 25
Expected output:
Beginning of the events:
1,1,1727311391,Event 1 at Location 1
1,2,1727312196,Event 2 at Location 1
3,1,1727312375,Event 1 at Location 3
0,1,1727312949,Event 1 at Location 0
0,2,1727313916,Event 2 at Location 0
2,1,1727314210,Event 1 at Location 2
2,2,1727314385,Event 2 at Location 2
4,1,1727314412,Event 1 at Location 4
3,2,1727314566,Event 2 at Location 3
1,3,1727314923,Event 3 at Location 1
3,3,1727315391,Event 3 at Location 3
2,3,1727315721,Event 3 at Location 2
4,2,1727316092,Event 2 at Location 4
1,4,1727316217,Event 4 at Location 1
1,5,1727316475,Event 5 at Location 1
0,3,1727316969,Event 3 at Location 0
4,3,1727317006,Event 3 at Location 4
1,6,1727317120,Event 6 at Location 1
2,4,1727317492,Event 4 at Location 2
2,5,1727317516,Event 5 at Location 2
3,4,1727317861,Event 4 at Location 3
1,7,1727318419,Event 7 at Location 1
4,4,1727318923,Event 4 at Location 4
0,4,1727319335,Event 4 at Location 0
0,5,1727320188,Event 5 at Location 0
End of the events.


Test 5
Command line input: 10 15
Expected output:
Beginning of the events:
7,1,1727311092,Event 1 at Location 7
1,1,1727311391,Event 1 at Location 1
1,2,1727312196,Event 2 at Location 1
3,1,1727312375,Event 1 at Location 3
5,1,1727312420,Event 1 at Location 5
7,2,1727312778,Event 2 at Location 7
0,1,1727312949,Event 1 at Location 0
9,1,1727313091,Event 1 at Location 9
6,1,1727313474,Event 1 at Location 6
8,1,1727313633,Event 1 at Location 8
0,2,1727313916,Event 2 at Location 0
2,1,1727314210,Event 1 at Location 2
2,2,1727314385,Event 2 at Location 2
4,1,1727314412,Event 1 at Location 4
3,2,1727314566,Event 2 at Location 3
End of the events.

Test 6
Command line input: 1 10000
Expected output:
Beginning of the events:
0,1,1727312949,Event 1 at Location 0
0,2,1727313916,Event 2 at Location 0
0,3,1727316969,Event 3 at Location 0
0,4,1727319335,Event 4 at Location 0
0,5,1727320188,Event 5 at Location 0
0,6,1727320194,Event 6 at Location 0
0,7,1727320526,Event 7 at Location 0
0,8,1727323066,Event 8 at Location 0
0,9,1727324053,Event 9 at Location 0
0,10,1727327070,Event 10 at Location 0
0,11,1727327853,Event 11 at Location 0
0,12,1727330482,Event 12 at Location 0
0,13,1727332706,Event 13 at Location 0
0,14,1727336155,Event 14 at Location 0
0,15,1727338107,Event 15 at Location 0
0,16,1727341549,Event 16 at Location 0
0,17,1727343684,Event 17 at Location 0
0,18,1727347034,Event 18 at Location 0
0,19,1727347094,Event 19 at Location 0
0,20,1727348252,Event 20 at Location 0
0,21,1727350401,Event 21 at Location 0
0,22,1727350894,Event 22 at Location 0
0,23,1727351480,Event 23 at Location 0
0,24,1727352930,Event 24 at Location 0
0,25,1727354626,Event 25 at Location 0
0,26,1727357932,Event 26 at Location 0
0,27,1727359879,Event 27 at Location 0
0,28,1727360845,Event 28 at Location 0
End of the events.
*/