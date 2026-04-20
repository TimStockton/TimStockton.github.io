/*
 * Application Title: Deadlock Detector
 * Author: Timothy C Stockton II (TC)
 * Class: CS 320, Operating System Design
 * Date: April 2023
 * Purpose: This is a driver class that handles user choices about the CPU state and calls the Matrix class
 */

package osd_projecta_stocktont;

// import scanner for menu choices
import java.util.Scanner;

public class DeadlockMonitor {
    
    public static void main(String[] args) {
        
        // Program information
        System.out.println("*************************************");
        System.out.println("Application Title: Deadlock Detector");
        System.out.println("Author: Timothy C Stockton II (TC)");
        System.out.println("Class: CS 320, Operating System Design");
        System.out.println("Purpose: This program simulates a CPU state");
        System.out.println("and determines if the state is safe or deadlocked");
        System.out.println("*************************************");
        
        // String to control the while loop
        String strStructureAgain = "y";
        
        // while loop for
        while (strStructureAgain.equalsIgnoreCase("y")) {
        
            // Instantiate an instance of the Matrix class to use data structures
            Matrix matrix = new Matrix();

            // Instantiate an instance of the Scanner class to accept user input
            Scanner scan = new Scanner(System.in);

            // String to control the while loop
            String strGoAgain = "y";

            // Integer used for menu choice
            int intChoice = 0;
        
            // while loop controls the execution of this program.
            while(strGoAgain.equalsIgnoreCase("y"))
            {
                // The menu.
                System.out.println("\nChoose an item by entering its number:");
                System.out.println("1. Edit Resource\t2. Clear Resource");
                System.out.println("3. Edit Process\t\t4. Clear Process");
                System.out.println("5. Edit Allocation\t6. Clear Allocation");
                System.out.println("7. Randomize State\t8. Clear State");
                System.out.println("9. Display State\t10. Determine Safe Sequence");
                System.out.println("11. Reset\t\t12. Exit Program\n");

                // The choice from a user.
                intChoice = scan.nextInt();

                // Switch statement to process the choice.
                switch(intChoice)
                {
                    case 1:
                        System.out.print("You chose to edit a resource \n");
                        // Prompt the user for the desired resource number.  
                        System.out.print("Which resource would you like to edit? [options: 0 through " + (matrix.Available.length-1) + "]\n");
                        int resourceEditID = scan.nextInt();
                        //validate input
                        if (resourceEditID > matrix.Available.length-1 || resourceEditID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        } else 
                        // Prompt the user for the number of instances.  
                        System.out.print("How many instances are available of this resource type? \n"); //add validation (max, min)
                        int numberInstances = scan.nextInt();
                        // validate input
                        if (numberInstances < 0) {
                            numberInstances = 0;
                            System.out.print("Available instances cannot be negative, value has been set to zero\n");
                        }
                        matrix.editResource(resourceEditID, numberInstances);
                        break;
                    case 2:
                        System.out.print("You chose to clear a resource \n");
                        // Prompt the user for the desired resource number.  
                        System.out.print("Which resource would you like to clear? [options: 0 through " + (matrix.Available.length-1) + "]\n");
                        int resourceClearID = scan.nextInt();
                        //validate input
                        if (resourceClearID > matrix.Available.length-1 || resourceClearID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        }
                        matrix.clearResource(resourceClearID);
                        break;
                    case 3:
                        System.out.print("You chose to edit a process \n");
                        // Prompt the user for the desired process number.  
                        System.out.print("Which process would you like to edit? [options: 0 through " + (matrix.Max.length-1) + "]\n");
                        int processEditID = scan.nextInt();
                        //validate input
                        if (processEditID > matrix.Max.length-1 || processEditID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        }
                        // Prompt the user for the number of instances required.
                        int[] newProcessRequiredInstances = new int[matrix.Available.length];
                        for (int i = 0; i < matrix.Available.length; i++) {
                            System.out.print("How many instances of resource " + i + " does this process need? \n");
                            int requiredResourceInstances = scan.nextInt();
                            //validate input
                            if (requiredResourceInstances < 0) {
                                requiredResourceInstances = 0;
                                System.out.print("Required instances cannot be negative, value has been set to zero\n");
                            }
                            newProcessRequiredInstances[i] = requiredResourceInstances;
                        }
                        matrix.editProcess(processEditID, newProcessRequiredInstances);
                        break;
                    case 4:
                        System.out.print("You chose to clear a process \n");
                        // Prompt the user for the desired process number.  
                        System.out.print("Which process would you like to clear? [options: 0 through " + (matrix.Max.length-1) + "]\n");
                        int processClearID = scan.nextInt();
                        //validate input
                        if (processClearID > matrix.Max.length-1 || processClearID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        }
                        matrix.clearProcess(processClearID);
                        break;
                    case 5:
                        System.out.print("You chose to edit an allocation\n");
                        // Prompt the user for the desired process number.  
                        System.out.print("Which process would you like to edit resources allocations for? [options: 0 through " + (matrix.Max.length-1) + "]\n");
                        int allocationEditID = scan.nextInt();
                        //validate input
                        if (allocationEditID > matrix.Max.length-1 || allocationEditID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        }
                        // Prompt the user for the number of instances to allocate for each resource type.
                        int[] newProcessAllocatedInstances = new int[matrix.Available.length];
                        for (int i = 0; i < matrix.Available.length; i++) {
                            System.out.print("How many instances of resource " + i + " would you like to allocate to this process? \n");
                            int allocatedResourceInstances = scan.nextInt();
                            //validate input
                            if (allocatedResourceInstances < 0) {
                                allocatedResourceInstances = 0;
                                System.out.print("Allocated instances cannot be negative, value has been set to zero\n");
                            }
                            newProcessAllocatedInstances[i] = allocatedResourceInstances;
                        }
                        matrix.editAllocation(allocationEditID, newProcessAllocatedInstances);
                        break;
                    case 6:
                        System.out.print("You chose to clear an allocation \n");
                        // Prompt the user for the desired process number.  
                        System.out.print("Which process would you like to clear the resource allocation for? [options: 0 through " + (matrix.Max.length-1) + "]\n");
                        int allocationClearID = scan.nextInt();
                        //validate input
                        if (allocationClearID > matrix.Max.length-1 || allocationClearID < 0) {
                            System.out.print("Invalid selection \n");
                            break;
                        }
                        matrix.clearAllocation(allocationClearID);
                        break;
                    case 7:
                        System.out.print("You chose to randomize the state \n");
                        matrix.randomizeState();
                        break;
                    case 8:
                        System.out.print("You chose to clear the state \n");
                        matrix.clearState();
                        break;
                    case 9:
                        System.out.print("You chose to display the current state \n");
                        matrix.displayState();
                        break;
                    case 10:
                        System.out.print("You chose to determine a safe sequence (if one exists) \n");
                        matrix.bankersAlgorithm();
                        break;
                    case 11:
                        System.out.print("Resetting data structures. \n");
                        strGoAgain="n"; //exit menu loop
                        break;
                    case 12:
                        System.out.print("You chose to quit, goodbye. \n");
                        strGoAgain = "n"; //exit menu loop
                        strStructureAgain = "n"; //exit initialize loop
                        break;
                    default:
                        System.out.println("Error: You must make a valid choice: ");
                        break;
                } // END OF menu switch() STATEMENT.
            }//end of menu while loop
        } //end of initialize while loop
    }//end of main    
}//end of class
