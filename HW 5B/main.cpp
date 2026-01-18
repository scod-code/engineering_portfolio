// IMPORTANT NOTE:
// Please do not submit the .cpp file
// This .cpp file will not be graded
// Submit the .h file only
//
#include <iostream>
#include "hw5b.h"

int main() {
    CourseGraph graph;
    
    graph.addCourse("14:332:221", "Principles of Electrical Engineering I");
    graph.addCourse("14:332:222", "Principles of Electrical Engineering II");
    graph.addCourse("14:332:226", "Probability and Random Processes");
    graph.addCourse("14:332:252", "Programming Methodology I");
    graph.addCourse("14:332:322", "Principles of Communication Systems");
    graph.addCourse("14:332:345", "Linear Systems and Signals");
    graph.addCourse("14:332:351", "Programming Methodology II");
    graph.addCourse("14:332:452", "Software Engineering");
    graph.addCourse("14:332:453", "Mobile App Engineering and User Experience");
    graph.addCourse("14:332:456", "Network Centric Programming");

    graph.addPrerequisite("14:332:222", "14:332:221"); 
    graph.addPrerequisite("14:332:322", "14:332:226");  
    graph.addPrerequisite("14:332:322", "14:332:345"); 
    graph.addPrerequisite("14:332:345", "14:332:222"); 
    graph.addPrerequisite("14:332:351", "14:332:252"); 
    graph.addPrerequisite("14:332:452", "14:332:351"); 
    graph.addPrerequisite("14:332:453", "14:332:351"); 
    graph.addPrerequisite("14:332:456", "14:332:351"); 
    
    graph.createAdjacencyList();
    
    graph.perCourseTopologicalSort();
    
    if (graph.isValidPerCourseTopologicalSort())
        std::cout << "The per-course sorted order is VALID" << std::endl;
    else 
        std::cout << "The per-course sorted order is NOT VALID" << std::endl;
    
    graph.perSemesterTopologicalSort();
    
    graph.printTopologicalSortedOrder();
    
    return 0;
}

// Please feel free to modify this .cpp file to add more courses and create more test cases.
// 
// Below is the expected output of the .cpp file included in the base template:
//
// The per-course sorted order is VALID
//
// Per-Course Topological Sorted Order:
// 14:332:221 Principles of Electrical Engineering I
// 14:332:222 Principles of Electrical Engineering II
// 14:332:226 Probability and Random Processes
// 14:332:252 Programming Methodology I
// 14:332:345 Linear Systems and Signals
// 14:332:322 Principles of Communication Systems
// 14:332:351 Programming Methodology II
// 14:332:452 Software Engineering
// 14:332:453 Mobile App Engineering and User Experience
// 14:332:456 Network Centric Programming

// Per-Semester Topological Sorted Order:
// Semester: 1
//   14:332:221 Principles of Electrical Engineering I
//   14:332:226 Probability and Random Processes
//   14:332:252 Programming Methodology I
// Semester: 2
//   14:332:222 Principles of Electrical Engineering II
//   14:332:351 Programming Methodology II
// Semester: 3
//   14:332:345 Linear Systems and Signals
//   14:332:452 Software Engineering
//   14:332:456 Network Centric Programming
//   14:332:453 Mobile App Engineering and User Experience
// Semester: 4
//   14:332:322 Principles of Communication Systems

