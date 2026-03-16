import java.io.*;
import java.net.*;

public class Gateway {

    static int[] workers = {6001,6002,6003};
    static int index = 0;

    public static void main(String[] args) throws Exception {

        ServerSocket server = new ServerSocket(5000);

        System.out.println("Gateway running on port 5000");

        while(true){

            Socket client = server.accept();

            new Thread(() -> process(client)).start();
        }
    }

    static synchronized int nextWorker(){

        int port = workers[index];
        index = (index + 1) % workers.length;

        return port;
    }

    static byte[] recvExact(InputStream in, int size) throws IOException {

        byte[] data = new byte[size];
        int read = 0;

        while(read < size){
            int r = in.read(data, read, size-read);
            if(r == -1) break;
            read += r;
        }

        return data;
    }

    static void process(Socket client){

        try{

            InputStream in = client.getInputStream();
            OutputStream out = client.getOutputStream();

            // receive conversion type
            byte[] convType = recvExact(in,10);

            System.out.println("Conversion request: " + new String(convType).trim());

            // receive file size
            byte[] sizeBuf = recvExact(in,16);

            int size = Integer.parseInt(new String(sizeBuf).trim());

            // receive file data
            byte[] fileData = recvExact(in,size);

            int workerPort = nextWorker();

            System.out.println("Sending job to worker on port "+workerPort);

            Socket worker = new Socket("localhost", workerPort);

            OutputStream workerOut = worker.getOutputStream();
            InputStream workerIn = worker.getInputStream();

            // forward job to worker
            workerOut.write(convType);
            workerOut.write(sizeBuf);
            workerOut.write(fileData);

            // receive result size
            byte[] resultSizeBuf = recvExact(workerIn,16);

            int resultSize = Integer.parseInt(new String(resultSizeBuf).trim());

            // receive converted file
            byte[] result = recvExact(workerIn,resultSize);

            // send result back to client
            out.write(resultSizeBuf);
            out.write(result);

            System.out.println("Job completed by worker on port "+workerPort);

            worker.close();
            client.close();

        }catch(Exception e){
            e.printStackTrace();
        }
    }
}