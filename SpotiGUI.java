import io.javalin.Javalin;

public class SpotiGUI {
    private static String portNum;

    public static void main(String[] args) {
        portNum = args[0];
        if (!validPortNumber(portNum)) {
            System.err.println("ERROR: Must provide port number as argument");
            System.exit(0);
        }
        System.out.println("AUTH: Using port " + portNum + " for auth server");



        Javalin app = Javalin.create().start(7000);
        app.get("/", ctx -> ctx.result("Hello World"));
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