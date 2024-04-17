NO_OF_CHARS = 94


def gusfield_z(txt: str) -> list[int]:
    """
    Implementation of Gusfield's Z-Algorithm to return the Z-values at each index of the string
    Time Complexity: O(n) where n is the length of the input string txt

    :param txt: String to preprocess
    :return: an array of Z-values for the input string
    """
    n = len(txt)
    z_array = [0] * n
    left = 0
    right = 0

    def explicit_comparison(start: int, end: int) -> None:
        """
        Helper function to explicitly compare a string to its substring until a mismatch occurs. Arguments are modified.

        :param start: index to start matching
        :param end: index to end matching
        :return: None
        """
        while end < n and txt[end - start] == txt[end]:
            end += 1
        z_array[k] = end - start
        end -= 1

    for k in range(1, n):
        if k > right:   # case 1
            left, right = k, k
            explicit_comparison(left, right)

        else:           # case 2
            index = k - left
            if z_array[index] < right - k:  # case 2a
                z_array[k] = z_array[index]
            else:                           # case 2b
                left = k
                explicit_comparison(left, right)

    return z_array


def get_char_index(char: str) -> int:
    """
    Utility function to get the index of a string character - ASCII value range [33, 126]
    Time Complexity: O(1)

    :param char: ASCII character inclusively between char(33) and char(126)
    :return: character index value
    """
    return ord(char) - 33


def read_file(file_path: str) -> str:
    """
    Utility function to read file and return its content

    :param file_path: file path
    :return: file content
    """
    f = open(file_path, 'r')
    line = f.readline()
    f.close()
    return line


def output_results(outputs: list, output_file: str) -> None:
    """
    Utility function to write output into output_file

    :param outputs: results to output taken as a list
    :param output_file: output file path/name
    :return: None
    """
    f = open(output_file, "w")
    for item in outputs:
        f.write(f"{item}\n")
    f.close()
