from utils import NO_OF_CHARS, char2index, read_file, output_results
import sys

global_end = -1


class Node:
    """
    Node class for the construction of a suffix tree
    """

    def __init__(self, leaf=False, root=False):
        """
        Constructor method for the Node class

        :param leaf: boolean indicating if the node is a leaf
        :param root: boolean indicating if the node is the root node
        """
        self.children = {i: None for i in range(NO_OF_CHARS)}
        self.suffix_link = None
        self.leaf = leaf
        self.isRoot = root

    def add_suffix_link(self, node):
        """
        Method to add a node as the suffix link to self

        :param node: a node to be added as a suffix link
        """
        self.suffix_link = node


class Edge:
    """
    Edge class for the construction of a suffix tree
    """

    def __init__(self, start: int, end: int, node: Node):
        """
        Constructor method for the Edge class

        :param start: the starting index of the substring which the edge represents
        :param end: the ending index of the substring which the edge represents (exclusive)
        :param node: the node which the edge connects to
        :return:
        """
        self.start = start
        self.end = end
        self.next_node = node

    def length(self):
        """
        Method to get the length of the edge
        """
        return self.end - self.start + 1

    def __getattribute__(self, name):
        """
        Extending the magic function __getattribute__ so that the global_end is returned if looking at a leaf node
        """
        if name == "end":
            if self.next_node.leaf:
                return global_end
        return super(Edge, self).__getattribute__(name)


class SuffixTree:
    """
    Suffix tree constructed with Ukkonen's Algorithm
    """

    def __init__(self, txt):
        """
        Constructor method for the SuffixTree class
        :param txt: the text to be inserted into the suffix tree
        """
        self.txt = txt
        self.size = len(self.txt)
        self.root = Node(root=True)  # initializing root node
        self.root.add_suffix_link(self.root)  # root has a suffix link to itself
        self.root_edge = Edge(
            -1, -1, self.root
        )  # since I am using edge, I need a root edge to begin traversal
        self.construct(self.txt)  # construct suffix tree

    def new_edge(self, start, end=None, leaf=False):
        """
        Helper fucntion to create a new edge

        :param start: starting index of the edge
        :param end: the ending index of the edge, default None due to previous modification to the __getattribute__ method
        :param leaf: boolean indicating if the node to be added is a leaf node
        """
        node = Node(leaf=leaf)
        node.add_suffix_link(self.root)

        return Edge(start, end, node)

    def construct(self, txt):
        """
        Implementation of Ukkonen's algorithm to construct a suffix tree
        """
        global global_end
        lastJ = 0  # Tracking the number of rule 2s - number of leaf nodes
        active_node = self.root  # start from the root node
        active_edge = (
            -1
        )  # initializaing active_edge, which is essentially the remainder's start
        active_length = 0  # length of the remainder

        for i in range(len(txt)):
            global_end = i  # extension rule 1, update global end
            pending = None  # Node waiting for a suffix link

            while (
                i - lastJ + 1 > 0
            ):  # i - lastJ + 1 gives the number of suffixes to be added in a phase
                if active_length == 0:
                    active_edge = i

                # if there is no outgoing edge starting with the active edge from the active node
                if active_node.children[char2index(txt[active_edge])] is None:
                    # extension rule 2, new leaf edge gets created
                    active_node.children[char2index(txt[active_edge])] = self.new_edge(
                        i, leaf=True
                    )
                    # rule 2, so increment lastJ
                    lastJ += 1

                    """A new node has been added, so if there is an internal node waiting
                    for a suffix link, we add the link here."""
                    if pending is not None:
                        pending.add_suffix_link(active_node)
                        pending = None

                # if there is outgoing edge starting with the active edge from the active node
                else:
                    # get the node which the edge connects to
                    next_edge = active_node.children[char2index(txt[active_edge])]

                    # skip count, walk down the tree
                    if active_length >= next_edge.length():
                        active_edge += next_edge.length()
                        active_length -= next_edge.length()
                        active_node = next_edge.next_node
                        continue

                    # extension rule 3, character being processed already exists on the edge
                    if txt[next_edge.start + active_length] == txt[i]:
                        # check if any node is waiting for a suffix link
                        if pending is not None and not active_node.isRoot:
                            pending.add_suffix_link(active_node)
                            pending = None

                        # update remainder
                        active_length += 1
                        # end phase
                        break

                    """This is where we do extension rule 2, where we create
                    a new internal node, that is, when the active point is in
                    the middle of an edge. A new internal node is added and a
                    new leaf edge and node are added, extending from said internal
                    node."""
                    split_end = next_edge.start + active_length - 1
                    split_edge = self.new_edge(next_edge.start, split_end)
                    split_node = split_edge.next_node
                    split_node.children[char2index(txt[i])] = self.new_edge(i, leaf=True)
                    next_edge.start += active_length
                    split_node.children[char2index(txt[next_edge.start])] = next_edge
                    active_node.children[char2index(txt[active_edge])] = split_edge

                    # extension rule 2 so increment lastJ
                    lastJ += 1

                    # check for nodes waiting on a suffix link
                    if pending is not None:
                        pending.add_suffix_link(split_node)

                    # new internal node now waiting for a suffix link
                    pending = split_node

                # if the active node is root and we are entering the next phase, take 1 off the remainder
                if active_node.isRoot and active_length > 0:
                    active_length -= 1
                    active_edge = lastJ
                elif not active_node.isRoot:    # otherwise follow the suffix link
                    active_node = active_node.suffix_link

    def walk_dfs(self, current: Edge, suffix_arr=[], depth=0, prefix_length=0, verbose=0):
        """
        DFS traversal method to traverse throught the tree

        :param current: the edge currently being traversed
        :param suffix_arr: suffix array
        :param depth: check what level of the tree the traversal is on for printing purposes
        :param prefix_length: length of traversal per traversal to each leaf
        :param verbose: 0 or 1 to print
        """
        # solely for testing and pretty-printing purposes
        if verbose:
            print("|- " * depth + self.txt[current.start : current.end + 1])

        # if the connected node is a leaf, calculate the suffix index
        if current.next_node.leaf:
            suffix_arr.append(current.start - prefix_length)

        # if the node is root, reset prefix length to 0
        if current.next_node.isRoot:
            prefix_length = 0
        else:   # otherwise add edge length to prefix length
            prefix_length += current.length()

        # Recursively traverse the children of the current edge's next node
        for i in range(NO_OF_CHARS):
            child = current.next_node.children[i]
            if child is not None:
                self.walk_dfs(child, suffix_arr, depth + 1, prefix_length, verbose=verbose)

    def get_suffix_array(self):
        """
        Method to get suffix array

        :return: suffix array
        """
        self.suffix_array = []
        self.walk_dfs(self.root_edge, suffix_arr=self.suffix_array, verbose=0)

        return self.suffix_array


def genbwt(data: str):
    """
    Generate the burrows-wheeler transform of a given string by generating a suffix tree using
    Ukkonen's algorithm then retrieving the suffix array.

    Assumes input data has the terminating character '$'

    :param data: string to be converted to a bwt
    :return: a bwt of the input
    """
    tree = SuffixTree(data)
    suffix_arr = tree.get_suffix_array()

    bwt = []

    for item in suffix_arr:
        bwt.append(tree.txt[item - 1])

    return "".join(bwt)


if __name__ == "__main__":
    _, filename1 = sys.argv
    txt_str = read_file(filename1)
    bwt = genbwt(txt_str)
    output_results(bwt, "output_genbwt.txt")
