from copy import copy
from utils import gusfield_z, get_char_index, read_file, output_results, NO_OF_CHARS
import sys


def extended_bad_character(pat: str) -> list[list[int]]:
    """
    Implementation of the extended bad character that finds the rightmost occurence of the bad character x in the pattern to the left of the mismatch

    Time Complexity: O(|A| * m) where m |A| is the size of the alphabet and m is the length of the pattern string

    :param pat: pattern to preprocess
    :return: an R_k(x) matrix
    """
    k_bad_chars = [[-1] * NO_OF_CHARS]

    for i in range(1, len(pat)):
        bad_chars = copy(k_bad_chars[i - 1])    # copying one row of k_bad_chars which is of |A| size, so O(|A|) time (avoiding pointer issues)
        bad_chars[get_char_index(pat[i - 1])] = i - 1
        k_bad_chars.append(bad_chars)

    return k_bad_chars


def good_suffix(pat: str) -> list[dict]:
    """
    Modified implementation of the good suffix rule, where instead of storing the just rightmost occurence good suffix, we store all the good
    suffixes in a dictionary, with the key being the preceding character to said good suffixes. Values in the dictionaries are all initialized as None
    except for a special key "GOOD", which only stores the rightmost occurence of the good suffix, initialized as 0. This value is used in the case
    where the strict good suffix rule doesn't apply, that is, when there are no good suffixes in the pattern that has a preceding character that
    matches the bad character exactly, in which case, getting the value from the dictionary will result in a None value.

    Time Complexity: O(|A|*m) where |A| is the size of the alphabet and m is the length of the input pattern string.

    :param pat: pattern string to preprocess
    :return:
    """
    m = len(pat)

    z_suffix = gusfield_z(pat[::-1])[::-1]                      # reverse string -> z-algorithm -> reverse output --- a series of O(m) operations

    gs_dicts = [None] * (m + 1)
    for i in range(m + 1):      # loop scaling with m
        gs_dicts[i] = {i: None for i in range(NO_OF_CHARS)}     # dictionary creation scaling with alphabet size (constant)
        gs_dicts[i]["GOOD"] = 0

    for p in range(m - 1):      # loop scaling with m, constant operations
        j = m - z_suffix[p]
        preceding_char = pat[p - z_suffix[p]]
        gs_dicts[j][get_char_index(preceding_char)] = p
        gs_dicts[j]["GOOD"] = p

    return gs_dicts


def matched_prefix(pat: str) -> list[int]:
    """
    Implementation of the matched prefix rule

    Time Complexity: O(m) where m is the length of the input pattern string

    :param pat:
    :return:
    """
    m = len(pat)
    mp_values = [0] * (m + 1)
    mp_values[0] = m
    z_values = gusfield_z(pat)      # O(m) z-algorithm

    j = 0
    for i in range(m - 1, 0, -1):       # loop scaling with m
        j = max(j, z_values[i])
        mp_values[i] = j

    return mp_values


def boyer_moore(txt: str, pat: str) -> list[int]:
    """
    Implementation of the boyer_moore algorithm with Galil optimization and the stricter good_suffix rule.

    Time Complexity: O(m + n)

    :param txt: main string to search through
    :param pat: pattern string to be matched against the main string txt
    :return: indices of where the matches occur (1-indexing)
    """
    m = len(pat)
    n = len(txt)

    # preprocessing of the pattern string
    bad_chars = extended_bad_character(pat)
    gs_dicts = good_suffix(pat)
    mp_values = matched_prefix(pat)

    matches = []

    shift = 0
    stop = 0
    start = 0
    while shift <= n - m:   # while the pattern is still fully bounded by the text
        k = m - 1           # start from the end of the pattern

        # do a right-to-left comparison
        while k >= 0 and pat[k] == txt[shift + k]:
            if k == stop:   # Galil's optimization to skip through the characters we know match
                k = start
            k -= 1

        if k < 0:   # if a match was found
            matches.append(shift + 1)

            shift += m - mp_values[1] if shift + m < n else 1       # shift by the maximum amount allowed by the matched prefix rule
        else:       # if a match was not found
            x = txt[shift + k]  # bad character

            # Get the bad-character shift
            bc_shift = max(1, k - bad_chars[k][get_char_index(x)])

            # Get the stricter good suffix shift
            p = gs_dicts[k + 1][get_char_index(x)]
            if p is None:
                p = gs_dicts[k + 1]["GOOD"]

            if p > 0:
                stop = p - 1
                start = p - m + k
                gs_shift = m - p - 1
            else:
                stop = mp_values[k + 1] - 1
                start = 0
                gs_shift = m - mp_values[k + 1] - 1

            # increment shift by the highest valued shift
            shift += max(bc_shift, gs_shift)

    return matches


if __name__ == "__main__":
    _, filename1, filename2 = sys.argv
    txt_str = read_file(filename1)
    pat_str = read_file(filename2)
    matching_ids = boyer_moore(txt_str, pat_str)
    output_results(matching_ids, "output_stricterBM.txt")



