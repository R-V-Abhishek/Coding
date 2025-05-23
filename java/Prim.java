import java.util.*;

public class Prim {
    private static final int INF = Integer.MAX_VALUE;

    public static void Prim(int[][] graph, int V) {
        boolean[] visited = new boolean[V];
        int[] key = new int[V];
        int[] parent = new int[V];
        for (int i = 0; i < V; i++) {
            key[i] = INF;
            parent[i] = -1;
        }
        key[0] = 0;
        for (int count = 0; count < V - 1; count++) {
            int u = minKeyVertex(key, visited, V);
            visited[u] = true;
            for (int v = 0; v < V; v++) {
                if (graph[u][v] != 0 && !visited[v] && graph[u][v] < key[v]) {
                    key[v] = graph[u][v];
                    parent[v] = u;
                }
            }
        }
        printMST(parent, graph, V);
    }

    private static int minKeyVertex(int[] key, boolean[] visited, int V) {
        int min = INF, minIndex = -1;
        for (int v = 0; v < V; v++) {
            if (!visited[v] && key[v] < min) {
                min = key[v];
                minIndex = v;
            }
        }
        return minIndex;
    }

    private static void printMST(int[] parent, int[][] graph, int V) {
        System.out.println("\nEdge \tWeight");
        for (int i = 1; i < V; i++) {
            System.out.println(parent[i] + " - " + i + "\t" + graph[i][parent[i]]);
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the number of vertices: ");
        int V = scanner.nextInt();
        int[][] graph = new int[V][V];
        System.out.println("Enter edges as: u v weight (0-indexed), and enter -1 -1 -1 to stop:");
        while (true) {
            int u = scanner.nextInt();
            int v = scanner.nextInt();
            int w = scanner.nextInt();
            if (u == -1 && v == -1 && w == -1) {
                break;
            }
            if (u >= 0 && v >= 0 && u < V && v < V) {
                graph[u][v] = w;
                graph[v][u] = w;
            } else {
                System.out.println("Invalid edge, please enter valid vertices.");
            }
        }
        Prim(graph, V);
        scanner.close();
    }
}