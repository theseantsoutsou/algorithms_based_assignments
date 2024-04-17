"""
Written by: Sean Tsou
Completed: 21/10/2022

    Assignment 3
    Part 2: Similarity Detector
        Implementation of pattern matching using a suffix tree and tree traversal.

    TC: Time Complexity
    ASC: Auxiliary Space Complexity

    Part2:
        N = length of the first string
        M = length of the second string
"""

########################################################################################################################
#                                                                                                                      #
# ----------------------------------------------------- Part 2 --------------------------------------------------------#
#                                                                                                                      #
########################################################################################################################


class Node:
    """ The Node class represents a node in a suffix tree """
    # 26 letters in the alphabet + space + | + }
    NUM_CHARACTERS = 29

    def __init__(self, label):
        """
        Constructor method for the node class

        :param label: a string that represents the part the suffix tree which this node represents

        :Time Complexity: O(1) - constant variable assignment

        :Auxiliary Space Complexity: O(1) - constant variable assignment
        """
        self.index = -1
        self.label = label
        # outgoing edges; maps characters to nodes
        self.nexts = [None] * self.NUM_CHARACTERS
        # type defines what the string label is referring to
        #     if type is "{" it belongs to the first string
        #     if type is "|" it belongs to the second string
        #     if type is None it is a common string between first and second string by the end of construction
        self.type = None
        self.children = 0


class SuffixTree:
    """ The SuffixTree class represents a suffix tree for two strings """
    # alphanumeric values of the terminating symbols used later to mark internal nodes
    LEFTB = ord("{")
    PIPE = ord("|")

    def __init__(self, txt1, txt2):
        """
        Constructor method for the suffix tree

        :param txt1: first string
        :param txt2: second string

        :Time Complexity: O((N+M)^2)
        The constructor calls the self.construct() method to create the suffix tree, which costs O((N+M)^2).

        :Auxiliary Space Complexity: O((N+M)^2)
        Constructing the suffix tree requires O((N+M)^2) space.
        """
        self.root = Node(None)
        self.root.index = 0
        self.nodes = 1
        self.construct(txt1, txt2)

    def construct(self, txt1, txt2):
        """
        This function generates the suffix tree. self.trim_label() is then called to make sure each node's label in the
        tree only contains strings for either string1 or string2 instead of both. self.mark_internal() is then called
        to mark all the internal nodes as one of: a substring of string1, a substring of string2, or a substring of
        both.

        :param txt1: first string
        :param txt2: second string
        :return: None; constructs a Suffix Tree

        :Time Complexity: O((N+M)^2)
        The TC is bounded by the creation of the suffix tree which goes through the combined string, from the longest
        suffix (the whole string) to the shortest sub string. Everything that occurs during construction, namely the
        operations within the loops, are all of constant time (except slicing). self.trim_label costs O((N+M)^2) and
        self.mark_internal() costs O(N+M). Therefore, overall TC is still O((N+M)^2).

        :Auxiliary Space Complexity: O((N+M)^2)
        The space required to construct this suffix tree is also O((N+M)^2) because it iterates through the combined
        string to look at all suffixes.
        """

        txt = self.combine(txt1, txt2)

        self.root.nexts[self.alphanum(txt[0])] = Node(txt)
        self.root.nexts[self.alphanum(txt[0])].index = self.nodes
        self.nodes += 1
        # add all possible suffixes from longest to shortest
        for i in range(len(txt)):
            # start at root and "traverse" down the string
            current = self.root
            j = i
            while j < len(txt):
                if current.nexts[self.alphanum(txt[j])] is not None:
                    child = current.nexts[self.alphanum(txt[j])]
                    label = child.label

                    # go along this path until the label is exhausted or until the string is mismatched
                    k = j + 1
                    while k - j < len(label) and txt[k] == label[k-j]:
                        k += 1
                    if k - j == len(label):     # if the edge has been exhausted
                        current = child
                        j = k
                    else:   # there is a mismatch and the "traversal" broke in the middle of the edge
                        childExist, childNew = self.alphanum(label[k-j]), self.alphanum(txt[k])

                        # create a node where the edge broke
                        mid = Node(label[:k-j])
                        mid.index = self.nodes
                        mid.nexts[childNew] = Node(txt[k:])
                        mid.children += 1
                        mid.nexts[childNew].index = self.nodes + 1
                        self.nodes += 2

                        # initial child becomes mid's child
                        mid.nexts[childExist] = child
                        mid.children += 1

                        # update initial child's label
                        child.label = label[k-j:]

                        # mid becomes new child of the original parent
                        current.nexts[self.alphanum(txt[j])] = mid
                        current.children += 1

                else:   # fell off the tree at a node, make a leaf node
                    current.nexts[self.alphanum(txt[j])] = Node(txt[j:])
                    current.children += 1
                    current.nexts[self.alphanum(txt[j])].index = self.nodes
                    self.nodes += 1

        self.trim_label(self.root)      # O((N+M)^2)
        self.mark_internal(self.root, 0)    # O(N+M)

    def trim_label(self, node):
        """
        This function uses DFS to traverse through the suffix tree to trim the labels of each node. At the same time,
        this function will mark the node types for the nodes which labels it trims.
        :param node: the node to traverse from
        :return: None

        :Time Complexity: O((N+M)^2)
        The time complexity is dominated by the recursive calls and the string slicing. String slicing costs O(N+M).
        It is done every iteration of the recursion, making the overall TC O((N+M)^2).

        :Auxiliary Space Complexity: O((N+M)^2)
        The recursion requires O(N+M) space in the stack to begin with. The list slicing for each iteration also
        requires O(N+M) amount of space to store. Therefore, the overall space complexity is O((N+M)^2).
        """

        for child in node.nexts:
            if child is not None:
                for i in range(len(child.label)):
                    if child.label[i] == "{":
                        child.label = child.label[:i+1]
                        child.type = "{"
                        break
                if child.label[-1] == "|":
                    child.type = "|"

                self.trim_label(child)

    def mark_internal(self, node, accumulated_types):
        """
        This function traverses through the suffix tree and marks nodes with an attribute type value of None. This is
        how the nodes will be fully differentiated as either, substring of string1, substring of string2, or a common
        substring. For example, if every single node extending from an internal node has the type {, indicating they
        belong to the first string, the sum of their types after conversion to alphanumeric values would be divisible by
        ord("{"), which makes the internal node a substring of string1. A similar check is applied to nodes of type |.
        If the accumulated sum is not divisible by either type, then it must contain both types in its children nodes,
        indicating the internal node is a common substring of both strings.

        :param node: the node to traverse from
        :param accumulated_types: an integer sum of the child node types (alphanumeric value of their type)
        :return: integer sum of the children node types

        :Time Complexity: O(N+M)
        The function executes constant-time operations so the TC is dominated by the recursive calls. This function
        is essentially utilizing DFS, which means the overall TC will scale with the number of nodes + edges, both
        scaling with N+M making the overall TC O(N+M).

        :Auxiliary Space Complexity: O(N+M)
        The recursive nature of the function makes it require O(N+M) space in the stack.
        """
        res_type = 0
        if node.type is None:
            for child in node.nexts:    # O(1) - length of node.nexts is constant
                if child is not None:
                    if child.type is None:
                        res_type += self.mark_internal(child, accumulated_types)
                    else:
                        res_type += ord(child.type)

            if node.index != 0:
                if res_type % self.LEFTB == 0:
                    node.type = "{"
                if res_type % self.PIPE == 0:
                    node.type = "|"

        return res_type

    def find_all_common_substrings(self, node, lcs="", lst=None):
        """
        This function recursively finds all possible common substrings the two strings in the suffix tree. Common
        substrings are marked by nodes with attribute type None. These substrings can be concatenated with parent nodes
        (also with attribute type None) to form a longer common substring.

        :param node: the node to traverse from
        :param lcs: the longest common substring in each iteration of recursion
        :param lst: the list containing all possible common substrings
        :return: a lst of all common substrings

        :Time Complexity: O(N+M)
        The TC is dominated by the traversal through the suffix tree's nodes, the amount of which depends on the lengths
        of string1 and string2, which makes the overall TC O(N+M).

        :Auxiliary Space Complexity: O(N+M)
        Due to the recursive nature of the function, the space required in the stack to make the recursive calls will
        scale with the number of internal nodes travelled to, which in turn scales with N+M, the total length of the two
        strings.
        """
        if lst is None:
            lst = []

        for child in node.nexts: # O(1) - the length of node.nexts is constant (29)
            if child is not None and child.type is None:
                lst = self.find_all_common_substrings(child, "".join([lcs, child.label]), lst)

        lst.append(lcs)

        return lst

    @staticmethod
    def alphanum(character) -> int:
        """
        This method maps a string character to an index from 0 to 28 (inclusive). That is, a-z gets mapped to 0-25, {
        gets mapped to 26, | gets mapped to 27, and *space* gets mapped to 28.

        :param character: a singular string character
        :return: an index

        :Time Complexity: O(1) - constant time operations

        :Auxiliary Space Complexity: O(1) - constant size return values
        """
        if character == " ":
            return ord(character) - 4   # maps space to index 28
        return ord(character) - ord('a')

    @staticmethod
    def combine(txt1: str, txt2: str) -> str:
        """
        This static method combines the two input strings to form a singular string, each marked with a terminating
        character.

        :param txt1: first string
        :param txt2: second string
        :return: a combined string

        :Time Complexity: O(N+M)
        This function uses join() to concatenate the two strings, which has a TC of O(len(string)). Hence, the overall
        TC is O(N+M)

        :Auxiliary Space Complexity: O(N+M)
        The space required for the returned value is dependent on the lengths of both inputs. Making ASC O(N+M).
        """
        output = [txt1, "{", txt2, "|"]

        return "".join(output)


def compare_subs(submission1: str, submission2: str) -> list[str, int, int]:
    """
    The main function to find the longest common substring between two strings.

    :param submission1: first string
    :param submission2: second string
    :return: a list containing the longest common substring, percentage in submission1, percentage in the submission2

    :Time Complexity: O((N+M)^2)
    The TC is dominated by the construction of the suffix tree. The call to traverse the tree to find the longest
    substring take O(N+M) time.

    :Auxiliary Space Complexity: O((N+M)^2)
    The construction of the suffix tree requires O((N+M)^2) space.
    """
    st = SuffixTree(submission1, submission2)
    # st.traverse(st.root)
    sub_list = st.find_all_common_substrings(st.root)
    max_sub = ""
    if sub_list:
        max_sub = max(sub_list, key=len)    # O(N+M) - the list of possible substrings depends on length of both strings
    return [max_sub, round(len(max_sub)/len(submission1) * 100), round(len(max_sub)/len(submission2) * 100)]
