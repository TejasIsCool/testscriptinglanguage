from src.helpers import ErrorManager
import src.input_handler as ip
import src.scanner as sc
import src.parser as ps

def main():
    mode, code = ip.get_code()
    if mode == 1:
        # Interactive mode!
        print("Interactive mode activated")
        while True:
            user_input = input(">>> ")
            ErrorManager.mode = 1
            if user_input.lower() == "exit":
                break
            token_list = sc.source_to_tokens(user_input)
            # If the last token of token list is not a semi colon, add it!
            if token_list and not isinstance(token_list[-1], ps.SemicolonToken):
                token_list.append(ps.SemicolonToken(-1))
            if token_list is None:
                print("Syntax Errors were found in the code")
                continue
            try:
                parser = ps.Parser(token_list)
                parser_output = parser.parse()
                print(parser_output.evaluate())
            except Exception as e:
                print(f"Error while parsing input: {e}")
                continue
        return
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