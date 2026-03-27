from Token import *
# Token matchup regexes
keywordsTokensMap =  {"while": "While", "if": "If", "else": "Else"}
# EOF character for end of file?

class TokenIdentifier:
    def __init__(self, line_number: int) -> None:
        self.line_number = line_number
        self.setup()
    
    def setup(self) -> None:
        self.word: str = ""
        # Maintain these below in dict!
        self.potential_keyword = True
        self.potential_number = False
        
    def token_detector(self, char: str, peek: str = "") -> None | Token:
        if char.isalpha():
                self.word += char
                self.potential_number = False
            
        # Is a keyword
        if self.potential_keyword and len(self.word) > 0 and not (char.isalpha() or char.isdigit()):
            if self.word not in keywordsTokensMap.keys():
                self.potential_keyword = False
                # Possibly an identifier
                pass
            else:
                tok = KeywordToken(keywordsTokensMap[self.word], self.line_number)
                
                return tok
        
        # Is a number
        if self.potential_number and not(char.isdigit() or char == "."):
            numb = float(self.word)
            tok = LiteralToken('Num', numb, self.line_number)
            return tok
    



def source_to_tokens(input_source: str) -> list[Token]:
    token_list: list[Token] = []
    code_lines = input_source.splitlines()
    for line_number, line in enumerate(code_lines):
        # Now we scan character by character
        tk_ident = TokenIdentifier(line_number)
        for char in line:
            tk_out = tk_ident.token_detector(char, line)
            if tk_out is not None:
                token_list.append(tk_out)
                
                # Resetting vs creating new objets. Idk
                tk_ident.setup()
            
            
        
        pass
    pass