import src.input_handler as ip
import src.scanner as sc

def main():
    code: str = ip.get_code()
    token_list = sc.source_to_tokens(code)
    print("The code has been scanned")
    print(code)
    print(token_list)



if __name__ == "__main__":
    main()