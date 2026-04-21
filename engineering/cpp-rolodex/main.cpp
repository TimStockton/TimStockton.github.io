// File: main.cpp
// Name: Timothy Stockton
// Date: 20251102
// Course: INFO.2680
// Desc: This program simulates a rolodex and provides functionality to:
//      list, view, flip, add, remove, search, and quit.
// Usage: run main.cpp, reads from data.txt file

// used for printing to output and grabbing user input
#include <iostream>
// reading from a file (where Card data originates)
#include <fstream>
// strings (no char arrays)
#include <string>
// for istringstream (used to split full name into parts)
#include <sstream>

// custom classes
// rolodex contains Cards, Cards store information on individuals
#include "Rolodex.h"
#include "Card.h"

// the following standard library packages are used
using std::string;
using std::cout;
using std::cin;
using std::endl;
using std::ifstream;
using std::istringstream;

string FILENAME = "RolodexData.txt";

// split a full name into first and last
void splitName(const string& fullName, string& first, string& last)
{
    istringstream iss(fullName);
    iss >> first >> last;
}

// retrieve file data and create Cards in the Rolodex
int readData(const string& filename, Rolodex& rolo)
{
    ifstream infile(filename);
    if (!infile) {
        cout << "Error opening file: " << filename << endl;
        return 1;
    }

    string name;
    string occupation;
    string address;
    string phone;
    int count = 0;

    int keepReading = 1;
    while (keepReading) {
        // read line from file
        getline(infile, name);
        
        // if error reading line (end of file), break loop
        if (!infile) {
            keepReading = 0;
        }
        
        // skip blank lines
        if (name.empty()) {
            continue;
        }

        getline(infile, occupation);
        getline(infile, address);
        getline(infile, phone);

        string first;
        string last;
        splitName(name, first, last);
        
        Card newCard(first, last, occupation, address, phone);
        rolo.add(newCard);

        // consume blank line
        string blank;
        getline(infile, blank);
        
        ++count;
    }

    return count;
}

int main()
{
    Rolodex rolo;
    
    // retrieve Card data from file and populate Rolodex with Cards
    readData(FILENAME, rolo);

    // program header
    cout << "Welcome to the Rolodex Program!\n";
    
    string command;
    char continueFlag = 'y';
    
    while (continueFlag == 'y') {
        // display command options, process command input
        cout << "\nCommands: list, view, flip, add, remove, search, quit\n";
        cout << "Enter command: ";
        cin >> command;
        cout << "\n";
        if (command == "list") {
            // display the entire rolodex
            rolo.show(cout);
        } else if (command == "view") {
            // display the Card at the current position in the rolodex
            Card card = rolo.getCurrentCard();
            card.show(cout);
            // formatting
            cout << "\n";
        } else if (command == "flip") {
            // update the current roledex position to the next Card, display it
            // flipping past the last Card wraps around to the first Card
            Card card = rolo.flip();
            card.show(cout);
            // formatting
            cout << "\n";
        } else if (command == "add") {
            // add a new Card to the rolodex
            // prompts for each field value and creates a new Card object
            string first;
            string last;
            string occupation;
            string address;
            string number;
            
            // flush leftover newline character before using getline
            cin.ignore();
    
            cout << "\nFirst name: ";
            getline(cin, first);
            cout << "\nLast name: ";
            getline(cin, last);
            cout << "\nOccupation: ";
            getline(cin, occupation);
            cout << "\nAddress: ";
            getline(cin, address);
            cout << "\nPhone number: ";
            getline(cin, number);
    
            Card newCard = Card(first, last, occupation, address, number);
            rolo.add(newCard);
            cout << "Card added.\n";
        } else if (command == "remove") {
            // remove the Card at the current position
            // display Card
            Card card = rolo.getCurrentCard();
            cout << "About to delete:\n";
            card.show(cout);
            // safety check
            string choice;
            cout << "\nDelete this card? (y/n): ";
            cin >> choice;
            if (choice == "y") {
                rolo.remove();
                cout << "Card removed.\n";
            }
        } else if (command == "search") {
            // find and display a Card
            // prompt for first and last name
            string first;
            string last;
            cout << "\nEnter first name: ";
            cin >> first;
            cout << "\nEnter last name: ";
            cin >> last;
            cout << "\n";

            if (rolo.search(last, first)) {
                // match found, display
                cout << "Matching card found:\n";
                Card card = rolo.getCurrentCard();
                card.show(cout);
                // formatting
                cout << "\n";
            } else {
                cout << "Card not found.\n";
            }
        } else if (command == "quit") {
            // exit the program
            continueFlag = 'n';
        } else { 
            // invalid command
            cout << "\nCommand not recognized.\n";
        } // end command if
        // prompt for continue, but not if quit was entered
        if (continueFlag != 'n') {
            cout << "Do you want to continue? (y/n): ";
            cin >> continueFlag;
        }
    }// end while

    cout << "Goodbye!\n";
    return 0;
}
