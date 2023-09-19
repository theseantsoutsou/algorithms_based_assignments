from bitarray import bitarray
from utils import gusfield_z, get_char_index, read_file, output_results, NO_OF_CHARS
import sys


def bitwisepm(txt: str, pat: str):
    """
    Bitwise pattern matching algorithm

    Time Complexity: O(m + n)

    :param txt:main string to search through
    :param pat: pattern string to be matched against the main string txt
    :return: indices of where the matches occur (1-indexing)
    """
    m = len(pat)
    n = len(txt)
    matches = []

    if n < m:   # the text is shorter than the pattern
        return matches

    # find the first bitvector using z-algorithm & pattern matching
    # essentially if any of txt[1...m]'s suffixes match pat[1...m]'s prefixes
    string = f"{pat}${txt[:m]}"         # string concatenation with f-string O(2 * m)
    z_values = gusfield_z(string)
    bitvec = bitarray()
    for val in z_values[m + 1:]:        # only interested in the z-values after the $, loop scales with m, constant boolean operations
        bitvec.append(not bool(val))

    # if match found at first index
    if not bitvec[0]:
        matches.append(1)

    # preprocess delta bitvectors, with the idea that, delta bitvector is essentially comparing the pattern string with each character in the alphabet
    deltas = {i: bitarray() for i in range(NO_OF_CHARS)}            # O(|A|) dictionary initalization
    for i in range(NO_OF_CHARS):                                    # nested loop overall O(|A| * m)
        for j in range(m - 1, -1, -1):
            deltas[i].append(get_char_index(pat[j]) != i)

    # the first bitvector is bitvector_m, so we just need to get the bitvectors m to n
    for j in range(m, n):   # loop scales with n
        bitvecJ = bitvec << 1 | deltas[get_char_index(txt[j])]      # relationship provided in the brief using bitwise operations

        if not bitvecJ[0]:
            matches.append(j - m + 2)                               # j-m+1 gets the 0-indexing index, another +1 to make it 1-indexing

        bitvec = bitvecJ                                            # updating bitvec_{j-1}

    return matches


if __name__ == "__main__":
    _, filename1, filename2 = sys.argv
    txt_str = read_file(filename1)
    pat_str = read_file(filename2)
    matching_ids = bitwisepm(txt_str, pat_str)
    output_results(matching_ids, "output_bitwisepm.txt")
