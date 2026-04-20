// File: Card.h
// Name: Timothy Stockton
// Date: 20251102
// Course: INFO.2680
// Desc: This program simulates a rolodex and provides functionality to:
//      list, view, flip, add, remove, search, and quit.
// Usage: run main.cpp, reads from data.txt file

#ifndef CARD_H
#define CARD_H

// no char* or char arrays
#include <string>
// used for printing to output
#include <iostream>

using std::string;
using std::ostream;

// this class organizes and stores contact information
class Card {
public:
    // constructor
    Card(const string& firstName, const string& lastName,
         const string& occupation, const string& address,
         const string& phoneNumber);
    
    // member functions
    void show(ostream& os) const;
    string getFirstName() const { return mFirstName; }
    string getLastName() const { return mLastName; }

private:
    // Card information
    string mFirstName;
    string mLastName;
    string mOccupation;
    string mAddress;
    string mPhoneNumber;
};

#endif   // CARD_H
