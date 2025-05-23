import java.util.*;
public class HeapSort {
    public static void heapsort(int l[]) {
        int n = l.length;
        int i, temp;
        // initialise heap structure
        for (i = n / 2 - 1; i >= 0; i--) {
            heapify(l, n, i);
        }

        for (i = n - 1; i > -1; i--) {
            temp = l[0];
            l[0] = l[i];
            l[i] = temp;
            heapify(l, i, 0);
        }
    }

    public static void heapify(int l[], int n, int i) {
        int largest, lc, rc, temp;
        largest = i;
        lc = 2 * i + 1;
        rc = 2 * i + 2;
        // max heap
        if (lc < n && l[lc] > l[largest])
            largest = lc;
        if (rc < n && l[rc] > l[largest])
            largest = rc;
        if (largest != i) { // swap step
            temp = l[largest];
            l[largest] = l[i];
            l[i] = temp;
            heapify(l, n, largest); // resort bottom elements
        }
    }

    public static void printarr(int l[]) {
        int i;
        for (i = 0; i < l.length; i++) {
            System.out.print(l[i] + " ");
        }
    }

    public static void main(String[] args) {
        int n, i;
        Scanner scan = new Scanner(System.in);
        System.out.println("Enter size of array: ");
        n = scan.nextInt();
        int arr[] = new int[n];

        System.out.println("Enter array to be sorted: ");
        for (i = 0; i < n; i++) {
            arr[i] = scan.nextInt();
        }

        System.out.println("Original Array: ");
        printarr(arr);
        System.out.println();
        heapsort(arr);
        System.out.println("Sorted Array: ");
        printarr(arr);
        System.out.println();

        scan.close();
    }
}