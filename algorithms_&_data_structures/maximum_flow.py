"""
Written by: Sean Tsou
Completed: 21/10/2022

    Assignment 3
    Part 1: Sharing the Meals
        Implementation of the maximum flow problem with consideration of lower bounds.


    TC: Time Complexity
    ASC: Auxiliary Space Complexity

    Part 1:
        n = number of days
"""

########################################################################################################################
#                                                                                                                      #
# ----------------------------------------------------- Part 1 --------------------------------------------------------#
#                                                                                                                      #
########################################################################################################################
from math import floor, ceil

# the total number of housemates to be allocated to cook
NUM_HOUSEMATES = 5


class Edge:
    """ The Edge class representing an edge between two nodes"""
    def __init__(self, destination: int, flow: int, capacity: int, reverse: int):
        """
        The constructor method for the edge class

        :param destination: the index of the destination node
        :param flow: the flow through this edge
        :param capacity: the maximum capacity allowed through this edge
        :param reverse: the pointer to the reverse edge in the destination node's adjacency list

        :Time Complexity: O(1) - attribute assignment
        :Auxiliary Space Complexity: O(1) - constant number of variable assignment
        """
        self.destination = destination
        self.flow = flow
        self.capacity = capacity
        self.reverse = reverse


def generate_graph(availability: list[list]) -> list[list]:
    """
    Generate a flow network with reverse edges. For consistency, for every edge u->v, a zero-capacity reverse edge v->u
    is created with a flow equivalent to the negative of the forward flow. However, all flows are initialized as 0. Upon
    generating this network, the capacity for every forward edge from source to housemate nodes are initialized as the
    lower bound, aka the minimum required flow. This is so that when the ford-fulkerson algorithm is called later, all
    edges will be saturated with the minimum flow required if there is a feasible solution.
    The capacity is updated at a later stage, described in max_flow().

    The general structure of the graph is as follows:
            source -> housemates -> selectors -> meals -> target
    In terms of the actual indexing for the graph, the order is as follows:
            source -> housemates -> breakfasts -> dinners -> target -> selectors for housemate0, housemate1 and so on

    There are 1 selector per day per person, meaning there are a total of NUM_HOUSEMATES * n selector nodes.
    The edge from housemates to each of their respective selectors have a capacity of 1, ensuring that no one can cook
    both meals on the same day.

    :param availability: a list of lists containing person j's availability on day i
    :return: a flow network

    :Time Complexity: O(n)
    This function creates an adjacency list to represent the flow network. Each block of code, each for loop in this
    function has a runtime that scales with O(n) or O(1). On top of which, since the creation of an adjacency list costs
    scales with the number of nodes, which in this case scales with n, the overall TC for this function is O(n)

    :Auxiliary Space Complexity: O(n)
    The space complexity for an adjacency list is O(V + E). The number of edges will always overtake the number of
    vertices. The number of edges also scales with n. Therefore, overall ASC scales with O(n).
    """
    n = len(availability)
    # minimum number of meals required per person
    min_flow = floor(0.36 * n)
    # index for the target node
    target = NUM_HOUSEMATES + 2 * n + 1
    num_of_selectors = NUM_HOUSEMATES * n

    # each edge = (vertex, flow, capacity, reverse)
    # O(n) - length of the network list depends on the number of days
    network = [[] for _ in range(target + num_of_selectors + 1)]

    # from source to housemates
    # O(1) - constant operations in a loop scaling with NUM_HOUSEMATES, which is a constant
    for i in range(1, NUM_HOUSEMATES + 1):
        reverse_id = len(network[i])
        forward_edge = Edge(i, 0, min_flow, reverse_id)
        network[0].append(forward_edge)
        # reverse edge from each housemate to source
        reverse_edge = Edge(0, 0, 0, len(network[0]) - 1)
        network[i].append(reverse_edge)

    # from meals to target
    # O(n) - constant operations in a loop scaling with the number of meals, which is bounded by 2*n
    for i in range(NUM_HOUSEMATES + 1, target):
        reverse_id = len(network[target])
        forward_edge = Edge(target, 0, 1, reverse_id)
        network[i].append(forward_edge)
        # reverse edge from target to each meal
        reverse_edge = Edge(i, 0, 0, len(network[i]) - 1)
        network[target].append(reverse_edge)

    # from selectors to meals and housemates to selectors
    # overall O(n) - inner for-loop scales with NUM_HOUSEMATES, which is a constant
    for i in range(n):
        # O(1) - constant operations in a loop scaling with a constant
        for j in range(NUM_HOUSEMATES):
            breakfast = NUM_HOUSEMATES + 1 + i
            dinner = NUM_HOUSEMATES + 1 + n + i
            selector = target + i + j * n + 1

            # if available to make breakfast
            if availability[i][j] == 1:
                meal_reverse_id = len(network[breakfast])
                # forward edge from selector to breakfast on the i-th day
                meal_forward_edge = Edge(breakfast, 0, 1, meal_reverse_id)
                network[selector].append(meal_forward_edge)
                # reverse edge from breakfast on the i-th day to selector
                meal_reverse_edge = Edge(selector, 0, 0, len(network[selector]) - 1)
                network[breakfast].append(meal_reverse_edge)

            # if available to make dinner
            elif availability[i][j] == 2:
                meal_reverse_id = len(network[dinner])
                # forward edge from selector to dinner on the i-th day
                meal_forward_edge = Edge(dinner, 0, 1, meal_reverse_id)
                network[selector].append(meal_forward_edge)
                # reverse edge from dinner on the i-th day to selector
                meal_reverse_edge = Edge(selector, 0, 0, len(network[selector]) - 1)
                network[dinner].append(meal_reverse_edge)

            # if available to make either breakfast or dinner
            elif availability[i][j] == 3:
                meal_reverse_id = len(network[breakfast])
                # forward edge from selector to breakfast on the i-th day
                meal_forward_edge = Edge(breakfast, 0, 1, meal_reverse_id)
                network[selector].append(meal_forward_edge)
                # reverse edge from breakfast on the i-th day to selector
                meal_reverse_edge = Edge(selector, 0, 0, len(network[selector]) - 1)
                network[breakfast].append(meal_reverse_edge)

                meal_reverse_id = len(network[dinner])
                # forward edge from selector to dinner on the i-th day
                meal_forward_edge = Edge(dinner, 0, 1, meal_reverse_id)
                network[selector].append(meal_forward_edge)
                # reverse edge from dinner on the i-th day to selector
                meal_reverse_edge = Edge(selector, 0, 0, len(network[selector]) - 1)
                network[dinner].append(meal_reverse_edge)

            # creates a flow between housemate and selector even if unavailable to cook either meals on the i-th day
            # the selector just does not point to anything
            selector_reverse_id = len(network[selector])
            # forward edge from the housemate to selector
            selector_forward_edge = Edge(selector, 0, 1, selector_reverse_id)
            network[j + 1].append(selector_forward_edge)
            # reverse edge from the selector to the housemate
            selector_reverse_edge = Edge(j + 1, 0, 0, len(network[j + 1]) - 1)
            network[selector].append(selector_reverse_edge)

    return network


def ford_fulkerson(graph: list[list[Edge]], u: int, t: int, bottleneck: int or float, visited: list[bool]) -> int:
    """
    This function is an implementation of the ford-fulkerson algorithm. It recursively goes through the flow network to
    increase the flow pushed through the graph as long as there is a viable augmented path in the residual network.
    This implementation uses depth-first search to find an augmented path.

    :param graph: a flow network
    :param u: the node to begin traversal from
    :param t: the target node
    :param bottleneck: the minimum capacity of a path
    :param visited: a list of Trues or Falses to keep track of which nodes have been visited
    :return: 0 if no augmented path is found; the flow for an augmented path otherwise.

    :Time Complexity: O(n)
    Ford-fulkerson's algorithm finds an augmenting path in a network recursively. This traversal has a complexity of
    O(E). Since the number of edges (E) scales with n, the TC for this algorithm would be O(n).

    :Auxiliary Space Complexity: O(n)
    There is a constant number of variable assignment and arithmetic operations in this function. But due to the
    recursive nature of this function, the space required in the stack would therefore scale with O(n).

    This code is implemented using Algorithm 61 in FIT2004 Algorithms and Data Structures Course Notes.
    """
    if u == t:      # the target/sink was reached
        return bottleneck

    visited[u] = True

    for i in range(len(graph[u])):
        forward_edge = graph[u][i]
        reverse_edge = graph[forward_edge.destination][forward_edge.reverse]
        residual = forward_edge.capacity - forward_edge.flow
        if residual > 0 and not visited[forward_edge.destination]:
            augment = ford_fulkerson(graph, forward_edge.destination, t, min(bottleneck, residual), visited)
            if augment > 0:     # an augmenting path has been found
                forward_edge.flow += augment
                reverse_edge.flow -= augment
                return augment

    return 0


def _max_flow_aux(graph, s, t):
    """
    This auxiliary function calls the ford-fulkerson algorithm in a loop that runs as long as there is an augmenting
    path remaining in the network.

    :param graph: a flow network
    :param s: the source node
    :param t: the target node
    :return: the maximum flow in the flow network

    :Time Complexity: O(n^2)
    The overall TC for this maximum flow solution using the dfs implementation of ford-fulkerson's algorithm is
    O(E*fMax), where E is the number of edges and fMax is the maximum flow through the network. The number of edges is
    bound by n. fMax, is also bounded by 2*n, as the maximum possible flow for any network in this given scenario is the
    total number of meals. Therefore, the overall TC is O(n^2).

    :Auxiliary Space Complexity: O(n^2)
    There are constant variable assignments in this function. The function then calls upon the recursive function
    ford-fulkerson, which would require O(n) space in the stack. The number of times ford-fulkerson is called, however,
    scales with fMax, which is bounded by 2*n. Therefore, the amount of ASC required would be O(n^2) instead.

    This code is implemented using Algorithm 61 in FIT2004 Algorithms and Data Structures Course Notes.
    """
    flow = 0
    augment = float("inf")
    while augment > 0:
        visited = [False for _ in range(len(graph))]
        augment = ford_fulkerson(graph, s, t, float("inf"), visited)
        flow += augment

    return flow


def max_flow(graph: list[list], s: int, t: int, n: int) -> int:
    """
    This function solves the network flow problem accounting for lower bound values. When the flow network was
    initialized, the capacity for each edge was set to lower bound, provided the lower bound is not 0 for that edge.
    After calling _max_flow_aux() on this initialized network, all flows with a lower bound capacity should be
    saturated, otherwise there is no feasible solution as it means some people cannot cook the minimum number of meals
    required per person. If these lower-bounded flows are saturated, their capacities can now be updated to be the
    upper bounds, which is the maximum number of meals each person is allowed to cook. _max_flow_aux() is then called
    on this updated network again, and the total maximum flow is then returned.

    :param graph: a flow network
    :param s: the source node
    :param t: the target node
    :param n: the number of days
    :return: the maximum flow satisfying the lower and upper bound requirements

    :Time Complexity: O(n^2)
    The TC of this function is dominated by the calls to _max_flow_aux() which has a complexity of O(n^2). The function
    call is made twice in series, leaving the overall TC as O(n^2).

    :Auxiliary Space Complexity: O(n)
    The ASC is dominated by the space required for _max_flow_aux(), which is O(n) overall.
    """
    capacity = ceil(0.44 * n)
    flow = 0

    flow += _max_flow_aux(graph, s, t)

    # O(1), the number of edges connect to the source node 0 is equivalent to NUM_HOUSEMATES, which is a constant
    for edge in graph[0]:
        if edge.flow == edge.capacity:  # integer comparison
            edge.capacity = capacity
        else:   # if there is no feasible solution because the lower-bounded flows are not saturated, return -1
            return -1

    flow += _max_flow_aux(graph, s, t)

    return flow


def meal_allocation(graph, n):
    """
    This function allocates each housemate to meal(s) they are responsible by analyzing the resulting network after the
    maximum flow has been found. This function goes through all the selector nodes to find who is allocated to which
    meal. The indices of the selectors are mathematically linked with the housemate they are connected to. Similarly,
    the indices of meals in the network can also be manipulated to find which day they belong to.

    :param graph: a flow network
    :param n: the number of days
    :return: a list of valid allocations for breakfasts and a list of valid allocations for dinners

    :Time Complexity: O(n)
    The TC for this function is dominated by the for loop, which loops through the number of selectors. The number of
    selectors scales with n. Constant operations are conducted in the loop, making the overall TC O(n).

    :Auxiliary Space Complexity: O(n)
    Initializing the breakfast and dinner lists both have lengths of n, dominating the overall ASC.
    """

    # initializing meals as 5 (the value for takeouts)
    # if the program enters this function, there is a feasible solution and the correct allocation will occur below
    breakfast = [5 for _ in range(n)]   # O(n)
    dinner = [5 for _ in range(n)]      # O(n)

    target_id = NUM_HOUSEMATES + 2 * n + 1

    # go through the selectors
    # overall O(n) as the number of selectors is NUM_HOUSEMATES * n
    for i in range(target_id + 1, len(graph)):
        housemate = (i - target_id - 1)//n
        # the maximum number of edges extending from a selector node is 3, one edge per meal on that day and a reverse
        # edge if one of the forward edges is saturated. A selector limits the incoming flow to just 1 to prevent
        # someone from cooking both meals a day. Therefore, this for-loop scales with O(1)
        for edge in graph[i]:
            # if the edge is saturated and is not a reverse edge
            if edge.flow > 0:
                meal = edge.destination
                # if the meal is a breakfast
                if meal <= NUM_HOUSEMATES + n:
                    meal_id = meal - NUM_HOUSEMATES - 1
                    breakfast[meal_id] = housemate
                else:   # if the meal is a dinner
                    meal_id = meal - NUM_HOUSEMATES - n - 1
                    dinner[meal_id] = housemate

    return breakfast, dinner


def allocate(availability: list[list]) -> tuple[list] or None:
    """
    The main function to allocate availabilities for meals. This function generates a flow network from the availability
    list by calling generate_graph() and calls the max_flow() method to saturate the flow network. Before allocating the
    meals, the function validates the maximum flow to check if there is a valid solution before calling
    meal_allocation() to allocate each housemate to a meal(s).

    :param availability: a list of lists containing person j's availability on day i
    :return: a list of valid allocations for breakfasts and a list of valid allocations for dinners

    :Time Complexity: O(n^2)
    The TC is dominated by all the function calls, with max_flow() dominating the overall TC. generate_graph() has an
    overall TC of O(n), max_flow() has an overall TC of O(n^2), and meal_allocation() has an overall TC of O(n).
    Therefore, the overall TC is O(n^2).

    :Auxiliary Space Complexity: O(n)
    The space required for this function is again respective to the sum of the space required for all the functions
    called, which is O(n) overall.
    """
    n = len(availability)   # the number of days
    max_take_out = floor(0.1 * n)   # maximum number of days when meals can be ordered
    source = 0      # source node index
    target = NUM_HOUSEMATES + 2 * n + 1     # target node index

    graph = generate_graph(availability)

    flow = max_flow(graph, source, target, n)

    if flow == -1:
        return None
    elif flow + max_take_out < 2 * n:
        return None

    return meal_allocation(graph, n)

