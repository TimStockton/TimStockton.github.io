
package rc4demo;

public class Rc4Demo 
{
    public static void main(String[] args) 
    {
        String key = "iamkey";
        int j = 0, temp = 0;
        int[] S = new int[256];
        int[] T = new int[256];	
        int[] K = new int[key.length()];
        for (int a = 0; a < key.length(); a++)
        {
            K[a] = key.charAt(a);
        }
        int keyLength = key.length();
        // Generation of the S-Box
        for (int a = 0; a < 256; a++)
        {
            S[a] = a;
            T[a] = Integer.parseInt(Integer.toHexString((char)K[a % (keyLength)]), 16);
        }
        System.out.println("The initial S-box is...");
        for (int p = 0; p < 16; p++)
        {
            for (int q = 0; q < 16; q++)
            {
                System.out.print(" " + S[q+16*p]);
            }		
            System.out.println();
        }
        System.out.println("The initial T-element is...");
        for (int p = 0; p < 16; p++)
        {
            for (int q = 0; q < 16; q++)
            {
                System.out.print(" " + T[q+16*p]);
            }		
            System.out.println();
        }
        for (int a = 0; a < 256; a++)
        {
            j = (j + S[a] + T[a]) % 256;
            temp = S[a];
            S[a] = S[j];
            S[j] = temp;
        }
        System.out.println("The final S-box after using KSA algorithm is...");
        for (int p = 0; p < 16; p++)
        {
            for (int q = 0; q < 16; q++)
            {
                System.out.print(" " + S[q+16*p]);
            }		
            System.out.println();
        }
    }
}
