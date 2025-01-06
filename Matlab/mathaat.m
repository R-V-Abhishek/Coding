%Dijksta's algorithm
S = [1 1 1 2 2 2 3 3 3 4 4 5]; % source vertex
T = [2 3 4 3 4 5 4 5 6 5 6 6]; % terminal vertex
W = [3 5 6 3 4 7 2 6 8 2 2 5]; % weight for each edge
G = graph(S,T,W); % to plot graph
[path,d] = shortestpath(G,1,6); % to calculate the shortest path from 1 to 6
P = plot(G,'Edgelabel',G.Edges.Weight); % to plot the given graph
highlight(P,path,'EdgeColor','red');
fprintf("%d\n",path); % to print the path
fprintf("The length %d:",d); % to print the shortest distance