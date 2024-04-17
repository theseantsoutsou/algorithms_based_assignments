from utils import NO_OF_CHARS, char2index, index2char, read_file
import sys


def get_rank(bwt: str):
    """
    Function to get the rank array indicating where each character of the alphabet first appears
    Complexity is bounded bwt string length and only the alphabets in the bwt will be inserted into the set. Furthermore, the terminating character $ will be removed from the dicitonary

    """
    size = len(bwt)
    
    count_lst = [0 for _ in range(NO_OF_CHARS + 1)]     # O(1)
    for i in range(size):   # O(N)
        count_lst[char2index(bwt[i])] += 1
    
    position_lst = [0 for _ in range(NO_OF_CHARS + 1)]  # O(1)
    for i in range(1, NO_OF_CHARS + 1):     # O(1)
        position_lst[i] = position_lst[i - 1] + count_lst[i - 1]

    position_set = {}
    for i in range(1, NO_OF_CHARS + 1):     # O(1)
        if count_lst[i]:
            position_set[index2char(i)] = position_lst[i]

    return position_set


def get_occurrences(bwt, alphabet):
    """
    Get the occurences information of each character at each position

    :param bwt: bwt string
    :param alphabet: characters used
    """
    result = {char: [0] for char in alphabet}   # O(1)
    for char in bwt:    # O(N)
        for key, occ_lst in result.items():     # O(1) as the number of items is bounded by alphabet size
            val = occ_lst[-1] if key != char else occ_lst[-1] + 1   # if key == char, another occurence was found
            occ_lst.append(val)
    return result


def hdbwtpm(bwt: str, pat: str, max_d: int):
    """
    Function to conduct hamming distance bwt pattern matching

    Based off the idea that bwt matches the lexicographically sorted string
    Characters are grouped together, creating "bands" which we can recursively look through
    with the help of ranks and occurences

    :param bwt: bwt
    :param pat: pattern to be matched
    :param max_d: maximum number of mismatches allowed (hamming distance)
    """

    size = len(bwt)
    ranks = get_rank(bwt)   # O(N)
    alphabet = list(ranks.keys())   # O(1), keys in ranks are bounded by alphabet size
    occurrences = get_occurrences(bwt, alphabet)    # O(N)

    def aux_hdbwtpm(sp, ep, mismatch_left, pat, index, depth=0):
        """
        auxiliary function to recursively find the matches

        :param sp: starting pointer
        :param ep: ending pointer
        :param mismatch_left: number of mismatches allowed
        :param pat: pattern to be matched
        :param index: index of the pattern we are looking at
        :param depth: to see which level of recursive call we are looking on
        """

        # if the band size is less than or equal to 0 or if the index is less than 0
        if ep - sp <= 0 or index < 0:
            return 0
        
        # if we are at the end of the pattern and no more mismatches allowed
        # return band size
        if index == 0 and mismatch_left == 0:
            return ep - sp

        ans = 0
        next_character = pat[index-1]
        
        for char in alphabet:   # O(1) because alphabet size is constant
            # the fist character of the bwt is an edge case to consider because
            # when we are looking at it, we still need the entire band of that character
            # if the depth is 0, so we subtract 1 from the occurrences value
            if char == bwt[0] and depth == 0:
                rank_top = occurrences[char][sp] - 1
            else:
                rank_top = occurrences[char][sp]

            rank_bottom = occurrences[char][ep]
            
            # reduce pattern index each recursive call
            if char == next_character :     # exact match 
                ans += aux_hdbwtpm(ranks[char] + rank_top, 
                                   ranks[char] + rank_bottom, 
                                   mismatch_left, pat, index-1, depth + 1)
            elif mismatch_left > 0:         # mismatch
                # decrease mismatch
                ans += aux_hdbwtpm(ranks[char] + rank_top,
                                   ranks[char] + rank_bottom,
                                   mismatch_left-1, pat, index-1, depth + 1)
        return ans

    output = []
    # get the number of matches for each value less than or equal to max_d
    for i in range(max_d + 1):
        iMatches = aux_hdbwtpm(1, size, i, pat, len(pat))
        output.append(iMatches)

    return output


def output_results(outputs: list, output_file: str) -> None:
    """
    Utility function to write output into output_file

    :param outputs: results to output taken as a list
    :param output_file: output file path/name
    :return: None
    """
    f = open(output_file, "w")
    for i in range(len(outputs)):
        f.write(f"d = {i}, nMatches = {outputs[i]}\n")
    f.close()
        


if __name__ == "__main__":
    _, filename1, filename2, max_d = sys.argv
    bwt = read_file(filename1)
    pat_str = read_file(filename2)
    nMatches = hdbwtpm(bwt, pat_str, int(max_d))
    output_results(nMatches, "output_hdbwtpm.txt")
