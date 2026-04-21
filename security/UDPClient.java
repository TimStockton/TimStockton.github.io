
import java.io.*;
import java.net.*;

class UDPClient {
    
    //***********************************************************************
    //Student/Author: Timothy C Stockton II
    //Wei Lu CS455 Cryptography and Network Security 2022	
    //Midterm Project Programming Question 4
    //Encodes a message.
    //Sends encrypted message to server.
    //Outputs the decoded message recieved from server.
    //***********************************************************************

    public static void main(String args[]) throws Exception {

        BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

        DatagramSocket clientSocket = new DatagramSocket(); //create a client socket 

        InetAddress IPAddress = InetAddress.getByName("158.65.80.43");

        byte[] sendData = new byte[64];
        byte[] receiveData = new byte[64];

        //prompt user for message to send
        System.out.println("enter message to be securely sent to UDP server");
        String sentence = inFromUser.readLine();
        //encrypt the entered message
        String encryptedSentence = encrypt(sentence);
        System.out.println("encrypted message: " + encryptedSentence);
        //prepare message to be sent to server
        sendData = encryptedSentence.getBytes();

        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 5000);

        //send encrypted message
        clientSocket.send(sendPacket);
        System.out.println("sent");

        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

        clientSocket.receive(receivePacket);

        String modifiedSentence = new String(receivePacket.getData());

        //display decrypted message recieved back from server
        System.out.println("FROM SERVER:" + modifiedSentence);
        clientSocket.close();
    }
    
    public static String encrypt(String plaintextMessage) {
        String message = plaintextMessage; //original message
        String key = "10001001"; //initial vector
        String nextKey = "";	//key used for next block
        String messageBin = ""; //original message in binary
        String encryptedBin = ""; //encrypted binary message
        String encryptedHex = ""; //encrypted hex message

        //convert original message to binary
        //--------------------------------------------------
        //convert message to an array of characters
        char[] chars = message.toCharArray();
        //for each character in the message
        for (char aChar : chars) {
            //convert character to binary (8 bits) and append to messageBin
            messageBin += (String.format("%8s", Integer.toBinaryString(aChar)).replaceAll(" ", "0"));
        }
        //---------------------------------------------------
        //XOR in 8 bit blocks beginning with initial vector
        //current 8 bit block becomes key for next block
        //-------------------------------------------------------
        //create a string array to make handling blocks easier
        String[] messageBinBlocks = new String[message.length()];
        //for each character (every 8 bits/block)
        for(int i = 0; i < message.length(); i++) {
            //take that characters binary digits and assign it to the respective block in the array
            messageBinBlocks[i] = messageBin.substring((8 * i), (8 * (i + 1)));
        }
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
        }
        //-----------------------------------------------------------------------
        //convert encrypted binary string to hex string
        //---------------------------------------------------------------------------
        //for each encrypted block (character, 8 bits)
        for(int i = 0; i < message.length(); i++) {
            //convert to 2 hex characters and append to encrypted hex string
            encryptedHex += Integer.toHexString(Integer.parseInt(encryptedBinBlocks[i], 2));
        }
        //--------------------------------------------------------------------------------
        return encryptedHex;
    }//end main()
}
