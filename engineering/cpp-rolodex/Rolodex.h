// File: Rolodex.h
// Name: Timothy Stockton
// Date: 20251102
// Course: INFO.2680
// Desc: This program simulates a rolodex and provides functionality to:
//      list, view, flip, add, remove, search, and quit.
// Usage: run main.cpp, reads from data.txt file

#ifndef ROLODEX_H
#define ROLODEX_H

// list is used to hold all of the Cards
#include <list>
// Cards contain String values
#include <string>
// Rolodex uses Cards
#include "Card.h"

using std::string;
using std::ostream;
using std::list;

// this class manages multiple Cards that store contact information
class Rolodex {
public:
    // default constructor
    Rolodex();
    
    // member functions
    void add(Card& card);
    Card remove();
    Card getCurrentCard() const;
    Card flip();
    bool search(const string& lastname, const string& firstname);
    void show(ostream& os) const;

private:
    // must be able to handle duplicate names (two Jim Smith)
    list<Card> mCards;
    // points to current Card, needs reset on Rolodex size change
    list<Card>::iterator mCurrent;
};

#endif   // ROLODEX_H
