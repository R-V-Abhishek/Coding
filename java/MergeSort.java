import java.util.*;

public class MergeSort {
    public static int[] merge(int[] A, int[] B, int m, int n) {
        int i = 0, j = 0, k = 0;
        int[] C = new int[m + n];
        while (i < m && j < n) {
            if (A[i] < B[j]) {
                C[k++] = A[i++];
            } else {
                C[k++] = B[j++];
            }
        }
        for (int a = i; a < m; a++) {
            C[k++] = A[a];
        }
        for (int b = j; j < n; j++) {
            C[k++] = B[j];
        }
        return C;
    }

    public static void mergesort(int[] A) {
        if (A.length < 2) return;
        int mid = A.length / 2;
        int[] left = new int[mid];
        int[] right = new int[A.length - mid];
        for (int i = 0; i < mid; i++) {
            left[i] = A[i];
        }
        for (int i = mid; i < A.length; i++) {
            right[i - mid] = A[i];
        }
        mergesort(left);
        mergesort(right);
        int[] C = merge(left, right, left.length, right.length);
        System.arraycopy(C, 0, A, 0, C.length);
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
        mergesort(ascendingArray);
        System.out.println("Sorted Ascending Array: " +
            Arrays.toString(ascendingArray));

        System.out.println("Original Ascending Array: " +
            Arrays.toString(descendingArray));
        mergesort(descendingArray);
        System.out.println("Sorted Ascending Array: " +
            Arrays.toString(descendingArray));

        System.out.println("Original Ascending Array: " +
            Arrays.toString(randomArray));
        mergesort(randomArray);
        System.out.println("Sorted Ascending Array: " +
            Arrays.toString(randomArray));

        scanner.close();
    }
}