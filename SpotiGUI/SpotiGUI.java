package SpotiGUI;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class SpotiGUI {
    private static String clientID;
    private static int transitPort;

    private static CredGetter credentials;

    public static void main(String[] args) {
        // Read clientID and available port number from configuration.conf
        readConfiguration();

        // Start credential reciever
        credentials = new CredGetter("1", transitPort);
        credentials.start();

        // TODO open default gui here and announce waiting for connection.
        // should also give machine's ip and port number

        while (credentials.getAccessToken() == null) {
            try {
                Thread.sleep(1000);
            } catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        }
        System.out.println(credentials.getAccessToken());
    }

    /**
     * Reads relevant fields from configuration.conf
     * 
     * Currently:
     *  - clientID      : For use interacting with api
     *  - transitPort   : Port used for getting OAuth tokens from auth.py
     */
    private static void readConfiguration() {
        // Get clientID and port numbers from configuration.conf
        File configFile = new File("configuration.conf");
        try {
            Scanner sc = new Scanner(configFile);
            while (sc.hasNextLine()) {
                String line = sc.nextLine();

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
    }
}




/**
 * CredGetter by Jackson Kerr
 * 
 * Recieves 
 */
class CredGetter extends Thread {
    private Integer transitPort;

    private String refreshToken;
    private String accessToken;

    public CredGetter(String str, int transitPort) {
        super(str);
        this.transitPort = transitPort;
    }

    public void run() {
        while (true) {
            try {
                ServerSocket ss = new ServerSocket(transitPort); // don't need hostname??
                Socket socket = ss.accept(); // blocking call, wait until connection is attempted.
    
                // get the input stream from the connected socket
                InputStream inputStream = socket.getInputStream();
                // create a DataInputStream so we can read data from it.
                DataInputStream dataInputStream = new DataInputStream(inputStream);
    
                // read the message from the socket
                String data;
                while ((data = dataInputStream.readLine()) != null) { // TODO remove depreciated
                    String[] tokens = data.split(" ");

                    this.accessToken = tokens[0];
                    this.refreshToken = tokens[1];
                }
                ss.close();
                socket.close();

            } catch (IOException e) {
                System.out.println("ERROR: Error recieving tokens from auth.py");
                e.printStackTrace();
                System.exit(1);
            }
        }
    }

    public String getRefreshToken() {
        return this.refreshToken;
    }

    public String getAccessToken() {
        return this.accessToken;
    }
}