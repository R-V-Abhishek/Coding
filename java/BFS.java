import java.util.*;

public class BFS {
    private int vertices; // Number of vertices
    private LinkedList<Integer>[] adjList; // Adjacency list

    public BFS(int v) {
        vertices = v;
        adjList = new LinkedList[v];
        for (int i = 0; i < v; ++i)
            adjList[i] = new LinkedList<>();
    }

    // Add edge to the digraph
    public void addEdge(int src, int dest) {
        adjList[src].add(dest);
    }

    // Print all nodes reachable from start using BFS
    public void bfs(int start) {
        boolean[] visited = new boolean[vertices];
        Queue<Integer> queue = new LinkedList<>();

        visited[start] = true;
        queue.add(start);

        System.out.print("Nodes reachable from " + start + ": ");
        while (!queue.isEmpty()) {
            int node = queue.poll();
            System.out.print(node + " ");

            for (int neighbor : adjList[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
        System.out.println();
    }

    // Example usage with user input
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter number of vertices: ");
        int v = scanner.nextInt();
        BFS g = new BFS(v);

        System.out.print("Enter number of edges: ");
        int e = scanner.nextInt();

        System.out.println("Enter edges (source destination):");
        for (int i = 0; i < e; i++) {
            int src = scanner.nextInt();
            int dest = scanner.nextInt();
            g.addEdge(src, dest);
        }

        System.out.print("Enter starting node for BFS: ");
        int start = scanner.nextInt();

        g.bfs(start);
        scanner.close();
    }
}
