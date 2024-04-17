"""
Written by: Sean Tsou
Completed: 18/08/2022

    Assignment 1
    Functional implementation to analyze a list of matches, each represented as ["team1", "team2", score], to find the
    top 10 matches, as well as matches with a specified score.

    TC: Time Complexity
    ASC: Auxiliary Space Complexity
    N: length of the input results
    M: length of the teams

    The input 'roster' is treated as a constant and will be assumed so when calculating complexity.
"""


def deep_copy(results: list[list]) -> list[list]:
    """
    Implementation of deepcopy specifically for lists of depth 2, where the inner-lists all have a length of 3.
    :param results: a list of matches, each represented by a list containing team1, team2, and score
    :return: a copy of the input
    
    :Time Complexity: TC = O(N)
    The TC is dominated by the nested for-loop. Since the inner for-loop runs a constant number of times and all
    operations within cost O(1), the nested for-loops overall scale with length of results, which is O(N).

    :Auxiliary Space Complexity: ASC = O(N)
    The function creates a new output list of the same size as the input list. Hence, ASC = O(N)
    """

    size = len(results)

    output = [[] for _ in range(size)]
    for i in range(size):
        for j in range(3):
            value = results[i][j]
            output[i].append(value)

    return output


def lexi_name(team: str, roster: int) -> str:
    """
    Implementation of counting sort to sort a string lexicographically.
    :param team: the team
    :param roster: a constant representing the character set used in team
    :return: a lexicographically sorted string of the team

    :Time Complexity: TC = O(M)
    Initialization of the count array cost O(roster). Assuming it's a constant, the cost is O(1). Counting the
    characters (for-loop) has constant operations done each iteration, so the loop scales with length of team, O(M).
    When storing the characters into sorted_char, the loop scale with roster(constant), but may append multiple
    characters at once. The number of characters appended is some fraction of M, so the block is technically O(M).
    Finally, the join operation costs O(length of list), which is O(M). Overall, TC = O(3M + roster), which is O(M).

    :Auxiliary Space Complexity: ASC = O(M)
    The function creates a count array, scaling with roster (constant), and a list for sorted_char, which will have
    a length of M. Hence, the overall ASC would be considered as O(M).
    """

    ALPHA_A = ord("A")

    # count array for all characters in the roster
    count = [0 for _ in range(roster)]  # O(roster)

    # counting the number of times each character appears and registering them in count array
    for i in range(len(team)):  # O(M)
        alphanum = ord(team[i])
        index = alphanum - ALPHA_A  # subtracting A's alphanumeric value to map to correct list indices
        count[index] += 1

    # sorting characters into a list
    sorted_char = []

    for i in range(roster):
        sorted_char.append(chr(i + ALPHA_A)*count[i])   # adding characters the number of times it was counted

    output = "".join(sorted_char)   # O(M)

    return output


def counting_sort(results: list[list]) -> list[list]:
    """
    Implementation of a stable counting sort for numerical values for this specific data type, will also remove
    duplicate items before returning. List is sorted in ascending order.
    :param results: a list of matches
    :return: a sorted list based on the scores of each match in ascending order

    :Time Complexity: TC = O(NM)
    The TC is dominated by the second to last for-loop. The loop itself scales with the length of results, N. The
    if-statements conduct list comparisons for matches in the list, which is always of size 3. However, team1 and team2
    are of type str, of length M. The list comparison will, therefore, each cost 2M+1, scaling with O(M).
    Hence, the for-loop overall scales with O(NM), making the function overall O(NM).

    :Auxiliary Space Complexity: ASC = O(N)
    The function creates new arrays that either scale with the constant MAX_SCORE, or the length of results, N.
    """
    size = len(results)
    MAX_SCORE = 100

    # count array for all possible scores
    count = [0 for _ in range(MAX_SCORE + 1)]   # O(1)

    # counting the number of times each score appears and registering them in count array
    for i in range(size):   # O(N)
        count[results[i][2]] += 1

    # position array for each score to make the function stable
    position = [0 for _ in range(MAX_SCORE + 1)]    # O(1)
    for i in range(1, MAX_SCORE + 1):   # O(1)
        position[i] = position[i-1] + count[i-1]

    # initializing the output
    temp_output = [[] for _ in range(size)]     # O(N)
    # overall cost O(NM)
    for item in results:   # O(N)
        # if the item being added is not equal to one at the previous index
        if item != temp_output[position[item[2]]-1]:    # O(M)
            # add the item and increment value in position array
            temp_output[position[item[2]]] = item
            position[item[2]] += 1

    # there will be empty lists from initialization due to the conditional statement above; remove them before returning
    output = []
    for item in temp_output:
        if len(item) != 0:
            output.append(item)

    return output


def _lexi_sort(results: list[list], roster: int, team: int, index: int) -> list[list]:
    """
    An implementation of counting sort specifically to be used in a radix sort to sort all matches in results in an
    ascending lexicographical order.
    :param results: a list of matches
    :param roster: a constant representing the character set used in teams
    :param team: the index of the team to be sorted; 0 for team1, 1 for team2
    :param index: the index of the character currently being sorted by.
    :return: a lexicographically sorted list based on the characters at index 'index'

    :Time Complexity: TC = O(N)
    The TC is dominated by the first and last for-loop block and initializing output list, which all run N times and
    does constant operations. The overall TC comes down to O(3roster + 3N). Since roster is a constant, TC = O(N).

    :Auxiliary Space Complexity: ASC = O(N)
    The function creates new lists that scale constantly with roster, or linearly with length of results, N. Making
    the ASC O(N).
    """

    size = len(results)
    ALPHA_A = ord("A")

    # count array for all characters in the roster
    count = [0 for _ in range(roster)]  # O(roster)

    # counting the number of time each character appears
    for item in results:    # O(N)
        char_id = ord(item[team][index]) - ALPHA_A  # subtracting A's alphanumeric value to map to correct list indices
        count[char_id] += 1

    # position array for each character to make the function stable
    position = [0 for _ in range(roster)]   # O(roster)
    for i in range(1, roster):  # O(roster)
        position[i] = position[i-1] + count[i-1]

    # constructing the output using the count array and position array
    output = [[] for _ in range(size)]  # O(N)
    for item in results:    # O(N)
        char_id = ord(item[team][index]) - ALPHA_A
        output[position[char_id]] = item
        position[char_id] += 1

    return output


def flip_and_combine(results: list[list]) -> None:
    """
    Get the list of flipped equivalent of each match in results and combine both lists into a single list.
    :param results: a list of matches

    :Time Complexity: TC = O(N)
    Every block in this function scale with the length of results, N, and does constant operations.

    :Auxiliary Space Complexity: ASC = O(N)
    Creates a new list flipped, which is a copy of results. Its size will therefore scale with N.
    """

    flipped = deep_copy(results)    # O(N)

    for item in flipped:    # O(N)
        item[0], item[1] = item[1], item[0]     # swap team1 and team2
        item[2] = 100 - item[2]     # update score

    for item in flipped:    # O(N)
        results.append(item)


def radix_sort(results: list[list], roster: int) -> list[list]:
    """
    Implementation of radix sort to sort a list of matches in ascending numerical order and descending lexicographical
    order when scores are tied. The function sorts from the least to most significant keys:
        team2 (from last character to first) --> team1 (from last character to first) --> score
    :param results: a list of matches
    :param roster: a constant representing the character set used in teams
    :return: a sorted list of matches, first by score, followed by team1 and then team2 when tied

    :Time Complexity: TC = O(NM)
    Sorting all teams in lexicographical order requires going through results and calling lexi_name(), making the
    overall cost O(NM). The main radix_sort goes through each team, M, and lexicographically sort the list, N, making
    the block O(NM) overall as well. Finally, the last call to counting_sort() cost O(NM) + O(N) for reversing the list.
    Therefore, the TC is O(NM) overall.

    :Auxiliary Space Complexity: ASC = O(N+M)
    The function creates a copy of results, makes a call to flip_and_combine(), and calls _lexi_sort(), all of which
    have an ASC of O(N). lexi_name() has an ASC of O(M), so the overall ASC for this function would be O(N+M).
    """

    team_size = len(results[0][0])

    output = deep_copy(results)     # O(N)

    # lexicographically sort all individual teams; overall cost O(NM)
    for item in output:     # O(N)
        for i in range(2):  # only two teams
            item[i] = lexi_name(item[i], roster)    # O(M)

    flip_and_combine(output)    # O(N)

    for team in range(1, -1, -1):   # O(1)
        i = team_size - 1
        while i > -1:   # O(M)
            output = _lexi_sort(output, roster, team, i)    # O(N)
            i -= 1

    # the output is first reversed (cost O(N)) to get the list into descending lexicographical order
    return counting_sort(output[::-1])  # O(NM+N)


def find_key(sorted_results: list[list], score: int) -> None or int:
    """
    This function searches through a list of matches sorted in a numerically ascending order based on scores and finds a
    key closest to the value of score that exists in the list.
    :param sorted_results: a list of sorted matches, each with the following format ["team1", "team2", score]
    :param score: the score to search for in the list of matches
    :return: the closest value, that exists in the list, greater or equal to the input score

    :Time Complexity: TC = O(N)
    The TC is dominated by the for-loop, which scales off the length of sorted_results, which is some fraction of or
    equal to the length of the input results to analyze(), hence scaling with N.

    :Space Complexity: O(1)
    The function does not create new variables and only runs through the input sorted_results to make comparisons.
    """
    # if the score is greater than the highest score in the results
    if score > sorted_results[-1][2]:   # O(1)
        return None

    # if the score is less than or equal to the lowest score in the results
    if score <= sorted_results[0][2]:   # O(1)
        return sorted_results[0][2]

    # if the above conditions were not met, go through the entire list
    for i in range(1, len(sorted_results)):     # O(N)
        # if score is less than or equal to the current score and greater than the previous score in the list
        if sorted_results[i][2] >= score > sorted_results[i - 1][2]:
            return sorted_results[i][2]


def analyze(results: list[list], roster: int, score: int) -> list[list]:
    """
    This function analyzes the input results and finds the top 10 matches with the highest scores, sorted in descending
    numerical order and ascending lexicographical order when tied; as well as a list of matches with a score greater or
    equal to the value score (if it exists).
    :param results: a list of matches
    :param roster: a constant representing the character set used in teams
    :param score: the score to be searched for in results
    :return: sorted top10matches and searched_matches in a list

    :Time Complexity: TC = O(NM)
    The TC is dominated by the call to radix_sort(), which costs O(NM). The top10matches block uses for loops that run
    constant numbers of time, unless there less than 10 matches, at which point, it is known the loop will run less than
    10 times. The searched_matches block will cost O(N) from searching through sorted_results for matches.

    :Auxiliary Space Complexity: ASC = O(N+M)
    The size of the new lists created in this function will scale with the size of results, O(N). However, radix_sort()
    will take up O(N+M) auxiliary space, making the overall ASC O(N+M)
    """
    # sorted_results will be sorted in ascending numerical order but descending lexicographical (when tied)
    # so that when looked at from the end, the items would be in descending numerical and ascending lexicographical
    # duplicates would be removed here
    sorted_results = radix_sort(results, roster)  # O(NM)

    # searches through sorted_results starting from the last element
    top10matches = []
    if len(sorted_results) >= 10:   # If there are 10 or more results after sorting
        # add the last 10 elements to top10matches in reverse order
        for i in range(len(sorted_results)-1, len(sorted_results)-11, -1):  # Runs a constant 10 times O(1)
            top10matches.append(sorted_results[i])
    else:   # if there are less than 10 results after sorting
        # add all elements to top10matches in reverse order
        for i in range(len(sorted_results)-1, -1, -1):  # Runs less than 10 times
            top10matches.append(sorted_results[i])

    # find the actual score which exists in the input data set to search for; None if no key greater or equal was found
    key = find_key(sorted_results, score)   # O(N)

    # searches from the end of the list
    searched_matches = []
    if key is not None:
        for i in range(len(sorted_results)-1, -1, -1):    # O(N)
            # if the match's score matches the key, add it to searched_matches
            if sorted_results[i][2] == key:
                searched_matches.append(sorted_results[i])

    return [top10matches, searched_matches]
