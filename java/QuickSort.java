import java.util.*;

public class QuickSort {
    public static void quicksort(int[] A, int low, int high) {
        if (low < high) {
            int pi = partition(A, low, high);
            quicksort(A, low, pi - 1);
            quicksort(A, pi + 1, high);
        }
    }

    private static int partition(int[] A, int low, int high) {
        int pivot = A[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (A[j] < pivot) {
                i++;
                int temp = A[i];
                A[i] = A[j];
                A[j] = temp;
            }
        }
        int temp = A[i + 1];
        A[i + 1] = A[high];
        A[high] = temp;
        return i + 1;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the length of the arrays: ");
        int length = scanner.nextInt();

        int[] ascendingArray = new int[length];
        int[] descendingArray = new int[length];
        int[] randomArray = new int[length];

        for (int i = 0; i < length; i++) {
            ascendingArray[i] = i + 1;
            descendingArray[i] = length - i;
        }

        Random random = new Random();
        for (int i = 0; i < length; i++) {
            randomArray[i] = random.nextInt(100) + 1;
        }

        System.out.println("Original Ascending Array: " +
            Arrays.toString(ascendingArray));
        quicksort(ascendingArray, 0, ascendingArray.length - 1);
        System.out.println("Sorted Ascending Array: " +
            Arrays.toString(ascendingArray));

        System.out.println("Original Descending Array: " +
            Arrays.toString(descendingArray));
        quicksort(descendingArray, 0, descendingArray.length - 1);
        System.out.println("Sorted Descending Array: " +
            Arrays.toString(descendingArray));

        System.out.println("Original Random Array: " +
            Arrays.toString(randomArray));
        quicksort(randomArray, 0, randomArray.length - 1);
        System.out.println("Sorted Random Array: " +
            Arrays.toString(randomArray));

        scanner.close();
    }
}