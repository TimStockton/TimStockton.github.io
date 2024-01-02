/*
 * Application Title: Deadlock Detector
 * Author: Timothy C Stockton II (TC)
 * Class: CS 320, Operating System Design
 * Date: April 2023
 * Purpose: This is class maintains the storage variables that represent the CPU state and has methods to manipulate them
 */

package osd_projecta_stocktont;

// import scanner for choices about number of resources and processes
import java.util.Scanner;

public class Matrix {
    
    //limits for matrix/vector/array sizes
    int numberResources;
    int numberProcesses;
    
    //DECLARE MATRICES AND VECTORS
    
    // the number of available instances of each resource type
    // Available[i] = number of instances for resource[i]
    int[] Available;
    
    // the maximum resource requirement of each process
    // the rows are processes, the columns are resource types
    int[][] Max;
    
    // the currently allocated resources of each process
    // the rows are processes, the columns are resource types
    int[][] Allocation;
    
    // the current resource needs of each process in order to reach max
    // the rows are processes, the columns are resource types
    // need = max - allocation
    int[][] Need;
    
    //arrays for pretend allocation used by bankers algorithm
    int[] pretendAvailable;
    int[][] pretendAllocation;
    int[][] pretendNeed;
    
    //constructor - INITIALIZE MATRICES AND VECTORS
    public Matrix() {
        // Instantiate an instance of the Scanner class to accept user input
        Scanner scan = new Scanner(System.in);
    
        System.out.print("\nInitializing... \n");

        int maxResources = 10;
        // Prompt the user for the desired number of resources.  
        System.out.print("\nHow many types of resources are there? [min: 1, max: " + maxResources + "]\n");
        numberResources = scan.nextInt();
        //if too many resources
        if (numberResources > maxResources) {
            numberResources = maxResources;
            System.out.print("That is too many resources, value has been set to " + maxResources + "\n");
        }
        //if too few (negative or zero) resources
        if (numberResources < 1) {
            numberResources = 1;
            System.out.print("That is too few resources, value has been set to 1\n");
        }

        int maxProcesses = 20;
        // Prompt the user for the desired number of processes.  
        System.out.print("\nHow many processes are there? [min: 1, max: " + maxProcesses + "]\n");
        numberProcesses = scan.nextInt();
        //if too many processes
        if (numberProcesses > maxProcesses) {
            numberProcesses = maxProcesses;
            System.out.print("That is too many processes, value has been set to " + maxProcesses + "\n");
        }
        //if too few (negative or zero) processes
        if (numberProcesses < 1) {
            numberProcesses = 1;
            System.out.print("That is too few processes, value has been set to 1\n");
        }
        
        Available = new int[numberResources];
        Max = new int[numberProcesses][numberResources]; //[row][column]
        Allocation = new int[numberProcesses][numberResources]; //[row][column]
        Need = new int[numberProcesses][numberResources]; //[row][column]
    }
    
    public void editResource(int resourceID, int numberInstances) {
        //add a resource (no validation, breaks when out of bounds)
        //adding a new entry in Available adds a new resource
        //the value added is the number of instances for that resource
        Available[resourceID] = numberInstances;
        System.out.println("Success: Resource " + resourceID + " has " + numberInstances + " instances available.");
    }
    
    public void clearResource(int resourceID) {
        //remove a resource (no validation, breaks when out of bounds)
        //remove the given numbered resource from Available
        Available[resourceID] = 0;
        System.out.println("Success: Resource " + resourceID + " now has no instances available.");
        //iterative removal of specified resource from Max, Allocation and Need (all same length)
        for (int i = 0; i < Max.length; i++) {
            Max[i][resourceID] = 0;
            Allocation[i][resourceID] = 0;
            Need[i][resourceID] = 0;
        }
        System.out.println("Success: Resource " + resourceID + " now has no instances allocated or needed.");
    }
    
    public void editProcess(int processID, int[] requiredResources) {
        //add a process (no validation, breaks when out of bounds)
        //add a new row (process) to Max with each column being a number of instances required from each resource
        //add the same data to Need (there is no allocation yet, the bankers algorithm does that, so Need = Max)
        //iterative assignment of specified resource instances to given process in Max and Need (same length)
        for (int i = 0; i < Available.length; i++) {
            Max[processID][i] = requiredResources[i];
            Need[processID][i] = requiredResources[i];
        }
        System.out.println("Success: Process " + processID + " now has the specificed resource instance requirements.");
    }
    
    public void clearProcess(int processID) {
        //remove a process (no validation, breaks when out of bounds)
        //remove the corresponding row for the process number from Max and Need, or set all columns equal to zero
        //iterative assignment of specified resource instances to given process in Max and Need (same length)
        for (int i = 0; i < Available.length; i++) {
            Max[processID][i] = 0;
            Need[processID][i] = 0;
        }
        System.out.println("Success: Process " + processID + " now has no resource instance requirements.");
    }
    
    public void editAllocation(int processID, int[] allocatedResources) {
        //edit a processes resource instance allocation (no validation, breaks when out of bounds)
        //iterative allocation of specified resource instances to given process
        //for each resource
        for (int i = 0; i < Available.length; i++) {
            Allocation[processID][i] = allocatedResources[i];
            Need[processID][i] = Max[processID][i] - Allocation[processID][i];
        }
        System.out.println("Success: Process " + processID + " now has the specificed resource instances allocated to it.");
    }
    
    public void clearAllocation(int processID) {
        //clear a processes resource instance allocation (no validation, breaks when out of bounds)
        //iterative assignment of zero to given process in Allocation
        for (int i = 0; i < Available.length; i++) {
            Allocation[processID][i] = 0;
            Need[processID][i] = Max[processID][i];
        }
        System.out.println("Success: Process " + processID + " now has no resource instance requirements.");
    }
    
    public void randomizeState() {
        //randomize the simulated CPU state
        //hardcoded min and max values for random numbers
        int minAvailable = 1;
        int maxAvailable = 20;
        int minRequired = 1;
        int maxRequired = 10;
        int minAllocated = 0;
        int maxAllocated = 4;
        
        //for each resource type
        for (int i = 0; i < Available.length; i++) {
            //generate a random number between max and min inclusive
            int randomNumberAvailableInstances = (int) Math.floor(Math.random() *(maxAvailable - minAvailable + 1) + minAvailable);
            //set that resource to have a random number of avaialable instances
            Available[i] = randomNumberAvailableInstances;
        }
        
        //for each process
        for (int i = 0; i < Max.length; i++) {
            //for each resource type
            for (int j = 0; j < Available.length; j++) {
                //generate a random number between max and min inclusive
                int randomNumberRequiredInstances = (int) Math.floor(Math.random() *(maxRequired - minRequired + 1) + minRequired);
                Max[i][j] = randomNumberRequiredInstances;
                Need[i][j] = Max[i][j] - Allocation[i][j];
                
                //generate a random number between max and min inclusive
                int randomNumberAllocatedInstances = (int) Math.floor(Math.random() *(maxAllocated - minAllocated + 1) + minAllocated);
                Allocation[i][j] = randomNumberAllocatedInstances;
            }
        }
        
        System.out.println("Success: The CPU state has been randomized.");
    }
    
    public void clearState() {
        //clear the simulated CPU state
        //set Available, Max, Allocation, and Need entries equal to zero
        
        //for each resource type
        for (int i = 0; i < Available.length; i++) {
            Available[i] = 0;
        }
        
        //for each process
        for (int i = 0; i < Max.length; i++) {
            //for each resource type
            for (int j = 0; j < Available.length; j++) {
                Max[i][j] = 0;
                Need[i][j] = 0;
            }
        }
        
        System.out.println("Success: The CPU state has been cleared.");
    }
      
    //display the current simulated CPU state
    public void displayState() {
        System.out.println("******************************************");
        
        //print AVAILABLE
        System.out.print("Available: [");
        //for each resource type
        for (int i = 0; i < Available.length; i++) {
            System.out.print("R" + i + "-" + Available[i] + ", ");
        }
        System.out.print("]\n");
        
        //print MAX
        System.out.print("\nMax: -----------------");
        //for each process
        for (int i = 0; i < Max.length; i++) {
            System.out.print("\nProcess " + i + ": [");
            //for each resource type
            for (int j = 0; j < Available.length; j++) {
                System.out.print("R" + j + "-" + Max[i][j] + ", ");
            }
            System.out.print("]");
        }
        System.out.print("\n----------------------\n");
        
        //print ALLOCATION
        System.out.print("\nAllocation: ----------");
        //for each process
        for (int i = 0; i < Max.length; i++) {
            System.out.print("\nProcess " + i + ": [");
            //for each resource type
            for (int j = 0; j < Available.length; j++) {
                System.out.print("R" + j + "-" + Allocation[i][j] + ", ");
            }
            System.out.print("]");
        }
        System.out.print("\n----------------------\n");
        
        //print NEED
        System.out.print("\nNeed: ----------------");
        //for each process
        for (int i = 0; i < Max.length; i++) {
            System.out.print("\nProcess " + i + ": [");
            //for each resource type
            for (int j = 0; j < Available.length; j++) {
                System.out.print("R" + j + "-" + Need[i][j] + ", ");
            }
            System.out.print("]");
        }
        System.out.print("\n----------------------\n");
        System.out.println("******************************************");
        System.out.println("Success: The CPU state has been displayed.");
    }
    
    public void bankersAlgorithm() {
        //bankers algorithm used on all processes
        
        // vector to store the number of instances being requested by the process
        int[] Request = new int[numberResources];
        
        //temporary use arrays for safety algorithm
        pretendAvailable = new int[numberResources];
        pretendAllocation = new int[numberProcesses][numberResources]; //[row][column]
        pretendNeed = new int[numberProcesses][numberResources]; //[row][column]
        
        // string to store safe sequence
        String strSafeSequence = "";
        
        //flag to determine if continue on while loop
        boolean deadlockFlag = false;
        
        // a vector to track T/F for each process being finished
        Boolean[] mainFinish = new Boolean[numberProcesses];
        
        //loop, for all processes to be initialized to unfinished
        for (int i = 0; i < numberProcesses; i++) {
            mainFinish[i] = false;
        }
        
        //variables to provide exit conditions
        int numberFinished = 0;
        int numberUnfinished = numberProcesses;
        int lastRoundUnfinished = 0;
        
        //int to hold number of process to pretend allocation for and pass to safety algorithm
        int processToCheck;
        
        //while state is safe
        while (!deadlockFlag){
            //for each process
            for (int i = 0; i < numberProcesses; i++) {
                //only perform actions if process has not previously been finished/allocated
                if (mainFinish[i] == false) {
                    //for each resource
                    for (int j = 0; j < numberResources; j++) {
                        //assign request vector with required resource instances for that process
                        Request[j] = Need[i][j];
                    }

                    //availableFlag
                    int availableFlag = 0;

                    //for each resource
                    for (int j = 0; j < numberResources; j++) {
                        // if the instances of the resource type being requested are available
                        if (Request[j] <= Available[j]) {
                            availableFlag = availableFlag + 1;
                        }
                    }

                    if (availableFlag == numberResources) { //if all needed instances of each resource type is available for this process
                        System.out.println("Bankers Algorithm: requested resource instances are available, pretending to allocate");
                        //for each resource
                        for (int j = 0; j < numberResources; j++) {
                            //set to avoid need being 0 when it's not and allocation being 0 when it's not
                            pretendAllocation = Allocation;
                            pretendNeed = Need;
                            
                            // pretend to allocate requested resources to the process
                            pretendAvailable[j] = Available[j] - Request[j]; // subtract requested instances from available instances
                            pretendAllocation[i][j] = pretendAllocation[i][j] + Request[j]; // add requested resources to allocated resources
                            pretendNeed[i][j] = pretendNeed[i][j] - Request[j]; // subtract requested resources from needed resources
                        }
                        
                        processToCheck = i;

                        System.out.println("Bankers Algorithm: calling safety algorithm");
                        // if pretend allocation puts system in a safe state
                        if (safetyAlgorithm(processToCheck)) {
                            System.out.println("Bankers Algorithm: current state is safe, actually allocating");
                            //actually allocate
                            Available = pretendAvailable;
                            Allocation = pretendAllocation;
                            Need = pretendNeed;

                            //add this process to safe sequence list
                            strSafeSequence = strSafeSequence + i + ", ";
                            
                            //set this process as finished
                            mainFinish[i] = true;
                        } else {
                            System.out.println("Bankers Algorithm: current state is unsafe, aborting allocation");
                        }
                    } else {
                        System.out.println("Bankers Algorithm: process is requesting unavailable resources and must wait ");
                    }
                }// end if not finished loop
            } //end process loop
            
            //prepare variables for exit conditions
            numberFinished = 0;
            numberUnfinished = numberProcesses;
            //for each process
            for (int i = 0; i < numberProcesses; i++) {
                //if that process is finished
                if (mainFinish[i] == true){
                    numberFinished = numberFinished + 1;
                    numberUnfinished = numberUnfinished - 1;
                }
            }
            
            //if no processes are safe or able to finish
            if (numberFinished == 0) {
                System.out.println("\nBankers Algorithm: deadlock is imminent, there is no safe sequence");
                //kill while loop
                deadlockFlag = true;
            }
            
            //if some but not all processes are safe or able to finish
            if (numberFinished > 0 && numberFinished < numberProcesses) {
                if (numberUnfinished == lastRoundUnfinished) { // if no change since last round
                    System.out.println("\nBankers Algorithm: deadlock is imminent, there is no safe sequence");
                    //kill while loop
                    deadlockFlag = true;
                } else {
                    lastRoundUnfinished = numberUnfinished;
                    System.out.println("Bankers Algorithm: looping");
                }
            }
            
            //if all processes are safe or able to finish
            if (numberFinished == numberProcesses) {
                System.out.println("\nBankers Algorithm: The system is in a safe state with the following safe process sequence -> " + strSafeSequence);
                //kill while loop
                deadlockFlag = true; // even though not deadlocked, need an end condition
            }
            
        }// end while loop
        
    } // end method
    
    public boolean safetyAlgorithm(int processToCheck) {
        //determines if the pretend allocation is safe
        
        // a vector to track instances of each resource type
        int[] Work = pretendAvailable;
        
        // a vector to release instances of each resource type for bankers algorithm
        int[] releaseWork = Work;
        
        // a vector to track T/F for each process being finished
        Boolean[] Finish = new Boolean[numberProcesses];
        
        //loop, for all processes to be initialized to unfinished
        for (int i = 0; i < numberProcesses; i++) {
            Finish[i] = false;
        }

        //flag to determine if continue on while loop
        boolean safetyIsDone = false;
        
        //vars to provide exit conditions
        int numberSafetyFinished = 0;
        int numberSafetyUnfinished = numberProcesses;
        int lastRoundSafetyUnfinished = 0;
        
        //while state is safe
        while (!safetyIsDone){
        
            //for each process
            for (int x = 0; x < numberProcesses; x++) {
                
                //only perform actions if process has not previously been finished/allocated
                if (Finish[x] == false) {

                    int conditionFlag = 0; //var used to see if the processes needed resources are available

                    //for each resource
                    for (int y = 0; y < numberResources; y++) {
                        //if the resource instances the process needs for this resources type to finish are available
                        if (pretendNeed[x][y] <= Work[y]) {
                            conditionFlag = conditionFlag + 1;
                        }
                    }//end resource loop

                    // if needed resources are available
                    if (conditionFlag == numberResources) {
                        System.out.println("safety algorithm: needed resources available, process 'finished', 'releasing' resources");
                        //for each resource
                        for (int y = 0; y < numberResources; y++) {
                            //release allocated resources for the process that now has finished after being allocated needed resources
                            Work[y] = Work[y] + pretendAllocation[x][y]; // add released resources to Work (local available var)
                            if (x == processToCheck) {
                                releaseWork[y] = Work[y]; // store new available array for the main process being checked
                            }
                            pretendAllocation[x][y] = 0; // get rid of allocation (they were released)
                        }//end resource loop
                        Finish[x] = true;
                    }//end condition check
                } // end finish check
            }//end process loop
            
            // prepare loop exit condition variables
            numberSafetyFinished = 0;
            numberSafetyUnfinished = numberProcesses;
            // for each process
            for (int z = 0; z < numberProcesses; z++) {
                if (Finish[z] == true){
                    numberSafetyFinished = numberSafetyFinished + 1;
                    numberSafetyUnfinished = numberSafetyUnfinished - 1;
                }
            }
            
            //if no processes are safe or able to finish, exit loop
            if (numberSafetyFinished == 0) {
                //kill while loop
                safetyIsDone = true;
            }
            
            //if some but not all processes are safe or able to finish
            if (numberSafetyFinished > 0 && numberSafetyFinished < numberProcesses) {
                if (numberSafetyUnfinished == lastRoundSafetyUnfinished) { // if no change since last round, exit loop
                    //kill while loop
                    safetyIsDone = true;
                } else { // go another round
                    System.out.println("safety algorithm: looping");
                    lastRoundSafetyUnfinished = numberSafetyUnfinished;
                }
            }
            
            //if all processes are safe or able to finish
            if (numberSafetyFinished == numberProcesses) {
                //kill while loop
                safetyIsDone = true;
            }
        } //end while loop
        
        //if ANY process is unfinished, return false, else return true
        // for each process
        if (numberSafetyFinished < numberProcesses) {
            System.out.println("safety algorithm: all processes unable to finish");
            return false;
        } else {
            //all processes able to finish
            System.out.println("safety algorithm: all processes able to finish, releasing tested processes held resource instances");
            Available = releaseWork; // release allocated resources for non-pretend/local Available matrix
            return true;
        }
        
    }//end method
    
}//end class
