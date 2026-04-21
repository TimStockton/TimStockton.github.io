// File: Rolodex.cpp
// Name: Timothy Stockton
// Date: 20251102
// Course: INFO.2680
// Desc: This program simulates a rolodex and provides functionality to:
//      list, view, flip, add, remove, search, and quit.
// Usage: run main.cpp, reads from data.txt file

#include "Rolodex.h"

using std::string;

// default constructor, initialize current iterator
Rolodex::Rolodex() {
    mCurrent = mCards.begin();
}

// add new Card to the list (in the appropriate spot, 
// alphabetical order [last name, first name])
// set it as the 'current' Card in the Rolodex by updating the iterator
void Rolodex::add(Card& card) {
    // reset current card iterator to beginning, prepping for loop
    std::list<Card>::iterator it = mCards.begin();
    
    // step through each Card, stop when last Card is reached
    for (; it != mCards.end(); ++it) {
        // find where new Card comes alphabetically before existing Card
        if (card.getLastName() < it->getLastName() ||
           (card.getLastName() == it->getLastName() &&
            card.getFirstName() < it->getFirstName())) {
            // found correct position
            break;
        }
    }
    // insert new Card in this position
    it = mCards.insert(it, card);
    // new Card becomes current
    mCurrent = it;
}

// remove the current Card from the list, then return it
// make the following Card the 'current' Card
// if last Card removed, set 'current' Card to first Card (wraps around)
Card Rolodex::remove() {
    // empty Rolodex means return blank Card
    if (mCards.empty()) {
        return Card("", "", "", "", "");
    }

    // track Card to be removed and the following Card
    Card removed = *mCurrent;
    std::list<Card>::iterator next = mCurrent;
    ++next;

    // remove Card from list
    mCurrent = mCards.erase(mCurrent);

    // account for wrap around
    if (mCurrent == mCards.end()) {
        mCurrent = mCards.begin();
    }

    return removed;
}

// return a copy of the 'current' Card
Card Rolodex::getCurrentCard() const {
    // empty Rolodex means return blank Card
    if (mCards.empty()) {
        return Card("", "", "", "", "");
    }
    // return iterater value via pointer
    return *mCurrent;
}

// update the 'current' Card to the next Card in the list, return it
// if last Card in the list, it wraps around to the first card
Card Rolodex::flip() {
    // empty Rolodex means return blank Card
    if (mCards.empty()) {
        return Card("", "", "", "", "");
    }

    // increment and account for wrap around
    ++mCurrent;
    if (mCurrent == mCards.end()) {
        mCurrent = mCards.begin();
    }

    // return iterater value via pointer
    return *mCurrent;
}

// find the requested Card , set it as 'current' Card
// returns true indicating the search found a Card
// if no match, 'current' is unchanged and false is returned
bool Rolodex::search(const string& lastname, const string& firstname) {
    // reset iterator, stop at end of Rolodex
    for (std::list<Card>::iterator it = mCards.begin(); 
                            it != mCards.end(); ++it) {
        if (it->getLastName() == lastname && it->getFirstName() == firstname) {
            // match found
            mCurrent = it;
            return true;
        }
    }
    // no match found
    return false;
}

// iterate through all Cards in list
// invoke each Card's show() method, passing the ostream parameter
// the 'current' Card remains unchanged
void Rolodex::show(ostream& os) const {
    for (const Card& card : mCards) {
        card.show(os);
        // formatting
        os << "\n";
    }
}
