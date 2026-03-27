from src.Token import *


class TokenIdentifier:

    # Token matchups
    keywords = ["while", "if", "else", "break", "continue"]
    literals = ["True", "False", "None"]
    
    # EOF character for end of file?

    token_interrupters = [
        ";", "+", "-", "*", "/", "^", "|", "&", " ", 
        "(", ")", "=", "/", "#",".", ">", "<",
        "[", "]", '"'
    ]
    """If these are just ahead of the character, it means the current word is ending.
    Ie, it should be made into a token"""

    def __init__(self, line_number: int) -> None:
        self.line_number = line_number
        self.setup()

    def setup(self) -> None:
        self.word: str = ""
        # Maintain these below in dict!
        self.is_comment = False
        self.is_string = False

    def token_detector(self, char: str, index: int, peek_line: str = "") -> None | Token:
        """Generates a token if it identifies it as one.

        Args:
            char (str): Current treading character
            index (int): Current position of the character in the line
            peek_line (str, optional): To allow look-ahead for other characters, inorder to know when to stop. Defaults to "".

        Returns:
            None | Token
        """

        peek = ""
        # ie, we are not at the last character
        if index + 1 != len(peek_line):
            peek = peek_line[index+1]
            
            
        # Design decision:
        # Should i add the character to the word, and tokenize it based on the peek character?
        # Or should i add it to the word if it matches certain criterion? (Currently doing this, should do 1 maybe)    
        
        # Will skip till the line end, we support a lot of comments!
        if char+peek in ["//", "--","/-","-/"] or self.word == "#":
            self.is_comment = True
        
        if char != " ":
            self.word += char
        
        if not self.is_comment and (self.word in self.token_interrupters):
            
            if self.word in ["+","-","*","/","^","%","|","&","<",">","|","&"]:
                # If its a assignment like, like x += 5, then its handled differently
                if not peek == "=":
                    tok = OperatorToken(self.word, "Bop", self.line_number)
                    return tok

            if self.word == "=":
                if not peek == "=":
                    return OperatorToken(self.word, "Bop", self.line_number)
            
            if self.word == "!":
                if not peek == "=":
                    return OperatorToken(self.word, "Uop", self.line_number)
                
            if self.word in ["(",")","[","]"]:
                return PunctuationToken(self.word, self.line_number)
            
            if self.word == ";":
                return SemicolonToken(self.line_number) 
        
        # Handling the two length operators
        if not self.is_comment and len(self.word) == 2:
            # not ==, <=, >=, != are binary operators
            # and +=,-=, ..., are assignment
            if self.word[0] in ["+","-","*","/","^","%","|","&","<",">","|","&","!","="]:
                if self.word[0] in ["<", ">", "=", "!"]:
                    return OperatorToken(self.word, "Bop", self.line_number)
                else:
                    return OperatorToken(self.word, "Ass", self.line_number)
        
        
        # Now perform checks on what our word is
        if not self.is_comment and (peek in self.token_interrupters or peek==""):
            # will not find something like +hello as seperate tokens!
            
            
            # Check if it matches any of the keywords:
            if self.word in self.keywords:
                tok = KeywordToken(self.word.capitalize(), self.line_number)
                return tok

            # Checking if it is a number:
            try:
                num = float(self.word)
                tok = LiteralToken('Num', num, self.line_number)
                return tok
            except ValueError:
                pass
            
            # Check if its a literal of some kind
            if self.word in self.literals:
                if self.word == "True" or "False":  
                    tok = LiteralToken("Bool", True if self.word == "True" else False, self.line_number)
                else:
                    tok = LiteralToken("Other", self.word, self.line_number)
                return tok
            
            
            # Else it is an identifier, if its a valid one
            
            # TODO: Check validity
            if len(self.word) > 0 and self.word not in self.token_interrupters:
                return IdentifierToken(self.word, self.line_number)
        return None


def source_to_tokens(input_source: str) -> list[Token]:
    token_list: list[Token] = []
    code_lines = input_source.splitlines()
    for line_number, line in enumerate(code_lines):
        # Now we scan character by character
        tk_ident = TokenIdentifier(line_number)
        for i, char in enumerate(line):
            tk_out = tk_ident.token_detector(char, i, line)
            if tk_out is not None:
                token_list.append(tk_out)

                # Resetting vs creating new objets. Idk
                tk_ident.setup()
    print(token_list)
    pass
