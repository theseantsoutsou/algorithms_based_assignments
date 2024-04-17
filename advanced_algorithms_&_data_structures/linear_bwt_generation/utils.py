NO_OF_CHARS = 91

def char2index(char: str) -> int:
    """
    Utility function to get the index of a string character - ASCII value range [36, 126]
    Time Complexity: O(1)

    :param char: ASCII character inclusively between char(33) and char(126)
    :return: character index value
    """
    return ord(char) - 36

def index2char(id: int) -> str:
    return chr(id + 36)


def read_file(file_path: str) -> str:
    """
    Utility function to read file and return its content

    :param file_path: file path
    :return: file content
    """
    f = open(file_path, "r")
    line = f.readline()
    f.close()
    return line


def output_results(output: str, output_file: str) -> None:
    """
    Utility function to write output into output_file

    :param outputs: results to output taken as a list
    :param output_file: output file path/name
    :return: None
    """
    f = open(output_file, "w")
    f.write(f"{output}")
    f.close()
