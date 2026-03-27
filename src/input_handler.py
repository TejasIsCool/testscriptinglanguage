import argparse


def get_code() -> str:
    """Has the compiler arguments, and gets the source code
    in the file provided as a string.

    Returns:
        str: The code in string format.
    """
    # Arguments of command line
    parser = argparse.ArgumentParser(
        prog='TCompilerPY',
        description='Compiles your program or something idk',
        epilog='And thus be it'
    )
    parser.add_argument("filepath")
    args = parser.parse_args()
    filepath: str = args.filepath

    with open(filepath, "r") as f:
        text = f.read()
    return text