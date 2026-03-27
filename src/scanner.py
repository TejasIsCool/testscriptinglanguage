from Token import *


class TokenIdentifier:

    # Token matchup regexes
    keywords = ["while", "if", "else"]
    # EOF character for end of file?

    token_interrupters = [";", "+", "-", "*", "/", "^", "|", "&", " ", "(", ")", "=", "/", "#","."]
    """If these are just ahead of the character, it means the current word is ending.
    Ie, it should be made into a token"""

    def __init__(self, line_number: int) -> None:
        self.line_number = line_number
        self.setup()

    def setup(self) -> None:
        self.word: str = ""
        # Maintain these below in dict!
        self.potential_keyword = True
        self.potential_number = False

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
        
        self.word += char
        
        # Now perform checks on what our word is
        if peek in self.token_interrupters or peek=="":
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
            
            
            pass
        
        # if char.isalpha():
        #     self.word += char
        #     self.potential_number = False

        # Is a keyword
        # if self.potential_keyword and len(self.word) > 0 and char in self.token_interrupters:
        #     if self.word not in self.keywords_tokens_map.keys():
        #         self.potential_keyword = False
        #         # Possibly an identifier
        #         pass
        #     else:
        #         tok = KeywordToken(
        #             self.keywords_tokens_map[self.word], self.line_number)
        #         return tok

        # # Is a number
        # if self.potential_number and not (char.isdigit() or char == "."):
        #     numb = float(self.word)
        #     tok = LiteralToken('Num', numb, self.line_number)
        #     return tok


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

        pass
    pass
