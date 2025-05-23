import java.util.Scanner;

public class Knapsack {

    public static int knapSack(int W, int[] weights, int[] values, int n) {
        int[][] dp = new int[n + 1][W + 1];

        for (int i = 0; i <= n; i++) {
            for (int w = 0; w <= W; w++) {
                if (i == 0 || w == 0) {
                    dp[i][w] = 0;
                } else if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        printSelectedItems(dp, weights, values, n, W);
        return dp[n][W];
    }

    public static void printSelectedItems(int[][] dp, int[] weights, int[] values, int n, int W) {
        System.out.println("Items included in the knapsack:");
        int w = W;
        for (int i = n; i > 0; i--) {
            if (dp[i][w] != dp[i - 1][w]) {
                System.out.println("Item " + i + " (Weight: " + weights[i - 1] + ", Value: " + values[i - 1] + ")");
                w -= weights[i - 1];
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number of items: ");
        int n = scanner.nextInt();

        int[] values = new int[n];
        int[] weights = new int[n];

        System.out.println("Enter the values of the items:");
        for (int i = 0; i < n; i++) {
            values[i] = scanner.nextInt();
        }

        System.out.println("Enter the weights of the items:");
        for (int i = 0; i < n; i++) {
            weights[i] = scanner.nextInt();
        }

        System.out.print("Enter the capacity of the knapsack: ");
        int W = scanner.nextInt();

        int maxValue = knapSack(W, weights, values, n);
        System.out.println("Maximum value in Knapsack = " + maxValue);

        scanner.close();
    }
}


