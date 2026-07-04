from src.helpers import ErrorManager
import src.input_handler as ip
import src.scanner as sc
import src.parser as ps

def main():
    code: str = ip.get_code()
    ErrorManager.code_lines = code.splitlines()
    token_list = sc.source_to_tokens(code)
    if token_list is None:
        print("Syntax Errors were found in the code")
        exit()
    
    print("The code has been scanned")
    # print(code)
    print(token_list)
    
    parser = ps.Parser(token_list)
    parser_output = parser.parse()
    print(parser_output)
    
    # Execute the ast!
    result = parser_output.evaluate()
    print(f"FINAL Result: {result}")


if __name__ == "__main__":
    main()