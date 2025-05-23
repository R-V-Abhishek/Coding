import java.util.*;

public class DFS {
    private int vertices;
    private List<List<Integer>> adjList;

    public DFS(int v) {
        vertices = v;
        adjList = new ArrayList<>();
        for (int i = 0; i < v; i++)
            adjList.add(new ArrayList<>());
    }

    public void addEdge(int u, int v) {
        adjList.get(u).add(v);
        adjList.get(v).add(u); // For undirected graph
    }

    private void dfsUtil(int v, boolean[] visited) {
        visited[v] = true;
        for (int n : adjList.get(v)) {
            if (!visited[n])
                dfsUtil(n, visited);
        }
    }

    public boolean isConnected() {
        boolean[] visited = new boolean[vertices];
        dfsUtil(0, visited);

        for (boolean v : visited) {
            if (!v)
                return false;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number of vertices: ");
        int v = sc.nextInt();
        System.out.print("Enter number of edges: ");
        int e = sc.nextInt();

        DFS g = new DFS(v);

        System.out.println("Enter edges (u v) one per line (0-based index):");
        for (int i = 0; i < e; i++) {
            int u = sc.nextInt();
            int w = sc.nextInt();
            g.addEdge(u, w);
        }

        if (g.isConnected())
            System.out.println("Graph is connected");
        else
            System.out.println("Graph is not connected");
    }
}
