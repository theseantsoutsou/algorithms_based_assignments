"""
Written by: Sean Tsou
Completed: 16/09/2022

    Assignment 2
    Part 1: Implementation of the class RoadGraph, which represents a city's road network as well as cafes. The class
            method routing() will return the most optimal route with a cafe from one node to another.
    Part 2: Given a list of downhill segments and associated scores, return the highest-scoring route for the skier.

    TC: Time Complexity
    ASC: Auxiliary Space Complexity
    Part 1:
        V: the total number of nodes (locations) in a graph
        E: the total number of edges (roads) in a graph
    Part2:
        P: the total number of nodes (intersection points) in a graph
        D: the total number of edges (downhill segments) in a graph

"""

import heapq


class RoadGraph:
    def __init__(self, roads: list[tuple[int, int, int]], cafes: list[tuple[int, int]]) -> None:
        """
        Constructor method for the class. Calls class methods to store inputs into specific data structures

        :param roads: a list of tuples (u,v,w), each representing a road from node u to node v with a travel time w
        :param cafes: a list of tuples (location,wait_time), representing a cafe at location with wait_time for coffee

        :Time Complexity: TC = O(V+E)
        Combing the TCs of the function calls self.find_v(), self.cafe_wait_times() and self.adj_list(). Details of the
        TC for each function are described below.

        :Auxiliary Space Complexity: ASC = O(V+E)
        Combing the ASCs of the function calls. Details of the ASCs for each function are described below.
        """
        self.roads = roads
        self.cafes = cafes
        self.v = self.find_v()
        self.wait_times = self.cafe_wait_times()
        self.graph = self.adj_list()

    def find_v(self) -> int:
        """
        Finds the total number of nodes from self.roads

        :return: the total number of nodes in a graph

        :Time Complexity: TC = O(E)
        The for-loop in this function scales with the size of self.roads, which is of length E as each item in
        self.roads represent an edge on the road graph.

        :Auxiliary Space Complexity: ASC = O(1)
        The variables created in this function are of constant size and do not scale.
        """
        v = 0

        for road in self.roads:
            if road[1] > v:
                v = road[1]
            elif road[0] > v:
                v = road[0]

        return v + 1

    def cafe_wait_times(self) -> list:
        """
        Processes the waiting times at each café to create a list of waiting times with the index representing the node.
        If a node is not a café, it would have a value of 0.

        :return: a list of waiting times

        :Time Complexity: TC = O(V)
        Initializing the wait_times scale with V, the number of locations in the RoadGraph. The for-loop then scales
        with the number of cafés, which would be some fraction of V. Hence, the overall TC is O(V)

        :Auxiliary Space Complexity: ASC = O(V)
        The list of wait_times will have a size dependent on V.
        """
        wait_times = [0 for _ in range(self.v)]

        for i in range(len(self.cafes)):
            wait_times[self.cafes[i][0]] = self.cafes[i][1]

        return wait_times

    def adj_list(self) -> list[list]:
        """
        Creates an adjacency list representing the paths in self.roads.
        The initial input stored in self.roads will be represented as a two-layered graph. Essentially, two identical
        graphs would be generated, each representing the paths in self.roads. These two graphs would then be connected
        via the cafés with an edge of a weight equivalent to its waiting time. This means that the second layer is
        only accessible through a café. For example node 0 will be connected to node 0+V with an edge weight of 3 if
        there is a café at node 0, with a waiting time of 3 minutes.

        :return: an adjacency list representing the RoadGraph

        :Time Complexity: TC = O(V+E)
        Initializing the adjacency list (graph) and the last for-loop both scale with V. The first for-loop scales with
        the size of self.roads, which is E. Everything happening within every for-loops are constant time. Hence, the
        overall TC is O(V+E)

        :Auxiliary Space Complexity: ASC = O(V+E)
        The only variable created is the adjacency list itself, which size will scale with V upon initialization.
        As the adjacency list is formed, however, roads/edges are being appended as neighbors. This scales with the
        number of edges E in the graph. Hence, overall ASC is O(V+E).
        """
        graph = [[] for _ in range(self.v * 2)]

        # Creating a two-layered graph
        for i in range(len(self.roads)):
            graph[self.roads[i][0]].append((self.roads[i][1], self.roads[i][2]))
            graph[self.roads[i][0]+self.v].append((self.roads[i][1] + self.v, self.roads[i][2]))

        # Connecting the two graphs via cafés with an edge of a weight equivalent to the café's waiting time
        for i in range(self.v):
            if self.wait_times[i] > 0:
                graph[i].append((i+self.v, self.wait_times[i]))

        return graph

    def routing(self, start: int, end: int) -> list[int] or None:
        """
        Implements Dijkstra's algorithm to find the shortest path from start to end, that also passes a café.

        :param start: the node to begin traversal
        :param end: the node to end traversal at
        :return: a list of nodes representing the shortest path; None if no such path exists

        :Time Complexity: TC = O(ElogV)
        The TC is dominated by the first while-loop, which is an implementation of Dijkstra's algorithm. As the priority
        queue is implemented with heap, updating the distances (heappush) and finding the minimum (heappop) will both
        cost log(V). This means that the algorithm itself will have a TC of O(ElogV + VlogV). However, E has a minimum
        value of V-1 and a maximum value of V^2, which means E will dominate V. Making the overall TC O(ElogV).
        The initialization of all the variables (distances, predecessors, priority_queue) scale with O(V). Traversing
        through the predecessors list to acquire the path is then O(E) as it would be dependent on edges between nodes.
        Overall, O(ElogV) still dominates all of them.

        :Auxiliary Space Complexity: ASC = O(V+E)
        The space required for the variables distances, predecessors, and priority_queue all scale with O(V). The size
        of the output variable path, however, will scale with E as the function traverses through the predecessors list.
        Traversal is dependent on the existing edges in a graph. These will give a combined ASC of O(3*V + E), which is
        O(V+E).
        """
        distances = [float("inf") for _ in range(self.v * 2)]
        predecessors = [-1 for _ in range(self.v * 2)]
        distances[start] = 0
        priority_queue = [(distances[start], start)]    # (key, value)

        # dijkstra's algorithm
        while len(priority_queue) > 0:
            current_dist, current_vertex = heapq.heappop(priority_queue)
            for neighbor in self.graph[current_vertex]:
                distance = current_dist + neighbor[1]
                if distance < distances[neighbor[0]]:   # or distances[neighbor[0]] == -1:
                    distances[neighbor[0]] = distance
                    predecessors[neighbor[0]] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor[0]))

        # if the equivalent end node on the second layer has no predecessors (-1), that means no paths between the start
        # and end nodes can contain a café
        if predecessors[end + self.v] == -1:
            return None

        # if a path containing a café exists, the traversal is from the start node on the first layer, to the end node
        # on the second layer
        path = [end]
        index = end + self.v    # start from the equivalent end node on the second layer
        while predecessors[index] != start:
            # if the predecessor is in the second layer
            if predecessors[index] >= self.v:
                path.append(predecessors[index] - self.v)
            # if the node wasn't previously added to path (due to the implementation of a two-layered graph)
            elif predecessors[index] != path[-1]:   # also implies "and predecessors[index] < self.v"
                path.append(predecessors[index])
            index = predecessors[index]

        # for the case of starting at the optimal cafe, its counterpart in the second layer would've been added to the
        # path while traversing above
        if path[-1] != start:
            path.append(start)

        return path[::-1]


def find_p(downhillScores: list[tuple[int, int, int]]) -> int:
    """
    Finds the total number of nodes from a list of edges/paths

    :param downhillScores:  a list of tuples, each representing the start node, target node, and score acquired from
                           travelling from start to target nodes

    :return: the total number of nodes in a graph

    :Time Complexity: TC = O(D)
    The for-loop in this function scales with the size of downhillScores, which is of length D as each item in
    downhillScores represent a downhill segment on the graph.

    :Auxiliary Space Complexity: ASC = O(1)
    The variables created in this function are of constant size and do not scale.
    """
    p = 0

    for segment in downhillScores:
        if segment[1] > p:
            p = segment[1]
        elif segment[0] > p:
            p = segment[0]

    return p + 1


def adj_listify(downhillScores: list[tuple[int, int, int]], p: int) -> list[list]:
    """
    Converts a list of paths/edges to an adjacency list

    :param downhillScores: a list of tuples, each representing the start node, target node, and score acquired from
                           travelling from start to target nodes
    :param p: the total number of nodes that exists
    :return: an adjacency list representing the ski paths

    :Time Complexity: TC = O(D+P)
    The initialization of the adjacency list (graph) scales with P. The for-loop then scales with the length of
    downhillScores, which is D, as downhillScores represents all the segments in a ski course. Hence, the overall TC is
    O(D+P).

    :Auxiliary Space Complexity: ASC = O(P)
    The only variable created is the adjacency list itself, which size will scale with P.

    """
    graph = [[] for _ in range(p)]

    for i in range(len(downhillScores)):
        graph[downhillScores[i][0]].append((downhillScores[i][1], downhillScores[i][2]))

    return graph


def critical_path(adj_list, predecessors, longest, u):
    """
    Traverses through a Directed Acyclic Graph and finds the longest (highest-scored) path

    :param adj_list: a graph represented by an adjacency list
    :param predecessors: a list of integers representing predecessors of each node
    :param longest: a list of integers representing the current highest possible score to reach each node
    :param u: the current node to traverse from
    :return: the highest possible score to reach u and list of predecessors for each node

    :Time Complexity: TC = O(D+P)
    The core idea of this critical path function is that the longest path for all descendants of a node must be computed
    before the result for said node can be computed. Therefore, this function implements a top-down recursion which
    iterates over every vertex and edge, giving the function a TC of O(D+P).

    :Auxiliary Space Complexity: ASC = O(D)
    As this function uses recursion, the space complexity will be determined by the program stack. The space would
    therefore be O(recursion depth). The depth of this recursion can be considered as when will the last recursive call
    be made and enter the return statement. The recursion will reach an end when the vertex has no reachable neighbors,
    which means that the space required for recursion scales with the existing edges in a graph, making the ASC O(D).
    """
    if longest[u] == -float("inf"):
        longest[u] = 0
        for v, score in adj_list[u]:
            total = score + critical_path(adj_list, predecessors, longest, v)
            if longest[u] < total:
                longest[u] = total
                predecessors[v] = u
    return longest[u]


def optimalRoute(downhillScores: list[tuple[int, int, int]], start: int, finish: int) -> list[int] or None:
    """
    Traverse through the downhill paths (a directed acyclic graph) to find the path with the highest possible score

    :param downhillScores: a list of tuples, each representing the start node, target node, and score acquired from
                           travelling from start to target nodes
    :param start: the start node
    :param finish: the target node to reach
    :return: a list of nodes representing the most optimal path for the highest score

    :Time Complexity: TC = O(D)
    The TC of this function is dominated by the function call to critical_path(). The TC of critical_path() is O(D+P).
    As the list of downhillScores can be represented as a connected directed acyclic graph, it is known that the number
    of downhill segments (D) will have a minimum value of P-1 and a maximum value greater than P. The growth of D will
    always overtake P, which therefore makes this function's overall TC O(D).

    :Auxiliary Space Complexity: ASC = O(D+P)
    The ASC includes all the space required for local function calls. Initializing the local variables longest and
    predecessors both scale with P. Traversing through the predecessors list and appending nodes to the output path,
    however, scales with D in terms of the space required for the list path. This is because the number of nodes to be
    traversed through is dependent on the existing edges of a graph (can't travel to a node if the edge doesn't exist).
    Hence, the overall ASC is O(D+P).
    """
    p = find_p(downhillScores)  # O(D)
    adj_list = adj_listify(downhillScores, p)   # O(D+P)
    longest = [-float("inf") for _ in range(p)]     # O(P)
    predecessors = [-1 for _ in range(p)]   # O(P)

    critical_path(adj_list, predecessors, longest, start)   # O(D+P), dominates the function's TC

    if predecessors[finish] == -1:
        return None

    path = [finish]
    index = finish

    # Traversing through the predecessor list costs O(D) as it is dependent on the existing edges between nodes
    while predecessors[index] != start:
        path.append(predecessors[index])
        index = predecessors[index]
    path.append(start)

    return path[::-1]
