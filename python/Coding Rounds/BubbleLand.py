import math
import heapq

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def line_intersects_circle(p1, p2, c, r):
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = c
    dx = x2 - x1
    dy = y2 - y1
    fx = x1 - cx
    fy = y1 - cy
    a = dx*dx + dy*dy
    b = 2*(fx*dx + fy*dy)
    c_val = fx*fx + fy*fy - r*r
    disc = b*b - 4*a*c_val
    if disc < 0:
        return False
    disc = math.sqrt(disc)
    t1 = (-b - disc)/(2*a)
    t2 = (-b + disc)/(2*a)
    return (0 <= t1 <= 1) or (0 <= t2 <= 1)

def ccw(A,B,C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def segments_intersect(A,B,C,D):
    return (ccw(A,C,D) != ccw(B,C,D)) and (ccw(A,B,C) != ccw(A,B,D))

def count_tax_crossings(p1, p2, tax_lines, buildings):
    count = 0
    for i,j in tax_lines:
        b1 = (buildings[i][0], buildings[i][1])
        b2 = (buildings[j][0], buildings[j][1])
        if segments_intersect(p1,p2,b1,b2):
            count +=1
    return count

def can_travel(p1, p2, buildings, radius):
    for bx,by,br in buildings:
        if line_intersects_circle(p1,p2,(bx,by),br+radius):
            return False
    return True

def solve():
    S = int(input())
    vx, vy, vr = map(int,input().split())
    dest_x, dest_y = map(int,input().split())
    N = int(input())
    buildings = [tuple(map(int,input().split())) for _ in range(N)]
    T = int(input())
    tax_lines = [tuple(map(lambda x:int(x)-1,input().split())) for _ in range(T)]

    start = (vx,vy)
    dest = (dest_x,dest_y)

    # Direct path check
    if can_travel(start,dest,buildings,vr):
        print(0)
        return

    # Graph nodes: start + destination + building centers
    nodes = [start, dest] + [(bx,by) for bx,by,_ in buildings]
    n_nodes = len(nodes)

    # Dijkstra: cost = number of tax crossings
    pq = [(0,0)] # (cost, node index)
    visited = [math.inf]*n_nodes
    visited[0]=0

    while pq:
        cost,u = heapq.heappop(pq)
        if cost>visited[u]:
            continue
        if u==1: # reached destination
            print(cost)
            return
        for v in range(n_nodes):
            if u==v:
                continue
            p1 = nodes[u]
            p2 = nodes[v]
            if can_travel(p1,p2,buildings,vr):
                extra = count_tax_crossings(p1,p2,tax_lines,buildings)
                if visited[v]>cost+extra:
                    visited[v]=cost+extra
                    heapq.heappush(pq,(visited[v],v))
    print("Impossible")

if __name__=="__main__":
    solve()
