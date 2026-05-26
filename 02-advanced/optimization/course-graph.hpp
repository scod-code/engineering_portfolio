// Your name here: Somtochukwu C Osigwe-Daniel
// Your NetID here: sco46
//
// IMPORTANT NOTE:
// In your submission, you are only allowed to make modifications where it is indicated, 
// and you must provide your implementation in those designated areas. 
// You are not permitted to make changes to the code in any other location.
//
#ifndef HW5B_H
#define HW5B_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <string>
#include <algorithm>
#include <iostream>

class Course {
public:
    std::string descName;
    std::string courseNum;
    std::vector<Course*> prerequisites;
    std::vector<Course*> postrequisites;
    
    Course(const std::string& courseNum, const std::string& courseName) : 
        descName(courseName),    // Match declaration order
        courseNum(courseNum) {}  // Must be in this order
    
    void addPrerequisite(Course* prerequisite) {
        prerequisites.push_back(prerequisite);
    }
};

class CourseGraph {
public:
    std::unordered_map<std::string, Course*> courseMap;
    std::vector<const Course*> perCourseTopoResult;
    std::vector<std::vector<const Course*>> perSemesterTopoResult;

    void addCourse(const std::string& courseNum, const std::string& courseName) {
        const auto& pair = courseMap.emplace(courseNum, nullptr);
        if (pair.second) {
            pair.first->second = new Course(courseNum, courseName);
        }
    }

    void addPrerequisite(const std::string& courseNum, const std::string& prerequisiteNum) {
        if (courseMap.count(courseNum) && courseMap.count(prerequisiteNum)) {
            courseMap[courseNum]->addPrerequisite(courseMap[prerequisiteNum]);
        } else {
            std::cerr << courseNum << " or " << prerequisiteNum << " does/do not exist" << std::endl;
        }
    }
    
    ~CourseGraph() {
        for (auto& pair : courseMap) {
            delete pair.second;
        }
    }
    
    void printTopologicalSortedOrder() {
        std::cout << std::endl;
        std::cout << "Per-Course Topological Sorted Order:" << std::endl;
        for (const Course* course : perCourseTopoResult) {
            std::cout << course->courseNum << " " << course->descName << std::endl;
        }
        
        std::cout << std::endl;
        std::cout << "Per-Semester Topological Sorted Order:" << std::endl;
        for (size_t i = 0; i < perSemesterTopoResult.size(); ++i) {
            std::cout << "Semester: " << i+1 << std::endl;
            for (const Course* course : perSemesterTopoResult[i]) {
                std::cout << "  " << course->courseNum << " " << course->descName << std::endl;
            }
        }
    }
    
    void createAdjacencyList() {
        // Provide your implementation here
        for (auto& pair : courseMap) {
            Course* course = pair.second;
            for (Course* prereq : course->prerequisites) {
                prereq->postrequisites.push_back(course);
            }
        }
        // End of your implementation
    }
    
    bool isValidPerCourseTopologicalSort() {
    // Provide your implementation here
        std::unordered_map<const Course*, int> position;
        for (size_t i = 0; i < perCourseTopoResult.size(); ++i) {  
            position[perCourseTopoResult[i]] = i;
        }

        for (auto& pair : courseMap) {
            const Course* course = pair.second;
            for (const Course* prereq : course->prerequisites) {
                if (position[prereq] > position[course]) {
                    return false;
                }
            }
        }
        return true;
        // End of your implementation
    }
    
    void perCourseTopologicalSort() {
        // Provide your implementation here
        std::unordered_set<const Course*> visited;
        perCourseTopoResult.clear();
        for (auto& pair : courseMap) {
            if (visited.find(pair.second) == visited.end()) {
                DFSVisit(pair.second, visited);
            }
        }
        std::reverse(perCourseTopoResult.begin(), perCourseTopoResult.end());
        // End of your implementation
    }

    void DFS() {
        // Provide your implementation here
        std::unordered_set<const Course*> visited;
        perCourseTopoResult.clear();
        for (auto& pair : courseMap) {
            const Course* course = pair.second;
            if (visited.find(course) == visited.end()) {
                DFSVisit(course, visited);
            }
        }
        std::reverse(perCourseTopoResult.begin(), perCourseTopoResult.end());
        // End of your implementation
    }

    void DFSVisit(const Course* course, std::unordered_set<const Course*>& visited) {
        // Provide your implementation here
        visited.insert(course);
        for (const Course* postreq : course->postrequisites) {
            if (visited.find(postreq) == visited.end()) {
                DFSVisit(postreq, visited);
            }
        }
        perCourseTopoResult.push_back(course);
        // End of your implementation
    }

    void perSemesterTopologicalSort() {
        // Provide your implementation here
        std::unordered_map<const Course*, int> inDegree;
        std::queue<const Course*> zeroInDegreeQueue;
        perSemesterTopoResult.clear();

        for (auto& pair : courseMap) {
            inDegree[pair.second] = 0;
        }
        
        for (auto& pair : courseMap) {
            const Course* course = pair.second;
            for (const Course* postreq : course->postrequisites) {
                inDegree[postreq]++;
            }
        }

        for (auto& pair : courseMap) {
            if (inDegree[pair.second] == 0) {
                zeroInDegreeQueue.push(pair.second);
            }
        }

        while (!zeroInDegreeQueue.empty()) {
            std::vector<const Course*> currentSemester;
            int size = zeroInDegreeQueue.size();
            for (int i = 0; i < size; ++i) {
                const Course* course = zeroInDegreeQueue.front();
                zeroInDegreeQueue.pop();
                currentSemester.push_back(course);

                for (const Course* postreq : course->postrequisites) {
                    inDegree[postreq]--;
                    if (inDegree[postreq] == 0) {
                        zeroInDegreeQueue.push(postreq);
                    }
                }
            }
            perSemesterTopoResult.push_back(currentSemester);
        }
        // End of your implementation
    }
};

#endif