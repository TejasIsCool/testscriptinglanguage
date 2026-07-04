import argparse


def get_code() -> tuple[int, str]:
    """Has the interpreter arguments, and gets the source code
    in the file provided as a string.

    Returns:
        tuple[int, str]: A tuple containing the mode and the source code as a string if there is.
    """
    # Arguments of command line
    cmd_parser = argparse.ArgumentParser(
        prog='TestScriptLang',
        description='Interprets your program or something idk',
        epilog='And thus be it'
    )
    cmd_parser.add_argument("filepath", nargs="?", default=None, help="The path to the file to interpret")
    args = cmd_parser.parse_args()
    filepath: str | None = args.filepath

    if filepath is not None:
        with open(filepath, "r") as f:
            text = f.read()
        return 0, text
    else:
        return 1, ""