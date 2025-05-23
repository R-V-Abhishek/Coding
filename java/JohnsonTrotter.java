import java.util.*;

public class JohnsonTrotter {
    private static final boolean LEFT_TO_RIGHT = true;
    private static final boolean RIGHT_TO_LEFT = false;

    public static int searchArr(int[] a, int n, int mobile) {
        for (int i = 0; i < n; i++)
            if (a[i] == mobile)
                return i + 1;
        return 0;
    }

    public static int getMobile(int[] a, boolean[] dir, int n) {
        int mobile_prev = 0, mobile = 0;
        for (int i = 0; i < n; i++) {
            if (dir[i] == RIGHT_TO_LEFT && i != 0) {
                if (a[i] > a[i - 1] && a[i] > mobile_prev) {
                    mobile = a[i];
                    mobile_prev = mobile;
                }
            }
            if (dir[i] == LEFT_TO_RIGHT && i != n - 1) {
                if (a[i] > a[i + 1] && a[i] > mobile_prev) {
                    mobile = a[i];
                    mobile_prev = mobile;
                }
            }
        }
        return mobile;
    }

    public static void printOnePerm(int[] a, boolean[] dir, int n) {
        int mobile = getMobile(a, dir, n);
        if (mobile == 0) return;
        int pos = searchArr(a, n, mobile);

        if (dir[pos - 1] == RIGHT_TO_LEFT) {
            int temp = a[pos - 1];
            a[pos - 1] = a[pos - 2];
            a[pos - 2] = temp;
            boolean tempDir = dir[pos - 1];
            dir[pos - 1] = dir[pos - 2];
            dir[pos - 2] = tempDir;
        } else if (dir[pos - 1] == LEFT_TO_RIGHT) {
            int temp = a[pos];
            a[pos] = a[pos - 1];
            a[pos - 1] = temp;
            boolean tempDir = dir[pos];
            dir[pos] = dir[pos - 1];
            dir[pos - 1] = tempDir;
        }

        for (int i = 0; i < n; i++) {
            if (a[i] > mobile) {
                dir[i] = !dir[i];
            }
        }

        for (int num : a)
            System.out.print(num + " ");
        System.out.println();
    }

    public static int fact(int n) {
        int res = 1;
        for (int i = 1; i <= n; i++)
            res *= i;
        return res;
    }

    public static void printPermutation(int[] input, boolean initialDirection) {
        int n = input.length;
        int[] a = Arrays.copyOf(input, n);
        boolean[] dir = new boolean[n];
        Arrays.fill(dir, initialDirection);

        for (int num : a)
            System.out.print(num + " ");
        System.out.println();

        for (int i = 1; i < fact(n); i++)
            printOnePerm(a, dir, n);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();
        int[] nums = new int[n];
        System.out.println("Enter " + n + " distinct integers:");
        for (int i = 0; i < n; i++) {
            nums[i] = sc.nextInt();
        }
        System.out.print("Enter initial direction (L for Left to Right, R for Right to Left): ");
        char ch = sc.next().toUpperCase().charAt(0);
        boolean initialDirection = (ch == 'L') ? LEFT_TO_RIGHT : RIGHT_TO_LEFT;
        System.out.println("\nPermutations:");
        printPermutation(nums, initialDirection);
        sc.close();
    }
}