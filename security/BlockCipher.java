
package blockcipher;

//@author timothy c stockton ii

public class BlockCipher {
    //***********************************************************************
    //Student/Author: Timothy C Stockton II
    //Wei Lu CS455 Cryptography and Network Security 2022	
    //Midterm Project Programming Question 3 - BlockCipher.java
    //Encodes a string of ascii characters to hex format using a block cipher.
    //After the given initial vector each 8 bit block will be encrypted using the
    //previously encrypted 8 bits.
    //Program displays the final encrypted hex message.
    //***********************************************************************

    public static void main(String[] args) {
        String message = "HTTP/1.1"; //original message
        String key = "10001001"; //initial vector
        String nextKey = "";	//key used for next block
        String messageBin = ""; //original message in binary
        String encryptedBin = ""; //encrypted binary message
        String encryptedHex = ""; //encrypted hex message

        System.out.println("***************************************************************************************\n"
                + "Student/Author: Timothy C Stockton II\n"
                + "Wei Lu CS455 Cryptography and Network Security 2022\n"
                + "Midterm Project Programming Question 3 - BlockCipher.java\n"
                + "Encodes a string of ascii characters to hex format using a block cipher.\n"
                + "After the given initial vector each 8 bit block will be encrypted using the previously\n"
                + "encrypted 8 bits.\n"
                + "Program displays the final encrypted hex message.\n"
                + "***************************************************************************************\n");

        System.out.println("Encrypting \"" + message + "\" using initial vector \"" + key + "\".\n");

        //convert original message to binary
        //--------------------------------------------------
        //convert message to an array of characters
        char[] chars = message.toCharArray();
        //for each character in the message
        for (char aChar : chars) {
            //convert character to binary (8 bits) and append to messageBin
            messageBin += (String.format("%8s", Integer.toBinaryString(aChar)).replaceAll(" ", "0"));
        }
        System.out.println("Plaintext binary:\n" + messageBin + "\n");
        //end convert to binary
        //---------------------------------------------------
        //XOR in 8 bit blocks beginning with initial vector
        //current 8 bit block becomes key for next block
        //-------------------------------------------------------
        //create a string array to make handling blocks easier
        String[] messageBinBlocks = new String[message.length()];
        System.out.print("Plaintext binary blocks: \n");
        //for each character (every 8 bits/block)
        for(int i = 0; i < message.length(); i++) {
            //take that characters binary digits and assign it to the respective block in the array
            messageBinBlocks[i] = messageBin.substring((8 * i), (8 * (i + 1)));
            System.out.print(messageBinBlocks[i] + " ");
        }
        System.out.print("\n\nEncrypted binary blocks: \n");
        //create a string array to make handling encrypted blocks easier
        String[] encryptedBinBlocks = new String[message.length()];
        //assign initial key as nextKey which will be replaced after each block
        nextKey = key;
        String temp = "";
        //for each block of binary (each character)
        for(int i = 0; i < message.length(); i++) {
            //for each binary digit in the current block
            for(int j = 0; j < 8; j++) {
                //exclusive or (XOR) message bit with key bit and append to temp
                temp += messageBinBlocks[i].charAt(j) ^ nextKey.charAt(j);
            }
            //append temp (current block, encrypted) to encryptedBin
            encryptedBin += temp;
            //assign temp to respective index of encrypted binary block array
            encryptedBinBlocks[i] = temp;
            //if not the last binary block/character, save current encrypted block as the next key
            if(i != message.length() - 1) {nextKey = temp;}
            //clear temp
            temp = "";
            System.out.print(encryptedBinBlocks[i] + " ");
        }
        //end xor
        //-----------------------------------------------------------------------
        //convert encrypted binary string to hex string
        //---------------------------------------------------------------------------
        //for each encrypted block (character, 8 bits)
        for(int i = 0; i < message.length(); i++) {
            //convert to 2 hex characters and append to encrypted hex string
            encryptedHex += Integer.toHexString(Integer.parseInt(encryptedBinBlocks[i], 2));
        }
        //end convert to hex
        System.out.println("\n\nEncrypted hex:\n" + encryptedHex);
        //--------------------------------------------------------------------------------
    }//end main()
}//end BlockCipher.java
