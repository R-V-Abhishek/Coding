import collections

def solve_max_worth():
    def calculate_worth(s):
        return sum(ord(char) - ord('a') + 1 for char in s)
    
    try:
        n, m = map(int, input().split())
        strings = input().split()
        costs = list(map(int, input().split()))
        contradictory_pairs = [input().split() for _ in range(m)]
        budget = int(input())
    except (IOError, ValueError):
        print(0)
        return
    
    string_to_idx = {s: i for i, s in enumerate(strings)}
    worths = [calculate_worth(s) for s in strings]
    
    
    adj = collections.defaultdict(set)
    for s1, s2 in contradictory_pairs:
        if s1 in string_to_idx and s2 in string_to_idx:
            u, v = string_to_idx[s1], string_to_idx[s2]
            adj[u].add(v)
            adj[v].add(u)

    
    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            component = []
            q = collections.deque([i])
            visited[i] = True
            while q:
                u = q.popleft()
                component.append(u)
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
            components.append(component)

    
    component_options = []
    for component in components:
        comp_size = len(component)
        
        # Use exact enumeration for smaller components
        if comp_size <= 12:  # Further reduced threshold
            options = collections.defaultdict(int)
            options[0] = 0
            
            for i in range(1, 1 << comp_size):
                subset = []
                valid = True
                total_cost = 0
                total_worth = 0
                
                for j in range(comp_size):
                    if (i >> j) & 1:
                        idx = component[j]
                        
                        # Early termination if cost exceeds budget
                        if total_cost + costs[idx] > budget:
                            valid = False
                            break
                        
                        # Check contradiction with already selected
                        for sel in subset:
                            if idx in adj[sel]:
                                valid = False
                                break
                        if not valid:
                            break
                            
                        subset.append(idx)
                        total_cost += costs[idx]
                        total_worth += worths[idx]
                
                if valid:
                    options[total_cost] = max(options[total_cost], total_worth)
            component_options.append(list(options.items()))
        else:
            # For larger components, use a more sophisticated approach
            # Generate all maximal independent sets using backtracking
            options = collections.defaultdict(int)
            options[0] = 0
            
            def backtrack(idx, current_cost, current_worth, selected):
                if idx == comp_size:
                    options[current_cost] = max(options[current_cost], current_worth)
                    return
                
                node = component[idx]
                
                # Option 1: Don't include current node
                backtrack(idx + 1, current_cost, current_worth, selected)
                
                # Option 2: Include current node if valid
                can_include = True
                for sel_node in selected:
                    if node in adj[sel_node]:
                        can_include = False
                        break
                
                if can_include and current_cost + costs[node] <= budget:
                    selected.add(node)
                    backtrack(idx + 1, current_cost + costs[node], 
                             current_worth + worths[node], selected)
                    selected.remove(node)
            
            backtrack(0, 0, 0, set())
            component_options.append(list(options.items()))

 
    dp = [0] * (budget + 1)
    for options in component_options:
        for b in range(budget, -1, -1):
            for c, w in options:
                if b >= c:
                    dp[b] = max(dp[b], dp[b - c] + w)

    print(dp[budget])

if __name__ == "__main__":
    solve_max_worth()