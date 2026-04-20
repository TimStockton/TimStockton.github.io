
package additivecipher;

//@author timothy c stockton ii

public class AdditiveCipher {
    //***********************************************************************
    //Student/Author: Timothy C Stockton II
    //Wei Lu - CS455 Cryptography and Network Security 2022	
    //Midterm Project - AdditiveCipher.java
    //Simulates a brute force attack on an additive cipher.
    //Displays every possible plaintext result by progressing through each key choice.
    //***********************************************************************
	
    public static void main(String[] args) {
	System.out.println("**********************************************************************************************\n"
        +"Student/Author: Timothy C Stockton II\n"
        +"Wei Lu - CS455 Cryptography and Network Security 2022\n"
        +"Midterm Project - AdditiveCipher.java\n"
        +"Simulates a brute force attack on an additive cipher.\n"
        +"Displays every possible plaintext result by progressing through each key choice.\n"
        +"**********************************************************************************************\n");	

        String guess = "";
        String cipherText = "UOISCXEWLOBDOX";

        //array of characters we can use 
        char[] alphabet = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
                        'P','Q','R','S','T','U','V','W','X','Y','Z'};

        //try each key on the cipher text
        for(int key = 0; key < 26; key++) {
            //for each character in the ciphertext
            for(int i = 0; i < cipherText.length(); i++) {
                for(int x = 0; x < 26; x++) {
                    //grab the character from ciphertext at index i (converts to char)
                    char cipherChar = cipherText.charAt(i);
                    //convert it to a string for processing
                    String cipherString = String.valueOf(cipherChar);
                    //make it uppercase to get the proper ASCII number
                    cipherString = cipherString.toUpperCase();
                    //convert it back to a char in order to cast as an int
                    cipherChar = cipherString.charAt(0);
                    //convert uppercase cipher letter to an ASCII number
                    int cipherASCII = (int) cipherChar;
                    int alphabetASCII = (int) alphabet[x];
                    //compare letter at alphabet[index] to current ciphertext character
                    if (cipherASCII == alphabetASCII) {
                        //if it's a match, apply the key shift and add to guess
                        try {
                            guess = guess + alphabet[x - key]; //in bounds
                        } //end try
                        catch(Exception e) {
                            guess = guess + alphabet[x + 26 - key]; //out of bounds
                        } //end catch
                    } //end if
                } //end for
            } //end for
            System.out.print(guess + "\n"); //display each guess
            guess = "";
	} //end for
    }//end main
}//end AdditiveCipher.java
