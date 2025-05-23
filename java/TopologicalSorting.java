import java.util.Scanner;

public class TopologicalSorting {
    public static int[] topologicalSort(int[][] graph, int numNodes) {
        int[] inDegree = new int[numNodes];
        int[] queue = new int[numNodes];
        int front = 0, rear = 0;

        // Calculate in-degrees
        for (int i = 0; i < numNodes; i++) {
            for (int neighbor = 0; neighbor < numNodes; neighbor++) {
                if (graph[i][neighbor] == 1) {
                    inDegree[neighbor]++;
                }
            }
        }

        // Enqueue nodes with in-degree 0
        for (int i = 0; i < numNodes; i++) {
            if (inDegree[i] == 0) {
                queue[rear++] = i;
            }
        }

        int[] topoOrder = new int[numNodes];
        int index = 0, processedNodes = 0;

        while (front < rear) {
            int node = queue[front++];
            topoOrder[index++] = node;
            processedNodes++;
            for (int neighbor = 0; neighbor < numNodes; neighbor++) {
                if (graph[node][neighbor] == 1) {
                    inDegree[neighbor]--;
                    if (inDegree[neighbor] == 0) {
                        queue[rear++] = neighbor;
                    }
                }
            }
        }

        if (processedNodes < numNodes) {
            System.out.println("Cycle detected! Topological sorting is not possible.");
            return new int[0];
        }
        return topoOrder;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number of vertices: ");
        int numNodes = sc.nextInt();
        int[][] graph = new int[numNodes][numNodes];

        System.out.println("Enter edges (start end), type -1 -1 to stop:");
        while (true) {
            int start = sc.nextInt();
            int end = sc.nextInt();
            if (start == -1 && end == -1) {
                break;
            }
            if (start < 0 || start >= numNodes || end < 0 || end >= numNodes) {
                System.out.println("Invalid edge. Enter values between 0 and " + (numNodes - 1));
                continue;
            }
            graph[start][end] = 1;
        }
        sc.close();

        int[] result = topologicalSort(graph, numNodes);
        if (result.length > 0) {
            System.out.print("Topological Order: ");
            for (int node : result) {
                System.out.print(node + " ");
            }
            System.out.println();
        }
    }
}