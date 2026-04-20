// File: Card.cpp
// Name: Timothy Stockton
// Date: 20251102
// Course: INFO.2680
// Desc: This program simulates a rolodex and provides functionality to:
//      list, view, flip, add, remove, search, and quit.
// Usage: run main.cpp, reads from data.txt file

#include "Card.h"

using std::string;
using std::cout;
using std::cin;

// constructor
Card::Card(const string& firstName, const string& lastName,
           const string& occupation, const string& address,
           const string& phoneNumber)
        : mFirstName(firstName), mLastName(lastName),
          mOccupation(occupation), mAddress(address),
          mPhoneNumber(phoneNumber) {}

// display the stored values for this card
void Card::show(ostream& os) const {
    os << mFirstName << " " << mLastName << "\n"
       << mOccupation << "\n"
       << mAddress << "\n"
       << mPhoneNumber << "\n";
}
