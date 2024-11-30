import java.util.concurrent.TimeUnit;

public class Prime implements Runnable {
    public void run() {
        System.out.println("Hello world from thread number " + Thread.currentThread().getName());
    }
    public static void main (String[] args){
        long startTime = System.nanoTime(); // Computation start time
        /* Do computation Here */
        int len=0;
        for (int i = 10; i <= 1000000; i++) {
            isPrime(i);
        }
        System.out.println(len);
        // The difference between the start time and the end time
        long difference = System.nanoTime() - startTime;
        // Print it out
        long minutesInDifference = TimeUnit.NANOSECONDS.toMinutes(difference);
        long secondsInDifference = TimeUnit.NANOSECONDS.toSeconds(difference) - TimeUnit.MINUTES.toSeconds(minutesInDifference);
        System.out.format(
            "Total execution time: %d min, %d sec\n",
            minutesInDifference,
            secondsInDifference
        );
    }
    public static boolean isPrime(int number) {
        if (number < 2) return false;
        for (int i = 2; i <= Math.sqrt(number); i++) {
            if (number % i == 0) return false;
        }
        return true;
    }
}





    //     Thread[] threads = new Thread[10]; // create an array of threads
    //     for (int i = 0; i < 10; i++) {
    //         String threadName = Integer.toString(i);
    //         // create threads
    //         threads[i] = new Thread(new Prime(), threadName);
    //     }
    //     for (Thread thread : threads) {
    //         thread.start(); // start the threads
    //     }
    //     for (Thread thread : threads) {
    //         try {
    //             thread.join(); // wait for the threads to terminate
    //         } catch (InterruptedException e) {
    //             e.printStackTrace();
    //         }
    //     }
    // System.out.println("That's all, folks");