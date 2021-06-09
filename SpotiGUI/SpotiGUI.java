package SpotiGUI;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class SpotiGUI {
    private static String clientID;
    private static int transitPort;

    public static void main(String[] args) {
        System.out.println("Started Java");
        // Get clientID and port numbers from configuration.conf
        File configFile = new File("configuration.conf");
        try {
            Scanner sc = new Scanner(configFile);
            while (sc.hasNextLine()) {
                String line = sc.nextLine();
                // Remove comments and whitespace

                // Remove comments & whitespace
                line = line.split("#")[0].replaceAll("\\s+","");
                
                if (line.contains("clientID")) {
                    clientID = line.replace("clientID=", "");
                } else if (line.contains("transitPort")) {
                    transitPort = Integer.parseInt(line.replace("transitPort=", ""));
                }
            }
            sc.close();
        } catch (Exception e) {
            System.out.println("ERROR: Couldn't find configuration file");
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("clientID = " + clientID);


        try {
            ServerSocket ss = new ServerSocket(transitPort); // don't need hostname??
            System.out.println("ServerSocket awaiting connection on port "+transitPort);
            Socket socket = ss.accept(); // blocking call, wait until connection is attempted.
            System.out.println("Connection from " + socket + "!");

            // get the input stream from the connected socket
            InputStream inputStream = socket.getInputStream();
            // create a DataInputStream so we can read data from it.
            DataInputStream dataInputStream = new DataInputStream(inputStream);

            // read the message from the socket
            String tmp;
            while ((tmp = dataInputStream.readLine()) != null) {
                System.out.println(tmp);
            }

            System.out.println("Closing sockets.");
            ss.close();
            socket.close();
        } catch (IOException e) {
            System.out.println("ERROR: IOException");
            e.printStackTrace();
            System.exit(1);
        }
    }

    /***
     * @param givenPort
     * @return true if givenPort is a valid port number
     */
    private static Boolean validPortNumber(String givenPort) {
        if (givenPort.length() > 0 && givenPort.matches("[0-9]+"))  { // Check is numeric
            return true;
        } else {
            return false;
        }
    }

}