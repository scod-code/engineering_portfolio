// IMPORTANT NOTE:
// Please do not submit the .cpp file
// This .cpp file will not be graded
// Submit the .h file only
//
#include <iostream>
#include <stdexcept>
#include "hw4b.h"

void printVector(const std::vector<int>& vec) { // note the "const" keyword
    for (int num : vec) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    BinarySearchTree<int> bst;

    std::cout << "Tree Height: ";
    try {
        std::cout << bst.treeHeight() << std::endl;
    } catch (const std::runtime_error& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    bst.treeInsert(15);
    bst.treeInsert(6);
    bst.treeInsert(18);
    bst.treeInsert(3);
    bst.treeInsert(8);
    bst.treeInsert(7);
    bst.treeInsert(17);
    bst.treeInsert(20);
    bst.treeInsert(2);
    bst.treeInsert(4);
    bst.treeInsert(12);
    bst.treeInsert(9);

    std::cout << "Tree Height: ";
    try {
        std::cout << bst.treeHeight() << std::endl;
    } catch (const std::runtime_error& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
    
    std::cout << "Inorder Tree Walk: ";
    bst.inorderTreeWalk();
    std::cout << std::endl;

    std::cout << "Preorder Tree Walk: ";
    bst.preorderTreeWalk();
    std::cout << std::endl;

    std::cout << "Postorder Tree Walk: ";
    bst.postorderTreeWalk();
    std::cout << std::endl;
    
    int searchValue = 18;
    if (bst.treeSearch(searchValue)) {
        std::cout << searchValue << " is found in the Binary Search Tree." << std::endl;
    } else {
        std::cout << searchValue << " is not found in the Binary Search Tree." << std::endl;
    }
    
    searchValue = 40;
    if (bst.treeSearch(searchValue)) {
        std::cout << searchValue << " is found in the Binary Search Tree." << std::endl;
    } else {
        std::cout << searchValue << " is not found in the Binary Search Tree." << std::endl;
    }

    bst.treeDelete(12);

    std::cout << "Inorder Tree Walk after deleting 12: ";
    bst.inorderTreeWalk();
    std::cout << std::endl;

    // Additional inserts
    bst.treeInsert(5);
    bst.treeInsert(10);
    bst.treeInsert(25);
    bst.treeInsert(40);

    std::cout << "Inorder Tree Walk after inserting 5, 10, 25, 40: ";
    bst.inorderTreeWalk();
    std::cout << std::endl;

    searchValue = 40;
    if (bst.treeSearch(searchValue)) {
        std::cout << searchValue << " is found in the Binary Search Tree." << std::endl;
    } else {
        std::cout << searchValue << " is not found in the Binary Search Tree." << std::endl;
    }

    bst.treeDelete(15);

    std::cout << "Inorder Tree Walk after deleting 15: ";
    bst.inorderTreeWalk();
    std::cout << std::endl;
    
    std::vector<int> results;
    int min = 7;
    int max = 25;
    bst.rangeSearch(min,max, results);
    std::cout << "Range Search Results for [" << min << ", " << max << "]" << std::endl;
    printVector(results); 
    
    BinarySearchTree<int> mirroredBst = bst.treeMirror();
    
    std::cout << "Inorder Tree Walk of mirrored tree: ";
    mirroredBst.inorderTreeWalk();
    std::cout << std::endl;

    return 0;
}



// Please feel free to modify this .cpp file to create more test cases.
// 
// Below is the expected output of the .cpp file included in the base template:
//
// Tree Height: Exception: Tree is empty.
// Tree Height: 4
// Inorder Tree Walk: 2 3 4 6 7 8 9 12 15 17 18 20 
// Preorder Tree Walk: 15 6 3 2 4 8 7 12 9 18 17 20 
// Postorder Tree Walk: 2 4 3 7 9 12 8 6 17 20 18 15 
// 18 is found in the Binary Search Tree.
// 40 is not found in the Binary Search Tree.
// Inorder Tree Walk after deleting 12: 2 3 4 6 7 8 9 15 17 18 20 
// Inorder Tree Walk after inserting 5, 10, 25, 40: 2 3 4 5 6 7 8 9 10 15 17 18 20 25 40 
// 40 is found in the Binary Search Tree.
// Inorder Tree Walk after deleting 15: 2 3 4 5 6 7 8 9 10 17 18 20 25 40 
// Range Search Results for [7, 25]
// 7 8 9 10 17 18 20 25 
// Inorder Tree Walk of mirrored tree: 40 25 20 18 17 10 9 8 7 6 5 4 3 2 


